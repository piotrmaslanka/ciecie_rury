from __future__ import division
import random

from deap import tools
from scoop import futures

from problem import ProblemLoader, create_toolbox

POPULATION_SIZE = 60
WIN_POPULATION_SIZE = 10
GENERATIONS = 600

CX_PROB = 0.3

def solve(*args):
    problem = ProblemLoader('problem.txt')
    toolbox = create_toolbox(problem)
    population = toolbox.population(n=10*POPULATION_SIZE)
    last_best_fitness, fitness_stuck_for, fitnesses = float('inf'), 0, []

    for i in xrange(0, GENERATIONS):
        best_fitness = float('inf')

        # evaluate the population
        for ind, fit in zip(population, map(toolbox.evaluate, population)):
            ind.fitness.values = fit
            fit, = fit
            if fit < best_fitness:
                best_fitness = fit

        fitnesses.append(best_fitness)

        if best_fitness == last_best_fitness:
            fitness_stuck_for += 1
        else:
            fitness_stuck_for = 0
            last_best_fitness = best_fitness

        best = toolbox.select(population, k=WIN_POPULATION_SIZE)
        population = best[:]  # elitism

        for member in best:  # mutations of elites
            c1 = toolbox.clone(member)
            toolbox.mutate(c1)
            del c1.fitness.values
            population.append(member)

        while len(population) < POPULATION_SIZE:
            if random.random() < CX_PROB:
                c1 = toolbox.mate(*map(toolbox.clone, random.sample(best, 2)))[0]
            else:
                c1 = toolbox.clone(random.sample(best, 1)[0])
                toolbox.mutate(c1)

            for _ in xrange(0, fitness_stuck_for // 3):  # irradiation factor
                toolbox.mutate(c1)

            del c1.fitness.values
            population.append(c1)

    for ind, fit in map(toolbox.evaluate, population): ind.fitness.values = fit

    sb, = tools.selBest(population, 1)
    return sb, sb.fitness.values[0], fitnesses

if __name__ == '__main__':
    res = list(futures.map(solve(_) for _ in xrange(0, 4)))
    fitnesses = [fit for sol, fit, fitnesses in res]

    print 'Average fitness: %s of %s trials' % (sum(fitnesses)/len(fitnesses), len(fitnesses))
    print 'Best fitness: %s' % (min(fitnesses), )
