import numpy as np
import random
import time
from numba import njit, jit
import cProfile


@njit
def first_numerical_grid(rows, cols):
    grid = np.zeros(rows*cols)

    def blinker(grid):
        grid = grid.reshape(rows, cols)
        grid[rows//2 - 1: rows//2 + 2, cols//2-1: cols//2 + 2] = np.array([[0,1,0],[0,1,0],[0,1,0]])
        return grid

    def glider(grid):
        grid = grid.reshape(rows, cols)
        grid[rows // 2 - 1: rows // 2 + 2, cols // 2 - 1: cols // 2 + 2] = np.array([[1, 0, 0], [0, 1, 1], [1, 1, 0]])
        return grid

    def n_dots33(grid):
        grid = grid.reshape(rows, cols)
        grid[rows // 2 - 1: rows // 2 + 2, cols // 2 - 1: cols // 2 + 2] = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
        return grid

    def striped_grid(grid):
        """if resolution 600x600, creates checkerboard pattern for cell_size == 8 or 24"""
        for i in range(rows*cols):
            if i % 2 == 0:
                grid[i] = 1
        return grid.reshape(rows, cols)

    def single_line(grid):
        grid[:cols] = np.ones(cols)
        return grid.reshape(rows, cols)


    def random_grid(grid):
        for i in range(rows*cols):
            if random.random() <= 0.5:
                grid[i] = 1
        return grid.reshape(rows, cols)


    grid = random_grid(grid)
    return grid

def set_bc(grid):
    rows, cols = np.shape(grid)
    zeros_matrix = np.zeros([rows+2, cols+2])
    zeros_matrix[1:-1,1:-1] = grid
    return zeros_matrix

@njit()
def sum33(zeros_matrix, pos):
    # small_matrix = np.array([])
    cell_sum = 0
    for x in range(-1,2):
        for y in range(-1,2):
            neighbour = zeros_matrix[pos[0]+x, pos[1]+y]
            # small_matrix = np.append(small_matrix, alive)
            if neighbour == 1:
                cell_sum += 1
    # print(small_matrix.reshape(3,3), cell_sum)
    return cell_sum, zeros_matrix[pos[0],pos[1]]

@njit()
def rules(cell_sum, alive):
    def GameOfLife():
        if (alive and (cell_sum == 3 or cell_sum == 4)) or (not alive and (cell_sum == 3)):
            return 1
        else:
            return 0

    def negatives():
        # slow deterioration on random_grid()
        if alive and ((0 <= cell_sum <= 3) or cell_sum == 5):
            return 0
        elif not alive and ((0 <= cell_sum <= 3) or cell_sum == 5):
            return 1
        else:
            return 0

    def accumulation():
        if ((0 <= cell_sum <= 3) or cell_sum == 5):
            return 0
        elif ((6 <= cell_sum <= 9) or cell_sum == 4):
            return 1
        else:
            return 0

    return GameOfLife()

@jit
def main_function(grid, zeros_matrix):
    rows, cols = np.shape(grid)
    temp = np.zeros([rows,cols])
    for r in range(rows):
        for c in range(cols):
            # print()
            # cell_sum, alive = sum33(zeros_matrix, [r+1,c+1])
            # temp[r,c] = rules(cell_sum, alive)
            temp[r, c] = rules(sum33(zeros_matrix, [r+1,c+1])[0],sum33(zeros_matrix, [r+1,c+1])[1])

    return temp

if __name__ == "__main__":
    grid = first_numerical_grid(500,500)
    for i in range(10):
        zeros_grid = set_bc(grid)
        # print('\n',zeros_grid)
        t1 = time.time()
        grid = main_function(grid, zeros_grid)
        print(time.time() - t1)
        # print(cProfile.run('main_function(grid, zeros_grid)'))

