import time
import pickle
import os
from collections import deque
from math import comb

from cube.state import CubeState
from cube.moves import apply_move
from solver.phase1 import G1_MOVES

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "edge_pdb.pkl")

def save_db(db, path=DB_PATH):
    with open(path, "wb") as f:
        pickle.dump(db, f)


def load_db(path=DB_PATH):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    return None

class EdgePatternDB:
    """
    Pattern database for 6 edges (UD-slice edges).
    """

    TRACKED_EDGES = [0, 1, 4, 5, 8, 9]

    def __init__(self):
        self.table: dict[int, int] = {}
        db = load_db()

        if db is None:
            print("Building Edge Pattern Database (first time)...")
            self._build()
            save_db(self.table)
        else:
            print("Loaded Edge Pattern Database from file")
            self.table = db

    def _encode(self, state: CubeState) -> int:
        """
        Encode position of 6 specific edges.

        Part 1: combination — which 6 of 12 positions hold our edges (924 choices)
        Part 2: permutation — order of those 6 edges (720 choices)
        Total : 924 × 720 = 665,280
        """
        tracked_positions = [
            i for i, edge_id in enumerate(state.edges)
            if edge_id in self.TRACKED_EDGES
        ]

        if len(tracked_positions) != 6:
            return 0

        combination_rank = self._rank_combination(tracked_positions)
        tracked_order    = [state.edges[pos] for pos in tracked_positions]
        permutation_rank = self._rank_permutation(tracked_order, self.TRACKED_EDGES)

        return combination_rank * 720 + permutation_rank

    def _rank_combination(self, positions: list) -> int:
        rank = 0
        for i, pos in enumerate(positions):
            rank += comb(pos, i + 1)
        return rank

    def _rank_permutation(self, perm: list, reference: list) -> int:
       
        indexed    = [reference.index(p) for p in perm]
        rank       = 0
        factorials = [1, 1, 2, 6, 24, 120, 720]

        for i in range(6):
            digit = indexed[i]
            for j in range(i):
                if indexed[j] < indexed[i]:
                    digit -= 1
            rank += digit * factorials[5 - i]

        return rank

    def _build(self):
        print("Building Edge Pattern Database (665,280 states)...")
        start    = time.time()

        solved   = CubeState()
        encoding = self._encode(solved)

        queue    = deque([(solved, 0)])
        self.table[encoding] = 0

        max_depth = 0

        while queue:
            state, depth = queue.popleft()

            if depth > max_depth:
                max_depth = depth
                print(f"  Depth {depth}: {len(self.table)} states")

            for move in G1_MOVES:
                next_state = apply_move(state, move)
                encoding   = self._encode(next_state)

                if encoding not in self.table:
                    self.table[encoding] = depth + 1
                    queue.append((next_state, depth + 1))

        elapsed = time.time() - start
        print(f"Edge PDB built: {len(self.table)} states in {elapsed:.2f}s")
        print(f"Max depth: {max_depth}")

    def lookup(self, state: CubeState) -> int:
        """Return exact distance for these 6 edges."""
        return self.table.get(self._encode(state), 0)
