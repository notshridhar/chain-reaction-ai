# Chain Reaction AI
AI opponent for the strategic board game Chain Reaction.

## Usage
    $ ./play.py --help
    usage: play.py [-h] enemy

    positional arguments:
    enemy       Opponent to play with - [human, minimax]

    optional arguments:
    -h, --help  show this help message and exit


## Game Rules
* All cells are initially empty. The two players take turns to place __orbs__ of their corresponding colors. A player can only place an orb in an empty cell or a cell which already contains colored orbs of his own. When two or more orbs are placed in the same cell, they stack up.
* The __critical mass__ of a cell is equal to the number of orthogonally adjacent cells. That would be 4 for usual cells, 3 for edge cells and 2 for corner cells.
* When a cell is loaded with a number of orbs equal to its critical mass, the stack explodes. As a result of the explosion, all the orbs from the initial cell fly to adjacent cells. The explosions might result in overloading of an adjacent cell and the chain reaction of explosion continues until every cell is stable.
* When a red cell explodes and there are green cells around, the green cells are converted to red and the other rules of explosions still follow. The same rule is applicable for other colors.
* The winner is the one who eliminates other player's orbs.


## Enemy Agents
Here is a list of agents you can play against -
1. __Minimax__ : Defaults to a depth of 1 (max of min of heuristic) because the branching factor is too large for deeper searches even with alpha-beta pruning.


## Gameplay
A normal two player version looks like this - 

![](images/two_player.gif)


## Dependencies
* python3
* numpy
* pygame

Tested on python 3.6 and pygame 1.9.6 on both Mac and Linux

## Licence
The project is completely open-source under MIT Licence, so feel free to fork and modify this code. 
