# system
import contextlib
import argparse
import random
import time
import os

# configuration
import config.minimax as mmconfig
import config.mcts as mctsconfig

# engines
import core.wrappers.engine as game
import core.wrappers.minimax as minimax
import core.wrappers.mcts as mcts

# suppress welcome messages
with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
    import core.graphics.window as window


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


def construct_agent(oftype: str, player: int):
    """ Construct agent lambda functions  """

    if oftype == "human":
        agent_func = None

    elif oftype == "random":
        agent_func = lambda x: random.choice(game.valid_board_moves(x, player))

    elif oftype == "mcts":
        mcts_time_lim = mctsconfig.TIME_LIMIT
        mcts_param = mctsconfig.C_PARAM
        agent_func = lambda x: mcts.best_move(
            x, player, mcts_time_lim, mcts_param
        )

    elif oftype == "minimax":
        mm_depth = mmconfig.DEPTH
        mm_randn = mmconfig.RANDOM
        agent_func = lambda x: minimax.best_move(x, player, mm_depth, mm_randn)

    else:
        raise ValueError("Invalid player type " + oftype)

    return agent_func


def main():

    # default shape - not hardcoded
    shape = (4, 4)

    # get valid args
    args = get_args()

    # args - backend
    backend = "c" if args.c_backend else "python"

    # init game engine and window
    game.init(shape)
    window.init(shape)

    # init minimax
    if args.enemy == "minimax":
        minimax.init(backend)
        if backend == "c" and shape != (9, 6):
            err_msg = "minimax in c cannot work with shape != (9, 6)"
            raise ValueError(err_msg)
        print("Using %s backend for minimax" % backend)

    # init mcts
    if args.enemy == "mcts":
        assert not args.c_backend, "No c module for mcts :("

    # construct agents from args
    enemy_agent = construct_agent(args.enemy, 1)

    # construct game engine and window instances
    if args.minimal:
        game_engine = game.ChainReactionGame()
        game_window = window.StaticGameWindow(fps=40)
    else:
        game_engine = game.ChainReactionAnimated()
        game_window = window.AnimatedGameWindow(fps=40)

    # play game
    game_window.main_loop(game_engine, None, enemy_agent)


main()
