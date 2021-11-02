This is a package that uses the Simplex method to solve linear optimisation problems. The input problem must be placed
into a file named 'input.txt'. To run the algorithm simply run the function main() in main.py

This algorithm can:
- Solve maximisation problems for single or multiple optima
- Solve Minimisation problems for single or multiple optima (using dual method)
- Automatically add slack and surplus variables
- Automatically add artificial variables

The input file is designed to make it very easy insert a problem.
It automatically parses through the lines and converts the information into a tableau.

Some important things to note are:
- There must be spaces between variables and +/-/=/≤/≥ operators
- There must not be a space between coefficients and variables
- The first line must specify whether it is a maximisation or minimisation problem by max or min
- z must have coefficient of 1

Example input files:

a)
min
z = 0.12x1 + 0.15x2
60x1 + 60x2 ≥ 300
12x1 + 6x2 ≥ 36
10x1 + 30x2 ≥ 90
x1 ≥ 0
x2 ≥ 0

b)
max
z = 60x1 + 90x2 + 300x3
x1 + x2 + x3 ≤ 600
x1 + 3x2 ≤ 600
2x1 + x3 ≤ 900

The output file contains the tableau and steps at each iteration, explaining what the pivots are and how it found them.
It has the (general) solution at the bottom.