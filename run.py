from problem import Problem
from solver import GeneticSolver

import random
from deap import base
from deap import creator
from deap import tools

POPULATION_SIZE = 100
WIN_POPULATION_SIZE = 10
GENERATIONS = 1000

CX_PROB = 0.5


# Load the problem
problem = Problem.laduj_z_pliku('problem.txt')

# Initialize generator
creator.create("FitnessMin", base.Fitness, weights=(-1.0, ))
creator.create("Individual", list, fitness=creator.FitnessMin)
toolbox = base.Toolbox()
toolbox.register("indices", random.sample, xrange(len(problem.elementy)), len(problem.elementy))
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)


population = [toolbox.individual() for _ in xrange(0, POPULATION_SIZE)]


# fitness operator
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

    leftovers += stock_size - currentsum        # adjust for last processed element

    return -leftovers,

# register the toolbox
toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxPartialyMatched)
toolbox.register("select", tools.selBest)
toolbox.register("mutate", tools.mutShuffleIndexes)



for g in xrange(0, GENERATIONS):
    top_pop = toolbox.select(population, WIN_POPULATION_SIZE)
    top_pop = map(toolbox.clone, top_pop)

    while len(top_pop) < POPULATION_SIZE:
        if random.random() < CX_PROB:
            c1, c2 = random.sample(top_pop, 2)
            c1 = toolbox.clone(c1)
            c2 = toolbox.clone(c2)
            toolbox.mate(c1, c2)
            del c1.fitness.values
            del c2.fitness.values

            top_pop.append(c1)
            top_pop.append(c2)
        else:
            c1, = random.sample(top_pop, 1)
            c1 = toolbox.clone(c1)
            toolbox.mutate(c1, 1.0/len(problem.elementy))
            del c1.fitness.values
            top_pop.append(c1)

    population = top_pop



population = toolbox.select(population, WIN_POPULATION_SIZE)


print 'Najlepsze rozwiazania:'
for solution in population:
    print -evaluate(solution)[0], solution
