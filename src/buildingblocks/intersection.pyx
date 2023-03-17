import math
import buildingblocks.helper as helper
from decimal import *


'''
v - input volume
P - set of points
d - dimension
v_coords - map point to 

'''
def buildIntersection(v, P, v_coords, d):
	max_level, mu = helper.roundUpCellVolume(v, d)
	cells = helper.getCells(max_level, d)

	cellsWithPoints = {}
	for point in P:
		coords = v_coords[point]
		cell = []

		for i in range(d):
			cell.append(math.floor(coords[i] / Decimal(2 ** (-max_level))))

		if tuple(cell) not in cellsWithPoints:
			cellsWithPoints[tuple(cell)] = []	
		cellsWithPoints[tuple(cell)].append(point)

	A = []
	s_i = {}
	accum = 0
	for cell in cells:

		if tuple(cell) in cellsWithPoints.keys():
			A.extend(cellsWithPoints[tuple(cell)])
			s_i[cell] = [accum, accum + len(cellsWithPoints[tuple(cell)])] # might go out of bounds????

			accum += len(cellsWithPoints[tuple(cell)])
		else:
			s_i[cell] = [accum, accum]

	return s_i, A, max_level



def countIntersection(C, s_i, A, int l):
	cdef int old_l

	old_l = C[0]

	if old_l > l: # cell C has to have a volume at least v
		print("wtffffffffffffffffffff")
		return None

	# find indices in cells of lowest and highest of C
	lowest, highest = [], []
	for i in range(2):
		lowest.append((C[1][i] * 2**(-old_l)) / (2**(-l)))
		highest.append(((C[1][i] + 1) * 2**(-old_l)) / (2**(-l)) - 1)

	return s_i[tuple(highest)][1] - s_i[tuple(lowest)][0]

def getIntersection(C, s_i, A, l):
	cdef float old_l
	old_l = C[0]

	if old_l > l: # cell C has to have a volume at least v
		print("wtffffffffffffffffffff")
		return None

	# find indices in cells of lowest and highest of C
	lowest, highest = [], []
	for i in range(2):
		lowest.append((C[1][i] * 2**(-old_l)) / (2**(-l)))
		highest.append(((C[1][i] + 1) * 2**(-old_l)) / (2**(-l)) - 1)

	return A[s_i[tuple(lowest)][0] : s_i[tuple(highest)][1]] # works even if we are past the arr

def getkthIntersection(C, k, s_i, A, l):
	cdef int old_l
	old_l = C[0]

	if old_l > l: # cell C has to have a volume at least v
		print("wtffffffffffffffffffff")
		return None

	# find indices in cells of lowest and highest of C
	lowest, highest = [], []
	for i in range(2):
		lowest.append((C[1][i] * 2**(-old_l)) / (2**(-l)))
		highest.append(((C[1][i] + 1) * 2**(-old_l)) / (2**(-l)) - 1)

	if k <= (s_i[tuple(highest)][1] - s_i[tuple(lowest)][0]):
			return A[s_i[tuple(lowest)][0] + k - 1]
	else:
		print("wtfffffffffffffffffffff")
		return None
