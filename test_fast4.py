import time
from main import RubiksSolverV2
from cube.state import CubeState
from cube.moves import Move, apply_move
from solver.ida_star import ida_star_solve_v2

def test():
    solver = RubiksSolverV2()
    state = CubeState()
    for m in ['U', 'R', 'F', 'L', 'D', 'B']:
        state = apply_move(state, Move(m))
    
    start = time.time()
    try:
        short_moves = ida_star_solve_v2(
            state,
            lambda state: 0,
            max_depth=6,
            is_g1=False
        )
        print("Moves:", [m.name for m in short_moves])
    except Exception as e:
        print("Error:", e)
    print("Solved in", time.time() - start, "seconds.")

if __name__ == "__main__":
    test()
