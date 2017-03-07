import networkx as nx
import matplotlib.pyplot as plt
import geocode_gather


class TSPVisual:
    # plt.draw()
    def __init__(self, cities: list, edges=[]):
        # plt.ion()
        self.G = nx.Graph()
        self.G.add_nodes_from(range(len(cities)))
        self.G.add_edges_from(edges)
        self.cities = cities
        self.edges = edges
        self.coords = geocode_gather.run(cities)
        self.labels = {i: cities[i] for i in range(len(cities))}
        nx.draw_networkx(self.G, self.coords, labels=self.labels)
        plt.gca().axes.get_xaxis().set_visible(False)
        plt.gca().axes.get_yaxis().set_visible(False)
        plt.title('Iteration 1')
        # plt.show()

    def update_edges(self, new_edges: list, iterations: int):
        plt.clf()
        plt.ion()
        self.edges = new_edges
        # self.G.remove_edges_from(self.edges)
        self.G.clear()
        self.G.add_nodes_from(range(len(self.cities)))
        self.G.add_edges_from(new_edges)
        nx.draw_networkx(self.G, self.coords, edgelist=self.edges, labels=self.labels)
        plt.gca().axes.get_xaxis().set_visible(False)
        plt.gca().axes.get_yaxis().set_visible(False)
        plt.title('Iteration %i' % iterations)
        # plt.show()


    def hold(self):
        plt.ioff()
        plt.show()

