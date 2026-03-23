from zardinolab.models import MarkovChain


def test_markov_chain_returns_known_state() -> None:
    chain = MarkovChain(
        transition_matrix={
            "A": {"A": 0.0, "B": 1.0},
            "B": {"A": 1.0, "B": 0.0},
        },
        initial_state="A",
    )
    assert chain.next_state() == "B"
