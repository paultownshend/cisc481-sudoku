import sudoku
import sys


# PART 2
# takes a puzzle, and two variables
# removes any values from the xi's domain that don't have a corresponding
# value in xj's domain that satisfies the constraints of sudoku
# returns true if any domains were altered, false otherwise
def revise(s, xi, xj):
    revised = False

    for c in s.domains[xi]:
        if not any([s.constraint(c, y) for y in s.domains[xj]]):
            if xi not in s.pruned:
                s.pruned[xi] = [c]
            else:
                s.pruned[xi].append(c)
            s.domains[xi].remove(c)
            revised = True

    return revised


# PART 3
# AC-3 function
# revises the domains of each variable based on the constraints of sudoku
# returns false if there is a variable with no possible value, true otherwise
def ac3(s):

    queue = list(s.constraints)

    while queue:

        xi, xj = queue.pop(0)

        if revise(s, xi, xj):
            s.print_board()
            if len(s.domains[xi]) == 0:
                return False

            for xk in s.neighbors[xi]:
                if xk != xi:
                    queue.append([xk, xi])
    return True


# part 4
# Takes a sudoku and a set of assignments and iterates through all variables of the sudoku
# if a variable is not assigned, then it gets added to the unassigned dictionary, as well as
# the length of that variable's domain.
# Returns the variable with the most restricted domain
def min_rem_values(s, assignment):
    unassigned = {}
    for var in s.variables:
        if var not in assignment:
            unassigned[var] = len(s.domains[var])
    return min(unassigned, key=unassigned.get)


def order_domain(s, v):
    if len(s.domains[v]) == 1:
        return s.domains[v]

    return sorted(s.domains[v], key=lambda value: s.conflicts(s, v, value))


def backtracking_search(s):
    if ac3(s):
        if s.is_complete():
            return
        else:
            assignment = {}
            for v in s.variables:
                if len(s.domains[v]) == 1:
                    assignment[v] = s.domains[v][0]

            assignment = backtrack(s, assignment)

            for d in s.domains:
                if len(d) == 1:
                    s.domains[d] = assignment[d]


def backtrack(s, assignment):
    if len(s.variables) == len(assignment):
        return assignment

    v = min_rem_values(s, assignment)

    for x in order_domain(s, v):
        if s.is_consistent(assignment, v, x):
            s.assign(assignment, v, x)

            result = backtrack(s, assignment)

            if result:
                s.print_board()
                return result

            s.unassign(v, assignment)
    return False


puzzle1 = [[7, 0, 0, 4, 0, 0, 0, 8, 6],
           [0, 5, 1, 0, 8, 0, 4, 0, 0],
           [0, 4, 0, 3, 0, 7, 0, 9, 0],
           [3, 0, 9, 0, 0, 6, 1, 0, 0],
           [0, 0, 0, 0, 2, 0, 0, 0, 0],
           [0, 0, 4, 9, 0, 0, 7, 0, 8],
           [0, 8, 0, 1, 0, 2, 0, 6, 0],
           [0, 0, 6, 0, 5, 0, 9, 1, 0],
           [2, 1, 0, 0, 0, 3, 0, 0, 5]]
puzzle2 = [[1, 0, 0, 2, 0, 3, 8, 0, 0],
           [0, 8, 2, 0, 6, 0, 1, 0, 0],
           [7, 0, 0, 0, 0, 1, 6, 4, 0],
           [3, 0, 0, 0, 9, 5, 0, 2, 0],
           [0, 7, 0, 0, 0, 0, 0, 1, 0],
           [0, 9, 0, 3, 1, 0, 0, 0, 6],
           [0, 5, 3, 6, 0, 0, 0, 0, 1],
           [0, 0, 7, 0, 2, 0, 3, 9, 0],
           [0, 0, 4, 1, 0, 9, 0, 0, 5]]
puzzle3 = [[1, 0, 0, 8, 4, 0, 0, 5, 0],
           [5, 0, 0, 9, 0, 0, 8, 0, 3],
           [7, 0, 0, 0, 6, 0, 1, 0, 0],
           [0, 1, 0, 5, 0, 2, 0, 3, 0],
           [0, 7, 5, 0, 0, 0, 2, 6, 0],
           [0, 3, 0, 6, 0, 9, 0, 4, 0],
           [0, 0, 7, 0, 5, 0, 0, 0, 6],
           [4, 0, 1, 0, 0, 6, 0, 0, 7],
           [0, 6, 0, 0, 9, 4, 0, 0, 2]]
puzzle4 = [[0, 0, 0, 0, 9, 0, 0, 7, 5],
           [0, 0, 1, 2, 0, 0, 0, 0, 0],
           [0, 7, 0, 0, 0, 0, 1, 8, 0],
           [3, 0, 0, 6, 0, 0, 9, 0, 0],
           [1, 0, 0, 0, 5, 0, 0, 0, 4],
           [0, 0, 6, 0, 0, 2, 0, 0, 3],
           [0, 3, 2, 0, 0, 0, 0, 4, 0],
           [0, 0, 0, 0, 0, 6, 5, 0, 0],
           [7, 9, 0, 0, 1, 0, 0, 0, 0]]
puzzle5 = [[0, 0, 0, 0, 0, 6, 0, 8, 0],
           [3, 0, 0, 0, 0, 2, 7, 0, 0],
           [7, 0, 5, 1, 0, 0, 6, 0, 0],
           [0, 0, 9, 4, 0, 0, 0, 0, 0],
           [0, 8, 0, 0, 9, 0, 0, 2, 0],
           [0, 0, 0, 0, 0, 8, 3, 0, 0],
           [0, 0, 4, 0, 0, 7, 8, 0, 5],
           [0, 0, 2, 8, 0, 0, 0, 0, 6],
           [0, 5, 0, 9, 0, 0, 0, 0, 0]]

sudoku1 = sudoku.Sudoku(9, puzzle1)
sudoku2 = sudoku.Sudoku(9, puzzle2)
sudoku3 = sudoku.Sudoku(9, puzzle3)
sudoku4 = sudoku.Sudoku(9, puzzle4)
sudoku5 = sudoku.Sudoku(9, puzzle5)

sys.setrecursionlimit(5000)
#backtracking_search(sudoku1)
#backtracking_search(sudoku2)

#backtracking_search(sudoku3)
#backtracking_search(sudoku4)
backtracking_search(sudoku5)





