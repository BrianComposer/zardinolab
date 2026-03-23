from zardinolab.generators import PatternRhythmGenerator, SerialRhythmGenerator


def test_pattern_generator_returns_valid_pattern() -> None:
    generator = PatternRhythmGenerator([["1/4"], ["1/8", "1/8"]])
    pattern = generator.next_pattern()
    assert pattern in [["1/4"], ["1/8", "1/8"]]


def test_serial_generator_cycles() -> None:
    generator = SerialRhythmGenerator([["1/4"], ["1/8"]])
    assert generator.next_pattern() == ["1/4"]
    assert generator.next_pattern() == ["1/8"]
    assert generator.next_pattern() == ["1/4"]
