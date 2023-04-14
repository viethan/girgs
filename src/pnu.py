import math
import itertools

def get_cells(level, torus_dimension):
    # Determine the number of cells along one dimension at the given level
    num_cells_per_dim = 2 ** level

    # Initialize an empty list to store the cells
    cells = []

    # Generate all cell coordinates in a torus_dimension-dimensional grid
    for index in itertools.product(range(num_cells_per_dim), repeat=torus_dimension):
        cell = tuple(index)
        cells.append(cell)

    return cells

def get_children(cell, dimension):
    children = []
    for offset in itertools.product(range(2), repeat=dimension):
        child = tuple(2 * coord + offset_coord for coord, offset_coord in zip(cell, offset))
        children.append(child)
    return children

def get_neighbors(cell, level, dimension):
    neighbors = []
    for offset in itertools.product(range(-1, 2), repeat=dimension):
        if offset == tuple([0] * dimension):
            continue
        neighbor = tuple((coord + offset_coord) % (2 ** level)
                         for coord, offset_coord in zip(cell, offset))
        neighbors.append(neighbor)
    return neighbors

def partition_torus(nu, torus_dimension):
    highest_level = math.floor(-(math.log2(nu) / torus_dimension))

    if highest_level == 0:
        return {((tuple([0 for _ in range(torus_dimension)]) , tuple([0 for _ in range(torus_dimension)])), 0, 1)}

    cell_pairs = set()

    for level in range(1, highest_level + 1):
        cells = get_cells(level, torus_dimension)
        for A in cells:
            neighbors = get_neighbors(A, level, torus_dimension)

            if level == highest_level:
                # Include the cell itself for type I pairs
                cell_pairs.add(((A, A), level, 1))

            for B in neighbors:
                if level == highest_level:
                    # Type I
                    cell_pairs.add(((A, B), level, 1))
                else:
                    # Type II
                    A_children = get_children(A, torus_dimension)
                    B_children = get_children(B, torus_dimension)

                    A_child_neighbors = {
                        child_A: get_neighbors(child_A, level + 1, torus_dimension)
                        for child_A in A_children
                    }

                    for child_A in A_children:
                        for child_B in B_children:
                            if child_B not in A_child_neighbors[child_A]:
                                cell_pairs.add(((child_A, child_B), level + 1, 2))

    return cell_pairs
