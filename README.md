## Synopsis

Our EA will evolve to make a viable crossword puzzle. We will start with an input of an empty grid, where some squares in the grid will represent spaces where we can place letters, and some squares in the grid will contain black squares (places where we cannot place letters). Our output would be a grid filled in with words and black squares.  A good solution will include a high number of valid words (both horizontal and vertical), and a low number of invalid words. Our evaluation method will penalize for any invalid words. We think the scope of this project is appropriate - it is doable in a few weeks but isn’t too easy.

|   |   |   |   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|
| ■ | ■ | ■ | ■ | b | ■ | ■ | ■ | ■ | ■ |
| ■ | ■ | r | y | a | n | ■ | ■ | ■ | ■ |
| ■ | ■ | ■ | ■ | r | ■ | p | ■ | ■ | ■ |
| ■ | i | s | e | r | l | o | t | h | ■ |
| ■ | ■ | ■ | ■ | ■ | ■ | l | ■ | ■ | ■ |
| ■ | c | a | r | o | l | y | n | ■ | ■ |
| ■ | ■ | ■ | ■ | ■ | ■ | a | ■ | ■ | ■ |
| ■ | ■ | ■ | n | i | c | k | i | ■ | ■ |
| ■ | ■ | ■ | ■ | ■ | ■ | o | ■ | ■ | ■ |
| ■ | ■ | ■ | ■ | ■ | ■ | v | ■ | ■ | ■ |
## Motivation

This project acts as a final project for CS 361: Evolutionary Computing and Artificial Life.  We have an EA here that will create a crossword puzzle to fill out a grid.  To further complicate the project, we added letter weights so less common letters are weighted so as to increase fitness in complicated crosswords.  We also added Multi-Objective fitness calculation in the form of NSGA and fitness sharing.

## Installation

executable: python genetic.py
to change EA parameters look to settings.txt

dependency: imports matplotlib.pyplot for graph popups

## Tests

Example tests and parameters for settings.txt can be found in the report.pdf.

## Contributors

Authors:  Nicki Polyakov, Barr Iserloth, and Carolyn Ryan

## License

Majority of code base taken from open github repository found at https://github.com/groger/crossword-solver. Recieved great help from Sherri Goings on how to implement NSGA and fitness sharing.  Also for teaching us everything we used for this project.


## Our Additions

Changed how masks are read in order to read all valid masks (that is,
all properly formatted masks). (throughout)

Debugged some issues with minimum length words. (throughout)

Printing crosswords in a grid, similar to how they would appear phenotypically. (print_solution: line 392)

Added settings.txt for easy changes to any parameters we use. (readSettings: line 24)

Added maximum generations so as to continue evolving until at specified generation. (in readSettings)

Added NSGA.  Non-Dominated Sorting Genetic Algorithm added with fitness sharing. (findNonDominatedFronts: line 593, shareValue: line 654, distance: line 660, individual.dominates: in individual.py)
Thanks to Sherri Goings for help on this part.

Added tournament selection. (tournament: line 376)

Added custom mutation to only mutate to words that maintain intersection validity. (mutate: line 679)

Added a new objective fitness of letter weights, so less common letters are more likely to appear in the crosswords. (findTotalValue: line 830)

Added individual.py, a class that stores all information for individuals. (individual.py, integration throughout genetic.py)

Added optional MOB or single objective fitnesses. (throughout, mostly fit calculation and selection)

Added graphing ability to see the changes in fitness over time. (line 360, plots)
