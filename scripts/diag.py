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
print("--- Diagnostic: single 5-move scramble (verbose) ---")
start_state = scramble(5)
result = solver.solve(start_state, verbose=True)
final = start_state.clone()
for m in result["solution"]:
    final = apply_move(final, m)
print("Solved:", final.is_solved())
