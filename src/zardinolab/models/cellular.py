"""Elementary cellular automata."""

from __future__ import annotations

import numpy as np


class ElementaryCellularAutomaton:
    def __init__(self, rule: int = 30, initial_state: list[int] | None = None) -> None:
        if not 0 <= rule <= 255:
            raise ValueError("Elementary cellular automaton rules must lie in [0, 255].")
        if initial_state is None:
            initial_state = [0] * 7 + [1] + [0] * 8
        self.rule_bits = list(map(int, np.binary_repr(rule, width=8)))
        self.state = np.array(initial_state, dtype=int)
        self.dimension = len(initial_state)

    def step(self) -> np.ndarray:
        padded = np.pad(self.state, pad_width=1, mode="wrap")
        triplets = np.array([padded[i : i + 3] for i in range(self.dimension)])
        self.state = np.array(
            [self.rule_bits[7 - int("".join(map(str, triplet)), 2)] for triplet in triplets],
            dtype=int,
        )
        return self.state.copy()
