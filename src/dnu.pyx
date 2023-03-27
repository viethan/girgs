# dnu.pyx
import numpy as np
cimport numpy as np
from libc.math cimport ceil, log2, floor, pow
from libc.stdlib cimport calloc, free
import cython

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef class DNu:
	cdef int *prefix_sums
	cdef np.ndarray A
	cdef int d, l
	cdef double nu

	def __init__(self, np.ndarray[np.float64_t, ndim=2] P, double nu):
		cdef int n_points = P.shape[0]
		cdef np.ndarray[np.float64_t, ndim=1] point
		cdef int i, n_cells, cell_idx
		cdef int *temp_prefix_sums
		cdef double mu
		
		self.nu = nu
		self.d = P.shape[1]
		self.l = <int>floor(-(log2(nu) / self.d))
		mu = pow(2, (-self.l * self.d))

		# Determine geometric ordering of cells and initialize prefix_sums
		n_cells = int(ceil(1 / mu))

		self.prefix_sums = <int*>calloc(n_cells + 1, sizeof(int))
		temp_prefix_sums = <int*>calloc(n_cells + 1, sizeof(int))

		# Compute prefix_sums
		for i in range(n_points):
			point = P[i, :]
			cell_idx = self._point_cell_index(point)
			self.prefix_sums[cell_idx + 1] += 1

		temp_prefix_sums[0] = self.prefix_sums[0]
		for i in range(n_cells):
			self.prefix_sums[i + 1] += self.prefix_sums[i]
			temp_prefix_sums[i + 1] = self.prefix_sums[i+1]

		# Initialize and fill A array
		self.A = np.empty(n_points, dtype=object)
		for i in range(n_points):
			point = P[i, :]
			cell_idx = self._point_cell_index(point)
			k = temp_prefix_sums[cell_idx]
			self.A[k] = point
			temp_prefix_sums[cell_idx] += 1

		free(temp_prefix_sums)

	cdef int _point_cell_index(self, np.ndarray[np.float64_t, ndim=1] coords):
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

		free(cell)
		return index

	cdef int _cell_index(self, np.ndarray[np.float64_t, ndim=1] cell):
		cdef int index = 0
		cdef int i, b

		# Obtain index of the cell
		for b in range(self.l):
			for i in range(self.d-1, -1, -1):
				index |= ((<int>cell[i] >> b) & 1) << (b * self.d + (self.d-i-1))

		return index

	cpdef int cell_size(self, np.ndarray[np.float64_t, ndim=1] coords, int cell_l):
		cdef np.ndarray[np.float64_t, ndim=1] lowest_cell, highest_cell

		if cell_l > self.l:
			return -1

		lowest_cell = (coords * pow(2,(-cell_l))) / pow(2, (-self.l))
		highest_cell = ((coords + 1) * pow(2, (-cell_l))) / pow(2, (-self.l)) - 1

		cdef int lowest_idx = self._cell_index(lowest_cell)
		cdef int highest_idx = self._cell_index(highest_cell)

		return self.prefix_sums[highest_idx + 1] - self.prefix_sums[lowest_idx]

	cpdef np.ndarray[np.float64_t, ndim=1] kth_point_in_cell(self, np.ndarray[np.float64_t, ndim=1] coords, int cell_l, int k):
		cdef np.ndarray[np.float64_t, ndim=1] lowest_cell, highest_cell

		if cell_l > self.l:
			return None

		lowest_cell = (coords * pow(2,(-cell_l))) / pow(2, (-self.l))
		highest_cell = ((coords + 1) * pow(2, (-cell_l))) / pow(2, (-self.l)) - 1

		cdef int lowest_idx = self._cell_index(lowest_cell)
		cdef int highest_idx = self._cell_index(highest_cell)

		if k < 0 or k >= (self.prefix_sums[highest_idx + 1] - self.prefix_sums[lowest_idx]):
			return None

		return self.A[self.prefix_sums[lowest_idx] + k]

	cpdef np.ndarray[np.float64_t, ndim=2] cell(self, np.ndarray[np.float64_t, ndim=1] coords, int cell_l):
		cdef np.ndarray[np.float64_t, ndim=1] lowest_cell, highest_cell

		if cell_l > self.l:
			return None

		lowest_cell = (coords * pow(2,(-cell_l))) / pow(2, (-self.l))
		highest_cell = ((coords + 1) * pow(2, (-cell_l))) / pow(2, (-self.l)) - 1

		cdef int lowest_idx = self._cell_index(lowest_cell)
		cdef int highest_idx = self._cell_index(highest_cell)

		return self.A[self.prefix_sums[lowest_idx]:self.prefix_sums[highest_idx + 1]]
