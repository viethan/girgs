import numpy as np
import buildingblocks.weightlayers as weightlayers
import buildingblocks.partition as partition
import buildingblocks.geo as geo
import buildingblocks.intersection as intersection
import buildingblocks.helper as helper

# 0. Parameters

E = []
n = 10
d = 2

weightMapping = {}

for i in range(1, n+1):
	weightMapping[i] = i % 10 + 1

w_0 = min(weightMapping.values())
W = sum(weightMapping.values())

# 1. Sample Positions

positionMapping = {}
for i in range(1, n+1):
	pos = tuple(np.random.uniform(low=0.0, high=1.0, size=d)) 
	positionMapping[i] = pos
	positionMapping[pos] = i # making it bidirectional

# 2. Determine weight layers V_i

weightLayers = weightlayers.getWeightLayers(weightMapping)


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

		w_i, w_j = (2 ** layer_i) * w_0, (2 ** layer_j) * w_0
		vol = (w_i * w_j) / W
		pv = partition.Partitioning(vol, d)

		for level, pair in pv.P:
			A, B = pair

			if level == pv.l: # type I

				for u in [positionMapping[pt] for pt in dv[layer_i].getIntersection([level, A])]:
					for v in [positionMapping[pt] for pt in dv[layer_j].getIntersection([level, B])]:
						p_uv = min(1, (weightMapping[u] * weightMapping[v]) / W)

						if np.random.binomial(1, p_uv):
							E.append([u, v])

		# 	else: # type II
		# 		phat = min(c * (1/(d(A,B)**(alpha*d))) * (((w_i * w_j) / W) ** (alpha)), 1)
		# 		r = geo(phat)

		# 		while r <= :

		# 			p_uv = 
		# 			p_uv / phat
		# 			r += geo(p_hat)


		# if layer_i == layer_j:

print(E)