"""MusicXML export through music21."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Iterable

from zardinolab.core.events import Score


class MusicXMLExporter:
    def export(
        self,
        score: Score,
        output_path: str | Path,
        show: bool = False
    ) -> Path:
        """Backward-compatible single score export."""
        return self.export_multiple([score], output_path, show=show)

    def export_multiple(
        self,
        scores: Iterable[Score],
        output_path: str | Path,
        show: bool = False
    ) -> Path:
        try:
            from music21 import meter, note, stream, tie  # type: ignore
        except ImportError as exc:
            raise ImportError(
                "music21 is required for MusicXML export. Install with `pip install zardinolab[musicxml]`."
            ) from exc

        output_path = Path(output_path)

        music21_score = stream.Score()

        for part_index, score in enumerate(scores):
            music21_part = stream.Part()
            previous_ts: str | None = None

            for measure_index, measure in enumerate(score.measures, start=1):
                music21_measure = stream.Measure(number=measure_index)

                ts_text = str(measure.time_signature)
                if previous_ts != ts_text:
                    music21_measure.insert(0, meter.TimeSignature(ts_text))
                    previous_ts = ts_text

                for event in measure.events:
                    quarter_length = float(Fraction(4, 1) * event.duration)

                    if event.is_rest:
                        rest = note.Rest(quarterLength=quarter_length)
                        music21_measure.append(rest)
                        continue

                    current_note = note.Note(
                        event.pitch,
                        quarterLength=quarter_length
                    )

                    if event.tie_start and event.tie_stop:
                        current_note.tie = tie.Tie("continue")
                    elif event.tie_start:
                        current_note.tie = tie.Tie("start")
                    elif event.tie_stop:
                        current_note.tie = tie.Tie("stop")

                    music21_measure.append(current_note)

                music21_part.append(music21_measure)

            # 👇 clave: cada part independiente
            music21_score.insert(part_index, music21_part)

        if show:
            music21_score.show()

        music21_score.write("musicxml", fp=str(output_path))
        return output_path