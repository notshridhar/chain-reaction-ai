import argparse
import time

import core.wrappers.engine as game
import core.wrappers.minimax as agent
import core.graphics.window as window


def human_vs_human():
    # main classes
    win = window.StaticGameWindow()
    eng = game.GameEngine()

    # main loop
    while win.open and not eng.gmovr:

        # trigger only when mouse clicked
        if win.midx is not None:
            eng.fast_play(win.midx)
            win.draw_all(eng.board, eng.plrid)

        # handle events
        win.event_handler()

    # print winner
    if eng.winnr == 1:
        print("Green Wins!")
    elif eng.winnr == 0:
        print("Red Wins!")


def human_vs_minimax(depth=1, rand=True):
    # main classes
    win = window.StaticGameWindow()
    eng = game.GameEngine()

    cpu_turn = False
    req_draw = True
    samples = 3 if rand else 1

    # main loop
    while win.open and not eng.gmovr:

        # for agent
        if cpu_turn:
            best_move = agent.move_chooser(eng.board, 1, depth, samples)
            eng.fast_play(best_move)
            req_draw = True
            cpu_turn = False

        # for human player
        else:
            if win.midx is not None and eng.fast_play(win.midx):
                req_draw = True
                cpu_turn = True

        # acknowledge draw request
        if req_draw:
            req_draw = False
            win.draw_all(eng.board, eng.plrid)

        # handle events
        win.event_handler()

    # print winner
    if eng.winnr == 1:
        print("CPU Wins!")
    elif eng.winnr == 0:
        print("You Win!")


def main():
    # parse arguments
    parser = argparse.ArgumentParser(description="Chain Reaction")
    parser.add_argument(
        "enemy", type=str, help="Opponent to play with - [human, minimax]",
    )
    parser.add_argument(
        "-c", "--c-backend", help="Use c for processing", action="store_true",
    )
    args = parser.parse_args()

    # store variables
    shape = (9, 6)
    backend = "c" if args.c_backend else "python"
    if args.c_backend:
        print("Using C backend")


    # initialize modules
    window.init(shape)
    game.init(shape, backend=backend)
    agent.init(backend=backend)

    # choose game
    if args.enemy == "human":
        human_vs_human()
    elif args.enemy == "minimax":
        human_vs_minimax()
    else:
        print("Error: invalid enemy choice " + str(args.enemy))


main()
