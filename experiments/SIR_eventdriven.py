import sys
from pathlib import Path

parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from src import girg
import graph_tool.all as gt
from queue import PriorityQueue
import matplotlib.pyplot as plt
import numpy as np

def fast_SIR(G, τ, γ, initial_infecteds, t_max):
    times, S, I, R = [0], [G.num_vertices()], [0], [0]
    Q = PriorityQueue()
    status = G.new_vertex_property("int")
    pred_inf_time = G.new_vertex_property("double")
    rec_time = G.new_vertex_property("double")
    ordering = {0 : 0}

    for u in G.vertices():
        status[u] = 0 # susceptible
        pred_inf_time[u] = float('inf')

    for u in initial_infecteds:
        event = {"node": G.vertex(u), "time": 0, "action": "transmit"}
        pred_inf_time[G.vertex(u)] = 0
        Q.put((0, ordering[0], event))
        ordering[0] += 1

    while not Q.empty():
        time, order, event = Q.get()
        if event["action"] == "transmit":
            if status[event["node"]] == 0: # susceptible
                process_trans_SIR(G, event["node"], time, τ, γ, times, S, I, R, Q, t_max, status, pred_inf_time, rec_time, ordering)
        else:
            process_rec_SIR(event["node"], time, times, S, I, R, status)

    return times, S, I, R

def process_trans_SIR(G, u, t, τ, γ, times, S, I, R, Q, t_max, status, pred_inf_time, rec_time, ordering):
    times.append(t)
    S.append(S[-1] - 1)
    I.append(I[-1] + 1)
    R.append(R[-1])

    status[u] = 1 # infected
    rec_time[u] = t + np.random.exponential(1/γ)

    if rec_time[u] < t_max:
        new_event = {"node": u, "time": rec_time[u], "action": "recover"}

        if rec_time[u] not in ordering:
            ordering[rec_time[u]] = 0
        Q.put((rec_time[u], ordering[rec_time[u]], new_event))
        ordering[rec_time[u]] += 1

    for v in u.out_neighbors():
        find_trans_SIR(Q, t, τ, u, v, t_max, status, pred_inf_time, rec_time, ordering)

def find_trans_SIR(Q, t, τ, source, target, t_max, status, pred_inf_time, rec_time, ordering):
    if status[target] == 0: # susceptible
        inf_time = t + np.random.exponential(1/τ)
        if inf_time < min(rec_time[source], pred_inf_time[target], t_max):
            new_event = {"node": target, "time": inf_time, "action": "transmit"}

            if inf_time not in ordering:
                ordering[inf_time] = 0
            Q.put((inf_time, ordering[inf_time], new_event))
            ordering[inf_time] += 1
            pred_inf_time[target] = inf_time

def process_rec_SIR(u, t, times, S, I, R, status):
    times.append(t)
    S.append(S[-1])
    I.append(I[-1] - 1)
    R.append(R[-1] + 1)

    status[u] = 2 # recovered

def plot_SIR(times, S, I, R):
    plt.figure(figsize=(10, 6))
    plt.plot(times, S, label='Susceptible', color='blue')
    plt.plot(times, I, label='Infected', color='red')
    plt.plot(times, R, label='Recovered', color='green')
    plt.xlabel('Time')
    plt.ylabel('Number of Individuals')
    plt.legend()
    plt.title('SIR Epidemic Simulation')
    plt.grid()
    plt.show()

def plot_infected_proportion(times, I, total_population):
    infected_proportion = [i / total_population for i in I]

    plt.figure(figsize=(10, 6))
    plt.plot(times, infected_proportion, label='Infected Proportion', color='red')
    plt.xlabel('Time')
    plt.ylabel('Proportion of Infected Individuals')
    plt.legend()
    plt.title('Proportion of Infected Individuals Over Time')
    plt.grid()
    plt.show()

n = 10000
alpha = 8
beta = 2.
d = 2
c = 1
min_weigth = 3

g, _ = girg.sample_girg(n, alpha, beta, d, c, min_weigth)

# Set 1% of nodes as initially infected, selected randomly
initial_infection_rate = 0.01
initial_infected_count = int(n * initial_infection_rate)
initial_infecteds = np.random.choice(g.get_vertices(), initial_infected_count, replace=False)

# Set parameters and run the simulation
τ = 0.5
γ = 0.4
t_max = 200

times, S, I, R = fast_SIR(g, τ, γ, initial_infecteds, t_max)

# Plot the results
plot_SIR(times, S, I, R)
plot_infected_proportion(times, I, n)
