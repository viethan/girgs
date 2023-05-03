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

def plot_median_degree_distribution_with_error_bars(n, alpha, beta, d, c, min_weight):
    num_graphs = 23
    degree_frequencies = []

    max_degree = 0
    for _ in range(num_graphs):
        g, coords = girg.sample_girg(n, alpha, beta, d, c, min_weight)

        # Calculate the degree distribution
        deg_freq = vertex_hist(g, "total")[0].tolist()
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
    ax.errorbar(degrees, median, yerr=[median - q1, q3 - median], fmt="o", capsize=5, ecolor='black')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Degree')
    ax.set_ylabel('Median Frequency')
    ax.set_title('Median Degree Distribution with Error Bars')
    plt.show()


N = 1000
alpha = 2.3
beta = 2.8
d = 2
c = 2
min_weight = 3

plot_median_degree_distribution_with_error_bars(N, alpha, beta, d, c, min_weight) 
