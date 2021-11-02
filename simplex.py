import numpy as np


class Simplex:
    def __init__(self, tableau, solve_type, variables):
        self.tableau = tableau
        self.solution = {}
        self.solution_set = []
        self.solve_type = solve_type
        self.logs = [[0, self.tableau.copy(), 0]]
        self.variables = variables
        self.solution_cols = []
        self.optima_idxs = []
        print(self.tableau)

    def solve_maxim_step(self, manual_col=-1):
        """
        Calculates a single step of the simplex method, and returns the tableau and other information to be saved in the
        logs.
        :returns: (whether the problem is solved, the logs of the step)
        """
        # Find the most negative entry in the objective function row, and it's index.
        most_negative = min(self.tableau[-1])

        # If there are multiple negative that are equal, just pick the first one.
        most_negative_index = np.where(self.tableau[-1] == np.amin(self.tableau[-1]))[0]
        if len(most_negative_index) > 1:
            most_negative_index = int(most_negative_index[0])
        else:
            most_negative_index = int(most_negative_index)

        # If we manually want to force a column to pivot around (if there are multiple optima), then we use the
        # column passed as an argument. Otherwise the most_negative_index is unchanged

        if manual_col >= 0:
            most_negative_index = manual_col

        # Find the ratios of the Solution column
        # Since we will be dividing by zero in some cases, I will turn off the warning message when this happens.
        np.seterr(divide='ignore', invalid='ignore')
        ratios = self.tableau[:, -1] / self.tableau[:, most_negative_index]

        # Make any zeros or negatives into infinities, so they are ignored (will never be the smallest value).
        ratios = [i if i > 0 else np.inf for i in ratios]
        smallest_ratio = np.nanmin(ratios)

        smallest_ratio_index = np.where(ratios == np.nanmin(ratios))[0]
        if len(smallest_ratio_index) > 1:
            smallest_ratio_index = int(smallest_ratio_index[0])
        else:
            smallest_ratio_index = int(smallest_ratio_index)

        # This gives us the pivot value as self.tableau[smallest_ratio_index][most_negative_index]
        pivot = self.tableau[smallest_ratio_index][most_negative_index].copy()
        for idx, row in enumerate(self.tableau):

            # If we are not in the pivot row and there isn't already a zero, we need to make a zero.

            if idx != smallest_ratio_index and row[most_negative_index] != 0:

                # Scale the pivot row so that the pivot number is 1.

                self.tableau[smallest_ratio_index] = (self.tableau[smallest_ratio_index] /
                                                      self.tableau[smallest_ratio_index][most_negative_index])

                # Multiply the pivot row by the absolute of the target value in the pivot column

                scaled_pivot = self.tableau[smallest_ratio_index] * np.abs(row[most_negative_index])

                # If the target value is negative, we add the scaled pivot row to make it positive and vice versa.

                if row[most_negative_index] < 0:
                    self.tableau[idx] = row + scaled_pivot
                elif row[most_negative_index] > 0:
                    self.tableau[idx] = row - scaled_pivot

        # Check if solved, by seeing if there are still negative values in the objective row.

        step = np.array([most_negative, most_negative_index, smallest_ratio, smallest_ratio_index, pivot])
        most_negative = min(self.tableau[-1])
        solved = False
        if most_negative >= 0:
            solved = True
        return solved, step

    def solve(self, print_solution=False):
        """
        Iterates through the Simplex method using the step function, and ends once a solved state is detected.
        Saves the logs each iteration to the Simplex.logs object.
        :returns: The solution for the x variables in a list of dictionaries (for multiple optima).
        """

        # If it is a minimisation problem then the dual is solved (transposition).

        solved = False
        idx = 1
        while not solved:
            solved, step = self.solve_maxim_step()
            self.logs.append([0, self.tableau.copy(), step])
            print(self.tableau)
        self.find_solution()
        if print_solution:
            print(self.solution_set)

        return self.solution_set

    def find_solution(self):
        """
        Calculates the solution(s) from the finished Tableau.
        :return: Whether a single solution or multiple optima were found
        """

        # Transposes the Tableau, to extract the columns, and iterates over them to find the solution columns.
        for idx, column in enumerate(np.transpose(self.tableau)):

            # If the column is an x variable

            if self.variables[idx][0] == 'x':

                # If the set of the absolute values in each column is just {1,0} and the sum  is 1, it is a solution
                # case, and add these values to the solution dictionary as a single solution.

                if set(abs(column)) == {1, 0} and np.sum(abs(column)) == 1:

                    self.solution_cols.append(idx)

                    if self.solve_type == 'min\n':

                        s_ = 's' + self.variables[idx][1:]
                        s_index = np.where(self.variables == s_)[0]
                        self.solution[self.variables[idx]] = np.transpose(self.tableau)[s_index[0]][-1]

                    else:
                        index = np.where(column == (1 or -1))
                        self.solution[self.variables[idx]] = self.tableau[index[0][0], -1]

                # In the case where it isn't a unit column, but the objective function row has a 0 (multiple optima)

                elif column[-1] == 0:
                    self.solution[self.variables[idx]] = 0
                    self.optima_idxs.append(idx)

                else:
                    self.solution[self.variables[idx]] = 0

        # The bottom right value is always the solution.
        self.solution['z'] = self.tableau[-1][-1]

        # Add the solution that is found to the set of solutions
        self.solution_set.append(self.solution.copy())

        # Find the solutions for the other optima (if any) using recursion

        for i in self.optima_idxs:
            if i not in self.solution_cols:
                solved, step = self.solve_maxim_step(i)
                self.optima_idxs.remove(i)
                self.find_solution()
                self.logs.append([1, self.tableau.copy(), step])
