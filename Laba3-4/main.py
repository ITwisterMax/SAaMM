import sys

from models.transitions import TRANSITIONS
from services.simulator import simulate, UnitsSettings
from services.characteristics import *
from random import random

START_STATE = '000'
TACTS_COUNT = 1000000

DEFAULT_SETTINGS = UnitsSettings(p=0.75, pi1=0.85, pi2=0.65)


def read_probability(value_name):
    result = None
    while result is None:
        raw_input = input('{}: '.format(value_name))
        try:
            result = float(raw_input)
        except ValueError:
            print('Invalid input.')
    return result


def read_units_settings():
    values = {}
    for setting in UnitsSettings._fields:
        values[setting] = read_probability(setting)
    return UnitsSettings(**values)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == '-d':
        units_settings = DEFAULT_SETTINGS
    else:
        units_settings = read_units_settings()

    characteristics = [
        FailureProbability(),
        BlockingProbability(),
        AverageQueueLength(TACTS_COUNT),
        AverageSystemLength(TACTS_COUNT),
        RelativeThroughput(),
        AbsoluteThroughput(TACTS_COUNT),
        AverageQueueTime(TACTS_COUNT),
        AverageSystemTime(TACTS_COUNT),
        KProbability(TACTS_COUNT)
    ]

    states_statistics, characteristics_results = simulate(TRANSITIONS, units_settings, TACTS_COUNT, START_STATE, characteristics)

    print('\nProbabilities:')
    for state, count in sorted(states_statistics.items(), key=lambda x: int(x[0])):
        if (state == START_STATE):
            start_state_p = count / TACTS_COUNT

        print('P {} = {}'.format(state, count / TACTS_COUNT))

    print('\nCharacteristics:')

    for name, result in characteristics_results.items():
        print('{} = {}'.format(name, result))

if __name__ == '__main__':
    main()
