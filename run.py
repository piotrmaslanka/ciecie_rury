from problem import Problem
from solver import GeneticSolver

problem = Problem.load_from_file('problem.txt')

solv = GeneticSolver([], 100, 30)
solv.build_start_population(problem)

for i in xrange(0, 20000):
    wp = solv.select_winning_population()
    solv.create_population(wp)

print 'Najlepsze rozwiazania:'
for solution in solv.select_winning_population():
    solution.evaluate_fitness()
    print 'Resztek: %s' % (-solution.fitness,)
