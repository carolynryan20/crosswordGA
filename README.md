## Synopsis

At the top of the file there should be a short introduction and/ or overview that explains **what** the project is. This description should match descriptions added for package managers (Gemspec, package.json, etc.)

Our EA will evolve to make a viable crossword puzzle. We will start with an input of a 10x10 empty grid, where some squares in the grid will represent spaces where we can place letters, and some squares in the grid will contain black squares (places where we cannot place letters). Our output would be a grid filled in with words and black squares.  A good solution will include a high number of valid words (both horizontal and vertical), and a low number of invalid words. Our evaluation method will penalize for any invalid words. We think the scope of this project is appropriate - it is doable in a few weeks but isn’t too easy.

 \---------------------------------------- <br>
| ■ | ■ | ■ | ■ | b | ■ | ■ | ■ | ■ | ■ | <br>
 \---------------------------------------- <br>
| ■ | ■ | r | y | a | n | ■ | ■ | ■ | ■ | <br>
 \---------------------------------------- <br>
| ■ | ■ | ■ | ■ | r | ■ | p | ■ | ■ | ■ | <br>
 \---------------------------------------- <br>
| ■ | i | s | e | r | l | o | t | h | ■ | <br>
 \---------------------------------------- <br>
| ■ | ■ | ■ | ■ | ■ | ■ | l | ■ | ■ | ■ | <br>
 \---------------------------------------- <br>
| ■ | c | a | r | o | l | y | n | ■ | ■ | <br>
 \---------------------------------------- <br>
| ■ | ■ | ■ | ■ | ■ | ■ | a | ■ | ■ | ■ | <br>
 \---------------------------------------- <br>
| ■ | ■ | ■ | n | i | c | k | i | ■ | ■ | <br>
 \---------------------------------------- <br>
| ■ | ■ | ■ | ■ | ■ | ■ | o | ■ | ■ | ■ | <br>
 \---------------------------------------- <br>
| ■ | ■ | ■ | ■ | ■ | ■ | v | ■ | ■ | ■ | <br>
 \---------------------------------------- <br>

## Code Example

Show what the library does as concisely as possible, developers should be able to figure out **how** your project solves their problem by looking at the code example. Make sure the API you are showing off is obvious, and that your code is short and concise.

## Motivation

This project acts as a final project for CS 361: Evolutionary Computing and Artificial Life.  We have an EA here that will create a crossword puzzle to fill out a grid.  To further complicate the project, we added letter weights so less common letters are weighted so as to increase fitness in complicated crosswords.  We also added Multi-Objective fitness calculation in the form of NSGA and fitness sharing.

## Installation

executable: python genetic.py
to change EA parameters look to settings.txt

## Tests

Describe and show how to run the tests with code examples.

## Contributors

Authors:  Nicki Polyakov, Barr Iserloth, and Carolyn Ryan

## License

Majority of code base taken from open github repository found at https://github.com/groger/crossword-solver



What we've done:
    - All masks (of proper formatting) are able to work as crossword grid samples
    - Edited crossover to be what we said in our paper
    - Debugging so code will run no matter if user input is valid with hardcoded integers
    - Print crossword in the desired grid format
    - Added max generations so format follows more closely that in code we've seen throughout class
    - Settings.txt will take in information to use to give parameters to our GA
    - Weighted letters! Uncommon letters increase crossword fitness

