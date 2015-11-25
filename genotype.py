# coding=UTF-8
from __future__ import division
from copy import deepcopy
from random import random, choice, sample, randint

class Genotype(object):
    __slots__ = ('elements', 'problem', 'fitness', 'stock_indices', 'degeneracy')

    def __init__(self, indices, problem):
        """
        :param indices: indices to elementy array in problem
        :type problem: Problem
        """
        self.indices = indices
        self.problem = problem
        self.fitness = None
        self.stock_indices = []

        self.degeneracy = 0

    def evaluate_fitness(self):
        """Calculates fitness, sets .fitness appropriately
        Fitness is, in this case, minus total waste
        Also fills in stock_indices"""


    def copy(self):
        ":return: Genotype"
        q = deepcopy(self)
        q.degeneracy = 0
        return q

    def degenerate(self):
        self.degeneracy += 1

    def mutate(self):
        """
        Mutate this instance.

        Runtime: O(N)
        """
        all_leftovers = -self.fitness

        def pickindex():
            #pq = random()
            #for ss, se, leftovers in self.stock_indices:
            #    pce = leftovers / all_leftovers / (se-ss)
            #    for i in xrange(ss, se):
            #        if pq < pce:
            #            return i
            #        pq -= pce
            #return self.problem.elements_size-1
            return randint(0, self.problem.elements_size-1)

        for i in xrange(0, (self.degeneracy // 2)+1):

            while True:
                a, b = pickindex(), pickindex()

                if self.elements[a] == self.elements[b]:
                    continue

                a_ = self.elements[a]
                self.elements[a] = self.elements[b]
                self.elements[b] = a_

                break


