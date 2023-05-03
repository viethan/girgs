import sys
from pathlib import Path

parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from src import girg
import numpy as np
from graph_tool.all import *
import matplotlib.pyplot as plt
from networkx.utils.random_sequence import powerlaw_sequence

def compute_avg_distance_giant(g):
    giant_component = extract_largest_component(g, directed=False)
    dist = shortest_distance(giant_component)
    avg_distance_giant = sum([sum(i) for i in dist])/(giant_component.num_vertices()**2-giant_component.num_vertices())

    return avg_distance_giant

def plot_avg_distance_giant_vs_vertices():
    alpha = 8
    betas = [2.1, 2.3, 2.6, 2.9]
    colours = ['red', 'orange', 'maroon', 'tan']
    vertex_counts = [100, 200, 400, 800, 1600, 3200, 6400, 10000]

    plots = {}
    for beta, colour in zip(betas, colours):
        medians = []
        q1_vals = []
        q3_vals = []

        for n in vertex_counts:
            avg_distances_giant = []
            for _ in range(23):
                g, coords = girg.sample_girg(n, alpha, beta, 2, 2, 3)

                avg_distance_giant = compute_avg_distance_giant(g)
                avg_distances_giant.append(avg_distance_giant)

            median = np.median(avg_distances_giant)
            q1 = np.percentile(avg_distances_giant, 25)
            q3 = np.percentile(avg_distances_giant, 75)
            medians.append(median)
            q1_vals.append(q1)
            q3_vals.append(q3)

        plots[(beta, colour)] = [vertex_counts, medians, q1_vals, q3_vals]

        
    for (beta, colour) in plots.keys():
        fig, ax = plt.subplots()
        ax.errorbar(plots[(beta, colour)][0], plots[(beta, colour)][1], yerr=[np.array(plots[(beta, colour)][1]) - np.array(plots[(beta, colour)][2]), np.array(plots[(beta, colour)][3]) - np.array(plots[(beta, colour)][1])], fmt="o-", capsize=5, label=f"beta={beta}", color=colour)

        ax.set_xlabel("Number of vertices (n)")
        ax.set_ylabel("Avg Distance in Largest Component")
        ax.legend()
        plt.show()

    fig, ax = plt.subplots()
    for (beta, colour) in plots.keys():
        ax.errorbar(plots[(beta, colour)][0], plots[(beta, colour)][1], yerr=[np.array(plots[(beta, colour)][1]) - np.array(plots[(beta, colour)][2]), np.array(plots[(beta, colour)][3]) - np.array(plots[(beta, colour)][1])], fmt="o-", capsize=5, label=f"beta={beta}", color=colour)

    ax.set_xlabel("Number of vertices (n)")
    ax.set_ylabel("Avg Distance in Largest Component")
    ax.legend()
    plt.show()


plot_avg_distance_giant_vs_vertices()
