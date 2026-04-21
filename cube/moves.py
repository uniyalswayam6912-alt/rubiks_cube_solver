from enum import Enum

from cube.state import CubeState


class Move(Enum):
    """18 possible moves"""
    U  = "U"
    U2 = "U2"
    Up = "U'"
    D  = "D"
    D2 = "D2"
    Dp = "D'"
    L  = "L"
    L2 = "L2"
    Lp = "L'"
    R  = "R"
    R2 = "R2"
    Rp = "R'"
    F  = "F"
    F2 = "F2"
    Fp = "F'"
    B  = "B"
    B2 = "B2"
    Bp = "B'"


# Move tables: precomputed transformations.
# For each move, store which cubies go where and how they orient.

CORNER_MOVE_TABLE = {

    Move.U: {
        'permutation': [1, 2, 3, 0, 4, 5, 6, 7],
        'orientation': [0]*8,
    },

    Move.D: {
        'permutation': [0, 1, 2, 3, 5, 6, 7, 4],
        'orientation': [0]*8,
    },

    Move.R: {
        'permutation': [0, 5, 1, 3, 4, 6, 2, 7],
        'orientation': [0, 2, 1, 0, 0, 1, 2, 0],
    },

    Move.L: {
        'permutation': [3, 1, 2, 7, 0, 5, 6, 4],
        'orientation': [1, 0, 0, 2, 2, 0, 0, 1],
    },

    Move.F: {
        'permutation': [0, 1, 6, 2, 4, 5, 7, 3],
        'orientation': [0, 0, 2, 1, 0, 0, 1, 2],
    },

    Move.B: {
        'permutation': [4, 0, 2, 3, 5, 1, 6, 7],
        'orientation': [2, 1, 0, 0, 1, 2, 0, 0],
    },
}

EDGE_MOVE_TABLE = {

    Move.U: {
        'permutation': [1, 2, 3, 0, 4, 5, 6, 7, 8, 9, 10, 11],
        'orientation': [0]*12,
    },

    Move.D: {
        'permutation': [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 8],
        'orientation': [0]*12,
    },

    Move.R: {
        'permutation': [0, 6, 2, 3, 4, 1, 9, 7, 8, 5, 10, 11],
        'orientation': [0]*12,
    },

    Move.L: {
        'permutation': [0, 1, 2, 7, 3, 5, 6, 11, 8, 9, 10, 4],
        'orientation': [0]*12,
    },

    Move.F: {
        'permutation': [0, 1, 6, 3, 4, 5, 10, 2, 8, 9, 7, 11],
        'orientation': [0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0],
    },

    Move.B: {
        # 4-cycle: edges 0 (UB), 4 (BL), 8 (DB), 5 (BR).
        # Flow: 0 -> 4 -> 8 -> 5 -> 0
        'permutation': [5, 1, 2, 3, 0, 8, 6, 7, 4, 9, 10, 11],
        'orientation': [1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0],
    },
}

def apply_move(state: CubeState, move: Move) -> CubeState:

    if move.name.endswith("2"):
        base = Move[move.name[:-1]]
        return apply_move(apply_move(state, base), base)

    if move.name.endswith("p"):  # prime
        base = Move[move.name[:-1]]
        s = state
        for _ in range(3):
            s = apply_move(s, base)
        return s

    # Base moves only from here
    corner_table = CORNER_MOVE_TABLE[move]
    edge_table = EDGE_MOVE_TABLE[move]

    new_state = state.clone()

    # Corners
    perm = corner_table['permutation']
    ori  = corner_table['orientation']

    new_state.corners = [state.corners[perm[i]] for i in range(8)]
    new_state.corner_ori = [
        (state.corner_ori[perm[i]] + ori[i]) % 3
        for i in range(8)
    ]

    # Edges
    perm = edge_table['permutation']
    ori  = edge_table['orientation']

    new_state.edges = [state.edges[perm[i]] for i in range(12)]
    new_state.edge_ori = [
        (state.edge_ori[perm[i]] + ori[i]) % 2
        for i in range(12)
    ]

    return new_state
