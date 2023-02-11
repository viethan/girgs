import math
import helper

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
cells = helper.getCells(l, d)
P = [[0, 0], [0.2, 0.56], [0.3, 0.8], [0.6, 0.7], [0.7, 0.7], [0.8, 0.8]]
A = []
for point in P:
	cell = []
	for i in range(d):
		cell.append(math.floor(point[i] / (2 ** (-l))))

	A.append([cells[tuple(cell)], point])	

A.sort()

print(getCountIntersection([2, [2, 2]], A, cells, l, d)) #[0.5..1] x [0.5..1]
