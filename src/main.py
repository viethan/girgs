from networkx.utils.random_sequence import powerlaw_sequence
from graph_tool.all import *
import numpy as np
import math

import buildingblocks.weightlayers as weightlayers
import buildingblocks.partition as partition
import buildingblocks.geo as geo
import buildingblocks.intersection as intersection
import buildingblocks.helper as helper


def dist(a, b):
	return np.random.uniform(low=np.nextafter(0.1, 1.0), high=1.0) 

N = 100
alpha = 100
beta = 2.5
d = 2
c = 2

g = Graph(directed=False)
v_weight = g.new_vertex_property("float")
v_coords = g.new_vertex_property("vector<double>")

g.add_vertex(N)
W, w_0 = 0, float('inf')

# For each vertex, obtain weight and coords
for i, weight in enumerate(powerlaw_sequence(N, beta)):
	v = g.vertex(i)
	v_weight[v] = weight

	pos = list(np.random.uniform(low=0.0, high=1.0, size=d)) 
	v_coords[v] = pos

	W = W + weight 			# sum of all weights
	w_0 = min(w_0, weight) 	# minimum weight

# Determine weight layers V_i
L, weightLayers = weightlayers.getWeightLayers(g, v_weight)

# Build cell-points intersection data structures
dv = {}

for layer in range(1, L+1):
	if layer not in weightLayers.keys(): # might be the case we don't have any vertices in a weight layer
		continue

	w_i = (2 ** layer) * w_0
	vol = (w_i * w_0) / W
	dv[layer] = intersection.CellPointsIntersection(vol, weightLayers[layer], v_coords, d)

# Sample edges
for i in range(1, L+1):
	if i not in weightLayers.keys():
		continue

	for j in range(i, L+1):
		if j not in weightLayers.keys():
			continue
		
		# Construct Partitioning
		w_i, w_j = (2 ** i) * w_0, (2 ** j) * w_0
		vol = (w_i * w_j) / W
		pv = partition.Partitioning(vol, d)
		
		# For all (A, B) pairs in the Partitioning
		for level, pair in pv.P:

			A, B = pair
			V_iA = dv[i].getIntersection([level, A])
			V_jB = dv[j].getIntersection([level, B])

			if level == pv.l: # If type I

				# Iterate through all vertex pairs
				for u in V_iA:
					for v in V_jB:

						# Use trivial sampling algorithm
						p_uv = min((1 / (dist(v_coords[u], v_coords[v]) ** (alpha * d))) * (((v_weight[u] * v_weight[v]) / W) ** (alpha)), 1) 
						print(p_uv)
						if np.random.binomial(1, p_uv): # with probability p_uv add edge
							if i != j or (i == j and int(u) < int(v)): # if same layer, idx u must be less than idx v
								g.add_edge(u, v)


			else: # If type II
				w_i, w_j = 3, 4
				#phat = min(c * (1 / (dist(A,B) ** (alpha * d))) * (((w_i * w_j) / W) ** (alpha)), 1) # ??
				phat = 0.9
				r = geo.geo(phat)

				while r <= len(V_iA) * len(V_jB):
					u = dv[i].getKthPoint([level, A], math.floor(r / len(V_jB)) - 1) 
					v = dv[j].getKthPoint([level, B], r % len(V_jB) - 1) # 0-index??????

					p_uv = min((1 / (dist(v_coords[u], v_coords[v]) ** (alpha * d))) * (((v_weight[u] * v_weight[v]) / W) ** (alpha)), 1)
					print(p_uv / phat)
					if np.random.binomial(1, p_uv / phat):
						if i != j or (i == j and int(u) < int(v)): # if same layer, idx u must be less than idx v
							g.add_edge(u, v)

					r += geo.geo(phat)


graph_draw(g, vertex_text=g.vertex_index, output="temp.pdf")