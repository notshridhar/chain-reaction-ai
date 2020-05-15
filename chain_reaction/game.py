# system
import contextlib
import random
import os

# engines
import chain_reaction.wrappers.engine as game
import chain_reaction.wrappers.minimax as minimax
import chain_reaction.wrappers.mcts as mcts

# suppress welcome messages
with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
    import chain_reaction.graphics.window as window


def construct_agent(oftype: str, player: int, configs: dict):
    """ Construct agent lambda functions  """

    if oftype == "human":
        agent_func = None

    elif oftype == "random":
        agent_func = lambda x: random.choice(game.valid_board_moves(x, player))

    elif oftype == "mcts":
        mcts_timelim = configs["mcts"]["time_limit"]
        mcts_c_param = configs["mcts"]["c_param"]
        agent_func = lambda x: mcts.best_move(
            x, player, mcts_timelim, mcts_c_param
        )

    elif oftype == "minimax":
        mm_depth = configs["minimax"]["search_depth"]
        mm_randn = configs["minimax"]["randomness"]
        agent_func = lambda x: minimax.best_move(x, player, mm_depth, mm_randn)

    else:
        raise ValueError("Invalid player type " + oftype)

    return agent_func


def construct_instance(oftype: str):
    """ Construct game and window instances """

    if oftype == "static":
        game_inst = game.ChainReactionGame()
        win_inst = window.StaticGameWindow(fps=40)

    elif oftype == "animated":
        game_inst = game.ChainReactionAnimated()
        win_inst = window.AnimatedGameWindow(fps=40)

    else:
        raise ValueError("Invalid instance type " + oftype)

    return (game_inst, win_inst)


def main_graphical_loop(game_inst, win_inst, agent1_func, agent2_func):
    """
    Play graphical game with agents
    -------------------------------
    - game_inst   - Game Instance
    - win_inst    - Window Instance
    - agent1_func - function that outputs move for agent 1
    - agent2_func - function that outputs move for agent 2
    """

    # splash screen
    win_inst.on_game_start()

    # draw for first time
    win_inst.on_game_move(game_inst, None)

    # construct human agent functions
    if agent1_func is None:
        agent1_func = lambda x: win_inst.midx
    if agent2_func is None:
        agent2_func = lambda x: win_inst.midx

    # play until game over or closed
    while not game_inst.game_over and win_inst.open:

        # players alternate
        if game_inst.player == 0:
            move = agent1_func(game_inst.board)
        else:
            move = agent2_func(game_inst.board)

        # play move
        if move is not None:
            win_inst.event_flush()  # agent takes long time
            win_inst.on_game_move(game_inst, move)
            move = None

        # handle events and limit fps
        win_inst.event_handler()
        win_inst.clock.tick(win_inst.fps)

    # game over
    win_inst.on_game_end(game_inst)


def start_game(
    shape: tuple,
    backend: str,
    win_type: str,
    player1: str,
    player2: str,
    config1: dict,
    config2: dict,
):
    """ Game Entry Point """

    # initialize for shapes
    game.init(shape)
    window.init(shape)

    # minimax init
    if player1 == "minimax" or player2 == "minimax":

        # invalid condition
        if backend == "c" and shape != (9, 6):
            err_msg = "minimax in c cannot work with shape != (9, 6)"
            raise ValueError(err_msg)

        minimax.init(backend)
        print("Using %s backend for minimax" % backend)

    # mcts init
    if player1 == "mcts" or player2 == "mcts":

        # invalid condition
        if backend == "c":
            raise ValueError("No c module for mcts :(")

    # construct players
    player1_agent = construct_agent(player1, 0, config1)
    player2_agent = construct_agent(player2, 1, config2)

    # construct window and game instances
    game_inst, win_inst = construct_instance(win_type)

    # start game loop
    main_graphical_loop(game_inst, win_inst, player1_agent, player2_agent)
