import sys
from pathlib import Path

parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from src import girg
import numpy as np
import graph_tool.all as gt
import time

def convert_number_to_circle_coordinates(number, radius=1):
    angle_rad = number * 2 * np.pi
    x = radius * np.cos(angle_rad)
    y = radius * np.sin(angle_rad)
    return (x, y)

n = 10000
alpha_H = (2.9 - 1) / 2
C_H = 1
T_H = 1/4

start_time = time.time()
g, coords = girg.sample_hrg(n, alpha_H, C_H, T_H)
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
    x, y = convert_number_to_circle_coordinates(pos[0])
    v_coords[i] = [x, y]

degrees = g.get_total_degrees(g.get_vertices())
normalised_degrees = degrees / np.max(degrees)
base_size = 10
vertex_sizes = base_size * (1 + normalised_degrees)
size_map = g.new_vertex_property("double", vals=vertex_sizes)

base_colour = np.array([1.0, 0.0, 0.0])
vertex_colours = np.outer(1 - normalised_degrees, base_colour)
vertex_colours = np.insert(vertex_colours, 3, 1, axis=1)  # Add an alpha channel
colour_map = g.new_vertex_property("vector<double>", vals=vertex_colours)

gt.graph_draw(g, pos=v_coords, vertex_size=size_map, vertex_fill_color=colour_map, output="drawing.pdf")
