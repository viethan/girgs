import cython
import numpy as np
cimport numpy as np
from libc.math cimport log2, floor, pow, abs

from dnu import DNu
import pnu
import weightlayers

@cython.boundscheck(False)
cdef long double dist_torus_points(np.ndarray[np.float64_t, ndim=1] x_u, np.ndarray[np.float64_t, ndim=1] x_v, int d):
    cdef long double maximum, dist
    maximum = 0.0

    for i in range(d):
        dist = min(abs(x_u[i] - x_v[i]), 1)
        maximum = max(maximum, dist)

    return maximum

@cython.boundscheck(False)
cdef long double dist_torus_cells(np.ndarray[np.float64_t, ndim=1] cell_u, np.ndarray[np.float64_t, ndim=1] cell_v, int l, int d):
    cdef long double maximum, minimum, dist
    cdef double u1, u2, v1, v2, factor
    maximum = 0.0
    factor = pow(2, -l)

    for i in range(d):
        u1 = cell_u[i] * factor
        u2 = (cell_u[i] + 1) * factor

        v1 = cell_v[i] * factor
        v2 = (cell_v[i] + 1) * factor

        minimum = 1.0

        dist = min(abs(u1 - v1), 1 - abs(u1 - v1))
        minimum = min(minimum, dist)

        dist = min(abs(u1 - v2), 1 - abs(u1 - v2))
        minimum = min(minimum, dist)

        dist = min(abs(u2 - v1), 1 - abs(u2 - v1))
        minimum = min(minimum, dist)

        dist = min(abs(u2 - v2), 1 - abs(u2 - v2))
        minimum = min(minimum, dist)

        maximum = max(maximum, minimum)

    return maximum


@cython.cdivision(True)
cdef long double p_uv(np.ndarray[np.float64_t, ndim=1] x_u, np.ndarray[np.float64_t, ndim=1] x_v, double w_u, double w_v, double W, double alpha, int d):
    cdef long double dist = dist_torus_points(x_u, x_v, d)
    
    return min(1, pow(pow((1 / dist), d) * ((w_u * w_v) / W), alpha))

@cython.cdivision(True)
cdef long double bar_p(np.ndarray[np.float64_t, ndim=1] cell_A, np.ndarray[np.float64_t, ndim=1] cell_B, double w_i, double w_j, double W, double alpha, int level, int d):
    cdef long double dist = dist_torus_cells(cell_A, cell_B, level, d)

    return min(1, pow(pow((1 / dist), d) * ((w_i * w_j) / W), alpha))

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cpdef sample_graph(np.ndarray[np.float64_t, ndim=1] v_weights, double alpha, int d, double c):
    cdef int n
    cdef int L, level, highest_level, pair_type
    cdef long double nu, w_0, W, w_i, w_j
    cdef long double bar_p_val , p_uv_val
    cdef int i, j, k, u, v
    cdef long long r, n_A, n_B, r_A, r_B, total_pairs
    cdef np.ndarray x_u, x_v, A, B

    E = set()
    coords_to_i = {}                                                        # !!!!!!!!!!!!
    partition_dic = {}
    n = v_weights.shape[0]

    # For each vertex, sample the positions
    v_coords = np.ndarray(shape=(n,d), dtype='float64')
    for i in range(n):
        v_coords[i] = np.random.uniform(low=0.0, high=1.0, size=d)
        coords_to_i[tuple(v_coords[i])] = i

    # Determine weight layers V_i
    layers = weightlayers.split(v_weights)
    L = max(layers.keys())
    w_0 = min(v_weights)
    W = sum(v_weights)

    # Build cell-points intersection data structures
    dnus = np.ndarray((L+1), dtype='object')
    for i in range(1, L+1):
        if len(layers[i]) == 0:
            continue

        w_i = pow(2, i) * w_0
        nu = min(1, (w_i * w_0) / W)                                        # !!!!!!!!!!!!
        pts = np.array([v_coords[k] for k in layers[i]])
        dnus[i] = DNu(pts, nu)

    # Sample edges
    for i in range(1, L+1):
        if len(layers[i]) == 0:
            continue

        for j in range(i, L+1):
            if len(layers[j]) == 0:
                continue

            w_i = pow(2, i) * w_0
            w_j = pow(2, j) * w_0
            nu = min(1, (w_i * w_j) / W)                                    # !!!!!!!!!!!!
            highest_level = <int>floor(-(log2(nu) / d))

            if highest_level not in partition_dic:
                partition_dic[highest_level] = pnu.partition_torus(nu, d)
            partitioning = partition_dic[highest_level]
            

            for pair, level, pair_type in partitioning:
                A = np.array(pair[0], dtype='float64')
                B = np.array(pair[1], dtype='float64')

                V_i_A = dnus[i].cell(A, level)
                V_j_B = dnus[j].cell(B, level)

                # Type I
                if pair_type == 1: 

                    for x_u in V_i_A:
                        for x_v in V_j_B:
                            u = coords_to_i[tuple(x_u)]
                            v = coords_to_i[tuple(x_v)]

                            if u == v:
                                continue

                            p_uv_val = p_uv(x_u, x_v, v_weights[u], v_weights[v], W, alpha, d)
                            if np.random.binomial(1, p_uv_val):
                                if i != j or (i == j and u < v):
                                    E.add((u, v))

                # Type II
                else: 

                    bar_p_val = bar_p(A, B, w_i, w_j, W, alpha, level, d)
                    r = np.random.geometric(bar_p_val)
                    n_A = V_i_A.shape[0]
                    n_B = V_j_B.shape[0]
                    total_pairs = n_A * n_B 

                    while r > 0 and r <= total_pairs:
                        r_A = <int>floor((r-1) / n_B)
                        r_B = <int>((r-1) % n_B)

                        x_u = V_i_A[r_A]
                        x_v = V_j_B[r_B]
                        u = coords_to_i[tuple(x_u)]
                        v = coords_to_i[tuple(x_v)]
                        p_uv_val = p_uv(x_u, x_v, v_weights[u], v_weights[v], W, alpha, d)

                        if np.random.binomial(1, min(1, p_uv_val / bar_p_val)): # ?
                            if i != j or (i == j and u < v):
                                E.add((u, v))

                        r += np.random.geometric(bar_p_val)


    return E, v_coords
