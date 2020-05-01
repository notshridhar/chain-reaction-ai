import core.engine as game
import core.graphics.window as window

import random


def two_player():
    # main classes
    win = window.StaticGameWindow()
    eng = game.GameEngine()

    # main loop
    while win.open and not eng.gmovr:

        # trigger only when mouse clicked
        if win.mclk and win.midx is not None:
            eng.fast_play(win.midx)
            win.draw_all(eng.state, eng.plrid)

        # handle events
        win.event_handler()

    # print winner
    winner = ("None", "RED", "GREEN")[eng.winnr]
    print("\nWinner is " + winner + "!")

def main():
    # init modules
    shape = (9, 6)
    game.init(shape)
    window.init(shape)

    two_player()

main()
