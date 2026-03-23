"""Pitch generator implementations."""

from __future__ import annotations

import math
import random
from abc import ABC, abstractmethod

from zardinolab.models.chaos import LogisticMap
from zardinolab.models.markov import MarkovChain


class BasePitchGenerator(ABC):
    @abstractmethod
    def next_pitch(self) -> int:
        raise NotImplementedError


class RandomPitchGenerator(BasePitchGenerator):
    def __init__(self, pitches: list[int], distribution: str = "uniform") -> None:
        if not pitches:
            raise ValueError("Pitch list cannot be empty.")
        if distribution not in {"uniform", "triangular", "gaussian"}:
            raise ValueError("distribution must be 'uniform', 'triangular', or 'gaussian'.")
        self.pitches = pitches
        self.distribution = distribution

    def next_pitch(self) -> int:
        if self.distribution == "uniform":
            index = random.randrange(len(self.pitches))
        elif self.distribution == "triangular":
            index = math.floor(random.triangular(0, len(self.pitches), len(self.pitches) / 2))
            index = max(0, min(index, len(self.pitches) - 1))
        else:
            index = int(random.gauss(len(self.pitches) / 2, 2)) % len(self.pitches)
        return self.pitches[index]


class SerialPitchGenerator(BasePitchGenerator):
    def __init__(self, pitches: list[int]) -> None:
        if not pitches:
            raise ValueError("Pitch list cannot be empty.")
        self.pitches = pitches
        self.index = 0

    def next_pitch(self) -> int:
        pitch = self.pitches[self.index % len(self.pitches)]
        self.index += 1
        return pitch


class ChaosPitchGenerator(BasePitchGenerator):
    def __init__(self, low: int = 48, high: int = 72, r: float = 3.7, x0: float = 0.5) -> None:
        if low >= high:
            raise ValueError("The lower pitch bound must be smaller than the upper bound.")
        self.low = low
        self.high = high
        self.map = LogisticMap(r=r, x0=x0)

    def next_pitch(self) -> int:
        value = self.map.step()
        return self.low + round((self.high - self.low) * value)


class MarkovPitchGenerator(BasePitchGenerator):
    def __init__(self, transition_matrix: dict[int, dict[int, float]], initial_state: int = 0) -> None:
        self.chain = MarkovChain(transition_matrix=transition_matrix, initial_state=initial_state)

    def next_pitch(self) -> int:
        return self.chain.next_state()

    @classmethod
    def from_c_major_profile(cls, initial_state: int = 0) -> "MarkovPitchGenerator":
        matrix = {
            0: {0: 0.10, 2: 0.10, 4: 0.10, 5: 0.15, 7: 0.20, 9: 0.10, 11: 0.15, 1: 0.02, 3: 0.02, 6: 0.02, 8: 0.02, 10: 0.02},
            1: {0: 0.1087, 1: 0.0217, 2: 0.1087, 3: 0.0217, 4: 0.1087, 5: 0.1087, 6: 0.0217, 7: 0.1630, 8: 0.0217, 9: 0.1087, 10: 0.0217, 11: 0.1848},
            2: {0: 0.15, 1: 0.02, 2: 0.10, 3: 0.02, 4: 0.10, 5: 0.15, 6: 0.02, 7: 0.15, 8: 0.02, 9: 0.10, 10: 0.02, 11: 0.15},
            3: {0: 0.1087, 1: 0.0217, 2: 0.1087, 3: 0.0217, 4: 0.1087, 5: 0.1087, 6: 0.0217, 7: 0.1630, 8: 0.0217, 9: 0.1087, 10: 0.0217, 11: 0.1848},
            4: {0: 0.15, 1: 0.02, 2: 0.10, 3: 0.02, 4: 0.10, 5: 0.15, 6: 0.02, 7: 0.15, 8: 0.02, 9: 0.10, 10: 0.02, 11: 0.15},
            5: {0: 0.20, 1: 0.02, 2: 0.10, 3: 0.02, 4: 0.10, 5: 0.10, 6: 0.02, 7: 0.15, 8: 0.02, 9: 0.10, 10: 0.02, 11: 0.15},
            6: {0: 0.1087, 1: 0.0217, 2: 0.1087, 3: 0.0217, 4: 0.1087, 5: 0.1087, 6: 0.0217, 7: 0.1630, 8: 0.0217, 9: 0.1087, 10: 0.0217, 11: 0.1848},
            7: {0: 0.2941, 1: 0.0196, 2: 0.0980, 3: 0.0196, 4: 0.0980, 5: 0.1471, 6: 0.0196, 7: 0.0980, 8: 0.0196, 9: 0.0980, 10: 0.0196, 11: 0.0686},
            8: {0: 0.1087, 1: 0.0217, 2: 0.1087, 3: 0.0217, 4: 0.1087, 5: 0.1087, 6: 0.0217, 7: 0.1630, 8: 0.0217, 9: 0.1087, 10: 0.0217, 11: 0.1848},
            9: {0: 0.15, 1: 0.02, 2: 0.10, 3: 0.02, 4: 0.10, 5: 0.15, 6: 0.02, 7: 0.15, 8: 0.02, 9: 0.10, 10: 0.02, 11: 0.15},
            10: {0: 0.1087, 1: 0.0217, 2: 0.1087, 3: 0.0217, 4: 0.1087, 5: 0.1087, 6: 0.0217, 7: 0.1630, 8: 0.0217, 9: 0.1087, 10: 0.0217, 11: 0.1848},
            11: {0: 0.15, 1: 0.02, 2: 0.10, 3: 0.02, 4: 0.10, 5: 0.15, 6: 0.02, 7: 0.15, 8: 0.02, 9: 0.10, 10: 0.02, 11: 0.15},
        }
        return cls(transition_matrix=matrix, initial_state=initial_state)
