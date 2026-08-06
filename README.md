# Four Fours Solver

A small Python program that solves Four Fours-style puzzles using dynamic programming.

Given a number (the "basis"), the solver attempts to generate expressions using exactly that number a fixed number of times and finds the shortest expression for each possible result.

By default, it solves the classic puzzle:

> Use four 4s to make as many numbers as possible.

## Features

- Supports arbitrary single-digit bases (`4`, `5`, `7`, etc.)
- Uses exact rational arithmetic (`fractions.Fraction`)
- Finds shortest known expressions for each value
- Supports:
  - addition (`+`)
  - subtraction (`-`)
  - multiplication (`*`)
  - division (`/`)
  - exponentiation (`^`)
  - factorial (`!`)
  - square root (`√`)
  - concatenated digits (`44`, `444`, etc.)
  - decimal forms (`.4`, `.44`, etc.)
- Configurable search limits to avoid runaway expressions
- Reports completion percentage

## Requirements

- Python 3.10+

No external dependencies are required.

## Usage

Run the solver:

```bash
python solver.py
```

Or run with `--help` for command-line options:
```bash
python solver.py --help
```