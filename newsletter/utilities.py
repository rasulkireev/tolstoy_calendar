import random


def random_digits():
    return "%0.12d" % random.randint(0, 999999999999)