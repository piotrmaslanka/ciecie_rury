# coding=UTF-8
from osobnik import Osobnik
from copy import copy
import random
import numpy as np

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

    def build_start_population(self, problem):
        """Buduje populacje startowa ex nihilo. Ewaluuje fitness"""
        for i in xrange(0, self.population_size):
            oso = Osobnik(np.random.randint(0, 50, size=problem.dl_rek), problem)
            oso.evaluate_fitness()
            self.population.append(oso)

    def select_winning_population(self):
        """
        Return winning population.

        :return: list of (osobnik, osobnik's fitness) sorted DESC
        """
        self.population.sort(key=lambda osobnik: osobnik.fitness, reverse=True)
        return self.population[:self.winning_population_size]

    def create_population(self, winning_population):
        """Zasadniczo osobniki z winning_population awansem przechodza do nowej populacji.
        Reszta to dzieci osobnikow z populacji zwycieskiej.
        Ewaluuje im fitness"""

        new_population = copy(winning_population)

        while len(new_population) < self.population_size:
            # ok. Dopoki nie ma wystarczajacej ilosc osobnikow, zrob typa
            if random.random() < self.probability_of_selecting_mutant:
                osob = random.choice(winning_population).copy()
                osob.mutate()
            else:
                o1 = random.choice(winning_population)
                o2 = random.choice(winning_population)
                osob = o1.crossover(o2)

            osob.evaluate_fitness()
            new_population.append(osob)

