# coding=UTF-8
import numpy as np
from copy import deepcopy
from random import random, choice, sample
"""
Klasa implementujaca osobnika wraz z procedurami reprodukcji i mutacji

Osobnik to wektor opisujacy ile rur trzeba przeznaczyc na i-ty sposob ciecia
    wszystkie mozliwe sposoby ciecia sa wygenerowane wczesniej przez mozliwe_skroje.py
"""

class Osobnik(object):
    __slots__ = ('rozkroj', 'problem', 'fitness')

    def __init__(self, osobnik_vector, problem):
        """
        :param osobnik_vector: lista - wektor osobnika
        :type problem: Problem
        :return:
        """
        self.rozkroj = osobnik_vector
        self.problem = problem
        self.fitness = None

    def evaluate_fitness(self):
        """Oblicza fitness i ustawia .fitness odpowiednio"""
        leftovers = 0

        belek_itego_rodzaju = np.zeros(len(self.problem.typy_elementow), dtype=np.int32)
        leftovers = 0

        for krotnosc, sposob_ciecia, resztka in zip(self.rozkroj,
                                                    self.problem.mozliwe_sposoby_ciecia,
                                                    self.problem.resztka_z_ntego_sposobu_ciecia):
            belek_itego_rodzaju += sposob_ciecia * krotnosc
            leftovers += resztka * krotnosc

        if (belek_itego_rodzaju < self.problem.ilosc_elementow).any():
            self.fitness = float('-inf')
            return

        # nadmiarowe belki musza zostac policzone jako straty
        leftovers += np.sum((belek_itego_rodzaju - self.problem.ilosc_elementow) * self.problem.typy_elementow)

        self.fitness = -leftovers

    def crossover(self, osobnik):
        """:return: Osobnik"""
        # wylosuj x rozkrojow z jednego osobnika, y rozkrojow z drugiego osobnika i dawej

        nowy = np.zeros(len(self.rozkroj), dtype=np.int32)
        for i in xrange(0, len(nowy)):
            if random() > 0.5:
                nowy[i] = self.rozkroj[i]
            else:
                nowy[i] = osobnik.rozkroj[i]

        return Osobnik(nowy, self.problem)

    def copy(self):
        ":return: Osobnik"
        return deepcopy(self)

    def mutate(self):
        """Mutate this instance with probability xray"""

        index_to_mutate = np.random.randint(0, len(self.rozkroj))

        if random() > 0.5:
            self.rozkroj[index_to_mutate] -= 1
        else:
            self.rozkroj[index_to_mutate] += 1
