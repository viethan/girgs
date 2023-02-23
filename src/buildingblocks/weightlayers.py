import math
from graph_tool.all import *
import buildingblocks.helper as helper

def getWeightLayers(g, v_weight):
	weightLayers = {}

	# find minimum weight
	w_0 = float('inf')

	for v in g.vertices():
		weight = v_weight[v]
		w_0 = min(w_0, weight)

	# for each vertex, determine its respective layer and add it
	for v in g.vertices():
		weight = v_weight[v]
		layer = math.floor(math.log2(weight / w_0)) + 1

		if layer not in weightLayers:
			weightLayers[layer] = []
		weightLayers[layer].append(v)

	return weightLayers

# return L!!!!