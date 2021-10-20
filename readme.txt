The input file is set out to make it very easy insert a problem.
It automatically parses through the lines and converts the information into a tableau.
Some important things to note are:
- There must be spaces between variables and +/-/=/≤/≥ operators
- z must have coefficient of 1


Example input files:

a)

max
z = 2x1 - x2 + 2x3
2x1 + x2 ≤ 10
x1 + 2x2 - 2x3 ≤ 20
x2 + 2x3 ≤ 5
x1 ≥ 0
x2 ≥ 0
x3 ≥ 0

b)

max
z = 60x1 + 90x2 + 300x3
x1 + x2 + x3 ≤ 600
x1 + 3x2 ≤ 600
2x1 + x3 ≤ 900
