import time
from main import RubiksSolverV2
from cube.state import CubeState
from cube.moves import Move, apply_move


def run_test(scramble_moves):
    solver = RubiksSolverV2()
    state = CubeState()

    for m in scramble_moves:
        state = apply_move(state, Move(m))

    start = time.time()
    result = solver.solve(state)
    end = time.time()

    print("\nScramble:", scramble_moves)
    print("Solution:", result)
    print("Time:", round(end - start, 4), "seconds")


def test_performance():
    test_cases = [
        ['R', 'U', 'F'],                      # easy
        ['R', 'U', 'R', 'U', 'R', 'F'],       # medium
        ['U', 'R', 'F', 'L', 'D', 'B'],       # random
        ['R2', 'U2', 'R', 'U', 'R', 'F2'],    # harder
    ]

    for case in test_cases:
        run_test(case)


if __name__ == "__main__":
    test_performance()