from networkx.utils.random_sequence import powerlaw_sequence
from graph_tool.all import *
import numpy as np



import buildingblocks.weightlayers as weightlayers
import buildingblocks.partition as partition
import buildingblocks.geo as geo
import buildingblocks.intersection as intersection
import buildingblocks.helper as helper


N = 100
alpha = 2.5
d = 2

g = Graph(directed=False)
v_weight = g.new_vertex_property("float")
v_coords = g.new_vertex_property("vector<double>")

g.add_vertex(N)
W, w_0 = 0, float('inf')

# for each vertex, obtain weight and coords
for i, weight in enumerate(powerlaw_sequence(N, alpha)):
	v = g.vertex(i)
	v_weight[v] = weight

	pos = list(np.random.uniform(low=0.0, high=1.0, size=d)) 
	v_coords[v] = pos

	W = W + weight 			# sum of all weights
	w_0 = min(w_0, weight) 	# minimum weight

# Determine weight layers V_i
weightLayers = weightlayers.getWeightLayers(g, v_weight)









'''

# 3. Build cell-points intersection data structures

dv = {}

for layer in weightLayers.keys():
	pts = [positionMapping[point] for point in weightLayers[layer]]
	w_i = (2 ** layer) * w_0
	vol = (w_i * w_0) / W
	dv[layer] = intersection.CellPointsIntersection(vol, pts, d)

# 4. Sample edges between V_i and V_j

for layer_i in weightLayers.keys():
	for layer_j in weightLayers.keys(): #  HIGHER LAYER VALSSSSSSSSS
		if layer_j < layer_i:
			continue

		# 4.1 Construct Partitioning
		w_i, w_j = (2 ** layer_i) * w_0, (2 ** layer_j) * w_0
		vol = (w_i * w_j) / W
		pv = partition.Partitioning(vol, d)
		E_temp = []

		# 4.2 for all (A, B) in P_v(i,j)
		for level, pair in pv.P:
			A, B = pair
			V_iA = dv[layer_i].getIntersection([level, A])
			V_jB = dv[layer_j].getIntersection([level, B])

			if level == pv.l: # of type I

				for u in [positionMapping[pt] for pt in V_iA]: # for all u in V_i A
					for v in [positionMapping[pt] for pt in V_jB]: # for all v in V_j B
						p_uv = min(1, (weightMapping[u] * weightMapping[v]) / W) # fix meeeee!!!!!!!!!!!!!!!!!!!!!!!!!

						if np.random.binomial(1, p_uv): # with probability p_uv add edge
							E_temp.append([u, v])

			else: # of type II
				phat = min(c * ( 1 / (dist(A,B)**(alpha*d)) ) * ( ((w_i * w_j) / W) ** (alpha) ), 1)
				r = geo(phat)


				while r <= len(V_iA) * len(V_jB):

					r1 = floor(len(V_iA) / r)
					r2 = len(V_iA) % r
					u, v = V_iA[r1], V_jB[r2]

					p_uv = 

					if np.random.binomial(1, p_uv / phat):
						E_temp.append([u, v])

					r += geo(p_hat)


		if layer_i == layer_j:
			for u, v in E_temp:
				if u < v:
					E.append([u, v])
		else:
			E.extend(E_temp)

print(E)


'''