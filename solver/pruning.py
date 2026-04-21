from cube.moves import Move
from solver.phase1 import G1_MOVES


def get_valid_moves_v2(
    last_move: Move | None,
    second_last_move: Move | None,
    is_g1: bool,
) -> list:
    
    available = G1_MOVES if is_g1 else list(Move)

    if last_move is None:
        return available

    last_face = last_move.name[0]
    opposite  = {'U': 'D', 'D': 'U', 'L': 'R', 'R': 'L', 'F': 'B', 'B': 'F'}
    same_axis = {
        'U': ['U', 'D'], 'D': ['U', 'D'],
        'L': ['L', 'R'], 'R': ['L', 'R'],
        'F': ['F', 'B'], 'B': ['F', 'B'],
    }

    pruned = []
    for move in available:
        face = move.name[0]

        if face == last_face:
            continue

        if face == opposite.get(last_face) and last_face > face:
            continue

        if second_last_move is not None:
            second_last_face = second_last_move.name[0]
            if face == second_last_face and face in same_axis.get(last_face, []):
                continue

        pruned.append(move)

    return pruned
