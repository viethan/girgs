import math

# returns the smallest volume >= to x
# when we have a d-dimensional hypercube
def roundUpCellVol(x, d):
	x = x ** (-1)
	l = math.floor(math.log(x, 2**d))
	return l, 2 ** ((-1) * l * d)


def getMiniCubes(comb, node, i, minicubes):
	if i is len(node):
		minicubes.append(comb[:])
		return

	left, right = node[i]
	mid = left + (right - left) / 2

	comb.append([left, mid])
	getMiniCubes(comb, node, i+1, minicubes)
	comb.pop()

	comb.append([mid, right])
	getMiniCubes(comb, node, i+1, minicubes)
	comb.pop()

def getGeometricOrdering(node, l, d, ans):
	if l == 0:
		ans.append(node[:])
		return

	minicubes = []
	getMiniCubes([], node, 0, minicubes)
	for minicube in minicubes:
		getGeometricOrdering(minicube, l-1, d, ans)

def getCells(l, d):
	ordering = []
	getGeometricOrdering([[0, 1] for _ in range(d)], l, d, ordering)

	cells = {}
	for i, cube in enumerate(ordering):
		# print(cube)
		cell = []
		for interval in cube:
			cell.append(interval[0] / (2 ** (-l))) 
		
		print(cell, i)
		cells[tuple(cell)] = i

	print(len(ordering))
	return cells

def getNeighbours(c, l, d, i, comb, neighbours):
	if i == len(c):
		neighbours.append(comb[:])
		return

	comb.append(c[i])
	getNeighbours(c, l, d, i+1, comb, neighbours)
	comb.pop()

	increasing = c[i] + 1 if c[i] + 1 < 2**(l) else 0
	comb.append(increasing)
	getNeighbours(c, l, d, i+1, comb, neighbours)
	comb.pop()

	decreasing = c[i] - 1 if c[i] - 1 >= 0 else 2**(l) - 1
	comb.append(decreasing)
	getNeighbours(c, l, d, i+1, comb, neighbours)
	comb.pop()
