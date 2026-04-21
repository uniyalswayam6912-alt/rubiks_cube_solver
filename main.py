import random
import time

from cube.state import CubeState
from cube.moves import Move, apply_move
from solver.phase1 import phase1_dual_orientation, is_in_enhanced_g1
from solver.ida_star import ida_star_solve_v2
from heuristics.heuristic_engine import HeuristicEngine
from utils.transposition_table import TranspositionTable


class RubiksSolverV2:

    def __init__(self):
        self.heuristic = HeuristicEngine()

        self.solve_stats = {
            'phase1_moves': [],
            'phase2_moves': [],
            'total_moves':  [],
            'phase1_time':  [],
            'phase2_time':  [],
        }

    def solve(self, scrambled: CubeState, verbose: bool = True) -> dict:
        
        if verbose:
            print("\nRubik's Cube Solver")
            print("-" * 30)

        # FAST PATH: Try optimal single-phase solve for short scrambles (<= 6 moves)
        try:
            short_moves = ida_star_solve_v2(
                scrambled,
                self.heuristic.combined,
                max_depth=6,
                is_g1=False,
                time_limit=2
            )
            if short_moves is not None:
                if verbose:
                    print(f"Optimal fast-path solution found: {len(short_moves)} moves")
                return {
                    'phase1_moves': [],
                    'phase2_moves': short_moves,
                    'solution': short_moves,
                    'move_count': len(short_moves),
                    'phase1_time': 0,
                    'phase2_time': 0,
                    'total_time': 0,
                }
        except (ValueError, TimeoutError):
            pass # fallback to two-phase if depth > 6 is required (e.g. from tests)

        # Phase 1
        phase1_start = time.time()
        phase1_moves = phase1_dual_orientation(scrambled)
        phase1_time  = time.time() - phase1_start

        g1_state = scrambled.clone()
        for move in phase1_moves:
            g1_state = apply_move(g1_state, move)

        assert is_in_enhanced_g1(g1_state), "Phase 1 verification failed"

        if verbose:
            print(f"Phase 1: {len(phase1_moves)} moves ({phase1_time:.2f}s)")

        # Phase 2
        h_val = self.heuristic.combined(g1_state)
        phase2_start = time.time()
        try:
            phase2_moves = ida_star_solve_v2(
            g1_state,
            self.heuristic.combined,
            max_depth=25,
            )
        except TimeoutError:
            if verbose:
                print("\nSearch timed out. Try smaller scramble.")
            return {
                'solution': [],
                'move_count': 0,
                'total_time': 0,
            }
        phase2_time = time.time() - phase2_start

        if verbose:
            print(f"Phase 2: {len(phase2_moves)} moves ({phase2_time:.2f}s)")

        # Verify
        final = g1_state.clone()
        for move in phase2_moves:
            final = apply_move(final, move)
        assert final.is_solved(), "Solution verification failed!"

        solution = phase1_moves + phase2_moves
        result   = {
            'phase1_moves': phase1_moves,
            'phase2_moves': phase2_moves,
            'solution':     solution,
            'move_count':   len(solution),
            'phase1_time':  phase1_time,
            'phase2_time':  phase2_time,
            'total_time':   phase1_time + phase2_time,
        }

        if verbose:
            print("\nSolution:")
            print(' '.join(m.value for m in solution))
            print(f"Moves: {len(solution)}")
            print(f"Time: {result['total_time']:.2f}s")

        return result


def generate_random_scramble(num_moves: int) -> CubeState:
    """Return a CubeState after applying `num_moves` random moves."""
    state     = CubeState()
    all_moves = list(Move)
    for _ in range(num_moves):
        state = apply_move(state, random.choice(all_moves))
    return state


def test_move_engine():
    """ To Verify move correctness."""
    state = CubeState()

    # Test 1: Four quarter-turns return to solved
    for move in [Move.U, Move.R, Move.F]:
        s = state.clone()
        for _ in range(4):
            s = apply_move(s, move)
        assert s.is_solved(), f"{move}×4 should return to solved"

    # Test 2: Move followed by its inverse is identity
    s = apply_move(state, Move.R)
    s = apply_move(s, Move.Rp)
    assert s.is_solved(), "R·R' should be identity"


def test_suite():
    from heuristics.edge_db import EdgePatternDB

    print("Running test suite...")

    # Test 1: Pattern DB correctness
    print("\n1. Testing Edge Pattern DB...")
    edge_db = EdgePatternDB()
    solved  = CubeState()
    assert edge_db.lookup(solved) == 0, "Solved state should have h=0"

    # Test 2: Dual-orientation Phase 1
    print("\n2. Testing dual orientation Phase 1...")
    scrambled = generate_random_scramble(20)
    phase1    = phase1_dual_orientation(scrambled)

    result = scrambled.clone()
    for move in phase1:
        result = apply_move(result, move)
    assert is_in_enhanced_g1(result), "Phase 1 failed"

    # Test 3: Heuristic — h(solved) must equal 0
    print("\n3. Testing heuristic admissibility...")
    heuristic = HeuristicEngine()
    assert heuristic.combined(solved) == 0, "h(solved) must be 0"

    # Test 4: Transposition table
    print("\n4. Testing transposition table...")
    tt = TranspositionTable()
    tt.start_iteration()

    state = generate_random_scramble(10)
    assert not tt.should_prune(state, 5), "First visit shouldn't prune"
    assert tt.should_prune(state, 6),     "Deeper visit should prune"

    # Test 5: Full solve
    print("\n5. Testing full solve (10 scrambles)...")
    solver = RubiksSolverV2()

    for i in range(10):
        scrambled = generate_random_scramble(25)
        result    = solver.solve(scrambled, verbose=False)

        final = scrambled.clone()
        for move in result['solution']:
            final = apply_move(final, move)

        assert final.is_solved(), f"Solve {i} failed verification"
        print(
            f"  Scramble {i+1}: {result['move_count']} moves, "
            f"{result['total_time']:.2f}s"
        )

    print("\nAll tests passed!")


def benchmark():
    solver  = RubiksSolverV2()
    results = []

    print("\nBenchmarking on 50 scrambles...")

    for i in range(50):
        scramble = generate_random_scramble(25)
        result   = solver.solve(scramble, verbose=False)
        results.append(result)

        if (i + 1) % 10 == 0:
            avg_moves = sum(r['move_count'] for r in results) / len(results)
            avg_time  = sum(r['total_time'] for r in results) / len(results)
            print(f"  {i+1}/50: avg {avg_moves:.1f} moves, {avg_time:.2f}s")

    move_counts = [r['move_count'] for r in results]
    times       = [r['total_time'] for r in results]

    print("\n" + "=" * 60)
    print("BENCHMARK RESULTS")
    print("=" * 60)
    print(
        f"Moves: {min(move_counts)}-{max(move_counts)}, "
        f"avg {sum(move_counts)/len(move_counts):.1f}"
    )
    print(
        f"Time : {min(times):.2f}s-{max(times):.2f}s, "
        f"avg {sum(times)/len(times):.2f}s"
    )

def test_solver_simple():
    solver = RubiksSolverV2()

    state = CubeState()

    state = apply_move(state, Move.R)
    state = apply_move(state, Move.U)
    state = apply_move(state, Move.F)

    solution = solver.solve(state)

    s = state.clone()
    for move in solution['solution']:
        s = apply_move(s, move)

    assert s.is_solved(), "Solver failed!"

    print("test_solver_simple passed")

def generate_random_move_list(length=10):
    import random
    return [random.choice(list(Move)) for _ in range(length)]


def test_multiple_scrambles():
    solver = RubiksSolverV2()

    for i in range(10):
        state = CubeState()

        scramble = generate_random_move_list(6)
        print("\nScramble:", ' '.join(m.value for m in scramble))
        for move in scramble:
            state = apply_move(state, move)

        result = solver.solve(state, verbose=False)
        solution = result['solution']

        s = state
        for move in solution:
            s = apply_move(s, move)

        assert s.is_solved(), f"Failed on scramble {i}"
    print("multiple scramble test passed")

def run_interactive():
    solver = RubiksSolverV2()

    print("\nEnter moves separated by space (e.g. R U F):")
    user_input = input("Scramble: ").strip()
    moves = []
    for token in user_input.split():
        try:
            moves.append(Move(token))
        except ValueError:
            print(f"Invalid move: {token}")
            return

    state = CubeState()
    for move in moves:
        state = apply_move(state, move)

    result = solver.solve(state)
    solution = result['solution']

    print("\nSolution:")
    print(' '.join(m.value for m in solution))
    print(f"Moves: {len(solution)}")

if __name__ == "__main__":
    test_move_engine()
    test_solver_simple()
    test_multiple_scrambles()

    print("\n--- Interactive Mode ---")
    run_interactive()
    
