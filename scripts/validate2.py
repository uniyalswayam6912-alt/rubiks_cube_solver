import random
import time
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
print("--- 3-move scrambles (5 trials) ---")
for trial in range(5):
    t0 = time.time()
    start_state = scramble(3)
    result = solver.solve(start_state, verbose=True)
    final = start_state.clone()
    for m in result["solution"]:
        final = apply_move(final, m)
    ok = final.is_solved()
    print(f"  trial={trial+1}: {result['move_count']} moves, {time.time()-t0:.2f}s  [{'PASS' if ok else 'FAIL'}]")
    assert ok

print()
print("--- 5-move scrambles (5 trials) ---")
for trial in range(5):
    t0 = time.time()
    start_state = scramble(5)
    result = solver.solve(start_state, verbose=True)
    final = start_state.clone()
    for m in result["solution"]:
        final = apply_move(final, m)
    ok = final.is_solved()
    print(f"  trial={trial+1}: {result['move_count']} moves, {time.time()-t0:.2f}s  [{'PASS' if ok else 'FAIL'}]")
    assert ok

print()
print("--- 10-move scramble (1 trial, verbose) ---")
start_state = scramble(10)
result = solver.solve(start_state, verbose=True)
final = start_state.clone()
for m in result["solution"]:
    final = apply_move(final, m)
ok = final.is_solved()
print(f"  10-move: {result['move_count']} moves, {result['total_time']:.2f}s  [{'PASS' if ok else 'FAIL'}]")
assert ok

print()
print("All tests PASSED.")
