import time
from collections import deque

from cube.state import CubeState
from cube.moves import Move, apply_move
from cube.encoding import encode_dual_orientation

G1_MOVES = [
    Move.U, Move.U2, Move.Up,
    Move.D, Move.D2, Move.Dp,
    Move.L, Move.L2, Move.Lp,
    Move.R, Move.R2, Move.Rp,
    Move.F2, Move.B2,
]


def is_in_enhanced_g1(state: CubeState) -> bool:
    
    return (
        all(o == 0 for o in state.edge_ori) and
        all(o == 0 for o in state.corner_ori)
    )


def phase1_dual_orientation(state: CubeState) -> list:
    
    if is_in_enhanced_g1(state):
        return []

    print("Phase 1: Orienting edges AND corners...")
    start = time.time()

    queue     = deque([(state, [])])
    visited   = {encode_dual_orientation(state)}
    all_moves = list(Move)

    while queue:
        current, path = queue.popleft()

        if len(visited) % 100_000 == 0:
            print(f"Explored {len(visited):,} states, depth {len(path)}")

        for move in all_moves:
            next_state = apply_move(current, move)

            if is_in_enhanced_g1(next_state):
                elapsed = time.time() - start
                print(f"Phase 1 complete: {len(path)+1} moves in {elapsed:.2f}s")
                return path + [move]

            encoding = encode_dual_orientation(next_state)
            if encoding not in visited:
                visited.add(encoding)
                queue.append((next_state, path + [move]))

    raise ValueError("Phase 1 failed")
