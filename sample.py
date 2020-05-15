#!/usr/bin/env python3

# system
import chain_reaction.game as chain_reaction_game


def main():

    # parameters
    shape = (9, 6)
    backend = "python"
    win_type = "animated"

    # players
    player1 = "random"
    player2 = "minimax"

    # configurations
    config1 = {
        "minimax": {"search_depth": 1, "randomness": 3},
        "mcts": {"time_limit": 1.0, "c_param": 1.5},
    }
    config2 = {
        "minimax": {"search_depth": 1, "randomness": 3},
        "mcts": {"time_limit": 1.0, "c_param": 1.5},
    }

    # start game with given parameters
    chain_reaction_game.start_game(
        shape, backend, win_type, player1, player2, config1, config2
    )


if __name__ == "__main__":
    main()
