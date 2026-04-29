import numpy as np
import matplotlib.pyplot as plt
import time
from numba import jit
import os


def plot_md(w, x_lim, y_lim):
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1], frameon=False, aspect=1)
    ax.imshow(w, extent=[x_lim[0], x_lim[1], y_lim[0], y_lim[1]])
    ax.set_xticks([])
    ax.set_yticks([])
    plt.show()


def sequential(N, MAX_ITER, x_lim, y_lim, plot_flag=False):
    x = np.linspace(x_lim[0], x_lim[1], N).reshape((1, N))  # creating x coordinates
    y = np.linspace(y_lim[0], y_lim[1], N).reshape((N, 1))  # creating y coordinates
    c = x + 1j * y  # z_0 array of equation 1
    z = np.zeros((N, N), dtype=np.complex128)  # z_k array of equation 1
    w = np.zeros(z.shape)  # output array used for plotting


    start = time.time()
    # The calculation
    for i in range(N):
        for j in range(N):
            w[j, i] = do_calc(MAX_ITER, z[j, i], c[j, i])  # calculate whether a complex point is part of the Mandelbrot set element by element.
    exec_time = time.time() - start

    # Plot the Output
    if (plot_flag):
        plot_md(w.reshape(N, N), x_lim, y_lim)  # calling plotting function.

    return exec_time

# @jit
def do_calc(k, z, c):
    for i in range(k):
        z = z * z + c
        if abs(z) > 2:  # Mandelbrot set condition
            return i  # value is not part of Mandelbrot, return the iteration at which it exceeds 2.
    return 0  # value is part of Mandelbrot set


def vectorized(N, MAX_ITER, x_lim, y_lim, plot_flag=False):    
    x = np.linspace(x_lim[0], x_lim[1], N).reshape((1,N)) # creating x coordinates
    y = np.linspace(y_lim[0], y_lim[1], N).reshape((N,1)) # creating y coordinates
    c = x+1j*y # z_0 array of equation 1
    z = np.zeros((N, N),dtype=np.complex128) # z_k array of equation 1
    w = np.zeros(z.shape) # output array used for plotting

    start = time.time()
    w = do_calc_vec(MAX_ITER, z, c, w) #  calculatingwhether a complex point is part of the Mandelbrot set in a vectorized way.
    exec_time = time.time() - start


# Plot the Output
    if(plot_flag):
        plot_md(w.reshape(N,N), x_lim, y_lim) # calling plotting function.

    return exec_time

def do_calc_vec(MAX_ITER, z, c, out): # Works with flat or 2d array
    for i in range(MAX_ITER):
        mask = np.abs(z) <= 2 # find coordinates that have not violated the Mandelbrot set condition (yet)
        z = mask*(z*z + c)
        out = np.where(~mask & (out == 0), i, out) # update the output array
    return out



if __name__ == '__main__':
    # default parameters
    k = 50
    N = 2000
    x_lim = [-1.4, 0.6]
    y_lim = [-1, 1]
    print(sequential(N, k, x_lim, y_lim, False))
    print(vectorized(N, k, x_lim, y_lim, False))
