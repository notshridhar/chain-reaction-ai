# system
import os
import contextlib
import argparse
import time

# configuration
import config.minimax as mmconfig

# engines
import core.wrappers.engine as game
import core.wrappers.minimax as minimax

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
        help="Opponent to play with - [human, minimax]",
    )
    parser.add_argument(
        "--c-backend",
        action="store_true",
        help="Use c for processing",
    )
    args = parser.parse_args()
    # fmt: on

    return args


def check_validity(args):
    """ Raise ValueErrors if the arguments are invalid """

    # args - enemy
    if args.enemy not in ["human", "minimax"]:
        raise ValueError("Invalid enemy choice", args.enemy)


def main():

    args = get_args()
    check_validity(args)

    shape = (9, 6)

    # args - backend
    backend = "c" if args.c_backend else "python"
    print("Using %s backend" % backend)

    # args - enemy
    if args.enemy == "human":
        agent_func = None
    elif args.enemy == "minimax":
        mm_depth = mmconfig.DEPTH
        mm_randn = mmconfig.RANDOM
        agent_func = lambda x: minimax.best_move(x, 1, mm_depth, mm_randn)

    # initialize modules
    window.init(shape)
    game.init(shape, backend)
    minimax.init(backend)

    # class instances
    gwindow = window.StaticGameWindow()
    gengine = game.GameEngine()

    # main loop inside here
    gwindow.main_loop(gengine, None, agent_func)

    # print winner
    winner = ["Red", "Green", "No one"][gengine.winnr]
    print(str(winner) + " Wins!")


main()
