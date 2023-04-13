from dnu import DNu
import numpy as np

def test_DNu():
    # Test data
    points = np.array([
        [0.1, 0.2],
        [0.4, 0.4],
        [0.6, 0.8],
        [0.9, 0.3],
        [0.95, 0.95]
    ])
    nu = 0.0625

    # Initialise the DNu data structure
    d_nu = DNu(points, nu)

    # Test cell_size
    cell_coords = np.array([3.0, 3.0])
    cell_size = d_nu.cell_size(cell_coords, 2)
    assert cell_size == 1, f"Expected cell_size: 1, got: {cell_size}"

    # Test kth_point_in_cell
    kth_point = d_nu.kth_point_in_cell(cell_coords, 2, 0)
    expected_point = np.array([0.95, 0.95])
    assert np.allclose(kth_point, expected_point), f"Expected point: {expected_point}, got: {kth_point}"

    # Test invalid k for kth_point_in_cell
    invalid_kth_point = d_nu.kth_point_in_cell(cell_coords, 2, 1)
    assert invalid_kth_point is None, f"Expected point: None, got: {invalid_kth_point}"

    # Test cell with multiple points
    cell_coords_multiple = np.array([0.0, 0.0])
    cell_size_multiple = d_nu.cell_size(cell_coords_multiple, 1)
    assert cell_size_multiple == 2, f"Expected cell_size: 2, got: {cell_size_multiple}"

    # Test kth_point_in_cell for cell with multiple points
    kth_point_multiple = d_nu.kth_point_in_cell(cell_coords_multiple, 1, 1)
    expected_point_multiple = np.array([0.4, 0.4])
    assert np.allclose(kth_point_multiple, expected_point_multiple), f"Expected point: {expected_point_multiple}, got: {kth_point_multiple}"

if __name__ == "__main__":
    test_DNu()
    print("All tests passed!")

