import sudoku
import backtracking_search

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

sudoku1 = sudoku.Sudoku(9, puzzle1)
sudoku2 = sudoku.Sudoku(9, puzzle2)
sudoku3 = sudoku.Sudoku(9, puzzle3)

backtracking_search.backtracking_search(sudoku3)
sudoku3.print_board()

