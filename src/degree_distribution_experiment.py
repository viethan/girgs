import girg
import numpy as np
from graph_tool.all import *
import matplotlib.pyplot as plt
from networkx.utils.random_sequence import powerlaw_sequence

def plot_median_degree_distribution_with_error_bars(n, alpha, beta, d, c):
    num_graphs = 23
    degree_frequencies = []

    max_degree = 0
    for _ in range(num_graphs):
        v_weights = np.array(powerlaw_sequence(n, beta))
        edges, coords = girg.sample_graph(v_weights, alpha, d, c)

        g = Graph(directed=False)
        g.add_vertex(n)

        for u, v in edges:
            g.add_edge(u, v)

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



N = 10000
alpha = 2.3
beta = 2.8
d = 2
c = 2

plot_median_degree_distribution_with_error_bars(N, alpha, beta, d, c) 
