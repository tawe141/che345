import data_gather
from tsp_visual import TSPVisual
from ortools.linear_solver import pywraplp

cities = [
    "Chicago, IL",
    "Milwaukee, WI",
    "Indianapolis, ID",
    "Kansas City, MO",
    "St. Louis, MO",
    "Cincinnati, OH",
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
    # "Seattle, WA",
    # "Boston, MA",
    # "Memphis, TN",
    # "Washington, DC",
    # "Atlanta, GA",
    # "New Orleans, LA",
    # "Nashville, TN",
    # "Denver, CO",
    # "Las Vegas, NV",
    # "Austin, TX",
    # "Philadelphia, PA",
    # "Pittsburgh, PA",
    # "Dallas, TX",
    # "Corpus Christi, TX",
    # "Portland, OR",
    # "Billings, MT"
]

visual = TSPVisual(cities)


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
    print('Total Distance: ', solver.Objective().Value())

    tour = [key for key in x if x[key].solution_value() > 0]
    for t in tour:
        # print('Travel from %s to %s' % (cities[t[0]], cities[t[1]]))
        print('Travel from %i to %i' % t)

    visual.update_edges(tour, iterations)

    return tour


# def organize_tour(tour: set) -> list:
#     result = [tour.pop(0)]
#     while len(tour) > 0:
#         next = find_next_edge(result[-1][1], tour)
#         result.append(next)
#         tour.remove(next)
#     return result


# def generate_map_link(tour: set) -> str:
#     organized_tour = [tour[0]]
#     while len(tour) > 0:
#


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

    # objective function: minimize total distance travelled
    solver.Minimize(solver.Sum([dist(i, j) * x[i, j] for j in range(n) for i in range(n)]))

    # all rows sum to 1
    for i in range(n):
        solver.Add(solver.Sum([x[i, j] for j in range(n)]) == 1)

    # all columns sum to 1
    for j in range(n):
        solver.Add(solver.Sum([x[i, j] for i in range(n)]) == 1)

    # set diagonals x(i,i) for all i to 0
    solver.Add(solver.Sum([x[i, i] for i in range(n)]) == 0)

    # first iteration solve
    tour = pretty_solve(solver)
    iteration = 1

    # find all subtours in resulting trip
    tours = find_subtours(tour)

    # while number of subtours is more than 1...
    while len(tours) > 1:
        # # find smallest subtour among all subtours
        # smallest_subtour = min(tours, key=len)

        # # add a new constraint. let {S} be all x(i,j) in subtour
        # # sum of all x(i,j) in {S} must be less than |S|-1
        # solver.Add(solver.Sum([x[i] for i in smallest_subtour]) <= len(smallest_subtour) - 1)

        # for each subtour found, add constraint such that subtour is eliminated

        for t in tours:
            solver.Add(solver.Sum([x[i] for i in t]) <= len(t) - 1)

        iteration += 1
        tour = pretty_solve(solver, iteration)
        tours = find_subtours(tour)

    print('Feasible solution found for %i cities!' % n)
    print('Number of subtour eliminations: %i' % (iteration - 1))
    print('Number of variables: %i' % solver.NumVariables())
    print('Number of constraints: %i' % solver.NumConstraints())

    # visual = TSPVisual(cities, [key for key in x if x[key].solution_value() > 0])
    visual.hold()

    # print(organize_tour(tours[0]))

