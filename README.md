One-dimensional stock cutting solved using genetic algorithms

An university class project

# Solution 1

First, all possible optimal patterns are enumerated. This is done by a nice tree pruning algorithm, that assumes that there will be many elements of the same length (as frequently happens in the industry).
Chromosome is a vector of (how much stock will be cut according to this pattern).

Mutation is a 5-point increment/decrement with fine-tuned probabilities.
Cross-over is a multi-point chromosome crossover, decided on per-vector basis.

In each round a population is generated unique (duplicates are removed during generation).

# Problem
Given stock of length 520, cut 70 elements of length 70 and 40 elements of length 250.

This GA computes optimal solution within on average 20 rounds. Optimal solution is 700 leftovers, and that what the algorithm gets.

