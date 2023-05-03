import math

def split(vertex_weights):
    w_min = min(vertex_weights)
    n = len(vertex_weights)
    L = int(math.floor(math.log2(max(vertex_weights) / w_min))) + 1
    V = {i: set() for i in range(1, L + 1)}

    for vertex, weight in enumerate(vertex_weights):
        i = int(math.floor(math.log2(weight / w_min))) + 1
        V[i].add(vertex)

    return V
