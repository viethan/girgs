import sys
from pathlib import Path

parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from src import girg
import numpy as np
import graph_tool.all as gt
import matplotlib.pyplot as plt
import time

def plot_scaling():
    C_H = 1
    betas = [2.1, 2.3, 2.6, 2.9]
    alphas = [1.1, 1.6, 2, 4]
    colours = ['red', 'orange', 'maroon', 'tan']
    vertex_counts = [1000, 2500, 5000, 10000, 25000, 50000, 100000, 250000, 500000, 1000000]

    idx = 0
    plots1, plots2 = {}, {}
    for i in range(len(alphas)):
        alpha = alphas[i]
        beta = betas[i]
        colour = colours[i]

        medians1, medians2 = [], []
        q1_vals1, q1_vals2 = [], []
        q3_vals1, q3_vals2 = [], []

        for n in vertex_counts:
            scalings1 = []
            scalings2 = []

            t1, t2 = 0, 0
            for _ in range(1):
                while True:
                    try:
                        start_time = time.time()
                        g1, _ = girg.sample_girg(n, alpha, 2.8, 2, 1, 3)
                        t1 = time.time() - start_time
                        print(idx)
                        idx += 1
                    except ValueError:
                        print("wtf")
                        continue
                    break

                while True:
                    try:
                        start_time = time.time()
                        g2, _ = girg.sample_girg(n, 8, beta, 2, 1, 3)
                        t2 = time.time() - start_time
                        print(idx)
                        idx += 1
                    except ValueError:
                        continue
                    break

                scalings1.append(t1)
                scalings2.append(t2)

            median = np.median(scalings1)
            # q1 = np.percentile(scalings1, 25)
            # q3 = np.percentile(scalings1, 75)
            medians1.append(median)
            # q1_vals1.append(q1)
            # q3_vals1.append(q3)

            median = np.median(scalings2)
            # q1 = np.percentile(scalings2, 25)
            # q3 = np.percentile(scalings2, 75)
            medians2.append(median)
            # q1_vals2.append(q1)
            # q3_vals2.append(q3)

        plots1[(alpha, colour)] = [vertex_counts, medians1]#, q1_vals1, q3_vals1]
        plots2[(beta, colour)] = [vertex_counts, medians2]#, q1_vals2, q3_vals2]


    plt.figure(figsize=(10, 6))
    for (alpha, colour) in plots1.keys():
        #ax.errorbar(plots1[(alpha, colour)][0], plots1[(alpha, colour)][1], yerr=[np.array(plots1[(alpha, colour)][1]) - np.array(plots1[(alpha, colour)][2]), np.array(plots1[(alpha, colour)][3]) - np.array(plots1[(alpha, colour)][1])], fmt="o-", capsize=5, label=f"alpha={alpha:.1f}", color=colour)
        plt.plot(plots1[(alpha, colour)][0], plots1[(alpha, colour)][1], label=f"alpha={alpha:.1f}", color=colour)

    plt.xlabel("Number of vertices (n)")
    plt.ylabel("Time (s)")
    plt.title('Scaling Experiment - different alphas')
    plt.legend()
    plt.show()

    plt.figure(figsize=(10, 6))
    for (beta, colour) in plots2.keys():
        #ax.errorbar(plots1[(alpha, colour)][0], plots1[(alpha, colour)][1], yerr=[np.array(plots1[(alpha, colour)][1]) - np.array(plots1[(alpha, colour)][2]), np.array(plots1[(alpha, colour)][3]) - np.array(plots1[(alpha, colour)][1])], fmt="o-", capsize=5, label=f"alpha={alpha:.1f}", color=colour)
        plt.plot(plots2[(beta, colour)][0], plots2[(beta, colour)][1], label=f"beta={beta:.1f}", color=colour)

    plt.xlabel("Number of vertices (n)")
    plt.ylabel("Time (s)")
    plt.title('Scaling Experiment - different betas')
    plt.legend()
    plt.show()

plot_scaling()