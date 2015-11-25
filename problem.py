from __future__ import division
import random

from deap import base
from deap import creator
from deap import tools
from scoop import futures


class ProblemLoader(object):
    def __init__(self, filename):
        with open(filename, 'rb') as f:
            lines = f.readlines()

        _san = lambda l: int(l.strip())

        self.belka = _san(lines[0])

        elementy = []
        for i in xrange(0, _san(lines[1])):
            elementy.append(_san(lines[2 + i]))

        self.elementy = elementy


def mutMyShuffle(individual, indbp):
    """a mutShuffleIndexes that swaps only two indices"""
    q = random.random()
    for i, pro in enumerate(indbp):
        if q < pro:
            break
        else:
            q -= pro

    q = random.random()
    for j, pro in enumerate(indbp):
        if q < pro:
            break
        else:
            q -= pro

    individual[i], individual[j] = individual[j], individual[i]


def create_toolbox(problem):
    def evaluate(individual):
        leftovers = 0

        stock_size = problem.belka
        currentsum = 0

        for i in individual:
            e = problem.elementy[i]
            if e + currentsum > stock_size:
                # emit element, pass it as new one
                leftovers += stock_size - currentsum
                currentsum = e
            else:
                currentsum += e

        leftovers += stock_size - currentsum  # adjust for last processed element

        return leftovers,

    def index_shuffle_probability(individual):
        """Calculate the probability of index shuffling"""
        # total_leftovers = evaluate(individual)[0]
        total_leftovers, = individual.fitness.values

        def generate_probabilities(individual):
            stocksize, currentsum, elem_cnt, leftovers = problem.belka, 0, 0, 0

            for i in individual:
                e = problem.elementy[i]
                if e + currentsum > stocksize:
                    f = (stocksize - currentsum) / total_leftovers / elem_cnt
                    for _ in xrange(0, elem_cnt):
                        yield f
                    currentsum = e
                    elem_cnt = 1
                else:
                    currentsum += e
                    elem_cnt += 1
            else:
                f = (stocksize - currentsum) / total_leftovers / elem_cnt
                for _ in xrange(0, elem_cnt):
                    yield f

        return list(generate_probabilities(individual))

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)
    toolbox = base.Toolbox()
    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", tools.cxOrdered)
    toolbox.register("select", tools.selBest)
    toolbox.register("mutate", lambda x: mutMyShuffle(x, index_shuffle_probability(x)))
    toolbox.register("map", futures.map)
    toolbox.register("indices", random.sample, xrange(len(problem.elementy)), len(problem.elementy))
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    return toolbox
