from cube.state import CubeState
from cube.moves import Move, apply_move
from solver.pruning import get_valid_moves_v2
from utils.transposition_table import TranspositionTable
from utils.helpers import order_moves


def dfs_v2(
    current: CubeState,
    g: int,
    last_move: Move | None,
    second_last_move: Move | None,
    path: list,
    threshold: int,
    tt: TranspositionTable,
    heuristic_func,
    is_g1: bool = True,
) -> tuple:

    if current.is_solved():
        return path, threshold

    h = heuristic_func(current)
    f = g + h

    if f > threshold:
        return None, f

    if tt.misses % 1000 == 0:
        import time
        if time.time() - getattr(tt, 'start_time', 0) > getattr(tt, 'time_limit', float('inf')):
            raise TimeoutError("IDA* timed out")

    if tt.should_prune(current, g):
        return None, float('inf')

    moves = get_valid_moves_v2(last_move, second_last_move, is_g1=is_g1)
    moves = order_moves(current, moves, heuristic_func)

    min_threshold = float('inf')

    for move in moves:
        next_state            = apply_move(current, move)
        result, new_threshold = dfs_v2(
            next_state, g + 1,
            move, last_move,
            path + [move], threshold,
            tt, heuristic_func, is_g1
        )

        if result is not None:
            return result, new_threshold

        min_threshold = min(min_threshold, new_threshold)

    return None, min_threshold

def ida_star_solve_v2(
    
    state: CubeState,
    heuristic_func,
    max_depth: int = 25,
    is_g1: bool = True,
    time_limit: int = 60,
) -> list:
    
    import time
    start_time = time.time()
    tt        = TranspositionTable(max_size=500_000)
    tt.start_time = start_time
    tt.time_limit = time_limit
    threshold = max(heuristic_func(state), 1)

    print(f"Starting IDA* with h={threshold}")

    for iteration in range(max_depth + 1):
        if time.time() - start_time > time_limit:
            raise TimeoutError("IDA* timed out")
        tt.start_iteration()
        print(f"  Iteration {iteration}: threshold={threshold}")

        result, new_threshold = dfs_v2(
            state, 0,
            None, None,
            [], threshold,
            tt, heuristic_func, is_g1
        )

        if result is not None:
            s = tt.stats()
            print(f"Solution found: {len(result)} moves")
            print(
                f"  TT stats: {s['hits']:,} hits / {s['misses']:,} misses "
                f"({s['hit_rate']:.1%} hit rate)"
            )
            return result

        if new_threshold == float('inf'):
            break

        threshold = new_threshold

    raise ValueError("IDA* failed")
