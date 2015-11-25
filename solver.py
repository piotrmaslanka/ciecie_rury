# coding=UTF-8
from osobnik import Osobnik
from copy import copy
import random
try:
    import numpy as np
except ImportError:
    import numpypy as np

class GeneticSolver(object):
    """Rozwiazywacz problemu"""

    def __init__(self, starting_population,
                 population_size,
                 winning_population_size,
                 probability_of_selecting_mutant):
        self.population = starting_population
        self.population_size = population_size
        self.probability_of_selecting_mutant = probability_of_selecting_mutant
        self.winning_population_size = winning_population_size


    def _build_osobnik(self, problem):
        oso = Osobnik(np.zeros(problem.dl_rek, dtype=np.int32), problem)
        oso.evaluate_fitness()

        last_fit = float('-inf')
        while oso.fitness > last_fit:
            last_fit = oso.fitness
            oso.mutate()
            oso.evaluate_fitness()

        return oso

    def build_start_population(self, problem):
        """Buduje populacje startowa ex nihilo. Ewaluuje fitness"""
        for i in xrange(0, self.population_size):
            oso =  self._build_osobnik(problem)
            self.population.append(oso)

    def select_winning_population(self):
        """
        Return winning population.

        :return: list of (osobnik, osobnik's fitness) sorted DESC
        """
        self.population.sort(key=lambda osobnik: osobnik.fitness, reverse=True)
        return self.population[:self.winning_population_size]

    def create_population(self, winning_population, iteration):
        """Zasadniczo osobniki z winning_population awansem przechodza do nowej populacji.
        Reszta to dzieci osobnikow z populacji zwycieskiej.
        Ewaluuje im fitness"""

        new_population = set(copy(winning_population))

        posm = self.probability_of_selecting_mutant(iteration)

        def exp_pick(winning_population):
            """pick an element from winning_population with exponential probability"""
            while True:
                left, right = winning_population[:len(winning_population)/2], winning_population[len(winning_population)/2:]
                if random.random() < 0.7:
                    winning_population = left
                else:
                    winning_population = right

                if len(winning_population) == 1:
                    return winning_population[0]

        while len(new_population) < self.population_size:
            # ok. Dopoki nie ma wystarczajacej ilosc osobnikow, zrob typa

            if random.random() < posm:
                osob = exp_pick(winning_population).copy()
                osob.mutate()
            else:
                o1 = exp_pick(winning_population)
                o2 = exp_pick(winning_population)
                osob = o1.crossover(o2)
                osob.mutate()

            osob.evaluate_fitness()
            new_population.add(osob)

        self.population = list(new_population)

