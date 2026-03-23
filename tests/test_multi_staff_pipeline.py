from pathlib import Path

from zardinolab.composers import CompositionPipeline, PipelineConfig
from zardinolab.generators import (
    MarkovPitchGenerator,
    CellularAutomatonRhythmGenerator
)
from zardinolab.exporters import MusicXMLExporter


def build_pipeline(rule: int, measures):
    """
    Construye un pipeline con un generador rítmico distinto (regla CA)
    y un generador de pitch común (Markov en Do mayor).
    """

    pitch_gen = MarkovPitchGenerator.from_c_major_profile(
        initial_state=0
    )

    rhythm_gen = CellularAutomatonRhythmGenerator(
        rule=rule,
        initial_state=[0] * 7 + [1] + [0] * 8,
        rhythmic_unit="1/32"
    )

    config = PipelineConfig(
        measures=measures,
        minimal_subdivision="1/32",
        silence_probability=0.0,
        tie_probability=0.0,
        title=f"CA Rule {rule}",
        pitch_offset=60  # MIDI center (C4)
    )

    return CompositionPipeline(
        config=config,
        pitch_generator=pitch_gen,
        rhythm_generator=rhythm_gen
    )


def main():
    # Configuración global (similar a tu script antiguo)
    measures = ["4/4"] * 30

    # Reglas de autómata celular (como antes)
    rules = [30, 60, 90, 120, 82]

    staves = []

    # Generar múltiples pentagramas
    for rule in rules:
        pipeline = build_pipeline(rule, measures)
        score = pipeline.compose()
        staves.append(score)

    # Exportar todo como un único score multi-staff
    exporter = MusicXMLExporter()

    output_path = Path("multi_staff_output.musicxml")
    exporter.export_multiple(staves, output_path)

    print(f"Score exported to: {output_path}")


if __name__ == "__main__":
    main()