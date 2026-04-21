from collections import deque

from cube.state import CubeState
from cube.moves import apply_move
from solver.phase1 import G1_MOVES


class CornerPositionDB:
    """
    Small pattern database for 8 corner positions.
    """

    def __init__(self):
        self.table = {}
        self._build()

    def _build(self):
        """BFS from solved state to populate table."""
        solved  = CubeState()
        queue   = deque([(solved, 0)])
        visited = {self._encode(solved): 0}

        while queue:
            state, dist = queue.popleft()
            for move in G1_MOVES:
                next_state = apply_move(state, move)
                encoding   = self._encode(next_state)
                if encoding not in visited:
                    visited[encoding] = dist + 1
                    queue.append((next_state, dist + 1))

        self.table = visited

    def _encode(self, state: CubeState) -> int:
        """Encode corner permutation only (ignore orientation)."""
        encoding   = 0
        factorials = [1, 1, 2, 6, 24, 120, 720, 5040]

        for i in range(8):
            rank = state.corners[i]
            for j in range(i):
                if state.corners[j] < state.corners[i]:
                    rank -= 1
            encoding += rank * factorials[7 - i]

        return encoding

    def lookup(self, state: CubeState) -> int:
        """Return exact distance to solve corner positions."""
        return self.table.get(self._encode(state), 0)
