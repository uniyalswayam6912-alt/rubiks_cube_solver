class CubeState:

    # Corner pieces: 8 cubies, each with position + orientation
    # Position   : which physical location (0-7)
    # Orientation: 0, 1, 2 (which face is on top)
    corners: list       # Length 8: corner positions
    corner_ori: list    # Length 8: orientations (0, 1, 2)

    # Edge pieces: 12 cubies, each with position + orientation
    edges: list         # Length 12: edge positions
    edge_ori: list      # Length 12: orientations (0, 1)

    def __init__(self):
        # Solved state
        self.corners    = list(range(8))
        self.corner_ori = [0] * 8
        self.edges      = list(range(12))
        self.edge_ori   = [0] * 12

    def hash_key(self) -> int:
        """Compact hash for visited-state tracking"""
        h    = 0
        base = 31

        for pos in self.corners:
            h = (h * base + pos) & 0xFFFFFFFFFFFFFFFF
        for ori in self.corner_ori:
            h = (h * base + ori) & 0xFFFFFFFFFFFFFFFF
        for i in range(12):
            h = (h * base + self.edges[i])    & 0xFFFFFFFFFFFFFFFF
            h = (h * base + self.edge_ori[i]) & 0xFFFFFFFFFFFFFFFF

        return h

    def is_solved(self) -> bool:
        """Check if cube is in solved state."""
        return (
            self.corners    == list(range(8)) and
            all(o == 0 for o in self.corner_ori) and
            self.edges      == list(range(12)) and
            all(o == 0 for o in self.edge_ori)
        )

    def clone(self) -> 'CubeState':
        """Deep copy for state exploration."""
        new_state             = CubeState()
        new_state.corners     = self.corners[:]
        new_state.corner_ori  = self.corner_ori[:]
        new_state.edges       = self.edges[:]
        new_state.edge_ori    = self.edge_ori[:]
        return new_state
