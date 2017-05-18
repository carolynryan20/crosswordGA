Code for CS 361: Evolutionary Computing and Artificial Life Final Project

Authors:  Nicki Polyakov, Barr Iserloth, and Carolyn Ryan

Majority of code base taken from open github repository found at https://github.com/groger/crossword-solver

executable: python genetic.py <mask_size>.mask <dictionary>.txt


Our EA will evolve to make a viable crossword puzzle. We will start with an input of a 10x10 empty grid, where some squares in the grid will represent spaces where we can place letters, and some squares in the grid will contain black squares (places where we cannot place letters). Our output would be a grid filled in with words and black squares.  A good solution will include a high number of valid words (both horizontal and vertical), and a low number of invalid words. Our evaluation method will penalize for any invalid words. We think the scope of this project is appropriate - it is doable in a few weeks but isn’t too easy.

