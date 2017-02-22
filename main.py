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


def find_next_edge(origin: int, trip_list: list) -> bool or tuple:
    for i in range(n):
        if (origin, i) in trip_list:
            return origin, i
    return False


def find_one_subtour(origin: int, trip_list: list, partial=[]) -> list:
    if origin >= len(trip_list):
        raise ValueError('Origin index not found in trip list')
    next_edge = find_next_edge(origin, trip_list)
    if not next_edge:
        return partial
    else:
        trip_list.remove(next_edge)
        partial.append(next_edge)
        return find_one_subtour(next_edge[1], trip_list, partial)


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

    for i in range(n):
        solver.Add(solver.Sum([x[i, j] for j in range(n)]) == 1)

    for j in range(n):
        solver.Add(solver.Sum([x[i, j] for i in range(n)]) == 1)

    solver.Add(solver.Sum([x[i, i] for i in range(n)]) == 0)

    print('Iteration 1: No subtour elimination')
    sol = solver.Solve()
    print('Total Distance: ', solver.Objective().Value())

    tour = [key for key in x if x[key].solution_value() > 0]
    for t in tour:
        print('Travel from %i to %i' % t)

    print(find_one_subtour(0, tour))

