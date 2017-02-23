import data_gather
from ortools.linear_solver import pywraplp

cities = [
    "Chicago, IL",
    "Milwaukee, WI",
    "Indianapolis, ID",
    "Kansas City, MO",
    "St. Louis, MO",
    "Cincinnati, OH",
    "Minneapolis, MN"
]


def find_next_edge(origin: int, trip_list: list) -> bool or tuple:
    for i in range(n):
        if (origin, i) in trip_list:
            return origin, i
    return False


def find_one_subtour(origin: int, trip_list: list, partial=set()) -> set:
    next_edge = find_next_edge(origin, trip_list)
    if not next_edge:
        return partial
    else:
        trip_list.remove(next_edge)
        partial.add(next_edge)
        return find_one_subtour(next_edge[1], trip_list, partial)


def find_subtours(trip_list: list, visited=None, partial=[]) -> list:
    if len(trip_list) == 0:
        return partial
    if visited is None:
        origin = 0
        visited = []
        subtour = find_one_subtour(origin, trip_list)
        for edge in subtour:
            visited.append(edge[0])
        return find_subtours(trip_list, visited, [subtour])
    else:
        not_visited = [i for i in range(n) if i not in visited]
        new_origin = not_visited[0]
        subtour = find_one_subtour(new_origin, trip_list, partial=set())
        for edge in subtour:
            visited.append(edge[0])
        return find_subtours(trip_list, visited, partial + [subtour])


def pretty_solve(solver, iterations=1):
    if iterations == 1:
        print('Iteration %i: No subtour elimination' % iterations)
    else:
        print('Iteration %i: Subtour elimination %i' % (iterations, iterations - 1))
    solver.Solve()
    print('Total Distance: ', solver.Objective().Value())

    tour = [key for key in x if x[key].solution_value() > 0]
    for t in tour:
        print('Travel from %i to %i' % t)

    return tour


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

    tour = pretty_solve(solver)
    iteration = 1

    tours = find_subtours(tour)

    while len(tours) > 1:
        smallest_subtour = min(tours, key=len)
        solver.Add(solver.Sum([x[i] for i in smallest_subtour]) <= len(smallest_subtour) - 1)
        iteration += 1
        tour = pretty_solve(solver, iteration)
        tours = find_subtours(tour)
    print('Optimal Solution Found!')
