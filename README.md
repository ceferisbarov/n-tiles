# Project 2 – CSP – Tile Placement
## Problem statement

## Approach
The hardest part of the problem was formulating it is as a CSP. I did it as follows:
* **Variables** are 4x4 submatrices.
* **Domains** are generated dynamically. We achieve this by placing each tile on top of the matrix, and recording the result. There are maximum of 6 potential values in the domain: Full block, Outer boundary, EL(NW), EL(SW), EL(NE), EL(SE).

After establishing this, I implemented Backtracking algorithm to solve the problem.

I used a combination of **minimum remaining value** (MRV) and **degree** heuristics during the search. MRV heuristic always chooses the variable with the least number of options, while degree chooses variable that is involved in the highest number of constraints.

## Code

This code has been tested on Ubuntu 22.04 with Python 3.10.13.

```sh
pip install numpy

python3 -m src.run --input <INPUT_PATH> --output <OUTPUT_PATH> -n <DIMENSION>

# For example:
python3 -m src.run --input input/8_3.txt --output output/8_3.txt -n 8
```

## References
Solution was inspired from python-constraint library.
