import sys
sys.path.insert(0, '../src/girg.cpython-310-x86_64-linux-gnu.so')

import girg
import numpy as np
from graph_tool.all import *
from networkx.utils.random_sequence import powerlaw_sequence
import matplotlib.pyplot as plt


def generate_weights(n, exponent, min_weight):
    weights = powerlaw_sequence(n, exponent)
    weights = np.array(weights)  # Convert to numpy array for easier manipulation
    weights = weights - np.min(weights) + min_weight  # Shift weights to satisfy the minimum weight constraint
    return weights

N = 10000
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

v_coords = g.new_vertex_property("vector<long double>")
for i in range(N):
	pos = [float(val) for val in coords[i]]
	v_coords[i] = pos


graph_draw(g, pos=v_coords, output="drawing.pdf")
