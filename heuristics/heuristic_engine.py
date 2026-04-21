from cube.state import CubeState
from heuristics.corner_db import CornerPositionDB
from heuristics.edge_db import EdgePatternDB


class HeuristicEngine:

    def __init__(self):
        print("Initializing Heuristic Engine...")
        self.corner_position_db = CornerPositionDB()
        self.edge_pattern_db    = EdgePatternDB()
        print("Heuristic Engine ready")

    def corner_orientation(self, state: CubeState) -> int:
        misoriented = sum(1 for o in state.corner_ori if o != 0)
        return (misoriented + 1) // 2

    def corner_position(self, state: CubeState) -> int:
        """Exact distance for corner positions (PDB lookup)."""
        return self.corner_position_db.lookup(state)

    def edge_pattern(self, state: CubeState) -> int:
        """Exact distance for 6-edge pattern (PDB lookup)."""
        return self.edge_pattern_db.lookup(state)

    def edge_position_simple(self, state: CubeState) -> int:
        misplaced = sum(1 for i, e in enumerate(state.edges) if e != i)
        return (misplaced + 3) // 4

    def combined(self, state: CubeState) -> int:
        
        return max(
            self.corner_orientation(state),
            self.corner_position(state),
            self.edge_pattern(state),
            self.edge_position_simple(state),
        )

    def stats(self, state: CubeState) -> dict:
        return {
            'corner_ori':   self.corner_orientation(state),
            'corner_pos':   self.corner_position(state),
            'edge_pattern': self.edge_pattern(state),
            'edge_simple':  self.edge_position_simple(state),
            'combined':     self.combined(state),
        }
