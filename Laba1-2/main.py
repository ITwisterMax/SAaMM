import models.lcg as lcg
from models.distributions import ExponentialDistribution, GammaDistribution, GaussianDistribution, UniformDistribution, TriangularDistribution, SimpsonDistribution
from services.reader import read_positive_int
from views.histogram import draw_histogram
import sys
from math import pi
import statistics as stat
from collections import namedtuple


LcgParameters = namedtuple('LcgParameters', ['initial', 'multiplyer', 'base'])

DISTRIBUTIONS_DESCRIPTION = [
    UniformDistribution(),
    GaussianDistribution(),
    ExponentialDistribution(),
    GammaDistribution(),
    TriangularDistribution(),
    SimpsonDistribution()
]

DEFAULT_LCG_PARAMS = LcgParameters(
    base = 1046527,
    initial = 65537,
    multiplyer = 32771
)

RANDOM_VECTOR_LENGTH = 100000


def print_result(name, actual_result):
    if actual_result is not None:
        result = '{}: {}'.format(name, actual_result)
    else:
        result = 'Can not find {}.'.format(name)
    print(result)


def read_lcg_parameters():
    return LcgParameters(
        base = read_positive_int("m"),
        initial = read_positive_int("R0"),
        multiplyer = read_positive_int("a")
    )


def lcg_demo():
    params = read_lcg_parameters()
    result = list(lcg.random_vector(RANDOM_VECTOR_LENGTH, params))

    print_result('M', stat.mean(result))
    print_result('D', stat.variance(result))
    print_result('Q', stat.stdev(result))
    print_result('2 * K / N', lcg.uniform_ratio(result))

    period = lcg.period(lambda length: lcg.random_vector(length, params))

    print_result('Period', period)

    if period:
        print_result('Aperiodic interval', lcg.aperiodic_interval(lambda length: lcg.random_vector(length, params), period))

    draw_histogram(result)


def print_menu():
    for i, distribution in enumerate(DISTRIBUTIONS_DESCRIPTION):
        print('\t{} : {}'.format(i + 1, distribution.name))

    print('\t0 : exit')


def read_command():
    valid = False

    while not valid:
        try:
            command = int(input('>> '))
            valid = command >= 0 and command <= len(DISTRIBUTIONS_DESCRIPTION)
        except ValueError:
            print('Invalid input.')
            print_menu()

    return command


def distributions_demo():
    print_menu()

    command = read_command()

    while command != 0:
        distribution = DISTRIBUTIONS_DESCRIPTION[command - 1]

        result = list(distribution.generate(RANDOM_VECTOR_LENGTH, DEFAULT_LCG_PARAMS))

        print_result('M', stat.mean(result))
        print_result('D', stat.variance(result))
        print_result('Q', stat.stdev(result))

        draw_histogram(result)

        command = read_command()


def main():
    modes = {
        'lcg': lcg_demo,
        'dist': distributions_demo
    }

    if (len(sys.argv) == 2) and (sys.argv[1] in modes):
        command = modes[sys.argv[1]]
    else:
        print('Use: main.py dist|lcg.')

        return

    command()


if __name__ == '__main__':
    main()