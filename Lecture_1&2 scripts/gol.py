import time
import numpy as np
import matplotlib.pyplot as plt
from numba import jit

@jit
def update_parent_grid(row, col, grid_l, maxN):
    # Take account of boundary effects
    row_u = max(0,row-1)  
    row_d = min(maxN-1,row+1)
    col_l = max(0,col-1)      
    col_r = min(maxN-1,col+1)

    #  Count neighbors
    neighbors = (grid_l[row_u, col_l] 
                + grid_l[row, col_l] 
                + grid_l[row_d, col_l] 
                + grid_l[row_u, col] 
                + grid_l[row_d, col] 
                + grid_l[row_u, col_r] 
                + grid_l[row, col_r] 
                + grid_l[row_d, col_r])

    return (grid_l[row,col] & (neighbors == 2)) | (neighbors == 3)




def gol_elementwise(N, num_generations, plot_flag = False):
    wallclocktime = 0
    grid    = np.random.choice([1, 0] , N*N, p=[0.2, 0.8]).reshape(N, N)
    grid_temp = np.zeros_like(grid)
    fig, ax = plt.subplots()
    update_parent_grid(0,0,grid,N)
    
    # Do the calculations:
    for i in range(num_generations):
        grid_temp = grid.copy()
        start = time.time()
        for row in range(N):
            for col in range(N):
                grid[row,col] =  update_parent_grid(row,col,grid_temp,N)
        wallclocktime = wallclocktime + (time.time() - start)
                
        if plot_flag:
            ax.imshow(grid)
            plt.pause(0.0001) #ability to look at the animation
    
    #return the timing measurement variable
    return wallclocktime


def gol_vectorized(N,numGenerations,plotflag = False):
    # Create the timing measurement variable
    wallclocktime = 0


    # declare a grid of NxN random values
    grid = np.random.choice([1, 0] , N*N, p=[0.2, 0.8]).reshape(N, N)
    
    # Create figure
    fig, ax = plt.subplots()
    
    # Create the helper variables
    p = np.r_[0, 0:N-1]  #[0 0 1 2 ... N-2]
    q = np.r_[1:N, N-1]  #[1 2 3 .. N-1, N-1]


    # Do the calculations:
    for i in range(numGenerations):
        start = time.time()
        neighbors = grid[:,p] + grid[:,q] + grid[p,:] +  grid[q,:]  + grid[p,:][:,p] + grid[q,:][:,q]  + grid[p,:][:,q]  + grid[q,:][:,p]
        grid = (grid & (neighbors == 2)) | (neighbors == 3)
        wallclocktime = wallclocktime + (time.time() - start)
        if plotflag:
            ax.imshow(grid)
            plt.pause(0.0001) #ability too look at the animation


    return wallclocktime

if __name__ == '__main__':  
    print(gol_elementwise(300,200,plot_flag = False))
    print(gol_vectorized(300,200,plotflag = False))