
# PART 2
# takes a puzzle, and two variables
# removes any values from the xi's domain that don't have a corresponding
# value in xj's domain that satisfies the constraints of sudoku
# returns true if any domains were altered, false otherwise
def revise(sudoku, xi, xj):
    revised = False

    for c in sudoku.domains[xi]:
        if not any([sudoku.constraint(c, y) for y in sudoku.domains[xj]]):
            if xi not in sudoku.pruned:
                sudoku.pruned[xi] = [c]
            else:
                sudoku.pruned[xi].append(c)
            sudoku.domains[xi].remove(c)
            revised = True

    return revised


# PART 3
# AC-3 function
# revises the domains of each variable based on the constraints of sudoku
# returns false if there is a variable with no possible value, true otherwise
def ac3(sudoku):

    queue = list(sudoku.constraints)

    while queue:

        xi, xj = queue.pop(0)

        if revise(sudoku, xi, xj):
            sudoku.print_board()
            if len(sudoku.domains[xi]) == 0:
                return False

            for xk in sudoku.neighbors[xi]:
                if xk != xi:
                    queue.append([xk, xi])
    return True


# part 4
# Takes a sudoku and a set of assignments and iterates through all variables of the sudoku
# if a variable is not assigned, then it gets added to the unassigned dictionary, as well as
# the length of that variable's domain.
# Returns the variable with the most restricted domain
def min_rem_values(sudoku, assignment):
    unassigned = {}
    for var in sudoku.variables:
        if var not in assignment:
            unassigned[var] = len(sudoku.domains[var])
    return min(unassigned, key=unassigned.get)


def order_domain(sudoku, v):
    if len(sudoku.domains[v]) == 1:
        return sudoku.domains[v]

    return sorted(sudoku.domains[v], key=lambda value: sudoku.conflicts(sudoku, v, value))


def backtracking_search(sudoku):

    assignment = {}
    for v in sudoku.variables:
        if len(sudoku.domains[v]) == 1:
            assignment[v] = sudoku.domains[v][0]
    if ac3(sudoku):
        return backtrack(sudoku, assignment)
    else:
        return "No Solution"


def backtrack(sudoku, assignment):
    if sudoku.is_complete():
        return assignment

    v = min_rem_values(sudoku, assignment)

    for x in order_domain(sudoku, v):
        if sudoku.is_consistent(assignment, v, x):
            sudoku.assign(assignment, v, x)
            sudoku.print_board(assignment)
            result = backtrack(sudoku, assignment)

            if result:
                return result
        if len(sudoku.domains[v]) == 0:
            sudoku.unassign(v, assignment)

    return False
