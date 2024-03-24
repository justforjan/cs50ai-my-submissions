# My submissions for CS50AI
My submissions for the Introduction to Artificial Intelligence course CS50AI by Harvard - https://cs50.harvard.edu/ai/2024/


Course finished on 2024-03-24! :tada:


In most cases the coursemakers provided a template file. The course taker is then asked to write certain functions. What follows are list of functions that I had to write for each assignment.


- [My submissions for CS50AI](#my-submissions-for-cs50ai)
  - [Week 0 - Search](#week-0---search)
    - [degrees](#degrees)
    - [tictactoe](#tictactoe)
  - [Week 1 - Knowledge](#week-1---knowledge)
    - [knights](#knights)
    - [minesweeper](#minesweeper)
  - [Week 2 - Uncertainty](#week-2---uncertainty)
    - [heredity](#heredity)
    - [pagerank](#pagerank)
  - [Week 3 - Optimization](#week-3---optimization)
    - [crossword](#crossword)
  - [Week 4 - Learn](#week-4---learn)
    - [nim](#nim)
    - [shopping](#shopping)
  - [Week 5 - Neural Networks](#week-5---neural-networks)
    - [traffic](#traffic)
  - [Week 6 - Language](#week-6---language)
    - [parser](#parser)
    - [attention](#attention)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

## Week 0 - Search
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


## Week 1 - Knowledge
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


## Week 2 - Uncertainty
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

## Week 3 - Optimization
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


## Week 4 - Learn
### nim
Link to assignment: https://cs50.harvard.edu/ai/2024/projects/4/nim/

Short description:
> Write an AI that teaches itself to play Nim through reinforcement learning.

Functions implemented by me:
- get_q_value
- update_q_value
- best_future_reward
- chose_action

### shopping
Link to assignment: https://cs50.harvard.edu/ai/2024/projects/4/shopping/

Short description:
> Write an AI to predict whether online shopping customers will complete a purchase.

Functions implemented by me:
- load_data
- train_model
- evaluate

## Week 5 - Neural Networks
### traffic
Link to assignment: https://cs50.harvard.edu/ai/2024/projects/5/traffic/

Short description:
> Write an AI to identify which traffic sign appears in a photograph.

Functions implemented by me:
- load_data
- get_model


## Week 6 - Language
### parser
Link to assignment: https://cs50.harvard.edu/ai/2024/projects/6/parser/

Short description:
> Write an AI to parse sentences and extract noun phrases.

Functions implemented by me:
- preprocess
- np_chung

Additionally, I was tasked with providing the NONTERMINAL of the context-free grammer

### attention
Link to assigment: https://cs50.harvard.edu/ai/2024/projects/6/attention/

Short description:
> Write an AI to predict a masked word in a text sequence.

Functions implemented by me:
- get_mask_token_index
- get_color_for_attention_score
- visualize_attentions
