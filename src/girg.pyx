import cython
import numpy as np
from scipy.stats import rv_continuous
cimport numpy as np
from libc.math cimport log2, log, exp, floor, pow, abs

from dnu import DNu
import pnu
import weightlayers
import graph_tool.all as gt
from networkx.utils.random_sequence import powerlaw_sequence

cdef long double p_uv_hrg(double x_u, double x_v, double w_u, double w_v, double R, double T_H):    
    cdef long double d, p_H, r_v, phi_v, r_u, phi_u

    r_v = R - 2 * log(w_v)
    phi_v = 2 * 3.141592653589793 * x_v
    r_u = R - 2 * log(w_u)
    phi_u = 2 * 3.141592653589793 * x_u
    d = np.cosh(r_u) * np.cosh(r_v) - np.sinh(r_u) * np.sinh(r_v) * np.cos(phi_u - phi_v)
    d = np.arccosh(d)
    p_H = 1 / (1 + exp((d - R) / (2 * T_H)))
    p_H = np.clip(p_H, 0, 1)
    
    return p_H

@cython.boundscheck(False)
cdef long double dist_torus_points(np.ndarray[np.float64_t, ndim=1] x_u, np.ndarray[np.float64_t, ndim=1] x_v, int d):
    cdef long double maximum, dist
    maximum = 0.0

    for i in range(d):
        dist = min(abs(x_u[i] - x_v[i]), 1 - abs(x_u[i] - x_v[i]))
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
cdef long double bar_p(np.ndarray[np.float64_t, ndim=1] cell_A, np.ndarray[np.float64_t, ndim=1] cell_B, double w_i, double w_j, double W, double alpha, int level, int d, double c):
    cdef long double dist = dist_torus_cells(cell_A, cell_B, level, d)

    return min(1, c * pow(pow((1 / dist), d) * ((w_i * w_j) / W), alpha))

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cpdef sample_graph(np.ndarray[np.float64_t, ndim=1] v_weights, double alpha, int d, double c, int hrg=0, double R=0, double T_H=0.0, np.ndarray v_coords=None):
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
    if hrg == 0:
        v_coords = np.ndarray(shape=(n,d), dtype='float64')
        for i in range(n):
            v_coords[i] = np.random.uniform(low=0.0, high=1.0, size=d)
            coords_to_i[tuple(v_coords[i])] = i
    else:
        for i in range(n):
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

                            if hrg == 0:
                                p_uv_val = p_uv(x_u, x_v, v_weights[u], v_weights[v], W, alpha, d)
                            else:
                                p_uv_val = p_uv_hrg(x_u[0], x_v[0], v_weights[u], v_weights[v], R, T_H)

                            if np.random.binomial(1, p_uv_val):
                                if i != j or (i == j and u < v):
                                    E.add((u, v))

                # Type II
                else: 

                    bar_p_val = bar_p(A, B, w_i, w_j, W, alpha, level, d, c)
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

                        if hrg == 0:
                            p_uv_val = p_uv(x_u, x_v, v_weights[u], v_weights[v], W, alpha, d)
                        else:
                            p_uv_val = p_uv_hrg(x_u[0], x_v[0], v_weights[u], v_weights[v], R, T_H)

                        if np.random.binomial(1, min(1, p_uv_val / bar_p_val)): # ?
                            if i != j or (i == j and u < v):
                                E.add((u, v))

                        r += np.random.geometric(bar_p_val)


    return E, v_coords

def generate_weights(n, exponent, min_weight):
    weights = powerlaw_sequence(n, exponent)
    weights = np.array(weights)

    if min_weight != 1:
        weights = weights - np.min(weights) + min_weight  # Shift weights to satisfy the minimum weight constraint
    return weights

class HyperbolicDistribution(rv_continuous):
    def __init__(self, alpha_H, R):
        super().__init__()
        self.alpha_H = alpha_H
        self.R = R

    def _pdf(self, r):
        return self.alpha_H * np.sinh(self.alpha_H * r) / (np.cosh(self.alpha_H * self.R) - 1)

    def _get_support(self):
        return 0, self.R

def sample_girg(n, alpha, beta, d, c, min_weight):
    v_weights = generate_weights(n, beta, min_weight)
    edges, coords = sample_graph(v_weights, alpha, d, c, hrg=0)

    g = gt.Graph(directed=False)
    g.add_vertex(n)

    for u, v in edges:
        g.add_edge(u, v)

    return g, coords

def sample_hrg(n, alpha_H, C_H, T_H):
    # sampling random polar coordinates

    R = 2 * np.log(n) + C_H
    hyperbolic_dist = HyperbolicDistribution(alpha_H, R)
    r_coords = hyperbolic_dist.rvs(size=n)
    phi_coords = np.random.uniform(0, 2 * np.pi, size=n)

    # perform embedding
    d = 1
    beta = 2 * alpha_H + 1
    alpha = 1 / T_H
    v_weights = np.zeros(n, dtype='float64')
    v_coords = np.ndarray(shape=(n,d), dtype='float64')
    for i in range(n):
        v_weights[i] = np.exp((R - r_coords[i]) / 2)
        v_coords[i] = np.array([phi_coords[i] / (2 * np.pi)])

    # use girg sampler
    edges, coords = sample_graph(v_weights, alpha, d, 1, hrg=1, R=R, T_H=T_H, v_coords=v_coords)
    g = gt.Graph(directed=False)
    g.add_vertex(n)

    for u, v in edges:
        g.add_edge(u, v)

    return g, coords