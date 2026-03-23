# ZardinoLab

ZardinoLab is a modular Python toolkit for **algorithmic** and **computer-assisted composition**. It was designed for composers, researchers, and creative coders who want to combine multiple generative paradigms in a single workflow: **Markov chains**, **chaotic systems**, **cellular automata**, **symbolic grammars**, and rule-based score rendering.

The package refactors an earlier experimental codebase into a reusable, installable, and extensible project suitable for GitHub, PyPI, and research-oriented reuse.

## Features

- Modular pitch generators:
  - random distributions
  - cyclic / serial generators
  - logistic-map chaos
  - Markov chains
- Modular rhythm generators:
  - pattern-based random selection
  - serial pattern traversal
  - elementary cellular automata
- Lightweight symbolic grammar engine with optional and repeated constructs
- Score assembly pipeline with explicit musical event objects
- MusicXML export through `music21`
- Simple CLI demo
- Test suite and professional package layout

## Installation

### Minimal installation

```bash
pip install zardinolab
```

### With MusicXML support

```bash
pip install zardinolab[musicxml]
```

### Development installation

```bash
pip install -e .[all]
```

## Quick start

```python
from zardinolab.composers import CompositionPipeline, PipelineConfig
from zardinolab.exporters import MusicXMLExporter
from zardinolab.generators import MarkovPitchGenerator, CellularAutomatonRhythmGenerator

measures = ["4/4"] * 8

pitch_generator = MarkovPitchGenerator.from_c_major_profile(initial_state=0)
rhythm_generator = CellularAutomatonRhythmGenerator(rule=30, rhythmic_unit="1/16")

pipeline = CompositionPipeline(
    config=PipelineConfig(
        measures=measures,
        minimal_subdivision="1/16",
        silence_probability=0.10,
        tie_probability=0.05,
        time_signature_changes=True,
    ),
    pitch_generator=pitch_generator,
    rhythm_generator=rhythm_generator,
)

score = pipeline.compose()

exporter = MusicXMLExporter()
exporter.export(score, output_path="example_score.musicxml")
```

## Project structure

```text
zardinolab/
├── pyproject.toml
├── README.md
├── LICENSE
├── .gitignore
├── src/
│   └── zardinolab/
│       ├── __init__.py
│       ├── cli.py
│       ├── core/
│       │   ├── events.py
│       │   └── score.py
│       ├── models/
│       │   ├── chaos.py
│       │   ├── markov.py
│       │   ├── cellular.py
│       │   └── grammar.py
│       ├── generators/
│       │   ├── pitch.py
│       │   └── rhythm.py
│       ├── composers/
│       │   └── pipeline.py
│       └── exporters/
│           └── musicxml.py
├── examples/
│   └── basic_pipeline.py
└── tests/
    ├── test_markov.py
    ├── test_pipeline.py
    └── test_rhythm.py
```

## Design principles

ZardinoLab follows a few strong design rules:

1. **Explicit musical data structures** instead of loose nested lists.
2. **Single responsibility** for each module.
3. **Composable generators** for rhythm and pitch.
4. **Separation between generation and rendering**.
5. **Clean packaging** for open-source distribution.

## How this refactor improves the original codebase

The original project already had a strong conceptual core: separate note and rhythm generators, support for Markov chains, a logistic map, cellular automata, and a BNF-style symbolic grammar. It also used a score-assembly pipeline and exported to MusicXML through `music21`. These ideas appeared in the original experimental modules and are now reorganized into a cleaner public package.

This refactor keeps those same generative families, but replaces fragile list-based event encoding with dataclasses, enforces typed interfaces, normalizes naming, separates models from generators, and moves score export into its own dedicated exporter layer.

## Example workflows

### 1. Markov pitch + cellular rhythm
Use a cellular automaton to generate rhythmic on/off patterns and a Markov chain to generate pitch classes.

### 2. Serial pitch + random rhythm
Useful for twelve-tone or cyclic systems over constrained rhythmic cells.

### 3. Grammar-based formal planning
Use the grammar engine to generate symbolic formal plans before mapping them to actual musical material.

## Build and publish

### Build distributions

```bash
python -m build
```

This creates:

- `dist/*.tar.gz`
- `dist/*.whl`

### Check package metadata

```bash
twine check dist/*
```

### Upload to TestPyPI

```bash
python -m twine upload --repository testpypi dist/*
```

### Upload to PyPI

```bash
python -m twine upload dist/*
```

## GitHub checklist

Before publishing the repository:

- add your real author name to `pyproject.toml`
- replace the placeholder GitHub URLs
- choose a license if you want a different one
- add screenshots or generated score examples
- optionally add GitHub Actions for tests and linting

## Roadmap

- MIDI export
- harmonic constraints
- phrase-level generators
- grammar-to-score mapping utilities
- probabilistic articulation and dynamics
- corpus-derived transition estimation

## License

MIT
