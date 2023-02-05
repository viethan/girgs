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

	# print(len(ordering))
	return cells


def getCountIntersection(C, A, cells, l, d):
	old_l = C[0]

	# find indices in cells of lowest and highest of C
	lowest, highest = [], []
	for i in range(d):
		lowest.append((C[1][i] * 2**(-old_l)) / (2**(-l)))
		highest.append(((C[1][i] + 1) * 2**(-old_l)) / (2**(-l)) - 1)

	print(lowest, highest)
	left = cells[tuple(lowest)]
	right = cells[tuple(highest)]

	# determine first and last point in C intersect P
	s_c, e_c = -1, -1
	for i, point in enumerate(A):
		cell_idx, p = point
		if cell_idx >= left:
			s_c = i
			break

	for i, point in reversed(list(enumerate(A))):
		cell_idx, p = point
		if cell_idx <= right:
			e_c = i
			break

	if s_c != -1:
		return e_c - s_c + 1
	else:
		return 0


l, d = 2, 2
cells = getCells(l, d)
P = [[0, 0], [0.2, 0.56], [0.3, 0.8], [0.6, 0.7], [0.7, 0.7], [0.8, 0.8]]
A = []
for point in P:
	cell = []
	for i in range(d):
		cell.append(math.floor(point[i] / (2 ** (-l))))

	A.append([cells[tuple(cell)], point])	

A.sort()

print(getCountIntersection([1, [1, 1]], A, cells, l, d))

