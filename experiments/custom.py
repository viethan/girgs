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

def generate_weights(n, exponent, min_weight):
    weights = powerlaw_sequence(n, exponent)
    weights = np.array(weights)  # Convert to numpy array for easier manipulation
    weights = weights - np.min(weights) + min_weight  # Shift weights to satisfy the minimum weight constraint
    return weights

def compute_clustering_coefficient(g):
    clustering_coefficient = global_clustering(g)
    return clustering_coefficient[0]

N = 100000
alpha = 3
beta = 2.5
d = 2
c = 2

v_weights = generate_weights(N, beta, 3)
edges, coords = girg.sample_graph(v_weights, alpha, d, c)

g = Graph(directed=False)
g.add_vertex(N)

for u, v in edges:
	g.add_edge(u, v)


clustering_coefficient = compute_clustering_coefficient(g)
print(f"Clustering Coefficient: {clustering_coefficient}")


# v_coords = g.new_vertex_property("vector<long double>")
# for i in range(N):
# 	pos = [float(val) for val in coords[i]]
# 	v_coords[i] = pos


#graph_draw(g, pos=v_coords, output="temp.pdf")
#plot_degree_distribution(g)

