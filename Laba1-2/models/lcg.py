TEST_LENGTH = 10 ** 6


def minmax(data):
    iterator = iter(data)

    try:
        smallest = biggest = next(iterator)
    except StopIteration:
        raise ValueError('Data is an empty sequence.')

    for x in iterator:
        if x < smallest:
            smallest = x
        if x > biggest:
            biggest = x

    return smallest, biggest


def uniform_ratio(numbers):
    k = sum(x1 ** 2 + x2 ** 2 < 1 for x1, x2 in zip(numbers[::2], numbers[1::2]))

    return 2 * k / len(numbers)


def random_vector(length, lgc_parameters):
    x = lgc_parameters.initial

    for _ in range(length):
        x = (x * lgc_parameters.multiplyer) % lgc_parameters.base
        yield x / lgc_parameters.base


def last_element(iterable):
    try:
        result = next(iterable)
    except StopIteration:
        raise ValueError('Empty iterable.')

    for result in iterable:
        pass

    return result


def period(generator):
    last = last_element(generator(TEST_LENGTH))
    start = None

    for i, x in enumerate(generator(TEST_LENGTH)):
        if x == last:
            if not start:
                start = i
            else:
                return i - start

    return None


def aperiodic_interval(generator, found_period):
    sequence = list(generator(TEST_LENGTH))

    for i in range(TEST_LENGTH):
        if i + found_period < TEST_LENGTH:
            if sequence[i] == sequence[i + found_period]:
                return i + found_period

    return None