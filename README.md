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

# 🧊 Rubik's Cube Solver

## Overview

This project implements a Rubik’s Cube Solver using Python and BFS (Breadth-First Search).
It includes a full-stack setup with a Flask backend and an interactive 3D frontend.

---

## Tech Stack

* Python (Core logic, BFS)
* Flask (Backend API)
* HTML, CSS, JavaScript (Frontend)
* Three.js (3D Cube Visualization)

---

## Features

* Cube represented using a 54-character string model
* Move functions for all faces (U, D, L, R, F, B)
* BFS-based solver for short-depth scrambles
* Web interface for user input
* 3D cube visualization

---

##  Limitations

* Solver works for shallow scrambles (due to BFS)
* Cube visualization is not yet fully synced with solver state

---

## Usage

1. Enter scramble (e.g. `U R F`)
2. Click **Solve**
3. View solution sequence

---

## Future Improvements

* Implement IDA* for deeper solving
* Animate cube moves visually
* Sync cube state with solver

---


