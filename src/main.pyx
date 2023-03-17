from networkx.utils.random_sequence import powerlaw_sequence
from graph_tool.all import *
from decimal import *
import numpy as np
import math

import cython

import buildingblocks.weightlayers as weightlayers
import buildingblocks.partition as partition
import buildingblocks.geo as geo
#import buildingblocks.intersectionn as intersection
import intersection
import buildingblocks.helper as helper

@cython.boundscheck(False) # compiler directive
@cython.wraparound(False) # compiler directive
def girg():
	N = 1000
	alpha = 2.5 # 1.5 to 2.5 
	beta = 2.5
	d = 2
	c = 2

	g = Graph(directed=False)
	v_weight = g.new_vertex_property("python::object")
	v_coords = g.new_vertex_property("python::object")

	g.add_vertex(N)
	W, w_0 = 0, float('inf')

	# For each vertex, obtain weight and coords
	for i, weight in enumerate(powerlaw_sequence(N, beta)):
		v = g.vertex(i)
		v_weight[v] = Decimal(weight)

		pos = list(np.random.uniform(low=0.0, high=1.0, size=d))
		pos = [Decimal(val) for val in pos] 
		v_coords[v] = pos

		W = W + v_weight[v] 			# sum of all weights
		w_0 = min(w_0, v_weight[v]) 	# minimum weight

	# Determine weight layers V_i
	L, weightLayers = weightlayers.getWeightLayers(g, v_weight)

	# Build cell-points intersection data structures
	dv = {}

	for layer in range(1, L+1):
		if layer not in weightLayers.keys(): # might be the case we don't have any vertices in a weight layer
			continue

		w_i = Decimal((2 ** layer) * w_0)
		vol = Decimal((w_i * w_0) / W)
		dv[layer] = tuple(intersection.buildIntersection(vol, weightLayers[layer], v_coords, d))


	# Sample edges
	for i in range(1, L+1):
		if i not in weightLayers.keys():
			continue

		for j in range(i, L+1):
			if j not in weightLayers.keys():
				continue
		
			# Construct Partitioning
			w_i, w_j = Decimal((2 ** i) * w_0), Decimal((2 ** j) * w_0)
			vol = Decimal((w_i * w_j) / W)
			pv = partition.Partitioning(vol, d)
		
			# For all (A, B) pairs in the Partitioning
			for level, pair in pv.P:

				A, B = pair
				V_iA = intersection.getIntersection([level, A], dv[i][0], dv[i][1], dv[i][2]) #    .getIntersection([level, A])
				V_jB = intersection.getIntersection([level, B], dv[j][0], dv[j][1], dv[j][2]) #dv[j].getIntersection([level, B])

				if level == pv.l: # If type I

					# Iterate through all vertex pairs
					for u in V_iA:
						for v in V_jB:

							if int(u) == int(v):
								continue

							# Use trivial sampling algorithm
							p_uv = min((1 / (helper.distTorus(v_coords[u], v_coords[v]) ** Decimal(alpha * d))) * (((v_weight[u] * v_weight[v]) / W) ** Decimal(alpha)), 1) 
							#print(p_uv)
							if np.random.binomial(1, p_uv): # with probability p_uv add edge
								if i != j or (i == j and int(u) < int(v)): # if same layer, idx u must be less than idx v
									g.add_edge(u, v)

				else: # If type II
					# print("1 ", helper.distTorusCubes(A, B, level))
					# print("2 ", (helper.distTorusCubes(A, B, level) ** (alpha * d) + 2.22e-308))
					# print("3 ", (1 / (helper.distTorusCubes(A, B, level) ** (alpha * d) + 2.22e-308)))
					# print("4 ", w_i, w_j, W, (((w_i * w_j) / W) ** (alpha)))
					# phat = min(c * (1 / (helper.distTorusCubes(A, B, level) ** (alpha * d) + 2.22e-308)) * (((w_i * w_j) / W) ** (alpha)), 1) # ??
					phat = 1
					r = geo.geo(phat) # always 1??????

					while r <= len(V_iA) * len(V_jB):
						u = V_iA[math.floor(r / len(V_jB)) - 1] #   dv[i].getKthPoint([level, A], math.floor(r / len(V_jB)) - 1) 
						v = V_jB[r % len(V_jB) - 1]  #dv[j].getKthPoint([level, B], r % len(V_jB) - 1) # 0-index??????
						r += geo.geo(phat)

						if int(u) == int(v):
							continue

						p_uv = min((1 / (helper.distTorus(v_coords[u], v_coords[v]) ** Decimal(alpha * d))) * (((v_weight[u] * v_weight[v]) / W) ** Decimal(alpha)), 1)
						#print(p_uv / phat)
						if np.random.binomial(1, p_uv / phat):
							if i != j or (i == j and int(u) < int(v)): # if same layer, idx u must be less than idx v
								g.add_edge(u, v)


	v_temp = g.new_vertex_property("vector<long double>") 

	for v in g.vertices():
		poso = v_coords[v]
		pos = [float(val) for val in poso]
		v_temp[v] = pos


	graph_draw(g, pos=v_temp, output="temp.pdf")
