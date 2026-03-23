from pathlib import Path

from zardinolab.composers import CompositionPipeline, PipelineConfig
from zardinolab.exporters import MusicXMLExporter
from zardinolab.generators import CellularAutomatonRhythmGenerator, MarkovPitchGenerator


def main() -> None:
    measures = ["4/4"] * 8

    pitch_generator = MarkovPitchGenerator.from_c_major_profile(initial_state=0)
    rhythm_generator = CellularAutomatonRhythmGenerator(
        rule=30,
        initial_state=[0] * 7 + [1] + [0] * 8,
        rhythmic_unit="1/16",
    )

    pipeline = CompositionPipeline(
        config=PipelineConfig(
            measures=measures,
            minimal_subdivision="1/16",
            silence_probability=0.10,
            tie_probability=0.05,
            title="Example Cellular + Markov Piece",
            pitch_offset=60,
        ),
        pitch_generator=pitch_generator,
        rhythm_generator=rhythm_generator,
    )

    score = pipeline.compose()
    output_path = Path("example_score.musicxml")
    exporter = MusicXMLExporter()
    exporter.export(score, output_path=output_path)
    print(f"Wrote {output_path.resolve()}")


if __name__ == "__main__":
    main()
