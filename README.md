# Python Chess Engine

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [TODO](#todo)
* [Instructions](#instructions)
* [Further development ideas](#further-development-ideas)

[Reference Youtube video](https://www.youtube.com/watch?v=EnYui0e73Rs&ab_channel=EddieSharick)

## TODO
- [✅︎] Cleaning up the code - right now it is really messy.
- [✅︎] Using numpy arrays instead of 2d lists.
- [✅︎] Implementing a GUI for playing chess with an AI opponent.
- [✅︎] Add Opening Books
- [ ] Stalemate on 3 repeated moves or 50 moves without capture/pawn advancement.
- [ ] Menu to select player vs player/computer.
- [ ] Allow dragging pieces.
- [ ] Resolve ambiguating moves (notation).

#### Keybinds:
* Press `z` to undo a move.
* Press `r` to reset the game.

## Further development ideas
1. Ordering the moves (ex. looking at checks and/or captures) should make the engine much quicker (because of the alpha-beta pruning).
2. Keeping track of all the possible moves in a given position, so that after a move is made the engine doesn't have to recalculate all the moves.
3. Evaluating kings placement on the board (separate in middle game and in the late game).
4. Book of openings.