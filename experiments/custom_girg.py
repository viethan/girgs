import sys
from pathlib import Path

parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from src import girg
import graph_tool.all as gt
import time

n = 10000
alpha = 8
beta = 2.8
d = 2
c = 1
min_weigth = 3

start_time = time.time()
g, coords = girg.sample_girg(n, alpha, beta, d, c, min_weigth)
print("--- %s seconds ---" % (time.time() - start_time))

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
