#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.  

'''
Construct and return Tenner Grid CSP models.
'''

from cspbase import *
import itertools
import numpy as np

def sum_69?(*nums):
    '''Determines if the sum of input values are
    69.
    '''
    np_nums=np.array(nums)
    return (np.sum(np_nums) == 69)

def sum_138?(*nums):
    '''Determines if the sum of input values are
    138.
    '''
    np_nums=np.array(nums)
    return (np.sum(np_nums) == 138) 

def n-diff(*nums):
    '''Determines if each number in input is different from
    each other.
    '''
    return np.unique(nums).size == len(nums)


def initialization(initial_matrix):
    '''Sets all variables with their domain and
    returns the variable_array and all_vars where variable_array[i][j]
    is the Variable for the slot on ith row and jth column
    on the grid and all_vars is simply a list of all variables.
    '''
    # stores the input of the first n rows of the grid
    n_grid = initial_matrix
    # stores all values that has already been assigned in each
    # row in the input tenner grid
    fixed = []
    # stored all variables
    all_vars = []
    # stored the grid of variables
    vars_grid = []
    # overall domain for each cell
    dom_for_all = []

    # sets overall domain
    for j in range(1,34):
      dom_for_all.append(j)
    dom_for_all.remove(9)

    # sets all values that has already been assigned in each
    # row in the input tenner grid
    for i in range(len(n_grid)):
      for j in range(len(n_grid[i])):
        # Such a cell has already been pre-assigned.
        if n_grid[i][j] != -1:
          fixed.append(n_grid[i][j])

    # starts to sets the variable
    for i in range(len(n_grid)):
      vars_grid.append([])
      for j in range(len(n_grid[i])):
        # Such a cell has already been pre-assigned.
        if n_grid[i][j] != -1:
          # sets the domain to this variable to the value of
          # it
          var = Variable("Grid {} {}".format(i,j),[n_grid[i][j]])
        else:
          dom_cur = [] + dom_for_all
          # deletes the value of already assigned variables in same row
          # from domain
          for value in fixed:
            if value in dom_cur:
                dom_cur.remove(value)
          var = Variable("Grid {} {}".format(i,j),dom_cur)
        vars_grid[i].append(var)
        all_vars.append(var)

    return vars_grid, all_vars

def add_binary_ndiff_constrains(all_vars):
    '''Returns a list of binary constrains that describes the
    n different constrains
    '''
    constrains = []
    # sets binary constrains that every pairs of variables
    # in a row has different value
    for i in range(len(all_vars)-1):
      for j in range(i+1, len(all_vars)):
          constrain = Constraint(
            "C_diff",
            (all_vars[i],all_vars[j]))
          constrain.add_sat_func(lambda x,y:x!=y)
          constrains.append(constrain)

def add_n_ary_ndiff_constrains(all_vars):
    '''Returns a list of binary constrains that describes the
    n different constrains
    '''
    constrains = []
    # sets binary constrains that every pairs of variables
    # in a row has different value
    constrain = Constraint(
        "C_diff",
        all_vars)
    constrain.add_sat_func(lambda x,y:x!=y)
    constrains.append(constrain)

def add_sum_constrains(vars_grid):
    '''Returns a list of n-ary constrains that describes the Yang Hui
    magic concentric circle sum sum rule.
    '''
    #  sets n-ary constrains that every row's sum is 69
    constrains = []
    for i in range(vars_grid):
        constrain = Constraint(
          "row_sum %d".format(i+1),
          vars_grid[i])
        constrain.add_sat_func(sum_69?)
        constrains.append(constrain)

    # gets the transpose of vars_grid
    vars_grid_transpose = zip(*vars_grid)
    # sets n-ary constrains that every column's sum is 138
    for i in range(len(vars_grid_transpose)):
        constrain = Constraint(
          "column_sum %d".format(i+1),
          vars_grid_transpose[i])
        constrain.add_sat_func(sum_138?)
        constrains.append(constrain)
    return constrains



def magic_circle_model_1(initial_matrix):
    '''Return a CSP object representing a magic circle CSP problem along 
       with an array of variables for the problem. That is return

       magic_csp, variable_array

       where magic_csp is a csp representing magic concentric circle
       using model_1 and variable_array is a 8*4 matrix 

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]
       This function implements the model that using binary constrains
       for n-differnet.
    '''

    # initializes the variables
    vars_grid, all_vars = initialization(initial_tenner_board)
    constrains = add_binary_ndiff_constrains(all_vars)
    constrains += add_sum_constrains(vars_grid)

    csp = CSP("{}-Grid".format(len(vars_grid)),all_vars)
    for constrain in constrains:
        csp.add_constraint(constrain)

    return csp, vars_grid

def magic_circle_model_2(initial_matrix):
    '''Return a CSP object representing a magic circle CSP problem along 
       with an array of variables for the problem. That is return

       magic_csp, variable_array

       where magic_csp is a csp representing magic concentric circle
       using model_2 and variable_array is a 8*4 matrix 

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]
       This function implements the model that using n-ary constrains
       for n-differnet.
    '''

    # initializes the variables
    vars_grid, all_vars = initialization(initial_tenner_board)
    constrains = add_n_ary_ndiff_constrains(all_vars)
    constrains += add_sum_constrains(vars_grid)

    csp = CSP("{}-Grid".format(len(vars_grid)),all_vars)
    for constrain in constrains:
        csp.add_constraint(constrain)

    return csp, vars_grid