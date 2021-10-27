from data import *
from simplex import *

if __name__ == '__main__':
    np.set_printoptions(precision=5, suppress=True)

    init_tableau, solve_type, top_row = read_txt(input_filename='input.txt')
    problem = Simplex(init_tableau, solve_type, top_row)
    solution = problem.solve_max()
    logs = problem.logs
    save_logs(logs, top_row, solution, filename='output.txt')
