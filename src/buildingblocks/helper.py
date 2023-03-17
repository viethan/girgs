import math
from decimal import *

def roundUpCellVolume(x, d):
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


def interleave(coords, l, d):
	index = 0

	for b in range(l):
		for i, x in enumerate(reversed(coords)):
			bit = (int(x) >> b) & 1
			shifted_bit = bit << (b * d + (i))
			index |= shifted_bit
	return index


def getCells(l, d):
	ordering = []
	getGeometricOrdering([[0, 1] for _ in range(d)], l, d, ordering)

	cells = {}
	for i, cube in enumerate(ordering):
		cell = intervals2cell(cube, l)
		idx = 2 * (cell[0] % 2) + (cell[1] % 2)
		idxo = 2 * math.floor(cell[0] / 2) + math.floor(cell[1]/ 2)

		print(cell, i)
		cells[tuple(cell)] = i

	#return cells





















def cell2intervals(node, l):
	intervals = []
	for c in node:
		intervals.append([c * (2 ** (-l)), (c+1) * (2 ** (-l))])
	return intervals

def intervals2cell(node, l):
	cell = []
	for interval in node:
		cell.append(interval[0] / (2 ** (-l))) 
	return cell

def getChildren(node, l, d):
	node = cell2intervals(node, l)
	#print("yo")
	children_intervals, children_cells = [], []
	getMiniCubes([], node, 0, children_intervals)
	#print(node)
	for child in children_intervals:
		children_cells.append(intervals2cell(child, l+1))
		#print(child, children_cells[-1])

	#print()
	return children_cells

def getNeighbours(c, l, d, i, comb, neighbours):
	if i == len(c):
		neighbours.append(comb[:])
		return

	comb.append(c[i])
	getNeighbours(c, l, d, i+1, comb, neighbours)
	comb.pop()

	increasing = c[i] + 1 if c[i] + 1 < 2**(l) else 0.0
	comb.append(increasing)
	getNeighbours(c, l, d, i+1, comb, neighbours)
	comb.pop()

	decreasing = c[i] - 1 if c[i] - 1 >= 0.0 else 2**(l) - 1
	comb.append(decreasing)
	getNeighbours(c, l, d, i+1, comb, neighbours)
	comb.pop()

def distTorus(coords1, coords2):
	accum = Decimal('0')

	for i in range(len(coords1)):
		dist = abs(coords2[i] - coords1[i])

		if dist > 0.5:
			dist = Decimal(1 - dist)

		accum = accum + (dist ** 2)

	return accum.sqrt()

# temporary until we find fix
def distTorusCubes(A, B, level):
	print("??????????????????????????????/")
	A = cell2intervals(A, level)
	B = cell2intervals(B, level)

	u, v = [], []

	for interval in A:
		left, right = interval
		u.append(left + (right - left) / 2)

	for interval in B:
		left, right = interval
		v.append(left + (right - left) / 2)

	return distTorus(u, v)
