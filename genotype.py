# coding=UTF-8
from __future__ import division
from copy import deepcopy
from random import random, choice, sample, randint

class Genotype(object):
    __slots__ = ('elements', 'problem', 'fitness', 'stock_indices', 'degeneracy')

    def __init__(self, elements, problem):
        """
        :param elements: a genotype
        :type problem: Problem
        """
        self.elements = elements
        self.problem = problem
        self.fitness = None
        self.stock_indices = []

        self.degeneracy = 0

    def evaluate_fitness(self):
        """Calculates fitness, sets .fitness appropriately
        Fitness is, in this case, minus total waste
        Also fills in stock_indices"""
        leftovers = 0

        stock_size = self.problem.stock_size
        currentsum = 0
        stock_start = 0

        self.stock_indices = [] # tuple of (stock_start, stock_index_stop (exclusive), waste)

        for i, e in enumerate(self.elements):
            if e + currentsum > stock_size:
                # emit element, pass it as new one
                self.stock_indices.append((stock_start, i, stock_size - currentsum))
                leftovers += stock_size - currentsum
                stock_start = i
                currentsum = e
            else:
                currentsum += e

        self.stock_indices.append((stock_start, self.problem.elements_size, stock_size-currentsum))
        leftovers += stock_size - currentsum        # adjust for last processed element

        self.fitness = -leftovers

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
                a, b, c = pickindex(), pickindex(), pickindex()

                if self.elements[a] == self.elements[b] == self.elements[c]:
                    continue

                a_ = self.elements[a]
                self.elements[a] = self.elements[b]
                self.elements[b] = self.elements[c]
                self.elements[c] = a_

                break


