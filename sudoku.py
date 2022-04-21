import itertools


# code heavily modified from https://github.com/speix/sudoku-solver

# Main class to represent a sudoku puzzle
class Sudoku:

    def __init__(self, size, puzzle):
        self.variables = list()
        self.constraints = dict()
        self.domains = dict()
        self.puzzle = list()
        self.neighbors = dict()
        self.pruned = dict()
        self.size = size
        self.puzzle = puzzle

        self.make_vars()
        self.make_domains()
        if size == 4:
            self.get_constraints4x4()
        elif size == 9:
            self.get_constraints9x9()
        self.build_neighbors()

    # make variables with names of coordinates of cells
    def make_vars(self):
        row_char, col_char = '', ''
        i = 1
        j = 1
        while i <= self.size:
            row_char += str(i)
            col_char += str(i)
            i += 1
        self.variables = self.combine(row_char, col_char)

    # make the domains of each variable
    # if a cell is unassigned, then it's domain is 1 through self.size
    # if the cell is assigned, it's domain is the number it's assigned to
    def make_domains(self):
        i = 0
        c = 0
        while i < self.size:
            j = 0
            while j < self.size:
                if self.puzzle[i][j] == 0:
                    self.domains[self.variables[c]] = list(range(1, self.size + 1))
                else:
                    self.domains[self.variables[c]] = [self.puzzle[i][j]]
                j += 1
                c += 1
            i += 1

    # PART 1
    # builds the constraints for a 4x4 puzzle for the Sudoku rules
    def get_constraints4x4(self):
        if self.size == 4:

            row_char, col_char = '', ''

            i = 1
            j = 1
            while i <= self.size:
                row_char += str(i)
                col_char += str(i)
                i += 1
            blocks = ([self.combine(row_char, number) for number in col_char] +  # row constraints
                      [self.combine(character, col_char) for character in row_char] +  # col constraints
                      [self.combine(character, number) for character in ('12', '34')  # square constraints
                       for number in ('12', '34')])
            self.perm_constraints(blocks)

    def get_constraints9x9(self):
        if self.size == 9:
            row_char, col_char = '', ''

            i = 1
            j = 1
            while i <= self.size:
                row_char += str(i)
                col_char += str(i)
                i += 1
            blocks = ([self.combine(row_char, number) for number in col_char] +  # row constraints
                      [self.combine(character, col_char) for character in row_char] +  # col constraints
                      [self.combine(character, number) for character in ('123', '456', '789')  # square constraints
                       for number in ('123', '456', '789')])
            self.perm_constraints(blocks)

    def perm_constraints(self, blocks):
        for bl in blocks:
            perms = self.permutate(bl)

            for p in perms:
                if p not in self.constraints:
                    self.constraints[p] = list()
                    i = 0
                    while i < self.size:
                        j = 0
                        while j < self.size:
                            if i != j:
                                self.constraints[p].append([i + 1, j + 1])
                            j += 1
                        i += 1

    def build_neighbors(self):

        for x in self.variables:
            self.neighbors[x] = list()
            for c in self.constraints:
                if x == c[0]:
                    self.neighbors[x].append(c[1])

    def is_complete(self):
        for v in self.variables:
            if len(self.domains[v]) != 1:
                return False
        return True

    def is_consistent(self, assignment, var, val):
        for k in assignment:
            if assignment[k] == val and k in self.neighbors[var]:
                return False
        return True

    def assign(self, assignment, var, val):
        # print("assign")
        assignment[var] = val
        self.pruned[var] = self.domains[var]
        self.domains[var] = [val]

    def unassign(self, var, assignment):
        if var in assignment.keys():
            self.domains[var].append(self.pruned[var])
            self.pruned.pop(var)
            del assignment[var]

    def print_board(self):
        for v in self.variables:
            if len(self.domains[v]) == 1:
                print(self.domains[v][0], end=' ')
            elif len(self.domains[v]) > 1:
                print(0, end=' ')
            if v[1] == '9':
                print()
        print()

    @staticmethod
    def combine(i, j):
        return [a + b for a in i for b in j]

    @staticmethod
    def permutate(iterable):
        result = list()

        for L in range(0, len(iterable) + 1):
            if L == 2:
                for subset in itertools.permutations(iterable, L):
                    result.append(subset)

        return result

    @staticmethod
    def constraint(xi, xj):
        return xi != xj

    @staticmethod
    def conflicts(sudoku, var, val):
        c = 0
        for n in sudoku.neighbors[var]:
            if len(sudoku.domains[n]) > 1 and val in sudoku.domains[n]:
                c += 1

        return c
