
# READ THE CODE FIRST! OR IT WILL OVERWRITE EVERYTHING!



import numpy as np
import numerical_grid as ng
import matplotlib.pyplot as plt
from matplotlib import cm
import time


cell_size = 100
rows = cell_size//1
cols = cell_size//1


grid = ng.first_numerical_grid(rows,cols)
# path = "continue.csv" # don't use on first try.
# grid = np.genfromtxt(path, delimiter=',', dtype=int).reshape(cell_size,cell_size)


for i in range(0,200):
    t1 = time.time()
    plt.clf()
    plt.imshow(grid,interpolation="gaussian", cmap=cm.hot)
    plt.tight_layout()
    plt.pause(0.01)
    # name of saved png file
    # plt.savefig('frame{0:04d}'.format(i))

    zeros_grid = ng.set_bc(grid)
    grid = ng.main_function(grid, zeros_grid)
    print(i, time.time()-t1)


# last_grid = "continue"
# grid.tofile('continue.csv', sep=',', format="%d") #saves the very next grid
