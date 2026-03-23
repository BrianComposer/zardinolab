"""Small BNF-like grammar expander."""

from __future__ import annotations

import random
import re


class GrammarExpander:
    def __init__(self, grammar: dict[str, str]) -> None:
        if not grammar:
            raise ValueError("Grammar cannot be empty.")
        self.grammar = grammar
        self.prepared = {key: value.split("|") for key, value in grammar.items()}
        self.start_symbol = next(iter(grammar.keys()))

    def expand(self, max_iterations: int = 30) -> str:
        production = self.start_symbol
        for _ in range(max_iterations):
            production = self._expand_optional_blocks(production)
            production = self._expand_repetition_blocks(production)
            new_production = production
            for non_terminal, options in self.prepared.items():
                if non_terminal in new_production:
                    new_production = new_production.replace(non_terminal, random.choice(options), 1)
            production = new_production
            if not self._contains_non_terminal(production):
                return production.strip()
        raise RuntimeError("Maximum grammar expansion depth exceeded.")

    def _contains_non_terminal(self, text: str) -> bool:
        return any(symbol in text for symbol in self.grammar)

    def _expand_optional_blocks(self, text: str) -> str:
        pattern = re.compile(r"\[(.*?)\]")
        while True:
            match = pattern.search(text)
            if match is None:
                return text
            replacement = match.group(1) if random.randint(0, 1) else ""
            text = text[: match.start()] + replacement + text[match.end() :]

    def _expand_repetition_blocks(self, text: str) -> str:
        pattern = re.compile(r"\{(.*?)\}")
        while True:
            match = pattern.search(text)
            if match is None:
                return text
            repetitions = random.randint(1, 5)
            replacement = match.group(1) * repetitions
            text = text[: match.start()] + replacement + text[match.end() :]
