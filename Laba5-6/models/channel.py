from services.exponential_distribution import exponential_number


class Channel:
    def __init__(self, intensity):
        self.intensity = intensity
        self.ticks_for_process = 0
        self.help = 1

    def add(self):
        self.ticks_for_process = exponential_number(self.intensity)

    def is_processed(self):
        return self.ticks_for_process <= 0

    def tick(self):
        if self.ticks_for_process > 0:
            self.ticks_for_process -= self.help
