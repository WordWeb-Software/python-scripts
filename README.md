# Crossword Compiler Command Line Demo

Demonstrates how to call Crossword Compiler command line from Python.

**Note: For fill this is minimal working example, no error checking etc.**

## Requirements

- Crossword Compiler must be installed, looks for executable in: `'c:\Program Files (x86)\Crossword Compiler\ccw.exe'`
- Python 3.12+ for python example

## Usage

The command line interface and wrapper provides two main functions:

 - build word list
 - fill grid (minimal working example: fixed grid, one random fill, one output file)

The program can be run directly passing `-c jsonfile.json`, or programmatically via the python demo wrapper,
which pipes a dictionary to Crossword Compiler.

Running from command line and via python tested via Action, giving output puzzle files as artifact outputs.

## File Structure

```
├── source/
│   └── ccw.py         # Thin python wrapper implementation
├── tests/
│   └── fill.json      # Test configuration
└── github/
    └── workflows/     # GitHub Actions workflows
```
