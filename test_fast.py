import time
from main import RubiksSolverV2
from cube.state import CubeState
from cube.moves import Move, apply_move

def test():
    print("Initializing solver...")
    solver = RubiksSolverV2()
    print("Solver initialized.")
    state = CubeState()
    for m in ['R', 'U', 'F']:
        state = apply_move(state, Move(m))
    print("State prepared. Solving...")
    start = time.time()
    try:
        res = solver.solve(state, verbose=True)
        print("Solved in", time.time() - start, "seconds.")
        print(res)
    except Exception as e:
        print("Exception caught inside test block:", type(e), e)
if __name__ == "__main__":
    test()
