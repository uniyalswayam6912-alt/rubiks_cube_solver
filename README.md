# Rubik's Cube Solver

## Overview
A high-performance 3x3 Rubik’s Cube solver using advanced search algorithms and heuristic pruning.

This project includes:
- Backend solver (Python)
- API layer for solving
- Interactive frontend visualization

---

## Algorithm

The solver is based on:

- **IDA\*** (Iterative Deepening A*)
- Heuristic pruning using precomputed tables
- Optimized cube state representation

### Key Concepts
- Phase-based solving
- Heuristic evaluation (corner + edge databases)
- State-space reduction

---

## Features

- Solve any valid 3x3 cube state
- Fast solution generation using heuristics
- Frontend visualization of moves
- API integration for real-time solving

---

## Project Structure

## Example

Scramble (≤ 6 moves):
R U R' U' F2

Input representation:
[generated internally from scramble]

Output (solution):
F2 U R U' R'

Number of moves: 5  
Time taken: ~0.01s
