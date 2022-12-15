# Chain Reaction AI

AI opponent for the strategic board game Chain Reaction.

## Installation

To install the package in your computer, run the following (preferably in virtual environment)

    git clone https://github.com/shridharrhegde/chain-reaction-ai
    cd chain-reaction-ai
    pip install -r requirements.txt
    pip install .

## Usage

    $ chain-reaction
    usage:

    python3 chain-reaction.py

    Then provide the appropriate input values as suggested by the program.

## Configurations

To play a game with your own configurations, see sample.py

## Enemy Agents

Here is a list of agents you can play against (in ascending levels of difficulty)

1. **Random** : Just a random move maker that picks from valid moves.
2. **MCTS** : Naive Monte Carlo Tree Search that simulates games randomly. Needs long time to be good enough.
3. **Minimax** : Simple DFS to minimize loss. Very hard to beat because of the aggressive static board evaluation function.

## Game Rules

- Two players take turns to place **orbs** of their corresponding colors. A player can only place an orb in an empty cell or a cell which already contains colored orbs of his own. When two or more orbs are placed in the same cell, they stack up.
- The **critical mass** of a cell is equal to the number of adjacent cells i.e., 4 for usual cells, 3 for edge cells and 2 for corner cells.
- When a cell is loaded with a number of orbs equal to its critical mass, the stack explodes. As a result of the explosion, all the orbs from the initial cell fly to adjacent cells. The explosions might result in overloading of an adjacent cell and the chain reaction of explosion continues until every cell is stable.
- When a red cell explodes and there are green cells around, the green cells are converted to red and the other rules of explosions still follow. The same rule is applicable for other colors.
- The winner is the one who eliminates other player's orbs.

## Gameplay

A game against minimax agent looks like this -

![](images/preview.gif)

## Uninstalling

To uninstall, run

    pip uninstall chain-reaction

## Dependencies

### Runtime

- python3
- numpy
- pygame

### Building

- wheel
- setuptools
- gcc

Tested on python 3.6 and pygame 1.9.6 on both Mac and Linux

## Licence

The project is completely open-source under MIT Licence, so feel free to fork and modify this code.
