import numpy as np
import pandas as pd


# Read the line and put the coefficients into a dictionary

def line_to_dict(line, obj=False):
    """
    Parses through a line of the input and collects information about what the variables, coefficients and operators
    are.
    :param line: The input line, as a list of strings.
    :param obj: Whether the input line is the objective function or a constraint, as a bool.
    :return: A dictionary of the variable names to their values.
    """
    x_ = {}
    for idx, char in enumerate(line):
        try:
            # Determining the sign of the coefficient based on the previous character
            if line[idx - 1] == '-':
                sign = -1
            else:
                sign = 1

            # Finding the xs, and determining their coefficients
            if len(char) > 1:
                if char[-2] == 'x':
                    # No coefficient written, therefore coeff = 1.
                    if len(char) == 2:
                        coeff = 1
                    else:
                        coeff = float(char[0:-2])

                    x_[char[-2:]] = sign * coeff

            # Case if the objective function is not being encoded

            if not obj:
                if char == '=':
                    x_['sol'] = float(line[idx + 1])
                    x_['s'] = 0
                elif char == 'â‰¤':  # ASCII for less than or equal to
                    x_['sol'] = float(line[idx + 1])
                    x_['s'] = 1
                elif char == 'â‰¥':  # ASCII for greater than or equal to
                    x_['sol'] = float(line[idx + 1])
                    x_['s'] = -1
        except:
            exit("The input is not in the correct form. Refer to readme.txt to see how to set out the input txt.")
    return x_


# Reads the text file and returns a tableau

def read_txt(input_filename):
    """
    Reads a file input.txt in the current working directory and formats it into a tableau to be used in the solver.
    :return: The tableau, the problem type (maximum or minimum), and the variable names as a tuple.
    """
    with open(input_filename) as f:
        lines = f.readlines()
    # Converting the lines into a list
    solve = lines[0]
    lines = [lines[i].split() for i in range(len(lines))]
    obj_func = line_to_dict(lines[1], True)

    # Putting all the coefficient dictionaries together in a list
    coeffs_lists = [line_to_dict(s) for s in lines[2:]]

    # Finding the set of keys

    keys = set()
    for coeffs_list in coeffs_lists:
        keys.update(set(list(coeffs_list.keys())))
    keys = list(keys)

    # Counting the number of slack variables and indexing them correctly

    for idx, coeffs_list in enumerate(coeffs_lists):
        for key in keys:
            try:
                if key == 's':
                    slack = coeffs_list[key]
                    coeffs_list.pop(key)
                    test = key + str(idx + 1)
                    coeffs_list[test] = slack
            except:
                None
    keys = set()
    for coeffs_list in coeffs_lists:
        keys.update(set(list(coeffs_list.keys())))
    keys = list(keys)

    # Make all the dictionaries have the same coefficients by checking lengths, and matching the smaller ones with the
    # bigger ones by filling the missing xs with 0s.

    for idx, coeffs_list in enumerate(coeffs_lists):
        coeffs_list['z'] = 0
        for key in keys:
            try:
                coeffs_list[key]
            except:
                coeffs_list[key] = 0

    # Calculates the number of xs and slack/surplus variables and constructs a list of the strings of each.
    num_xs = sum([1 if i[0] == 'x' else 0 for i in keys])
    num_ss = sum([1 if i[0] == 's' else 0 for i in keys]) - 1  # The solution variable also starts with 's', so -1.

    x_strings = ['x' + str(i + 1) for i in range(num_xs)]
    s_strings = ['s' + str(i + 1) for i in range(num_ss)]

    if solve == 'max\n':
        # Constructs the tableau with the variables that make up the problem, and copies the top row (for use later).
        tableau = np.array([x_strings + s_strings + ['z', 'sol']] * len(coeffs_lists), dtype='object')
        top_row = tableau[0].copy()

        # Fills the tableau frame with the values that were parsed in the previous function.
        for idx, i in enumerate(tableau):
            for jdx, j in enumerate(i):
                tableau[idx][jdx] = coeffs_lists[idx][j]

        # Adds the objective function to the bottom of the tableau.
        obj_xs = [0] * len(x_strings)
        for idx, x in enumerate(x_strings):
            try:
                obj_xs[idx] = -1 * obj_func[x]
            except:
                obj_xs[idx] = 0
        obj_row = obj_xs + [0] * len(s_strings) + [1, 0]
        tableau = np.append(tableau, [obj_row], axis=0).astype(float)
    elif solve == 'min\n':

        # Constructs the tableau with the variables that make up the problem, and copies the top row (for use later).

        dual_x_strings = ['x' + str(i + 1) for i in range(num_xs)]
        y_strings = ['y' + str(i + 1) for i in range(num_ss - num_xs)]
        tableau = np.array([x_strings + s_strings + ['z', 'sol']] * len(coeffs_lists), dtype='object')

        top_row = np.array([y_strings + dual_x_strings + ['z', 'sol']])[0]
        # Fills the tableau frame with the values that were parsed in the previous function.

        for idx, i in enumerate(tableau):
            for jdx, j in enumerate(i):
                print(coeffs_lists[idx], j)
                tableau[idx][jdx] = coeffs_lists[idx][j]

        # detect the non-negativity rows
        nn_idx = []
        nn_row = []
        for idx, row in enumerate(tableau):
            if set(abs(row)) == {1, 0} and np.sum(abs(row)) == 2:
                nn_idx.append(idx)
                nn_row.append(row)

        nn_row = np.array(nn_row)
        tableau = np.delete(tableau, nn_idx, 0)

        # Adds the objective function to the bottom of the tableau.
        obj_xs = [0] * len(x_strings)
        for idx, x in enumerate(x_strings):
            try:
                obj_xs[idx] = obj_func[x]
            except:
                obj_xs[idx] = 0
        obj_row = obj_xs + [0] * len(s_strings) + [1, 0]

        tableau = np.append(tableau, [obj_row], axis=0).astype(float)
        tableau = tableau.transpose()
        for idx,column in enumerate(tableau.transpose()):
            if sum(column[num_xs:-1]) < 0:
                tableau[-1,idx] = tableau[-1,idx] * -1

        # add nn rows into the columns
        for row in nn_row:
            tableau = np.insert(tableau, -1, row.transpose(), 1)


    else:
        exit(
            "The problem type (max or min) was not specified clearly. Please refer to readme.txt for the correct "
            "format.")

    print(tableau)
    return tableau, solve, top_row


def save_logs(logs, top_row, solution_set, solve_type, output_filename='output.txt'):
    """
    Saves the logs and solution into the output file (with steps).
    :param top_row: The names of the variables for the top row of the tableau.
    :param solution: The dictionary of the solution.
    :param logs: The logs from the tableau solution.
    :param filename: The file that the logs will be saved to.
    """
    print("=========================")
    logs = np.array(logs, dtype=object)
    idxs, tableau, step = logs[:, 0], logs[:, 1], logs[1:, 2]

    step = np.array(step.tolist())
    most_negative, most_negative_index, smallest_ratio, smallest_ratio_index, pivot = [step[:, i] for i in range(5)]
    initial_message = ''
    if solve_type == 'min\n':
        num_xs = sum([1 if i[0] == 'x' else 0 for i in top_row])
        num_ys = sum([1 if i[0] == 'y' else 0 for i in top_row])
        x_strings = ['x' + str(i + 1) for i in range(num_xs)]
        y_strings = ['y' + str(i + 1) for i in range(num_ys)]
        top_row = y_strings + x_strings + ['sol']
        initial_message += ('The goal is to minimise the objective function. To use the simplex method, the dual'
                            ' must be calculated.\nAfter transposing and inserting values, ')
    initial_message += "The initial Tableau was encoded as:\n\n"
    rows = ['Equation ' + str(i + 1) for i in range(len(tableau[0]) - 1)] + ['Objective Function']

    df = pd.DataFrame(data=tableau[0], columns=top_row, index=rows).to_string()

    message = initial_message + df + '\n\n\n'
    for i in range(len(idxs) - 1):
        if idxs[i + 1] == 0:
            s1 = (f"The most negative value in the objective function row is %f, making column %i the pivot column. "
                  f"\nAfter dividing the solution column by each corresponding value in the pivot column, the smallest "
                  f"non-zero value \nwas %f, making row %i the pivot row. "
                  f"\nThe pivot is therefore %f at [%i, %i]. After making the pivot column a unit vector, the resulting"
                  f" tableau is:\n\n" % (
                      most_negative[i], most_negative_index[i] + 1, smallest_ratio[i], smallest_ratio_index[i] + 1,
                      pivot[i], most_negative_index[i] + 1, smallest_ratio_index[i] + 1))
            t = pd.DataFrame(data=tableau[i + 1], columns=top_row, index=rows).to_string()
            try:
                if idxs[i + 2] == 0:
                    s2 = "\n\nSince there are still negative values in the objective function row, another step is " \
                         "required.\n"
                else:
                    s2 = "\n\nThere are no negative values in the objective function row, making the solution:\n"
            except:
                s2 = "\n\nThere are no negative values in the objective function row, making the solution:\n"
            message += s1 + t + s2

    solution_counter = 1
    message += str(solution_set[0])

    if len(solution_set) > 1:
        s1 = "\n\nHowever, multiple solutions were found, since there are zeros under non unit x columns.\n"  #

        for i in range(len(idxs - 1)):
            if idxs[i] == 1:
                s2 = (
                        f"\nColumn %i is the next pivot column, since there is a 0 in the objective function row. "
                        f"\nAfter dividing the solution column by each corresponding value in the pivot column, "
                        f"the smallest "
                        f"non-zero value \nwas %f, making row %i the pivot row. "
                        f"\nThe pivot is therefore %f at [%i, %i]. After making the pivot column a unit vector, "
                        f"the resulting "
                        f" tableau is:\n\n" % (
                            most_negative_index[i - 1] + 1, smallest_ratio[i - 1],
                            smallest_ratio_index[i - 1] + 1,
                            pivot[i - 1], most_negative_index[i - 1] + 1, smallest_ratio_index[i - 1] + 1))

                t = pd.DataFrame(data=tableau[i], columns=top_row, index=rows).to_string()
                message += s1 + s2 + t
                message += "\n\nAnd therefore the corresponding solution can be read off the tableau as:\n"
                message += str(solution_set[solution_counter])
                solution_counter += 1

        # Turning the solution set into a general form.

        # Concatenate the solutions with coefficients.
        general_solution = [str(idx + 1) + str(np.array(list(sol.values()))) for idx, sol in enumerate(solution_set)]

        # Name the coefficients
        general_solution = ['a' + string + ' + ' if idx < len(solution_set) - 1 else 'a' + string for idx, string in
                            enumerate(general_solution)]

        # Turn the list of solutions with coefficients into a string
        str_general_solution = ''.join(general_solution)

        # Including the limits on the coefficients
        range_as = ' + '.join(['a' + str(i) for i in range(1, str_general_solution.count('a') + 1)])

        # Turning the limits into a string
        range_as = ('where %s = 1 ' % range_as)

        message += ('\n\nFinally, the general solution is:\n\n%s\n%s' % (str_general_solution, range_as))

    with open(output_filename, "w") as text_file:
        text_file.write(message)
    print("logs saved to " + output_filename)
