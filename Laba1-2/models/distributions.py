import models.lcg as lcg
from services.reader import read_float, read_positive_float, read_positive_int
from math import sqrt, log
from collections import namedtuple

class UniformDistribution:
    UniformParameters = namedtuple('UniformParameters', ['a', 'b'])


    def generate(self, length, lgc_parameters, parameters = None):
        if parameters is None:
            parameters = self._read_params()

        vector = lcg.random_vector(length, lgc_parameters)

        for x in vector:
            yield parameters.a + (parameters.b - parameters.a) * x


    def _read_params(self):
        a = read_float('a')
        b = read_float('b', lambda x: x > a)

        return UniformDistribution.UniformParameters(a, b)


    @property
    def name(self):
        return 'uniform'


class GaussianDistribution:
    GaussianParameters = namedtuple('GaussianParameters', ['m', 'q'])
    N = 6


    def generate(self, length, lgc_parameters, parameters = None):
        if parameters is None:
            parameters = self._read_params()

        vector = list(lcg.random_vector(length * GaussianDistribution.N, lgc_parameters))

        for x in range(0, len(vector), GaussianDistribution.N):
            sub_vector = vector[x:x + GaussianDistribution.N]
            yield parameters.m + parameters.q * sqrt(12 / GaussianDistribution.N) * (sum(sub_vector) - GaussianDistribution.N / 2)


    def _read_params(self):
        m = read_float('m')
        q = read_positive_float('q')

        return GaussianDistribution.GaussianParameters(m, q)


    @property
    def name(self):
        return 'gaussian'


class ExponentialDistribution:
    ExponentialParameters = namedtuple('ExponentialParameters', ['l'])


    def generate(self, length, lgc_parameters, parameters = None):
        if parameters is None:
            parameters = self._read_params()

        vector = lcg.random_vector(length, lgc_parameters)

        for x in vector:
            yield - (1 / parameters.l) * log(x)


    def _read_params(self):
        l = read_positive_float('l')

        return ExponentialDistribution.ExponentialParameters(l)


    @property
    def name(self):
        return 'exponential'


class GammaDistribution:
    GammaParameters = namedtuple('GammaParameters', ['n', 'l'])


    def generate(self, length, lgc_parameters, gamma_params = None):
        if gamma_params is None:
            gamma_params = self._read_params()

        vector = list(lcg.random_vector(length * gamma_params.n, lgc_parameters))

        for x in range(0, len(vector), gamma_params.n):
            yield - (1 / gamma_params.l) * sum(log(vector[x + i]) for i in range(0, gamma_params.n))


    def _read_params(self):
        n = read_positive_int('n')
        l = read_positive_float('l')

        return GammaDistribution.GammaParameters(n, l)


    @property
    def name(self):
        return 'gamma'


class TriangularDistribution:
    TriangularParameters = namedtuple('TriangularParameters', ['a', 'b'])


    def generate(self, length, lgc_parameters, triangular_params = None):
        if triangular_params is None:
            triangular_params = self._read_params()

        vector = list(lcg.random_vector(length * 2, lgc_parameters))

        for x in range(0, len(vector), 2):
            yield triangular_params.a + (triangular_params.b - triangular_params.a) * max(vector[x], vector[x + 1])


    def _read_params(self):
        a = read_float('a')
        b = read_float('b', lambda x: x > a)

        return TriangularDistribution.TriangularParameters(a, b)


    @property
    def name(self):
        return 'triangle'


class SimpsonDistribution:
    SimpsonParameters = namedtuple('SimpsonParameters', ['a', 'b'])


    def generate(self, length, lgc_parameters, simpson_params = None):
        if simpson_params is None:
            simpson_params = self._read_params()
        uniform_params = UniformDistribution.UniformParameters(
            a = simpson_params.a / 2,
            b = simpson_params.b / 2
        )
        uniform_distribution = UniformDistribution()
        vector = list(uniform_distribution.generate(length * 2, lgc_parameters, uniform_params))

        return map(sum, zip(vector[::2], vector[1::2]))


    def _read_params(self):
        a = read_float('a')
        b = read_float('b', lambda x: x > a)

        return SimpsonDistribution.SimpsonParameters(a, b)


    @property
    def name(self):
        return 'simpson'