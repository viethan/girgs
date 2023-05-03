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

def compute_clustering_coefficient(g):
    clustering_coefficient = local_clustering(g)

    sumo = 0
    for i in range(g.num_vertices()):
        sumo += clustering_coefficient[i]

    return sumo / g.num_vertices()

def plot_clustering_coefficient_vs_vertices():
    tau = 2.5
    alphas = [1.1, 1.6, 2, 4]
    colours = ['red', 'orange', 'maroon', 'tan']
    vertex_counts = [100, 200, 400, 800, 1600, 3200, 6400, 10000]

    plots = {}
    for alpha, colour in zip(alphas, colours):
        medians = []
        q1_vals = []
        q3_vals = []

        for n in vertex_counts:
            clustering_coefficients = []
            for _ in range(23):
                g, coords = girg.sample_girg(n, alpha, tau, 2, 2, 3)

                clustering_coefficient = compute_clustering_coefficient(g)
                clustering_coefficients.append(clustering_coefficient)

            median = np.median(clustering_coefficients)
            q1 = np.percentile(clustering_coefficients, 25)
            q3 = np.percentile(clustering_coefficients, 75)
            medians.append(median)
            q1_vals.append(q1)
            q3_vals.append(q3)

        plots[(alpha, colour)] = [vertex_counts, medians, q1_vals, q3_vals]

        
    for (alpha, colour) in plots.keys():
        fig, ax = plt.subplots()
        ax.errorbar(plots[(alpha, colour)][0], plots[(alpha, colour)][1], yerr=[np.array(plots[(alpha, colour)][1]) - np.array(plots[(alpha, colour)][2]), np.array(plots[(alpha, colour)][3]) - np.array(plots[(alpha, colour)][1])], fmt="o-", capsize=5, label=f"alpha={alpha}", color=colour)

        ax.set_xlabel("Number of vertices (n)")
        ax.set_ylabel("Avg Clustering Coefficient")
        ax.legend()
        plt.show()

    fig, ax = plt.subplots()
    for (alpha, colour) in plots.keys():
        ax.errorbar(plots[(alpha, colour)][0], plots[(alpha, colour)][1], yerr=[np.array(plots[(alpha, colour)][1]) - np.array(plots[(alpha, colour)][2]), np.array(plots[(alpha, colour)][3]) - np.array(plots[(alpha, colour)][1])], fmt="o-", capsize=5, label=f"alpha={alpha}", color=colour)

    ax.set_xlabel("Number of vertices (n)")
    ax.set_ylabel("Avg Clustering Coefficient")
    ax.legend()
    plt.show()


plot_clustering_coefficient_vs_vertices()
