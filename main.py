from data import *
from simplex import *

if __name__ == '__main__':
    np.set_printoptions(precision=3, suppress=True)

    tableau, solve_type = read_txt()
    print("Starting Tableau...\n",tableau)
    problem = Simplex(tableau, solve_type)
    problem.solve_max()
