from __future__ import division
import random
from problem import ProblemLoader, create_toolbox
from deap import tools
from scoop import futures

POPULATION_SIZE = 60
WIN_POPULATION_SIZE = 10
GENERATIONS = 300

CX_PROB = 0.5

def solve(*args):
    # Load the problem
    problem = ProblemLoader('problem.txt')
    toolbox = create_toolbox(problem)
    # Initialize generator

    # fitness operator
    population = toolbox.population(n=10*POPULATION_SIZE)

    last_best_fitness = float('inf')
    fitness_stuck_for = 0

    fitnesses = []

    for i in xrange(0, GENERATIONS):
        best_fitness = float('inf')

        # evaluate the population
        for ind, fit in zip(population, map(toolbox.evaluate, population)):
            ind.fitness.values = fit
            fit,=fit
            if fit < best_fitness:
                best_fitness = fit

        fitnesses.append(best_fitness)

        if best_fitness == last_best_fitness:
            fitness_stuck_for += 1
        else:
            fitness_stuck_for = 0
            last_best_fitness = best_fitness

        best = toolbox.select(population, k=WIN_POPULATION_SIZE)
        population = best[:]

        for member in best:
            c1 = toolbox.clone(member)
            toolbox.mutate(c1)
            del c1.fitness.values
            population.append(member)

        while len(population) < POPULATION_SIZE:

            if random.random() < CX_PROB:
                # will cross over
                c1, c2 = random.sample(best, 2)
                c1 = toolbox.clone(c1)
                c2 = toolbox.clone(c2)

                c1 = toolbox.mate(c1, c2)[0]
            else:
                c1 = toolbox.clone(random.sample(best, 1)[0])
                toolbox.mutate(c1)

            for x in xrange(0, fitness_stuck_for//5):
                toolbox.mutate(c1)

            del c1.fitness.values
            population.append(c1)

    sb, = tools.selBest(population, 1)
    return sb, toolbox.evaluate(sb)[0], fitnesses

if __name__ == '__main__':
    res = list(futures.map(solve, xrange(0, 4)))
    fitnesses = [fit for sol, fit, fitnesses in res]

    print 'Average fitness: %s of %s trials' % (sum(fitnesses)/len(fitnesses), len(fitnesses))
    print 'Best fitness: %s' % (min(fitnesses), )

    for sol, fit, trace in res:
        if fit == min(fitnesses):
            print trace
