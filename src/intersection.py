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
		
		print(cube, i)
		cells[tuple(cell)] = i

	# print(len(ordering))
	return cells


l, d = 2, 2


cells = getCells(l, d)
# print(cells)

# iterate through the points in P

P = [[0.275, 0.768]]
A = []
for point in P:
	cell = []
	for i in range(d):
		cell.append(math.floor(point[i] / (2 ** (-l))))

	A.append([cells[tuple(cell)], point])	

print(A)


# determine first and last point in C intersect P

# have a pointer from P points to indices in the contiguous subsequence

# array A with the pointers has to also be ordered somehow


'''
- fix geometric ordering
- think of geometric ordering as a long rectangle
- C is a subset of that
- so are the Ps
- we can find in O(1) time !! using min max

'''
