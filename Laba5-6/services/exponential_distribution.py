from math import log
from random import uniform


def exponential_number(coef):
    return (-1 / coef) * log(uniform(0, 1))
