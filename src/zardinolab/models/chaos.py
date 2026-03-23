"""Chaotic systems used by generative components."""

from __future__ import annotations


class LogisticMap:
    """Simple logistic map x[n+1] = r * x[n] * (1 - x[n])."""

    def __init__(self, r: float, x0: float) -> None:
        if not 0.0 < x0 < 1.0:
            raise ValueError("x0 must lie strictly between 0 and 1.")
        self.r = r
        self.x = x0

    def step(self) -> float:
        self.x = self.r * self.x * (1.0 - self.x)
        return self.x
