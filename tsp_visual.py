import networkx as nx
import matplotlib.pyplot as plt
import geocode_gather


class TSPVisual:
    # plt.ion()
    # plt.draw()
    def __init__(self, cities: list, edges=[]):
        self.G = nx.Graph()
        self.G.add_nodes_from(range(len(cities)))
        self.G.add_edges_from(edges)
        self.cities = cities
        self.edges = edges
        self.coords = geocode_gather.run(cities)
        self.labels = {i: cities[i] for i in range(len(cities))}
        nx.draw_networkx(self.G, self.coords, labels=self.labels)
        # plt.gca().axes.get_xaxis().set_visible(False)
        # plt.gca().axes.get_yaxis().set_visible(False)
        plt.show()

    def update_edges(self, new_edges: list):
        self.edges = new_edges
        self.G.remove_edges_from(self.edges)
        self.G.add_edges_from(new_edges)
        nx.draw_networkx_edges(self.G, self.coords, edgelist=self.edges)
        plt.gca().axes.get_xaxis().set_visible(False)
        plt.gca().axes.get_yaxis().set_visible(False)
        plt.show()


# def run(cities, tour):
#     coords = geocode_gather.run(cities)
#     G = nx.Graph()
#     G.add_nodes_from(range(len(cities)))
#     G.add_edges_from(tour)
#     nx.draw_networkx(G, coords)
#     plt.show()


# def init(cities):
#     coords = geocode_gather.run(cities)
#     G =