import girg
import numpy as np
from graph_tool.all import *
import matplotlib.pyplot as plt
from networkx.utils.random_sequence import powerlaw_sequence

def compute_clustering_coefficient(g):
    clustering_coefficient = global_clustering(g)
    return clustering_coefficient[0]

def plot_clustering_coefficient_vs_vertices():
    tau = 2.5
    alphas = [1.1, 1.5, 2, 3]
    colors = ['blue', 'orange', 'green', 'red']
    vertex_counts = [100, 200, 400, 800, 1600, 3200, 6400, 12800, 25600]

    fig, ax = plt.subplots()
    for alpha, color in zip(alphas, colors):
        medians = []
        q1_vals = []
        q3_vals = []

        for n in vertex_counts:
            clustering_coefficients = []
            for _ in range(23):
                v_weights = np.array(powerlaw_sequence(n, tau))
                edges, coords = girg.sample_graph(v_weights, alpha, 2, 2)

                g = Graph(directed=False)
                g.add_vertex(n)

                for u, v in edges:
                    g.add_edge(u, v)

                clustering_coefficient = compute_clustering_coefficient(g)
                clustering_coefficients.append(clustering_coefficient)

            median = np.median(clustering_coefficients)
            q1 = np.percentile(clustering_coefficients, 25)
            q3 = np.percentile(clustering_coefficients, 75)
            medians.append(median)
            q1_vals.append(q1)
            q3_vals.append(q3)

        ax.errorbar(vertex_counts, medians, yerr=[np.array(medians) - np.array(q1_vals), np.array(q3_vals) - np.array(medians)], fmt="o-", capsize=5, label=f"alpha={alpha}", color=color)

    ax.set_xscale("log")
    ax.set_xlabel("Number of vertices (n)")
    ax.set_ylabel("Clustering coefficient")
    ax.legend()
    plt.title("Clustering coefficient vs number of vertices for different alpha values")
    plt.show()


plot_clustering_coefficient_vs_vertices()
