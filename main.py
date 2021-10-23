from data import *
from simplex import *

if __name__ == '__main__':
    np.set_printoptions(precision=5, suppress=True)

    init_tableau, solve_type, top_row = read_txt()
    print("Starting Tableau...\n",init_tableau)
    problem = Simplex(init_tableau, solve_type)
    problem.solve_max()
    logs = problem.logs
    save_log(logs, top_row, filename='output.txt')
