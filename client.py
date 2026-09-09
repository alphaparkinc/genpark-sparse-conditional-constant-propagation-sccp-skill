class SCCPOptimizer:
    """Sparse Conditional Constant Propagation (SCCP)."""
    TOP = 'TOP'
    BOTTOM = 'BOTTOM'

    def __init__(self, instructions):
        self.instructions = instructions
        self.lat_vals = {}

    def run(self):
        for dest, op, a1, a2 in self.instructions:
            self.lat_vals[dest] = self.TOP

        changed = True
        while changed:
            changed = False
            for dest, op, a1, a2 in self.instructions:
                old_val = self.lat_vals[dest]
                new_val = self._eval_inst(op, a1, a2)
                if new_val != old_val:
                    self.lat_vals[dest] = new_val
                    changed = True

        return {k: v for k, v in self.lat_vals.items() if v not in (self.TOP, self.BOTTOM)}

    def _eval_inst(self, op, a1, a2):
        if op == 'CONST':
            return a1

        v1 = self.lat_vals.get(a1, a1 if isinstance(a1, (int, float)) else self.BOTTOM)
        v2 = self.lat_vals.get(a2, a2 if isinstance(a2, (int, float)) else self.BOTTOM)

        if v1 == self.TOP or v2 == self.TOP:
            return self.TOP
        if v1 == self.BOTTOM or v2 == self.BOTTOM:
            return self.BOTTOM

        if op == '+': return v1 + v2
        elif op == '-': return v1 - v2
        elif op == '*': return v1 * v2
        elif op == '/': return v1 // v2 if v2 != 0 else self.BOTTOM
        return self.BOTTOM
