# Project 2 – CSP – Tile Placement
## Problem statement

## Approach
The hardest part of the problem was formulating it is as a CSP. I did it as follows:
* **Variables** are 4x4 submatrices.
* **Domains** are generated dynamically. We achieve this by placing each tile on top of the matrix, and recording the result. There are maximum of 6 potential values in the domain: Full block, Outer boundary, EL(NW), EL(SW), EL(NE), EL(SE).

After establishing this, I implemented a CSP solution for the problem. Solution consists of two different algorithms.

1. I used **backtracking** algorithm to solve the problem with small matrices (N <= 8). I used a combination of **minimum remaining value** (MRV) and **degree** heuristics during this search. MRV heuristic always chooses the variable with the least number of options, while degree chooses variable that is involved in the highest number of constraints. I used **forwardchecking** method to cross of invalid values.

2. For N > 8 cases, I used minimum conflcit algorithm. This algorithm randomly selects variables with conflicts violating one or more its constraints. Then it assigns to this variable the value that minimizes the number of conflicts. If there is more than one value with a minimum number of conflicts, it chooses one randomly. This process of random variable selection and min-conflict value assignment is iterated until a solution is found or a pre-selected maximum number of iterations is reached.

After performing some benchmarking, I realized that Minimum conflict algorithm works better as the size of the matrix increases. However, it can take unnecessarily long time in smaller cases.

## Code

This code has been tested on Ubuntu 22.04 with Python 3.10.13.

```sh
git clone https://github.com/ceferisbarov/n-tiles

cs n-tiles

pip install numpy

python3 -m src.run --input <INPUT_PATH> --output <OUTPUT_PATH> -n <DIMENSION>

# For example:
python3 -m src.run --input input/8_3.txt --output output/8_3.txt -n 8
```

## References
Implementation of the backtracking algorithm, especially the idea of using both degree and MRV heuristics together, was inspired from python-constraint` library. 
