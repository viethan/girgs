import sys
from pathlib import Path

parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from src import pnu
import itertools

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
        smallest_cells = pnu.get_cells(highest_level, torus_dimension)
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
        (0.1, 2),
        (0.1, 3),
        (0.01, 2),
        (0.01, 3),
    ]

    i = 1
    for nu, torus_dimension in test_cases:
        cell_pairs = pnu.partition_torus(nu, torus_dimension)
        
        assert check_pairs_are_unique(cell_pairs), \
            f"Test failed for nu={nu}, torus_dimension={torus_dimension}: cell pairs are not unique"
        
        assert check_pairs_are_valid(cell_pairs, torus_dimension), \
            f"Test failed for nu={nu}, torus_dimension={torus_dimension}: cell pairs are not valid"
        
        assert check_coverage(cell_pairs, torus_dimension), \
            f"Test failed for nu={nu}, torus_dimension={torus_dimension}: not all points in the torus are covered"
        
        assert check_volume(cell_pairs, torus_dimension), \
            f"Test failed for nu={nu}, torus_dimension={torus_dimension}: partition volume does not match torus volume"


    print("All tests passed.")

test_partition_torus()