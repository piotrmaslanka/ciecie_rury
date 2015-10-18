from problem import Problem
from solver import GeneticSolver

problem = Problem.laduj_z_pliku('problem.txt')
problem.print_()

solv = GeneticSolver([], 200, 20, 0.2)
solv.build_start_population(problem)


for i in xrange(0, 1000000):
    wp = solv.select_winning_population()
    solv.create_population(wp)


print 'Najlepsze rozwiazania:'
for solution in solv.select_winning_population():
    solution.evaluate_fitness()
    print 'Resztek: %s' % (-solution.fitness,)
    for howmany, sposob in zip(solution.rozkroj, problem.mozliwe_sposoby_ciecia):
        print '%s razy rozkroj typu %s' % (
            howmany,
            ' '.join(map(str, map(int, sposob)))
        )
    print ' '