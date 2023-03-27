import girg
import numpy as np
from graph_tool.all import *
from networkx.utils.random_sequence import powerlaw_sequence
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def cube_to_torus_coordinates(coords, R, r):
    # coords: list of d-dimensional coordinates, where each coordinate is a tuple (x, y, z, ...)
    # R: the major radius of the torus
    # r: the minor radius of the torus

    torus_coords = []
    for coord in coords:
        theta = 2 * np.pi * coord[0]  # Map the first coordinate to the circle around the z-axis
        phi = 2 * np.pi * coord[1]    # Map the second coordinate to the circle along the torus

        x = (R + r * np.cos(phi)) * np.cos(theta)
        y = (R + r * np.cos(phi)) * np.sin(theta)
        z = r * np.sin(phi)

        torus_coords.append((x, y, z))

    return torus_coords


def draw_torus(ax, R, r, num_points=100):
    u = np.linspace(0, 2 * np.pi, num_points)
    v = np.linspace(0, 2 * np.pi, num_points)
    U, V = np.meshgrid(u, v)

    X = (R + r * np.cos(V)) * np.cos(U)
    Y = (R + r * np.cos(V)) * np.sin(U)
    Z = r * np.sin(V)

    ax.plot_surface(X, Y, Z, color='c', alpha=0.3)

def visualize_torus_graph(g, vertex_positions, R, r):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Draw the 3D torus
    draw_torus(ax, R, r)

    torus_positions = cube_to_torus_coordinates(vertex_positions, R, r)

    # Plot vertices
    for pos in torus_positions:
        ax.scatter(*pos, color='r', s=20)

    # Plot edges
    for edge in g.edges():
        src, tgt = map(int, (edge.source(), edge.target()))
        src_pos, tgt_pos = torus_positions[src], torus_positions[tgt]
        ax.plot([src_pos[0], tgt_pos[0]], [src_pos[1], tgt_pos[1]], [src_pos[2], tgt_pos[2]], 'b--')

    plt.show()



N = 100000
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

# R, r = 3, 1  # Set the major and minor radii of the torus
# visualize_torus_graph(g, coords, R, r)

v_coords = g.new_vertex_property("vector<long double>")
for i in range(N):
	pos = [float(val) for val in coords[i]]
	v_coords[i] = pos

graph_draw(g, pos=v_coords, output="temp.pdf")
