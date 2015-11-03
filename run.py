from problem import Problem
from solver import GeneticSolver

problem = Problem.load_from_file('problem.txt')

solv = GeneticSolver([], 70, 10)
solv.build_start_population(problem)

for i in xrange(0, 1000):
    wp = solv.select_winning_population()
    solv.create_population(wp)

    if i % 250 == 0:
        print 'Best solution: '+str(-wp[0].fitness)

print 'Najlepsze rozwiazania:'
for solution in solv.select_winning_population():
    solution.evaluate_fitness()
    print 'Resztek: %s degeneracja: %s' % (-solution.fitness, solution.degeneracy)
    print solution.elements
