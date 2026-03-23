from pathlib import Path

from zardinolab.composers import CompositionPipeline, PipelineConfig
from zardinolab.generators import (
    MarkovPitchGenerator,
    RandomPitchGenerator,
    LogisticMapPitchGenerator,
    SerialPitchGenerator,
    CellularAutomatonRhythmGenerator
)
from zardinolab.exporters import MusicXMLExporter


def build_pipeline(rule: int, measures, pitch_generator, title: str, offset: int):
    rhythm_gen = CellularAutomatonRhythmGenerator(
        rule=rule,
        initial_state=[0] * 7 + [1] + [0] * 8,
        rhythmic_unit="1/32"
    )

    config = PipelineConfig(
        measures=measures,
        minimal_subdivision="1/32",
        silence_probability=0.05,
        tie_probability=0.05,
        title=title,
        pitch_offset=offset
    )

    return CompositionPipeline(
        config=config,
        pitch_generator=pitch_generator,
        rhythm_generator=rhythm_gen
    )


def main():
    measures = ["4/4"] * 30
    rules = [30, 60, 90, 120, 82]

    # 🎼 Generadores de pitch heterogéneos
    pitch_generators = [
        MarkovPitchGenerator.from_c_major_profile(initial_state=0),
        RandomPitchGenerator(list(range(-12, 13))),
        LogisticMapPitchGenerator(low=-12, high=12, r=3.7),
        SerialPitchGenerator(pitches=list(range(12))),
        MarkovPitchGenerator.from_c_major_profile(initial_state=5),
    ]

    titles = [
        "Markov (tonal)",
        "Random (chromatic)",
        "Logistic map (chaotic)",
        "Serial (12-tone)",
        "Markov variant"
    ]

    # offsets para separar registros (evita colisiones)
    offsets = [72, 60, 48, 84, 36]

    staves = []

    for i in range(len(rules)):
        pipeline = build_pipeline(
            rule=rules[i],
            measures=measures,
            pitch_generator=pitch_generators[i],
            title=titles[i],
            offset=offsets[i]
        )

        score = pipeline.compose()
        staves.append(score)

    exporter = MusicXMLExporter()
    output_path = Path("multi_staff_heterogeneous.musicxml")

    exporter.export_multiple(staves, output_path)

    print(f"Generated heterogeneous score → {output_path}")


if __name__ == "__main__":
    main()