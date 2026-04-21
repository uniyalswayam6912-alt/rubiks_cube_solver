import time
from main import RubiksSolverV2
from cube.state import CubeState
from cube.moves import Move, apply_move

def test():
    solver = RubiksSolverV2()
    state = CubeState()
    for m in ['R', 'U', "R'", "U'", 'R', 'F']:
        state = apply_move(state, Move(m))
    start = time.time()
    res = solver.solve(state, verbose=True)
    print("Solved in", time.time() - start, "seconds.")

if __name__ == "__main__":
    test()
