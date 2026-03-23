"""Discrete Markov-chain utilities."""

from __future__ import annotations

import random
from typing import Generic, TypeVar

StateT = TypeVar("StateT")


class MarkovChain(Generic[StateT]):
    def __init__(self, transition_matrix: dict[StateT, dict[StateT, float]], initial_state: StateT) -> None:
        if initial_state not in transition_matrix:
            raise ValueError("The initial state must exist in the transition matrix.")
        self.transition_matrix = transition_matrix
        self._validate()
        self.state = initial_state

    def _validate(self) -> None:
        for state, transitions in self.transition_matrix.items():
            if not transitions:
                raise ValueError(f"State {state!r} has no outgoing transitions.")
            total = sum(transitions.values())
            if total <= 0:
                raise ValueError(f"State {state!r} has a non-positive probability sum.")
            for target, probability in transitions.items():
                if target not in self.transition_matrix:
                    raise ValueError(f"Unknown target state {target!r} in transitions from {state!r}.")
                if probability < 0:
                    raise ValueError("Transition probabilities cannot be negative.")

    def next_state(self) -> StateT:
        transitions = self.transition_matrix[self.state]
        states = list(transitions.keys())
        weights = list(transitions.values())
        self.state = random.choices(states, weights=weights, k=1)[0]
        return self.state
