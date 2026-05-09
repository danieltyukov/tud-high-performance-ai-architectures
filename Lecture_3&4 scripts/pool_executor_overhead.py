# Example script to show the data copy overhead when using multiprocessing

from concurrent.futures import ProcessPoolExecutor
import numpy as np
import time

# naive and efficient multiprocessing


def naive_multiproc(N):
    """Naive multiprocessing

    Create all data inside the main process and copy pieces of the data
    to every child process.
    """

    x = np.linspace(1, N, N)
    out = np.zeros(shape=(N, N))

    tic = time.time()
    with ProcessPoolExecutor() as ex:
        # copies a row to every child process (N*[x] creates a list containing N copies of the array x)
        out = ex.map(naive_function, N*[x])
        # converts iterable to list and then to 2D NumPy array
        out = np.array(list(out))
    toc = time.time() - tic
    return toc


def naive_function(x):
    out = np.zeros((len(x), 1))
    # toy function
    for idx in range(len(x)):
        for t in range(100):
            out[idx] = x[idx]*x[idx]
    return out


def efficient_multiproc(N):
    """Efficient multiprocessing

    Create the data locally (within a child process) and send it back to the main process.
    """

    out = np.zeros((N, N))
    tic = time.time()
    with ProcessPoolExecutor() as ex:
        out = ex.map(efficient_function, N*[N])
        out = np.array(list(out))
    toc = time.time() - tic
    return toc


def efficient_function(N):
    # toy function that creates the data (rows) locally
    x = np.linspace(1, N, N)
    out = np.zeros(N)
    for idx in range(len(x)):
        for t in range(100):
            out[idx] = x[idx]*x[idx]
    return out


if __name__ == "__main__":
    N = 2000
    print("N:" + str(N))
    print("Naive way takes: {:.3f} sec.".format((naive_multiproc(N))))
    print("Efficient way takes: {:.3f} sec.".format(efficient_multiproc(N)))
