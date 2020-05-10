import os
import contextlib
import argparse
import time

# suppress welcome messages
with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
    import core.wrappers.engine as game
    import core.wrappers.minimax as agent
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
        "--depth",
        type=int,
        help="maximum tree depth for searching",
        default=1,
        metavar="",
    )
    parser.add_argument(
        "--c-backend",
        action="store_true",
        help="Use c for processing",
    )
    parser.add_argument(
        "--random",
        type=int,
        help="agent picks one out of n best moves randomly",
        default=3,
        metavar="",
    )
    args = parser.parse_args()
    # fmt: on

    return args


def check_validity(args):

    # args - depth
    if args.depth <= 0:
        raise ValueError("Depth has to be positive")
    if args.depth >= 3:
        raise ValueError("Ridiculously slow for depth %d" % args.depth)

    # args - random
    if args.random <= 0:
        raise ValueError("Randomness has to be positive")

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
        agent_func = lambda x: agent.best_move(x, 1, args.depth, args.random)

    # initialize modules
    window.init(shape)
    game.init(shape, backend)
    agent.init(backend)

    # class instances
    g_window = window.StaticGameWindow()
    g_engine = game.GameEngine()

    # main loop inside here
    g_window.main_loop(g_engine, None, agent_func)

    # print winner
    winner = ["Red", "Green", "No one"][g_engine.winnr]
    print(str(winner) + " Wins!")


main()
