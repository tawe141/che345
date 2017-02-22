import data_gather
from ortools.linear_solver import pywraplp

cities = [
    "Chicago, IL",
    "Milwaukee, WI",
    "Indianapolis, ID",
    "Kansas City, MO",
    "St. Louis, MO",
    # "Cincinnati, OH",
    # "Minneapolis, MN"
]

if __name__ == '__main__':
    d = data_gather.run(cities)
    n = len(d)
    solver = pywraplp.Solver('SolveIntegerProblem',
                             pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    def dist(i, j):
        return max(d[i][j], d[j][i])

    x = {}

    for i in range(n):
        for j in range(n):
            x[i, j] = solver.BoolVar('x[%i,%i]' % (i, j))

    solver.Minimize(solver.Sum([dist(i, j) * x[i, j] for j in range(n) for i in range(n)]))

    for i in range(n-1):
        solver.Add(solver.Sum([x[i, j] for j in range(n)]) == 1)

    for j in range(n):
        solver.Add(solver.Sum([x[i, j] for i in range(n)]) == 1)

    solver.Add(solver.Sum([x[i, i] for i in range(n)]) == 0)

    sol = solver.Solve()
    print('Total Distance: ', solver.Objective().Value())

    for key in x:
        if x[key].solution_value() > 0:
            print('travel from %d to %d' % key)

