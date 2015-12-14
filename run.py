from __future__ import division

import random
import sys
import time

from deap import tools

from problem import ProblemLoader, create_toolbox


def solve(POPULATION_SIZE, WIN_POPULATION_SIZE, CX_PROB, *args):
    problem = ProblemLoader(sys.argv[1])
    toolbox = create_toolbox(problem)
    population = toolbox.population(n=10 * POPULATION_SIZE)
    last_best_fitness, fitness_stuck_for, fitnesses = float('inf'), 0, []

    for i in xrange(0, 10000):
        best_fitness = float('inf')

        # evaluate the population
        for ind, fit in zip(population, map(toolbox.evaluate, population)):
            ind.fitness.values = fit
            fit, = fit
            if fit < best_fitness:
                best_fitness = fit

        fitnesses.append(best_fitness)

        if best_fitness >= last_best_fitness:
            fitness_stuck_for += 1
        else:
            fitness_stuck_for = 0
            last_best_fitness = best_fitness

        best = toolbox.select(population, k=WIN_POPULATION_SIZE)
        population = best[:]  # elitism

        for member in best:  # mutations of elites
            c1 = toolbox.clone(member)
            toolbox.mutate(c1)
            for _ in xrange(0, fitness_stuck_for // 3):  toolbox.mutate(c1) # irradiation factor
            del c1.fitness.values
            population.append(member)

        while len(population) < POPULATION_SIZE:
            if random.random() < CX_PROB:
                c1 = toolbox.mate(*map(toolbox.clone, random.sample(best, 2)))[0]
            else:
                c1 = toolbox.clone(random.sample(best, 1)[0])
                toolbox.mutate(c1)

            for _ in xrange(0, fitness_stuck_for // 3):  toolbox.mutate(c1) # irradiation factor
            del c1.fitness.values
            population.append(c1)

        if i % 10 == 0:
            print '%s %s' % (i, best_fitness)

        if fitness_stuck_for > 100:
            break

    for ind, fit in zip(population, map(toolbox.evaluate, population)): ind.fitness.values = fit

    the_best, = tools.selBest(population, 1)
    return the_best, the_best.fitness.values, fitnesses


if __name__ == '__main__':
    start = time.clock()
    best, fitnes, path = solve(350, 30, 0.5)
    stop = time.clock()
    print '%s %s' % (stop - start, fitnes)
