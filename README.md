# My submissions for CS50AI
My submissions for the Introduction to Artificual Intelligence course CS50AI by Harvard - https://cs50.harvard.edu/ai/2024/


Work in Progess - I am still working on the course's assignments.


In most cases the coursemakers provided a template file. The course taker is then asked to write certain functions. What follows are list of functions that I had to write for each assignment:

## Search
### degrees
Link to assignment: https://cs50.harvard.edu/ai/2024/projects/0/degrees/

Short description:
> Write a program that determines how many “degrees of separation” apart two actors are.

Functions implemented by me:
- shortest_path

### tictactoe
Link to assignment: https://cs50.harvard.edu/ai/2024/projects/0/tictactoe/

Short description:
> Using Minimax, implement an AI to play Tic-Tac-Toe optimally.

Functions implemented by me:
- player
- actions
- result
- winner
- terminal
- utility
- minimax


## Knowledge
### knights
Link to assignment: [https://cs50.harvard.edu/ai/2024/projects/0/tictactoe/](https://cs50.harvard.edu/ai/2024/projects/1/knights/)

Short description:
> Write a program to solve logic puzzles.

Here, we were tasked with adding logical sentences to the knoweldge base

### minesweeper
Link to assignment: https://cs50.harvard.edu/ai/2024/projects/1/minesweeper/

Short description:
> Write an AI to play Minesweeper.

Functions implemented by me:
class Sentence:
- known_mines
- known_safes
- mark_mine
- mark_safe

class MinesweeperAI
- add_knowledge
- make_safe_move
- make_random_move


## Uncertainty
### heredity
Link to assignment: https://cs50.harvard.edu/ai/2024/projects/2/heredity/

Short description:
> Write an AI to assess the likelihood that a person will have a particular genetic trait.

Functions implemented by me:
- joint_probability
- update
- normalize

### pagerank
Link to assignment: https://cs50.harvard.edu/ai/2024/projects/2/pagerank/

Short description:
> Write an AI to rank web pages by importance.

Functions implemented by me:
- transition_model
- sample_pagerank
- iterate_pagerank

## Optimization
### crossword
Link to assignment: https://cs50.harvard.edu/ai/2024/projects/3/crossword/

Short description:
> Write an AI to generate crossword puzzles.

Functions implemented by me:
- enforce_node_consistency
- revise
- ac3
- assignment_complete
- consistent
- order_domain_values
- select_unassigned_variable
- backtrack
