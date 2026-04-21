import random
from cube.state import CubeState
from cube.moves import Move, apply_move
from main import RubiksSolverV2


def scramble(n):
    s = CubeState()
    moves = list(Move)
    for _ in range(n):
        s = apply_move(s, random.choice(moves))
    return s


solver = RubiksSolverV2()

print()
print("--- Small scrambles (3-5 moves) ---")
for depth in [3, 4, 5]:
    for trial in range(5):
        start_state = scramble(depth)
        result = solver.solve(start_state, verbose=False)
        final = start_state.clone()
        for m in result["solution"]:
            final = apply_move(final, m)
        ok = final.is_solved()
        status = "PASS" if ok else "FAIL"
        print(f"  depth={depth} trial={trial+1}: {result['move_count']} moves, {result['total_time']:.2f}s  [{status}]")
        assert ok, "VERIFICATION FAILED"

print()
print("--- Medium scrambles (10-15 moves) ---")
for depth in [10, 12, 15]:
    for trial in range(3):
        start_state = scramble(depth)
        result = solver.solve(start_state, verbose=False)
        final = start_state.clone()
        for m in result["solution"]:
            final = apply_move(final, m)
        ok = final.is_solved()
        status = "PASS" if ok else "FAIL"
        print(f"  depth={depth} trial={trial+1}: {result['move_count']} moves, {result['total_time']:.2f}s  [{status}]")
        assert ok, "VERIFICATION FAILED"

print()
print("All end-to-end tests PASSED.")
