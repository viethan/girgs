import math
import buildingblocks.helper as helper

class CellPointsIntersection:
	def __init__(self, v, P, d):
		self.d = d
		self.l, self.mu = helper.roundUpCellVol(v, d)
		self.cells = helper.getCells(self.l, d) # might want to do this only once?????????????????? and also the whole __intersection

		self.A = []
		for point in P:
			cell = []
			for i in range(d):
				cell.append(math.floor(point[i] / (2 ** (-self.l))))

			self.A.append([self.cells[tuple(cell)], point])	
		self.A.sort()


	def __intersection(self, C):
		old_l = C[0]

		if old_l > self.l: # cell C has to have a volume at least v
			return -1, -1

		# find indices in cells of lowest and highest of C
		lowest, highest = [], []
		for i in range(self.d):
			lowest.append((C[1][i] * 2**(-old_l)) / (2**(-self.l)))
			highest.append(((C[1][i] + 1) * 2**(-old_l)) / (2**(-self.l)) - 1)

		left = self.cells[tuple(lowest)]
		right = self.cells[tuple(highest)]

		# determine first and last point in C intersect P
		s_c, e_c = -1, -1
		for i, point in enumerate(self.A):
			cell_idx, p = point
			if cell_idx >= left:
				s_c = i
				break

		for i, point in reversed(list(enumerate(self.A))):
			cell_idx, p = point
			if cell_idx <= right:
				e_c = i
				break

		return s_c, e_c


	def getCount(self, C):
		s_c, e_c = self.__intersection(C)

		if s_c != -1:
			return e_c - s_c + 1
		else:
			return 0

	
	def getIntersection(self, C):
		s_c, e_c = self.__intersection(C)

		if s_c != -1:
			return [point for i, point in self.A[s_c:e_c+1]]
		else:
			return []


	def getKthPoint(self, C, k):
		s_c, e_c = self.__intersection(C)

		if s_c != -1 and s_c + k <= e_c:
			return self.A[s_c + k][1]
		else:
			return None



# P = [[0, 0], [0.2, 0.56], [0.3, 0.8], [0.6, 0.7], [0.7, 0.7], [0.8, 0.8]]
# ds = CellPointsIntersection(0.0625, P, 2)
# print(ds.getIntersection([2, [2, 2]]))