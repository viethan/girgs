import math
import sys
from pathlib import Path

parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from src import weightlayers

def test_weight_layers():
    def check_layers(V, vertex_weights, w_min):
        for layer, vertices in V.items():
            for vertex in vertices:
                weight = vertex_weights[vertex]
                expected_layer = int(math.floor(math.log2(weight / w_min))) + 1
                if expected_layer != layer:
                    return False
        return True

    test_cases = [
        {
            "vertex_weights": [1, 2, 4, 8, 16],
            "w_min": 1
        },
        {
            "vertex_weights": [2, 4, 8, 16, 32],
            "w_min": 2
        },
        {
            "vertex_weights": [5, 10, 20, 40, 80],
            "w_min": 5
        },
        {
            "vertex_weights": [3, 5, 6, 12, 24],
            "w_min": 3
        },
        {
            "vertex_weights": [7, 14, 28, 56, 112],
            "w_min": 7
        }
    ]

    for case in test_cases:
        vertex_weights = case["vertex_weights"]
        w_min = case["w_min"]
        V = weightlayers.split(vertex_weights)
        assert check_layers(V, vertex_weights, w_min), \
            f"Test failed for vertex_weights={vertex_weights}, w_min={w_min}: layers are incorrect"

    print("All tests passed.")


test_weight_layers()
