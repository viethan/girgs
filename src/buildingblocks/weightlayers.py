import math
import helper

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

def getCellWeightLayers(weightMapping, positionMapping, cell):
	intervals = helper.cell2intervals(cell[1], cell[0])
	points = []

	for k in positionMapping.keys():
		p = positionMapping[k]

		valid = True
		for i, coord in enumerate(p):
			if not (intervals[i][0] <= coord and coord <= intervals[i][1]):
				valid = False
				break

		if valid:
			points.append(k)

	subsetWeightMapping = {}
	for point in points:
		subsetWeightMapping[point] = weightMapping[point]

	return getWeightLayers(subsetWeightMapping)


# weightMapping = {}
# for i in range(1, 100, 20):
# 	weightMapping[i] = i

# weightLayers = getWeightLayers(weightMapping)
# print(weightLayers)

# weightMapping = {1: 1, 2: 2, 3: 63}
# positionMapping = {1: [0.8, 0.8], 2: [0.6, 0.6], 3: [0.5, 0.5]}
# cell = [2, [2, 2]]
# temp = getCellWeightLayers(weightMapping, positionMapping, cell)
# print(temp)

# min weight 0????????? cant be the case
# return L!!!!
