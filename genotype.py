# coding=UTF-8
import numpy as np
from copy import deepcopy
from random import random, choice, sample
"""
Klasa implementujaca osobnika wraz z procedurami reprodukcji i mutacji

Osobnik to wektor opisujacy ile rur trzeba przeznaczyc na i-ty sposob ciecia
    wszystkie mozliwe sposoby ciecia sa wygenerowane wczesniej przez mozliwe_skroje.py
"""

class Genotype(object):
    __slots__ = ('elements', 'problem', 'fitness')

    def __init__(self, elements, problem):
        """
        :param elements: a genotype
        :type problem: Problem
        """
        self.elements = elements
        self.problem = problem
        self.fitness = None

    def evaluate_fitness(self):
        """Calculates fitness, sets .fitness appropriately
        Fitness is, in this case, minus total waste"""
        leftovers = 0

        stock_size = self.problem.stock_size
        currentsum = 0

        for e in self.elements:
            if e + currentsum > stock_size:
                # emit element, pass it as new one
                leftovers += stock_size - currentsum
                currentsum = e
            else:
                currentsum += e

        leftovers += stock_size - currentsum        # adjust for last processed element

        self.fitness = -leftovers

    def copy(self):
        ":return: Genotype"
        return deepcopy(self)

    def mutate(self):
        """Mutate this instance"""
        a, b, c = sample(xrange(0, self.problem.elements_size), 3)

        a_ = self.elements[a]
        self.elements[a] = self.elements[b]
        self.elements[b] = self.elements[c]
        self.elements[c] = a_
