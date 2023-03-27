import math


def get_cells(level, dimension):
    num_cells = 2 ** (level * dimension)
    cells = [divmod(i, 2 ** level) for i in range(num_cells)]
    return cells


def distance(cell_a, cell_b, dimension):
    return sum(abs(a - b) for a, b in zip(cell_a, cell_b)) ** (1 / dimension)


def get_neighbors(cell, level, dimension):
    neighbor_offsets = [-1, 0, 1]
    neighbors = []

    for offset in itertools.product(neighbor_offsets, repeat=dimension):
        neighbor = tuple(cell_i + offset_i for cell_i, offset_i in zip(cell, offset))
        if all(0 <= coord < 2 ** level for coord in neighbor) and neighbor != cell:
            neighbors.append(neighbor)

    return neighbors


def partition(nu, dimension):
    mu = math.ceil(nu * 2 ** dimension) / 2 ** dimension
    level = int(math.log2(1 / mu) / dimension)
    partition_set = set()

    for l in range(level + 1):
        cells = get_cells(l, dimension)

        for cell_a in cells:
            neighbors = get_neighbors(cell_a, l, dimension)

            for cell_b in neighbors:
                vol_a = 2 ** (-l * dimension)
                vol_b = 2 ** (-l * dimension)
                dist = distance(cell_a, cell_b, dimension)

                if vol_a >= nu and vol_b >= nu:
                    if vol_a == vol_b == mu and dist == 0:
                        partition_set.add((cell_a, cell_b))
                    elif dist > 0 and distance(get_cells(l - 1, dimension), get_cells(l - 1, dimension), dimension) == 0:
                        children_a = [cell for cell in get_cells(l + 1, dimension) if cell in get_cells(l, dimension)]
                        children_b = [cell for cell in get_cells(l + 1, dimension) if cell in get_cells(l, dimension)]

                        for child_a, child_b in itertools.product(children_a, children_b):
                            partition_set.add((child_a, child_b))

    return partition_set

# Example usage:
dimension = 2
nu = 0.1
partitions = partition(dimension, nu)
for idx, (A, B) in enumerate(sorted(partitions)):
    print(f"Partition {idx + 1}: A = {A}, B = {B}")

