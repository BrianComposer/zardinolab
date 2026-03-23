from fractions import Fraction

from zardinolab.composers import CompositionPipeline, PipelineConfig
from zardinolab.generators import SerialPitchGenerator, SerialRhythmGenerator


def test_pipeline_fills_measure_exactly() -> None:
    pipeline = CompositionPipeline(
        config=PipelineConfig(measures=["4/4", "3/4"], silence_probability=0.0),
        pitch_generator=SerialPitchGenerator([0, 2, 4]),
        rhythm_generator=SerialRhythmGenerator([["1/4"], ["1/8", "1/8"]]),
    )
    score = pipeline.compose()
    assert len(score.measures) == 2
    assert score.measures[0].total_duration == Fraction(1, 1)
    assert score.measures[1].total_duration == Fraction(3, 4)
