import networkx as nx
import matplotlib.pyplot as plt
import geocode_gather


def run(cities, tour):
    coords = geocode_gather.run(cities)
    G = nx.Graph()
    G.add_nodes_from(range(len(cities)))
    G.add_edges_from(tour)
    nx.draw_networkx(G, coords)
    plt.show()