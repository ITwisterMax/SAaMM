class SystemCharacteristic:
    def update(self, current_state, p_state, pi1_state, pi2_state):
        raise NotImplementedError()

    @property
    def result(self):
        raise NotImplementedError()

    @property
    def name(self):
        raise NotImplementedError()

class FailureProbability(SystemCharacteristic):
    def __init__(self):
        self._input_count = 0
        self._output_count = 0

    def update(self, current_state, p_state, pi1_state, pi2_state):
        if (not p_state):
            self._input_count += 1
        if (current_state[2] == '1' and not pi2_state):
            self._output_count += 1

    @property
    def result(self):
        return 1 - self._output_count / self._input_count

    @property
    def name(self):
        return 'P_failure'

class BlockingProbability(SystemCharacteristic):
    def update(self, current_state, p_state, pi1_state, pi2_state):
        return

    @property
    def result(self):
        return 0.0

    @property
    def name(self):
        return 'P_blocking'

class AverageQueueLength(SystemCharacteristic):
    def __init__(self, tacts_count):
        self._queue_length = 0
        self._tacts_count = tacts_count

    def update(self, current_state, p_state, pi1_state, pi2_state):
        if current_state[1] != '0':
            self._queue_length += int(current_state[1])

    @property
    def result(self):
        return self._queue_length / self._tacts_count

    @property
    def name(self):
        return 'L_queue'

class AverageSystemLength(SystemCharacteristic):
    def __init__(self, tacts_count):
        self._queue_length = 0
        self._channel_length = 0
        self._tacts_count = tacts_count

    def update(self, current_state, p_state, pi1_state, pi2_state):
        if current_state[1] != '0':
            self._queue_length += int(current_state[1])
        if current_state[0] == '1':
            self._channel_length += 1
        if current_state[2] == '1':
            self._channel_length += 1

    @property
    def result(self):
        return (self._queue_length + self._channel_length) / self._tacts_count

    @property
    def name(self):
        return 'L_system'

class RelativeThroughput(SystemCharacteristic):
    def __init__(self):
        self._input_count = 0
        self._output_count = 0

    def update(self, current_state, p_state, pi1_state, pi2_state):
        if (not p_state):
            self._input_count += 1
        if (current_state[2] == '1' and not pi2_state):
            self._output_count += 1

    @property
    def result(self):
        return self._output_count / self._input_count

    @property
    def name(self):
        return 'Q'

class AbsoluteThroughput(SystemCharacteristic):
    def __init__(self, tacts_count):
        self._result = 0
        self._tacts_count = tacts_count

    def update(self, current_state, p_state, pi1_state, pi2_state):
        if current_state[2] == '1' and not pi2_state:
            self._result += 1

    @property
    def result(self):
        return self._result / self._tacts_count

    @property
    def name(self):
        return 'A'

class AverageQueueTime(SystemCharacteristic):
    def __init__(self, tacts_count):
        self._curr_time = 0
        self._curr_count = 0
        self._prev_state = '000'
        self._prev_pi1_state = True
        self._prev_pi2_state = True
        self._prev_time = [False, False]
        self._sum_time = 0
        self._tacts_count = tacts_count

    def update(self, current_state, p_state, pi1_state, pi2_state):
        if (self._prev_state[0] == '1' and (self._prev_state[1] != '2' or not self._prev_pi2_state) and not self._prev_pi1_state):
            self._curr_count += 1

            if (current_state[1] + current_state[2] != '01'):
                if (self._prev_time[0] == False):
                    self._prev_time[0] = self._curr_time
                else:
                    self._prev_time[1] = self._curr_time

        if (current_state[1] != '0' and current_state[2] == '1' and not pi2_state):
            if (self._prev_time[0] != False):
                self._sum_time += self._curr_time - self._prev_time[0]

                self._prev_time[0] = self._prev_time[1]
                self._prev_time[1] = False

        self._curr_time += 1
        self._prev_state = current_state
        self._prev_pi1_state = pi1_state
        self._prev_pi2_state = pi2_state

    @property
    def result(self):
        if self._prev_time[0] != False:
            self._sum_time += self._tacts_count - self._prev_time[0]
        if self._prev_time[1] != False:
            self._sum_time += self._tacts_count - self._prev_time[1]

        return 0.0 if self._curr_count == 0 else self._sum_time / self._curr_count;

    @property
    def name(self):
        return 'W_queue'

class AverageSystemTime(SystemCharacteristic):
    def __init__(self, tacts_count):
        self._curr_time = 0
        self._curr_count = 0
        self._prev_state = '000'
        self._prev_pi1_state = True
        self._prev_pi2_state = True
        self._prev_time = [False, False]
        self._sum_time = 0
        self._tacts_count = tacts_count

        self._sum_time_c1 = 0
        self._curr_time_c1 = False
        self._curr_count_c1 = 0

        self._sum_time_c2 = 0
        self._curr_time_c2 = False
        self._curr_count_c2 = 0

    def update(self, current_state, p_state, pi1_state, pi2_state):
        if ((self._prev_state[0] == '0' and current_state[0] == '1') or (self._prev_state[0] == '1' and not self._prev_pi1_state)):
            self._curr_time_c1 = self._curr_time
            self._curr_count_c1 += 1

        if ((current_state[0] == '1' and not pi1_state) and (self._curr_time_c1 != False)):
            self._sum_time_c1 += self._curr_time + 1 - self._curr_time_c1
            self._curr_time_c1 = False

        if ((self._prev_state[2] == '0' and current_state[2] == '1') or (self._prev_state[2] == '1' and not self._prev_pi2_state)):
            self._curr_time_c2 = self._curr_time
            self._curr_count_c2 += 1

        if ((current_state[2] == '1' and not pi2_state) and (self._curr_time_c2 != '0')):
            self._sum_time_c2 += self._curr_time + 1 - self._curr_time_c2
            self._curr_time_c2 = False

        if (self._prev_state[0] == '1' and (self._prev_state[1] != '2' or not self._prev_pi2_state) and not self._prev_pi1_state):
            self._curr_count += 1

            if (current_state[1] + current_state[2] != '01'):
                if (self._prev_time[0] == False):
                    self._prev_time[0] = self._curr_time
                else:
                    self._prev_time[1] = self._curr_time

        if (current_state[1] != '0' and current_state[2] == '1' and not pi2_state):
            if (self._prev_time[0] != False):
                self._sum_time += self._curr_time - self._prev_time[0]

                self._prev_time[0] = self._prev_time[1]
                self._prev_time[1] = False

        self._curr_time += 1
        self._prev_state = current_state
        self._prev_pi1_state = pi1_state
        self._prev_pi2_state = pi2_state

    @property
    def result(self):
        if self._curr_time_c1 != False:
            self._sum_time_c1 += self._tacts_count - self._curr_time_c1

        Wc1 = 0.0 if self._curr_count_c1 == 0 else self._sum_time_c1 / self._curr_count_c1

        if self._curr_time_c2 != False:
            self._sum_time_c2 += self._tacts_count - self._curr_time_c2

        Wc2 = 0.0 if self._curr_count_c2 == 0 else self._sum_time_c2 / self._curr_count_c2

        if self._prev_time[0] != False:
            self._sum_time += self._tacts_count - self._prev_time[0]
        if self._prev_time[1] != False:
            self._sum_time += self._tacts_count - self._prev_time[1]

        Wq = 0.0 if self._curr_count == 0 else self._sum_time / self._curr_count

        return Wc1 + Wq + Wc2

    @property
    def name(self):
        return 'W_system'

class KProbability(SystemCharacteristic):
    def __init__(self, tacts_count):
        self._count = 0
        self._tacts_count = tacts_count

    def update(self, current_state, p_state, pi1_state, pi2_state):
        if (current_state != '000'):
            self._count += 1

    @property
    def result(self):
        return self._count / self._tacts_count

    @property
    def name(self):
        return 'K'