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


def test_partition_torus():
    def check_pairs_are_unique(cell_pairs):
        pair_set = set()
        for pair in cell_pairs:
            if pair in pair_set:
                return False
            pair_set.add(pair)
        return True

    def check_pairs_are_valid(cell_pairs, torus_dimension):
        for pair, level, t in cell_pairs:
            A, B = pair
            if len(A) != torus_dimension or len(B) != torus_dimension:
                return False
        return True

    def check_coverage(cell_pairs, torus_dimension):
        highest_level = max(level for _, level, _ in cell_pairs)
        smallest_cells = get_cells(highest_level, torus_dimension)
        all_point_pairs = set(itertools.product(smallest_cells, repeat=2))

        for point_pair in all_point_pairs:
            count = 0
            for (cell_A, cell_B), level, t in cell_pairs:
                level_diff = highest_level - level
                ancestor_A = tuple(coord // (2 ** level_diff) for coord in point_pair[0])
                ancestor_B = tuple(coord // (2 ** level_diff) for coord in point_pair[1])

                if ancestor_A == cell_A and ancestor_B == cell_B:
                    count += 1
                if count > 1:
                    return False

            if count != 1:
                return False

        return True


    def check_volume(cell_pairs, torus_dimension):
        total_volume = 0

        for (A, B), level, t in cell_pairs:
            cell_volume = (2 ** (-torus_dimension * level)) ** 2
            total_volume += cell_volume

        expected_volume = 1
        return total_volume == expected_volume


    test_cases = [
        (0.5, 2),
        (0.5, 3),
        (0.5, 4),
        (0.1, 2),
        (0.1, 3),
        (0.1, 4),
        (0.01, 2),
        (0.01, 3),
        (0.01, 4),
        (0.001, 2),
        (0.001, 3),
        (0.001, 4),
        (0.0001, 2),
        (0.0001, 3),
        (0.0001, 4),
    ]

    i = 1
    for nu, torus_dimension in test_cases:
        cell_pairs = partition_torus(nu, torus_dimension)
        
        assert check_pairs_are_unique(cell_pairs), \
            f"Test failed for nu={nu}, torus_dimension={torus_dimension}: cell pairs are not unique"
        
        assert check_pairs_are_valid(cell_pairs, torus_dimension), \
            f"Test failed for nu={nu}, torus_dimension={torus_dimension}: cell pairs are not valid"
        
        assert check_coverage(cell_pairs, torus_dimension), \
            f"Test failed for nu={nu}, torus_dimension={torus_dimension}: not all points in the torus are covered"
        
        assert check_volume(cell_pairs, torus_dimension), \
            f"Test failed for nu={nu}, torus_dimension={torus_dimension}: partition volume does not match torus volume"


    print("All tests passed.")

#test_partition_torus()