# Flocking Demo

A simple [Python](https://www.python.org/) / [Pygame Zero](https://pygame-zero.readthedocs.io/) demo.

<img src="https://github.com/retroredge/pgzero-games/raw/master/flocking/images/screen-shot.png?raw=true" width="50%" height="50%">

This demo implements the 3 basic flocking rules of Aligment, Cohesion and Separation. The birds use 3 different vectors to give them natural looking steering and movement.

The following constants control various aspects of the simulation: NUM_BIRDS, LOCAL_RADIUS, MAX_STEERING_FORCE and SPEED

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

## Controls

Z / X: decrease / increase Aligment weighting
C / V: decrease / increase Cohesion weighting
B / N: decrease / increase Separation weighting
