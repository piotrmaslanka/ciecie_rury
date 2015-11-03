# coding=UTF-8
from genotype import Genotype
from copy import copy
import random

class GeneticSolver(object):
    """Rozwiazywacz problemu"""

    def __init__(self, starting_population,
                 population_size,
                 winning_population_size):
        self.population = starting_population
        self.population_size = population_size
        self.winning_population_size = winning_population_size

    def build_start_population(self, problem):
        """Builds a starting population. Evaluates fitness"""
        for i in xrange(0, self.population_size):
            random.shuffle(problem.elements)
            oso = Genotype(problem.elements[:], problem)
            oso.evaluate_fitness()
            self.population.append(oso)

    def select_winning_population(self):
        """
        Return winning population.

        :return: list of (genotype, genotype's fitness) sorted DESC
        """
        self.population.sort(key=lambda genotype: genotype.fitness, reverse=True)
        return self.population[:self.winning_population_size]

    def create_population(self, winning_population):
        """Builds a population from winning population.
        Evaluates their fitness"""

        new_population = copy(winning_population)

        for winnar in winning_population[:self.population_size-len(new_population)]:
            osob = winnar.copy()
            osob.mutate()
            winnar.degenerate()
            osob.evaluate_fitness()
            new_population.append(osob)

        while len(new_population) < self.population_size:
            # ok. Dopoki nie ma wystarczajacej ilosc osobnikow, zrob typa
            rc = random.choice(winning_population)
            osob = rc.copy()
            osob.mutate()
            rc.degenerate()

            osob.evaluate_fitness()
            new_population.append(osob)

