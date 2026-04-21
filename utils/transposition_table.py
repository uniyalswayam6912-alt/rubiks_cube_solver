from cube.state import CubeState


class TranspositionTable:
    """
    Cache for IDA* with depth awareness.

    Prune if we've seen a state at equal or lesser depth in the current iteration.
    Structure: {state_hash: (depth, iteration)}
    """

    def __init__(self, max_size: int = 1_000_000):
        self.table: dict       = {}
        self.max_size          = max_size
        self.current_iteration = 0
        self.hits              = 0
        self.misses            = 0

    def start_iteration(self):
        """Called at the start of each IDA* iteration."""
        self.current_iteration += 1
        if len(self.table) > self.max_size:
            print(f"  TT: Clearing {len(self.table)} entries")
            self.table.clear()

    def should_prune(self, state: CubeState, depth: int) -> bool:
        """
        Return True if this branch should be pruned.
        Prune when state was already visited at equal or shallower depth
        in the current iteration.
        """
        state_hash = state.hash_key()

        if state_hash in self.table:
            cached_depth, cached_iter = self.table[state_hash]
            if cached_iter == self.current_iteration and cached_depth <= depth:
                self.hits += 1
                return True

        self.table[state_hash] = (depth, self.current_iteration)
        self.misses += 1
        return False

    def stats(self) -> dict:
        total    = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        return {
            'entries':  len(self.table),
            'hits':     self.hits,
            'misses':   self.misses,
            'hit_rate': hit_rate,
        }
