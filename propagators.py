#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.  

'''This file will contain different constraint propagators to be used within 
   bt_search.

   propagator == a function with the following template
      propagator(csp, newVar=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newVar (newly instaniated variable) is an optional argument.
      if newVar is not None:
          then newVar is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method). 
      bt_search NEEDS to know this in order to correctly restore these 
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been 
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newVar = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated 
        constraints) 
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope 
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newVar = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no 
    propagation at all. Just check fully instantiated constraints'''
    
    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []


def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with only
    one uninstantiated variable. Remember to keep track of
    all pruned variable,value pairs and return '''

    # when after a new variable is assigned
    if newVar:
      constrains = csp.get_cons_with_var(newVar)
    else:
      constrains = csp.get_all_cons()

    # pruned to store all pruned variable,value pairs
    pruned = []

    # loops through all constrains
    for constrain in constrains:
      # finds a constrain that has only one uninstantiated
      # variable
      if constrain.get_n_unasgn() == 1:
        unasgn = constrain.get_unasgn_vars()[0]
        # safty check :)
        if unasgn.cur_domain_size() == 0:
              return False, []
        # vals will store all values of variables
        # of a possible assignment
        vals = []
        vars = constrain.get_scope()
        unasgnIndex = vars.index(unasgn)
        for var in vars:
          # sets all assigned variables' value in vals
          if unasgn != var:
            vals.append(var.get_assigned_value())
          else:
            vals.append(None)
        for d in unasgn.cur_domain():
          # sets a possible choice of value of unassigned variables
          # in vals
          vals[unasgnIndex] = d
          # current assignment violates the constrain
          if not constrain.check(vals):
            unasgn.prune_value(d)
            pruned.append((unasgn, d))
            if unasgn.cur_domain_size() == 0:
              return False, pruned
    return True, pruned


def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce 
    processing all constraints. Otherwise we do GAC enforce with
    constraints containing newVar on GAC Queue'''
    # when after a new variable is assigned
    if newVar:
      GACQueue = [] + csp.get_cons_with_var(newVar)
    else:
      GACQueue = [] + csp.get_all_cons()
    pruned = []
    # loops while GACQueue is not empty
    while GACQueue:
      # extract the head element of the queue
      constrain = GACQueue.pop(0)
      vars = constrain.get_scope()
      for var in vars:
        # safety check
        if var.cur_domain_size() == 0:
              return False, pruned
        for d in var.cur_domain():
          # checks if current value choice is consistent
          # in this constrain
          if not constrain.has_support(var,d):
            var.prune_value(d)
            pruned.append((var,d))
            if var.cur_domain_size() == 0:
              GACQueue = []
              return False, pruned
            else:
              # adds all constrain that contains the variable we currently
              # look at in to queue
              for c in csp.get_all_cons():
                if (not (c in GACQueue)) and (var in c.get_scope()):
                  GACQueue.append(c)
    return True, pruned
