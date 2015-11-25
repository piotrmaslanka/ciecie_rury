"""Functions that were once used, but are not anymore"""

import random


def mutRSM(individual):
    """Reverse Sequence Mutation"""
    li = len(individual) - 1

    a = random.randint(0, li)
    while True:
        b = random.randint(0, li)
        if a != b:
            break

    a, b = min((a, b)), max((a, b))

    individual = individual[:a] + individual[a:b][::-1] + individual[b:]
