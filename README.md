# Rubik's Cube Solver (Work in Progress)

This project represents a 3x3 Rubik's Cube using a 54-character string model.
The goal is to build a solver capable of solving the cube within a limited number of moves using search algorithms.


## Cube Representation

The cube is represented as a 54-character string.

Face index mapping:

0–8   : U (White)
9–17  : R (Red)
18–26 : F (Green)
27–35 : D (Yellow)
36–44 : L (Orange)
45–53 : B (Blue)

Each face contains 9 stickers arranged in row-major order.

## Current Features

- Solved state representation
- Solved-state checker
- Cube face printer

## Roadmap

- Implement individual face moves (U, D, L, R, F, B)
- Add move application logic
- Implement BFS-based solver (depth-limited)
- Build Flask-based web interface


