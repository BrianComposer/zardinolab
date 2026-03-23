"""Rhythm generator implementations."""

from __future__ import annotations

import random
import re
from abc import ABC, abstractmethod
from fractions import Fraction

from zardinolab.models.cellular import ElementaryCellularAutomaton

_PATTERN_RE = re.compile(r"^-?\d+/\d+$")


class BaseRhythmGenerator(ABC):
    @abstractmethod
    def next_pattern(self) -> list[str]:
        raise NotImplementedError


class PatternRhythmGenerator(BaseRhythmGenerator):
    def __init__(self, rhythmic_patterns: list[list[str]], distribution: str = "uniform") -> None:
        self._validate_patterns(rhythmic_patterns)
        if distribution not in {"uniform", "gaussian", "weibull", "triangular"}:
            raise ValueError("Unsupported rhythm distribution.")
        self.rhythmic_patterns = rhythmic_patterns
        self.distribution = distribution

    def _validate_patterns(self, rhythmic_patterns: list[list[str]]) -> None:
        if not rhythmic_patterns:
            raise ValueError("The rhythmic pattern collection cannot be empty.")
        for pattern in rhythmic_patterns:
            if not pattern:
                raise ValueError("Rhythmic patterns cannot be empty.")
            for token in pattern:
                if not _PATTERN_RE.match(token):
                    raise ValueError(f"Invalid rhythmic token: {token!r}")

    def next_pattern(self) -> list[str]:
        patterns = self.rhythmic_patterns
        if self.distribution == "uniform":
            return list(random.choice(patterns))
        if self.distribution == "gaussian":
            index = int(abs(random.gauss(0, len(patterns) / 3)) % len(patterns))
            return list(patterns[index])
        if self.distribution == "weibull":
            index = round(random.weibullvariate(10, len(patterns) / 9)) % len(patterns)
            return list(patterns[index])
        index = round(random.triangular(0, len(patterns) - 1)) % len(patterns)
        return list(patterns[index])


class SerialRhythmGenerator(BaseRhythmGenerator):
    def __init__(self, rhythmic_patterns: list[list[str]]) -> None:
        if not rhythmic_patterns:
            raise ValueError("The rhythmic pattern collection cannot be empty.")
        self.rhythmic_patterns = rhythmic_patterns
        self.index = 0

    def next_pattern(self) -> list[str]:
        pattern = self.rhythmic_patterns[self.index % len(self.rhythmic_patterns)]
        self.index += 1
        return list(pattern)


class CellularAutomatonRhythmGenerator(BaseRhythmGenerator):
    def __init__(
        self,
        rule: int = 30,
        initial_state: list[int] | None = None,
        rhythmic_unit: str = "1/16",
    ) -> None:
        self.automaton = ElementaryCellularAutomaton(rule=rule, initial_state=initial_state)
        if not _PATTERN_RE.match(rhythmic_unit):
            raise ValueError("rhythmic_unit must have the form 'numerator/denominator'.")
        self.rhythmic_unit = rhythmic_unit

    def next_pattern(self) -> list[str]:
        state = self.automaton.state.copy()
        self.automaton.step()
        return [self.rhythmic_unit if cell == 1 else f"-{self.rhythmic_unit}" for cell in state]


def pattern_total(pattern: list[str]) -> Fraction:
    return sum((Fraction(token) for token in pattern), start=Fraction(0, 1))
