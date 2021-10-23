import numpy as np


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
                        coeff = int(char[0:-2])

                    x_[char[-2:]] = sign * coeff

            # Case if the objective function is not being encoded

            if not obj:
                if char == '=':
                    x_['sol'] = int(line[idx + 1])
                    x_['s'] = 0
                elif char == 'â‰¤':  # ASCII for less than or equal to
                    x_['sol'] = int(line[idx + 1])
                    x_['s'] = 1
                elif char == 'â‰¥':  # ASCII for greater than or equal to
                    x_['sol'] = int(line[idx + 1])
                    x_['s'] = -1
        except:
            exit("The input is not in the correct form. Refer to readme.txt to see how to set out the input txt.")
    return x_


# Reads the text file and returns a tableau

def read_txt():
    """
    Reads a file input.txt in the current working directory and formats it into a tableau to be used in the solver.
    :return: The tableau and the problem type (maximum or minimum) as a tuple.
    """
    with open('input.txt') as f:
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

    num_xs = sum([1 if i[0] == 'x' else 0 for i in keys])
    num_ss = sum([1 if i[0] == 's' else 0 for i in keys]) - 1

    x_strings = ['x' + str(i + 1) for i in range(num_xs)]
    s_strings = ['s' + str(i + 1) for i in range(num_ss)]

    tableau = np.array([x_strings + s_strings + ['z', 'sol']] * len(coeffs_lists))

    for idx, i in enumerate(tableau):
        for jdx, j in enumerate(i):
            tableau[idx][jdx] = int(coeffs_lists[idx][j])

    obj_xs = [-1 * obj_func[i] for i in x_strings]
    obj_row = obj_xs + [0] * len(s_strings) + [1, 0]
    tableau = np.append(tableau, [obj_row], axis=0).astype(float)
    return tableau, solve


def save_log(logs, init_tableau, filename='output.txt'):
    """

    :param init_tableau:
    :param logs:
    :param filename:
    """
    print("=========================")
    logs = np.array(logs, dtype=object)
    idxs, tableau, step = logs[:, 0], logs[:, 1], logs[1:, 2]

    step = np.array(step.tolist())
    most_negative, most_negative_index, smallest_ratio, smallest_ratio_index, pivot = [step[:, i] for i in range(5)]

    initial_message = "The initial Tableau was encoded as:\n"
    message = initial_message + np.array_str(tableau[0])
    for i in range(len(idxs)-1):
        s1 = (f"The most negative value in the objective function row is %f. Dividing the solution column by each entry\
              and finding the smallest non-zero value as %f " % (most_negative[i], smallest_ratio[i]))

    print(s1)



    with open(filename, "w") as text_file:
        text_file.write(message)
