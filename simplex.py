import numpy as np


class Simplex:
    def __init__(self, tableau, solve_type):
        self.tableau = tableau
        self.solve_type = solve_type
        self.logs = [[0, self.tableau.copy(), 0]]


    def solve_maxim_step(self):
        """
        Calculates a single step of the simplex method, and returns the tableau and other information to be saved in the
        logs.
        """
        # Find the most negative entry in the objective function row, and it's index.
        most_negative = min(self.tableau[-1])

        # If there are multiple negative that are equal, just pick the first one.
        most_negative_index = np.where(self.tableau[-1] == np.amin(self.tableau[-1]))[0]
        if len(most_negative_index) > 1:
            most_negative_index = int(most_negative_index[0])
        else:
            most_negative_index = int(most_negative_index)

        # Find the ratios of the Solution column
        # Since we will be dividing by zero in some cases, I will turn off the warning message when this happens.
        np.seterr(divide='ignore', invalid='ignore')
        ratios = self.tableau[:, -1] / self.tableau[:, most_negative_index]

        # Make any zeros or negatives into infinities, so they are ignored (will never be the smallest value).
        ratios = [i if i > 0 else np.inf for i in ratios]
        smallest_ratio = np.nanmin(ratios)

        smallest_ratio_index = int(np.where(ratios == np.nanmin(ratios))[0])

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

        step = np.array([most_negative,most_negative_index, smallest_ratio, smallest_ratio_index, pivot])
        most_negative = min(self.tableau[-1])
        solved = False
        if most_negative >= 0:
            solved = True

        return solved, step



    def solve_max(self):
        """
        Iterates through the Simplex method using the step function, and ends once a solved state is detected.
        Saves the logs each iteration to the Simplex.logs object.
        :returns: Logs containing the tableau
        """
        solved = False
        idx=1
        while not solved:
            print("Next iteration...")
            solved, step = self.solve_maxim_step()
            print(self.tableau)
            self.logs.append([idx, self.tableau.copy(), step])



        print("Successfully solved.")
