#https://carpentries-incubator.github.io/lesson-gpu-programming/02-cupy/index.html
#
#

from time import process_time
from cupy.random import default_rng
import cupy as cp
import numpy as np
import matplotlib.pyplot as plt


def precision_error():
    inp = cp.linspace(10000, 10000000, 100)
    computation_diff = cp.linspace(10000, 10000000, 100)
    n = len(inp)
    time_data_setup_GPU = cp.zeros((n, 2))
    time_computation_GPU = cp.zeros((n, 2))

    for i in range(n):
        #print("Creating a %d-by-%d matrix for single point precision data on the GPU" % (inp[i], inp[i]))
        A, time_data_setup_GPU[i, 0] = create_data_GPU(int(inp[i]), cp.float32)
        tic = process_time()
        x1 = formula(A)
        time_computation_GPU[i, 0] = process_time() - tic
        #print("Took: %f seconds to set up and %f seconds to compute" % (time_data_setup_GPU[i,0], time_computation_GPU[i,0]))

        #print("Creating a %d-by-%d matrix for double point precision data on the GPU" % (inp[i], inp[i]))
        A, time_data_setup_GPU[i, 1] = create_data_GPU(int(inp[i]), cp.float64)
        tic = process_time()
        x2 = formula(A)
        time_computation_GPU[i, 1] = process_time() - tic
        #print("Took: %f seconds to set up and %f seconds to compute" % (time_data_setup_GPU[i,1], time_computation_GPU[i,1]))

        computation_diff[i] = cp.sum(x1 - x2)/len(x1)
        #print(f"{i}: {computation_diff[i]:.3}")

    plt.plot(inp.get(), (time_computation_GPU[:, 1] - time_computation_GPU[:, 0]).get(), color='r', label='Time difference')
    plt.plot(inp.get(), time_computation_GPU[:, 1].get(), color='g', label='DFP time')
    plt.plot(inp.get(), time_computation_GPU[:, 0].get(), color='b', label='SFP time')
    plt.title('Execution-time difference between SFP and DFP operations')
    plt.legend()
    plt.xlabel("Input size [-]")
    plt.ylabel("Time [s]")
    plt.grid()

    plt.figure()
    plt.plot(inp.get(), computation_diff.get(), color='r', label='Precision error')
    plt.title('Precision error between SFP and DFP precision')
    plt.legend()
    plt.xlabel("Input size [-]")
    plt.ylabel("Error [s]")
    plt.grid()

    # function to show the plot
    plt.show()


def formula(x):
    #return x**3 + 3*x**2 + 3
    return cp.sqrt(cp.power((x**3 + 3*x**2 + 3),20))


def create_data_GPU(N, p):
    tic = process_time()
    A = default_rng().random(size=(N, 1), dtype=p)
    toc = process_time() - tic
    return A, toc


if __name__ == "__main__":
    precision_error()
