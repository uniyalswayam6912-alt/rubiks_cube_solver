from cube.state import CubeState
from cube.moves import Move, apply_move


def order_moves(state: CubeState, moves: list, heuristic_func) -> list:
    """
    Order moves by heuristic improvement (improving moves first).
    Uses the same heuristic as IDA* — no inconsistency possible.
    """
    current_h = heuristic_func(state)
    scored    = []

    for move in moves:
        next_state = apply_move(state, move)
        delta      = heuristic_func(next_state) - current_h
        scored.append((delta, move))

    scored.sort(key=lambda x: x[0])
    return [move for _, move in scored]
