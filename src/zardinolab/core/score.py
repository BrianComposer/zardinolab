"""Score helpers."""

from __future__ import annotations

from fractions import Fraction

from zardinolab.core.events import Measure, MusicalEvent, Score, TimeSignature


def make_rest(duration: Fraction) -> MusicalEvent:
    return MusicalEvent(duration=duration, is_rest=True)


def make_note(duration: Fraction, pitch: int) -> MusicalEvent:
    return MusicalEvent(duration=duration, is_rest=False, pitch=pitch)


def empty_measure(time_signature: TimeSignature) -> Measure:
    return Measure(time_signature=time_signature, events=[])


def empty_score(title: str = "Untitled") -> Score:
    return Score(measures=[], title=title)
