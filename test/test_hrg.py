import sys
from pathlib import Path

parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from src import girg
import numpy as np
import graph_tool.all as gt
import matplotlib.pyplot as plt

def plot_median_degree_distribution_with_error_bars(n, alpha_H, C_H, T_H):
    num_graphs = 23
    degree_frequencies = []

    idx = 1
    max_degree = 0
    for _ in range(num_graphs):
        while True:
            try:
                g, _ = girg.sample_hrg(n, alpha_H, C_H, T_H)
            except ValueError:
                continue
            print(idx)
            idx += 1
            break

        # Calculate the degree distribution
        deg_freq = gt.vertex_hist(g, "total")[0].tolist()
        max_degree = max(max_degree, len(deg_freq))
        degree_frequencies.append(deg_freq)

    padded_degree_frequencies = []
    for freq in degree_frequencies:
        padded_freq = np.pad(freq, (0, max_degree - len(freq)), 'constant', constant_values=(0))
        padded_degree_frequencies.append(padded_freq)

    degree_frequencies = np.array(padded_degree_frequencies)

    degrees = np.arange(max_degree)
    median = np.median(degree_frequencies, axis=0)
    q1 = np.round(np.percentile(degree_frequencies, 25, axis=0)).astype(int)
    q3 = np.round(np.percentile(degree_frequencies, 75, axis=0)).astype(int)

    non_zero_mask = median > 0
    degrees = degrees[non_zero_mask]
    median = median[non_zero_mask]
    q1 = q1[non_zero_mask]
    q3 = q3[non_zero_mask]

    fig, ax = plt.subplots()
    ax.errorbar(degrees, median, yerr=[median - q1, q3 - median], fmt="o", capsize=5, ecolor='black', color='maroon')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Degree')
    ax.set_ylabel('Median Frequency')
    ax.set_title('Median Degree Distribution with Error Bars')
    plt.show()

def compute_clustering_coefficient(g):
    clustering_coefficient = gt.local_clustering(g)

    sumo = 0
    for i in range(g.num_vertices()):
        sumo += clustering_coefficient[i]

    return sumo / g.num_vertices()

def compute_avg_distance_giant(g):
    giant_component = gt.extract_largest_component(g, directed=False)
    dist = gt.shortest_distance(giant_component)
    avg_distance_giant = sum([sum(i) for i in dist])/(giant_component.num_vertices()**2-giant_component.num_vertices())

    return avg_distance_giant

def plot_clustering_coeff_and_avg_distance_giant_vs_vertices():
    C_H = 1
    T_Hs = [1/1.1, 1/1.6, 1/2, 1/4] # cc
    alpha_Hs = [(2.1 - 1) / 2, (2.3 - 1) / 2, (2.6 - 1) / 2, (2.9 - 1) / 2] # avg dist
    colours = ['red', 'orange', 'maroon', 'tan']
    vertex_counts = [100, 200, 400, 800, 1600, 3200, 6400, 10000]

    idx = 0
    plots1, plots2 = {}, {}
    for i in range(len(alpha_Hs)):
        alpha_H = alpha_Hs[i]
        T_H = T_Hs[i]
        colour = colours[i]

        medians1, medians2 = [], []
        q1_vals1, q1_vals2 = [], []
        q3_vals1, q3_vals2 = [], []

        for n in vertex_counts:
            clustering_coefficients = []
            avg_distances_giant = []
            for _ in range(23):
                g1, _ = girg.sample_hrg(n, (2.5 - 1) / 2, C_H, T_H) # cc
                g2, _ = girg.sample_hrg(n, alpha_H, C_H, 1/8) # avg dist


                clustering_coefficient = compute_clustering_coefficient(g1)
                clustering_coefficients.append(clustering_coefficient)
                avg_distance_giant = compute_avg_distance_giant(g2)
                avg_distances_giant.append(avg_distance_giant)

            median = np.median(clustering_coefficients)
            q1 = np.percentile(clustering_coefficients, 25)
            q3 = np.percentile(clustering_coefficients, 75)
            medians1.append(median)
            q1_vals1.append(q1)
            q3_vals1.append(q3)

            median = np.median(avg_distances_giant)
            q1 = np.percentile(avg_distances_giant, 25)
            q3 = np.percentile(avg_distances_giant, 75)
            medians2.append(median)
            q1_vals2.append(q1)
            q3_vals2.append(q3)

        plots1[(T_H, colour)] = [vertex_counts, medians1, q1_vals1, q3_vals1]
        plots2[(alpha_H, colour)] = [vertex_counts, medians2, q1_vals2, q3_vals2]


    fig, ax = plt.subplots()
    for (T_H, colour) in plots1.keys():
        ax.errorbar(plots1[(T_H, colour)][0], plots1[(T_H, colour)][1], yerr=[np.array(plots1[(T_H, colour)][1]) - np.array(plots1[(T_H, colour)][2]), np.array(plots1[(T_H, colour)][3]) - np.array(plots1[(T_H, colour)][1])], fmt="o-", capsize=5, label=f"T_H={T_H:.1f}", color=colour)

    ax.set_xlabel("Number of vertices (n)")
    ax.set_ylabel("Avg Clustering Coefficient")
    ax.legend()
    plt.show()

    fig, ax = plt.subplots()
    for (alpha_H, colour) in plots2.keys():
        ax.errorbar(plots2[(alpha_H, colour)][0], plots2[(alpha_H, colour)][1], yerr=[np.array(plots2[(alpha_H, colour)][1]) - np.array(plots2[(alpha_H, colour)][2]), np.array(plots2[(alpha_H, colour)][3]) - np.array(plots2[(alpha_H, colour)][1])], fmt="o-", capsize=5, label=f"alpha_H={alpha_H:.1f}", color=colour)

    ax.set_xlabel("Number of vertices (n)")
    ax.set_ylabel("Avg Distance in Largest Component")
    ax.legend()
    plt.show()

n = 10000
alpha_H = (2.9 - 1) / 2
C_H = 1
T_H = 1/4

plot_median_degree_distribution_with_error_bars(n, alpha_H, C_H, T_H)
plot_clustering_coeff_and_avg_distance_giant_vs_vertices()