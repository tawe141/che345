import data_gather
from ortools.linear_solver import pywraplp

cost_lim = 7 * 10 ** 6

cities = [
    "Chicago, IL",
    "Milwaukee, WI",
    "Indianapolis, ID",
    "Kansas City, MO",
    "St. Louis, MO",
    "Cincinnati, OH",
    "Columbus, OH",
    "Minneapolis, MN",
    "Detroit, MI",
    "New York, NY",
    "Los Angeles, CA",
    "San Francisco, CA",
    "San Diego, CA",
    "Reno, NV",
    "Houston, TX",
    "Phoenix, AZ",
    "Charlotte, NC",
    "Seattle, WA",
    "Boston, MA",
    "Memphis, TN",
    "Washington, DC",
    "Atlanta, GA",
    "New Orleans, LA",
    "Nashville, TN",
    "Denver, CO",
    "Las Vegas, NV",
    "Austin, TX",
    "Philadelphia, PA",
    "Pittsburgh, PA",
    "Dallas, TX",
    "Corpus Christi, TX",
    "Portland, OR",
    "Billings, MT",
    "Miami, FL",
    "Orlando, FL",
    "Tampa, FL",
    "Little Rock, AR",
    "Providence, RI",
    "Salt Lake City, UT",
    "Tucson, AZ",
    "Albuquerque, NM",
    "Oklahoma City, OK"
]


def find_next_edge(origin: int, trip_list: list) -> bool or tuple:
    """
    Returns next edge in tour.
    Returns False if no next edge exists in trip_list.
    
    :rtype: False or tuple
    :param origin: int
    :param trip_list: list of edges (tuples)
    :return: next edge (tuple) in tour
    """
    for i in range(n):
        if (origin, i) in trip_list:
            return origin, i
    return False


def find_one_subtour(origin: int, trip_list: list, partial=set()) -> set:
    """
    Finds a single subtour in trip_list with a given origin
    
    :rtype: set
    :param origin: int
    :param trip_list: list
    :param partial: set
    :return: set containing all edges in a subtour
    """
    next_edge = find_next_edge(origin, trip_list)
    if not next_edge:
        return partial
    else:
        trip_list.remove(next_edge)
        partial.add(next_edge)
        return find_one_subtour(next_edge[1], trip_list, partial)


def find_subtours(trip_list: list, visited=None, partial=[]) -> list:
    """
    Finds all subtours in trip_list
    Returns list of sets, each set being a single subtour.

    :rtype: list
    :param trip_list: list of edges in trip
    :param visited: list of ints. each int is a vertex
    :param partial: object containing intermediate subtour sets
    :return: list of subtours (sets)
    """
    if len(trip_list) == 0:
        return partial
    if visited is None:
        origin = 0
        visited = []
        subtour = find_one_subtour(origin, trip_list)
        for edge in subtour:
            if edge[0] not in visited:
                visited.append(edge[0])
        return find_subtours(trip_list, visited, [subtour])
    else:
        new_origin = trip_list[0][0]
        subtour = find_one_subtour(new_origin, trip_list, partial=set())
        for edge in subtour:
            if edge[0] not in visited:
                visited.append(edge[0])
        return find_subtours(trip_list, visited, partial + [subtour])


def pretty_solve(solver, iterations=1):
    """
    Solves and prints result of iteration
    Iteration number defaults to first iteration (1)

    :param solver: solver Object (or-tools)
    :param iterations: int
    :return: list of edges travelled in tour as generated by solver.Solve()
    """
    if iterations == 1:
        print('Iteration %i: No subtour elimination' % iterations)
    else:
        print('Iteration %i: Subtour elimination %i' % (iterations, iterations - 1))
    solver.Solve()
    print('Cities visited: ', solver.Objective().Value())

    tour = [key for key in x if x[key].solution_value() > 0]
    for t in tour:
        # print('Travel from %s to %s' % (cities[t[0]], cities[t[1]]))
        print('Travel from %i to %i' % t)
    return tour


def organize_tour(tour: set) -> list:
    result = [tour.pop(0)]
    while len(tour) > 0:
        next = find_next_edge(result[-1][1], tour)
        result.append(next)
        tour.remove(next)
    return result


# def generate_map_link(tour: set) -> str:
#     organized_tour = [tour[0]]
#     while len(tour) > 0:
#

def visited(tour: set) -> list:
    v = []
    for t in tour:
        if t[0] not in v:
            v.append(t[0])
        if t[1] not in v:
            v.append(t[1])

    return v


if __name__ == '__main__':
    # gather distance data
    d = data_gather.run(cities)
    n = len(d)

    # instantiate MILP solver. uses CBC algorithm
    solver = pywraplp.Solver('SolveIntegerProblem',
                             pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)


    # reflect upper triangular matrix across diagonal
    def dist(i, j):
        return max(d[i][j], d[j][i])


    # instantiate x(i, j), binary decision variables
    # 0 indicates did not travel on edge x(i,j), 1 indicates did travel
    x = {}
    for i in range(n):
        for j in range(n):
            x[i, j] = solver.BoolVar('x[%i,%i]' % (i, j))

    # objective function: maximize the number of cities visited
    # caution: formulation actually assumes directed graph
    # undirected case as described by Laporte 1987 is far more efficient
    solver.Maximize(solver.Sum([x[i, j] for j in range(n) for i in range(n)]))

    solver.Add(solver.Sum([x[0, j] for j in range(1, n)]) == 1)
    solver.Add(solver.Sum([x[i, 0] for i in range(1, n)]) == 1)

    for k in range(1, n):
        solver.Add(solver.Sum([x[i, k] for i in range(n)]) == solver.Sum([x[k, j] for j in range(n)]))
        solver.Add(solver.Sum([x[i, k] for i in range(n)]) <= 1)

    solver.Add(solver.Sum([dist(i, j) * x[i, j] for j in range(n) for i in range(n)]) <= cost_lim)

    # set diagonals x(i,i) for all i to 0
    solver.Add(solver.Sum([x[i, i] for i in range(n)]) == 0)

    # first iteration solve
    tour = pretty_solve(solver)
    iteration = 1

    # find all subtours in resulting trip
    tours = find_subtours(tour)

    # while number of subtours is more than 1...
    while len(tours) > 1:
        # find smallest subtour among all subtours
        smallest_subtour = min(tours, key=len)
        v = visited(smallest_subtour)

        # # add a new constraint. let {S} be all x(i,j) in subtour
        # # sum of all x(i,j) in {S} must be less than |S|-1
        # solver.Add(solver.Sum([x[i] for i in smallest_subtour]) <= len(smallest_subtour) - 1)

        # add a new constraint.
        solver.Add(
            solver.Sum(
                [
                    solver.Sum(
                        [x[i, k] for i in range(n)]
                    ) +
                    solver.Sum(
                        [x[k, j] for j in range(n)]
                    )
                    for k in v
                    ]
            ) <= len(smallest_subtour) * (
                solver.Sum([x[i, j] for j in range(n) if j not in v for i in range(n) if i in v])
                +
                solver.Sum([x[i, j] for j in range(n) if j in v for i in range(n) if i not in v])
            )
        )

        iteration += 1
        tour = pretty_solve(solver, iteration)
        tours = find_subtours(tour)

    print('Feasible solution found for %i cities!' % n)
    print('Number of cities visited: %i' % int(solver.Objective().Value()))
    print('Number of subtour eliminations: %i' % (iteration - 1))
    print('Number of variables: %i' % solver.NumVariables())
    print('Number of constraints: %i' % solver.NumConstraints())

    # print(organize_tour(tours[0]))
