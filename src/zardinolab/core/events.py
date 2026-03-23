"""Core musical event data structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Optional


@dataclass(frozen=True)
class TimeSignature:
    numerator: int
    denominator: int

    @classmethod
    def parse(cls, value: str) -> "TimeSignature":
        numerator_text, denominator_text = value.split("/")
        numerator = int(numerator_text)
        denominator = int(denominator_text)
        if denominator <= 0:
            raise ValueError("Time signature denominator must be positive.")
        if numerator <= 0:
            raise ValueError("Time signature numerator must be positive.")
        return cls(numerator=numerator, denominator=denominator)

    @property
    def duration(self) -> Fraction:
        return Fraction(self.numerator, self.denominator)

    def __str__(self) -> str:
        return f"{self.numerator}/{self.denominator}"


@dataclass
class MusicalEvent:
    duration: Fraction
    is_rest: bool = False
    pitch: Optional[int] = None
    tie_start: bool = False
    tie_stop: bool = False
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.duration <= 0:
            raise ValueError("Event duration must be strictly positive.")
        if not self.is_rest and self.pitch is None:
            raise ValueError("Pitch events require a MIDI pitch or pitch class value.")
        if self.is_rest and self.pitch is not None:
            raise ValueError("Rest events cannot carry a pitch value.")


@dataclass
class Measure:
    time_signature: TimeSignature
    events: list[MusicalEvent] = field(default_factory=list)

    @property
    def total_duration(self) -> Fraction:
        return sum((event.duration for event in self.events), start=Fraction(0, 1))

    def validate(self) -> None:
        if self.total_duration != self.time_signature.duration:
            raise ValueError(
                f"Measure duration {self.total_duration} does not match time signature "
                f"{self.time_signature.duration} ({self.time_signature})."
            )


@dataclass
class Score:
    measures: list[Measure]
    title: str = "Untitled"

    def validate(self) -> None:
        for measure in self.measures:
            measure.validate()
