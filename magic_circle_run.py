from magic_csp import *
from propagators import *
import ast, sys

# the inputs are for yanghui magic circle, we provide one compelete case and 4
# incomplete cases for test. The 4 incomplete cases are in different difficulty
# levels, the more incomplete numbers to fill, the harder the puzzle is.
complete = ([28, 5, 11, 25],
        [27, 15, 3, 24],
        [6, 32, 29, 2],
        [8, 17, 26, 18],
        [12, 31, 19, 7],
        [20, 16, 23, 10],
        [4, 21, 14, 30],
        [33, 1, 13, 22])

incomplete_8 = ([-1, 5, 11, 25],
        [8, -1, 26, 18],
        [27, 15, -1, 24],
        [6, -1, 29, 2],
        [12, 31, 19, 7],
        [4, -1, 14, 30],
        [20, 16, -1, 10],
        [-1, 1, 13, -1])

incomplete_12 = ([-1, 5, 11, 25],
        [27, -1, -1, 24],
        [6, -1, 29, -1],
        [8, -1, 26, -1],
        [12, 31, -1, 7],
        [-1, 21, 14, 30],
        [20, -1, -1, 10],
        [-1, 1, 13, 22])

incomplete_16 = ([-1, -1, -1, 25],
        [6, -1, -1, 2],
        [8, -1, -1, 18],
        [-1, 31, 19, 7],
        [-1, -1, 14, -1],
        [27, 15, 3, -1],
        [-1, 16, -1, 10],
        [-1, -1, 13, 22])

incomplete_22 = ([-1, -1, 11, -1],
        [33, -1, -1, -1],
        [27, -1, -1, -1],
        [-1, -1, -1, 2],
        [8, -1, -1, 18],
        [-1, -1, -1, -1],
        [4, -1, -1, 30],
        [20, -1, -1, 10])




# change the following, these are from A2
def print_tenner_soln(var_array):
    for row in var_array:
        print([var.get_assigned_value() for var in row])

if __name__ == "__main__":

    for b in [b1, b2]:
        print("Solving board:")

        print("Using Model 1")
        csp, var_array = tenner_csp_model_1(b)
        solver = BT(csp)
        print("=======================================================")
        print("FC")
        solver.bt_search(prop_FC)
        print("Solution")
        print_tenner_soln(var_array)

        print("Using Model 2")
        csp, var_array = tenner_csp_model_2(b)
        solver = BT(csp)
        print("=======================================================")
        print("GAC")
        solver.bt_search(prop_GAC)
        print("Solution")
        print_tenner_soln(var_array)
