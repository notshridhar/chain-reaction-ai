#!/usr/bin/env python3

# system
import argparse
import time
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
    parser.add_argument(
        "--startsecond",
        action="store_true",
        help="Swap player 1 and player 2."
    )
    args = parser.parse_args()
    # fmt: on

    return args


def main():

    # get args
    # args = get_args()
    # print(args)

    # Formulating the MENU for the game as follows
    menu1 = "*********** CHAIN REACTI0N GAME WITH AI ***********  \nThis is a two player game and user needs to select both the players from the available list of players: \n1. Human Player \n2. Randomizer AI bot \n3. MCTS AI bot \n4. Minimax AI Bot \nEnter your choice number for Player 1:"
    print(menu1)
    first_Player = input()

    print("Enter your choice number for 2nd Player:")
    second_Player = input()

    match first_Player:
        case "1":
            player1 = "human"
        case "2":
            player1 = "random"
        case "3":
            player1 = "mcts"
        case "4":
            player1 = "minimax"
        case _:
            player1 = "cc"

    match second_Player:
        case "1":
            player2 = "human"
        case "2":
            player2 = "random"
        case "3":
            player2 = "mcts"
        case "4":
            player2 = "minimax"
        case _:
            player2 = "cc"

    print("Configuring game for " + player1 + " vs " + player2)
    
    # player1 = "human"
    # player2 = args.enemy

    print("What should be the size of the game matrix? \nEnter number of rows:")
    rows = input()
    print("Enter number of columns:")
    cols = input()

    if(int(rows) < 2):
        print("Minimum 2 rows are required. Setting rows=2")
        rows = "2"
    
    if(int(cols) < 2):
        print("Minimum 2 columns are required. Setting columns=2")
        cols = "2"
    

    # shape = (9, 6)
    # Handled the NotANumberException here
    print("Setting game matrix size as " + rows + " x " + cols)
    shape = (int(rows), int(cols))

    print("Thanks! Few more customizations and we are good to go! \nDo you want to enable Animations in UI? (For Yes press y or 1):")
    isAnimated = input()
    # win_type = "static" if args.minimal else "animated"
    if(isAnimated in {"y", "yes", "Y", "Yes", "1"}):
        win_type = "animated"
        print("Game animation enabled!")
    else: 
        win_type = "static"
        print("Game animation disabled!")

    print("RED is the color of first Player! Which player should start the game? (1 or 2)?")
    gameStarterPlayer = input()
    if(gameStarterPlayer == 1):
        print( player1 + " is the player in RED and "+ player2 + " is the player in GREEN")
    else:
        print( player2 + " is the player in RED and " + player1 + " is the player in GREEN")

    # backend = "c" if args.c_backend else "python"
    #using backend as python always
    backend = "python"

    # configurations
    config1 = {
        "minimax": {"search_depth": 1, "randomness": 3},
        "mcts": {"time_limit": 1.0, "c_param": 1.5},
    }
    config2 = {
        "minimax": {"search_depth": 1, "randomness": 3},
        "mcts": {"time_limit": 1.0, "c_param": 1.5},
    }

    # if args.startsecond:
    if gameStarterPlayer == "2":
        # print("Second Player is going to start the game!")
        player_temp = player1
        config_temp = config1

        player1 = player2
        config1 = config2

        player2 = player_temp
        config2 = config_temp

        print()

    # start game with given parameters
    chain_reaction_game.start_game(
        shape, backend, win_type, player1, player2, config1, config2
    )


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    time_taken = end_time - start_time
    print("Total Time taken: " + str(time_taken))