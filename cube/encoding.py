from cube.state import CubeState


def encode_dual_orientation(state: CubeState) -> int:
   
    edge_code = 0
    for i in range(11):
        edge_code = (edge_code << 1) | state.edge_ori[i]

    corner_code = 0
    for i in range(7):
        corner_code = corner_code * 3 + state.corner_ori[i]

    return (corner_code << 11) | edge_code
