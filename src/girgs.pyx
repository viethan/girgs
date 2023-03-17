# data_structure_optimized.pyx
import numpy as np
cimport numpy as np
from libc.math cimport ceil, log2, floor, pow
from libc.stdlib cimport calloc, free
import cython

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef class DNuOptimized:
	cdef int *prefix_sums
	cdef np.ndarray A
	cdef int d, l
	cdef double nu

	def __init__(self, np.ndarray[np.float64_t, ndim=2] P, double nu):
		cdef int n_points = P.shape[0]
		cdef np.ndarray[np.float64_t, ndim=1] point
		cdef int i, n_cells, cell_idx
		cdef double mu
		
		self.nu = nu
		self.d = P.shape[1]
		self.l = <int>floor(-(log2(nu) / self.d))
		mu = pow(2, (-self.l * self.d))

		print("nu: ", nu)
		print("d: ", self.d)
		print("l: ", self.l)
		print("mu: ", mu)
		print("")

		# Determine geometric ordering of cells and initialize prefix_sums
		n_cells = int(ceil(1 / mu))

		self.prefix_sums = <int*>calloc(n_cells + 1, sizeof(int))

		# Compute prefix_sums
		for i in range(n_points):
			point = P[i, :]
			cell_idx = self._cell_index(point)
			self.prefix_sums[cell_idx + 1] += 1

		for i in range(n_cells):
			self.prefix_sums[i + 1] += self.prefix_sums[i]

		# Initialize and fill A array
		self.A = np.empty(n_points, dtype=object)
		for i in range(n_points):
			point = P[i, :]
			cell_idx = self._cell_index(point)
			k = self.prefix_sums[cell_idx]
			self.A[k] = point
			self.prefix_sums[cell_idx] += 1 

	def _cell_index(self, np.ndarray[np.float64_t, ndim=1] coords):
		cdef int index = 0
		cdef int i, b
		cdef int *cell = <int*>calloc(self.d, sizeof(int))

		# Obtain cell that point belongs to
		for i in range(self.d):
			cell[i] = <int>(coords[i] / pow(2, (-self.l)))

		# Obtain index of the cell
		for b in range(self.l):
			for i in range(self.d-1, -1, -1):
				index |= ((cell[i] >> b) & 1) << (b * self.d + (self.d-i-1))

		print("point", coords)
		print("cell idx it belongs to", index)
		print("")
		return index

	def cell_size(self, np.ndarray[np.float64_t, ndim=1] coords):
		cdef int cell_idx = self._cell_index(coords)
		return self.prefix_sums[cell_idx + 1] - self.prefix_sums[cell_idx]

	def kth_point_in_cell(self, np.ndarray[np.float64_t, ndim=1] coords, int k):
		cdef int cell_idx = self._cell_index(coords)
		cdef int start_idx = self.prefix_sums[cell_idx]
		cdef int end_idx = self.prefix_sums[cell_idx + 1]

		if k < 0 or k >= end_idx - start_idx:
			return None

		return self.prefix_sums[start_idx + k]