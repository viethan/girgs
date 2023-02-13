import math

def getWeightLayers(weightMapping):
	weightLayers = {}

	w_0 = min(weightMapping.values())
	for i in weightMapping.keys():
		v = weightMapping[i]
		layer_i = math.floor(math.log2(v / w_0)) + 1

		if layer_i not in weightLayers:
			weightLayers[layer_i] = []
		weightLayers[layer_i].append(i)

	return weightLayers

weightMapping = {}
for i in range(1, 100):
	weightMapping[i] = i

weightLayers = getWeightLayers(weightMapping)
print(weightLayers)


# min weight 0?????????