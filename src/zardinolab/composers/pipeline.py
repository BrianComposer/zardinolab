"""High-level composition pipeline."""

from __future__ import annotations

import random
import re
from dataclasses import dataclass
from fractions import Fraction

from zardinolab.core.events import Measure, MusicalEvent, Score, TimeSignature
from zardinolab.generators.pitch import BasePitchGenerator
from zardinolab.generators.rhythm import BaseRhythmGenerator

_TIME_SIGNATURE_RE = re.compile(r"^(\d+)/(\d+)$")


@dataclass
class PipelineConfig:
    measures: list[str]
    minimal_subdivision: str = "1/16"
    silence_probability: float = 0.1
    tie_probability: float = 0.0
    permute_patterns: bool = False
    time_signature_changes: bool = True
    title: str = "Generated Score"
    pitch_offset: int = 60


class CompositionPipeline:
    def __init__(
        self,
        config: PipelineConfig,
        pitch_generator: BasePitchGenerator,
        rhythm_generator: BaseRhythmGenerator,
    ) -> None:
        self.config = config
        self.pitch_generator = pitch_generator
        self.rhythm_generator = rhythm_generator
        self._validate_config()

    def _validate_config(self) -> None:
        if not self.config.measures:
            raise ValueError("At least one measure must be provided.")
        if not 0.0 <= self.config.silence_probability <= 1.0:
            raise ValueError("silence_probability must lie in [0, 1].")
        if not 0.0 <= self.config.tie_probability <= 1.0:
            raise ValueError("tie_probability must lie in [0, 1].")
        if Fraction(self.config.minimal_subdivision).numerator != 1:
            raise ValueError("minimal_subdivision must be of the form '1/n'.")
        denominator = Fraction(self.config.minimal_subdivision).denominator
        if denominator & (denominator - 1) != 0:
            raise ValueError("minimal_subdivision denominator must be a power of two.")
        for value in self.config.measures:
            if _TIME_SIGNATURE_RE.match(value) is None:
                raise ValueError(f"Invalid time signature: {value!r}")

    def compose(self) -> Score:
        measures = [self._compose_measure(TimeSignature.parse(ts)) for ts in self.config.measures]
        score = Score(measures=measures, title=self.config.title)
        score.validate()
        self._apply_ties(score)
        return score

    def _compose_measure(self, time_signature: TimeSignature) -> Measure:
        events: list[MusicalEvent] = []
        accumulated = Fraction(0, 1)
        target = time_signature.duration
        attempts = 0
        while accumulated < target:
            attempts += 1
            if attempts > 500:
                raise RuntimeError(
                    "Unable to fill measure exactly. Check your rhythmic patterns and minimal subdivision."
                )
            pattern = self.rhythm_generator.next_pattern()
            if self.config.permute_patterns:
                random.shuffle(pattern)
            for token in pattern:
                duration = abs(Fraction(token))
                next_accumulated = accumulated + duration
                if next_accumulated > target:
                    break
                is_rest = token.startswith("-") or random.random() < self.config.silence_probability
                if is_rest:
                    event = MusicalEvent(duration=duration, is_rest=True)
                else:
                    pitch = self.config.pitch_offset + self.pitch_generator.next_pitch()
                    event = MusicalEvent(duration=duration, is_rest=False, pitch=pitch)
                events.append(event)
                accumulated = next_accumulated
                if accumulated == target:
                    break
        measure = Measure(time_signature=time_signature, events=events)
        measure.validate()
        return measure

    def _apply_ties(self, score: Score) -> None:
        previous_note_event: MusicalEvent | None = None
        for measure in score.measures:
            for event in measure.events:
                if event.is_rest:
                    previous_note_event = None
                    continue
                if previous_note_event is not None and random.random() < self.config.tie_probability:
                    previous_note_event.tie_start = True
                    event.tie_stop = True
                previous_note_event = event
