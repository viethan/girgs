import girg
import numpy as np
from graph_tool.all import *
from networkx.utils.random_sequence import powerlaw_sequence
import matplotlib.pyplot as plt


def plot_degree_distribution(g):
    hist = vertex_hist(g, "total")
    y = hist[0]
    x = hist[1][:-1]
    plt.loglog(x, y, "o")
    plt.xlabel("Degree")
    plt.ylabel("Frequency")
    plt.title("Degree Distribution")
    plt.show()


N = 10000
alpha = 8
beta = 2.8
d = 2
c = 2

v_weights = np.array(powerlaw_sequence(N, beta))
edges, coords = girg.sample_graph(v_weights, alpha, d, c)

g = Graph(directed=False)
g.add_vertex(N)

for u, v in edges:
	g.add_edge(u, v)


v_coords = g.new_vertex_property("vector<long double>")
for i in range(N):
	pos = [float(val) for val in coords[i]]
	v_coords[i] = pos


graph_draw(g, pos=v_coords, output="temp.pdf")
plot_degree_distribution(g)

