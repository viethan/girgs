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


#			temp.append([x_i * 2 ** (-l), (x_i+1) * 2 ** (-l)])


ordering = []
getGeometricOrdering([[0,1], [0,1]], 2, 2, ordering)

for cell in ordering:
	print(cell)
print(len(ordering))

# iterate through the points in P

'''
l = 1
d = 2
P = [[0.7, 0.2]]

for point in P:
	cell = []
	for i in range(d):
		cell.append(math.floor(point[i] / (2 ** (-l))))

	print(cell)	


# determine first and last point in C intersect P

# have a pointer from P points to indices in the contiguous subsequence

# array A with the pointers has to also be ordered somehow

'''

'''
- fix geometric ordering
- think of geometric ordering as a long rectangle
- C is a subset of that
- so are the Ps
- we can find in O(1) time !! using min max

'''
