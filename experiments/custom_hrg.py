import sys
from pathlib import Path

parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from src import girg
import numpy as np
import graph_tool.all as gt
from scipy.stats import rv_continuous

class HyperbolicDistribution(rv_continuous):
    def __init__(self, alpha_H, R):
        super().__init__()
        self.alpha_H = alpha_H
        self.R = R

    def _pdf(self, r):
        return self.alpha_H * np.sinh(self.alpha_H * r) / (np.cosh(self.alpha_H * self.R) - 1)

    def _get_support(self):
        return 0, self.R

def sample_hrg(n, alpha_H, C_H, T_H):
    # sampling random polar coordinates

    R = 2 * np.log(n) + C_H
    hyperbolic_dist = HyperbolicDistribution(alpha_H, R)
    r_coords = hyperbolic_dist.rvs(size=n)
    phi_coords = np.random.uniform(0, 2 * np.pi, size=n)

    # perform embedding
    d = 1
    beta = 2 * alpha_H + 1
    alpha = 1 / T_H
    v_weights = np.zeros(n, dtype='float64')
    v_coords = np.ndarray(shape=(n,d), dtype='float64')
    for i in range(n):
        v_weights[i] = np.exp((R - r_coords[i]) / 2)
        v_coords[i] = np.array([phi_coords[i] / (2 * np.pi)])

    # use girg sampler
    edges, coords = girg.sample_graph(v_weights, alpha, d, 1, hrg=1, R=R, T_H=T_H, v_coords=v_coords)
    g = gt.Graph(directed=False)
    g.add_vertex(n)

    for u, v in edges:
        g.add_edge(u, v)

    return g, coords

n = 1000
alpha_H = 1
C_H = 1
T_H = 0.5

g, coords = sample_hrg(n, alpha_H, C_H, T_H)

# 1. Global clustering coefficient of the graph
global_clustering_coeff = gt.global_clustering(g)[0]

# 2. Average degree of the graph
avg_degree = sum(g.degree_property_map("total").a) / g.num_vertices()

# 3. Maximum degree of the graph
max_degree = max(g.degree_property_map("total").a)

# 4. Average distance in the giant component
giant_component = gt.extract_largest_component(g, directed=False)
dist = gt.shortest_distance(giant_component)
avg_distance_giant = sum([sum(i) for i in dist])/(giant_component.num_vertices()**2-giant_component.num_vertices())

# 5. Diameter in the giant component
diameter_giant = gt.pseudo_diameter(giant_component)[0]

# Print results
print(f"Global clustering coefficient: {global_clustering_coeff}")
print(f"Average degree: {avg_degree}")
print(f"Maximum degree: {max_degree}")
print(f"Average distance in the giant component: {avg_distance_giant}")
print(f"Diameter in the giant component: {diameter_giant}")

# Drawing graph
v_coords = g.new_vertex_property("vector<long double>")
for i in range(n):
    pos = [float(val) for val in coords[i]]
    v_coords[i] = pos

gt.graph_draw(g, pos=v_coords, output="drawing.pdf")
