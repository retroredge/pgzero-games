# Conway's Game of Life

A simple [Python](https://www.python.org/) / [Pygame Zero](https://pygame-zero.readthedocs.io/) implementation
of John Conway's Game of Life.

<img src="https://github.com/retroredge/pgzero-games/raw/master/game-of-life/images/screen-shot.png?raw=true" width="50%" height="50%">

The Cellular Automata on a 2D grid follow these basic rules:

- live cells with less than 2 neighbours die
- live cells with 4 or more neighbours die
- dead cells with 3 neighbours come to life
- live cells with 2 or 3 neighbours survive

## Requirements

- Python 3
- Pygame Zero 1.2.1

```
python3 -m ensurepip
pip3 install pgzero
```

## To Run
```
python3 game.py
```

## Things to try

Try changing the following variables to see the effect on the simulation:

- starting DENSITY via the `int(MAP_HEIGHT * MAP_WIDTH * 0.3)` code
- screen WIDTH and HEIGHT
- CELL_SIZE
- frame rate via the `ticks % 10` code

