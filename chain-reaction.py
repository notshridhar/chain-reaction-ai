#!/usr/bin/env python3

# system
import argparse
import chain_reaction.game as chain_reaction_game


def get_args():
    """ Function to parse all arguments """

    # fmt: off
    parser = argparse.ArgumentParser(description="Chain Reaction")
    parser.add_argument(
        "enemy",
        type=str,
        help="Opponent to play with - [human, random, mcts, minimax]",
    )
    parser.add_argument(
        "--minimal",
        action="store_true",
        help="Play in a minimal non-animated window",
    )
    parser.add_argument(
        "--c-backend",
        action="store_true",
        help="Use c for processing",
    )
    args = parser.parse_args()
    # fmt: on

    return args


def main():

    # get args
    args = get_args()

    # parameters
    shape = (9, 6)
    backend = "c" if args.c_backend else "python"
    win_type = "static" if args.minimal else "animated"

    # players
    player1 = "human"
    player2 = args.enemy

    # configurations
    config1 = {}
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
