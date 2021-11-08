from data import *
from simplex import *


def main():
    np.set_printoptions(precision=5, suppress=True)

    init_tableau, solve_type, top_row = read_txt(input_filename='recipe bank')
    problem = Simplex(init_tableau, solve_type, top_row)
    solution = problem.solve(print_solution=True)
    logs = problem.logs
    save_logs(logs, top_row, solution, solve_type, output_filename='output.txt')


if __name__ == '__main__':
    main()
