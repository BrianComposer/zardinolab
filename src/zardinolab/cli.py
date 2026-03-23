"""Simple CLI demo entry point."""

from __future__ import annotations

from pathlib import Path

from zardinolab.composers import CompositionPipeline, PipelineConfig
from zardinolab.exporters import MusicXMLExporter
from zardinolab.generators import MarkovPitchGenerator, PatternRhythmGenerator


def main() -> None:
    rhythm = PatternRhythmGenerator(
        rhythmic_patterns=[
            ["1/4", "1/4", "1/4", "1/4"],
            ["1/8", "1/8", "1/4", "1/4", "1/4"],
            ["1/8", "1/8", "1/8", "1/8", "1/4", "1/4"],
        ]
    )
    pitch = MarkovPitchGenerator.from_c_major_profile(initial_state=0)
    pipeline = CompositionPipeline(
        config=PipelineConfig(measures=["4/4"] * 4, title="CLI Demo"),
        pitch_generator=pitch,
        rhythm_generator=rhythm,
    )
    score = pipeline.compose()
    exporter = MusicXMLExporter()
    output = exporter.export(score, Path("cli_demo.musicxml"))
    print(f"Generated MusicXML file: {output}")


if __name__ == "__main__":
    main()
