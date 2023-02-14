import numpy as np

# 0. Parameters

E = []
n = 4
d = 2

weightMapping = {}
w_0 = min(weightMapping.values())
W = sum(weightMapping.values())

# 1. Sample Positions

positionMapping = {}
for i in range(1, n+1):
	positionMapping[i] = np.random.uniform(low=0.0, high=1.0, size=d) 

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
	for layer_j in weightLayers.keys():
		w_i, w_j = (2 ** layer_i) * w_0, (2 ** layer_j) * w_0
		vol = (w_i * w_j) / W
		pv = partition.Partitioning(vol, d)

		for level, pair in pv.P:
			A, B = pair

			if level == pv.l : # type I
				





				

			if type II:
				p_hat = 
				r = geo(p_hat)

				while r <= :

					r += geo(p_hat)


		if layer_i == layer_j: