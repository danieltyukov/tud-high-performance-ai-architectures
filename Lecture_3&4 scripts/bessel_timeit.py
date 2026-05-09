# Bessel function profiled only as a whole (outer) via the timeit() function
# Using timeit() for both whole and kernel-only profiling is difficult

from timeit import timeit
import numpy as np
from scipy.special import jn
import matplotlib.pyplot as plt


def time_bessel_outer(nfunc):
    x = np.linspace(0, 20,100000)
    
    for n in range (nfunc):
        y = jn(n,x) # Bessel call
        plt.plot(x,y,label=r'$J_%s(x)$'%n);

    plt.axhline(0,color='black', label='_nolegend_')
    plt.grid()
    plt.legend()
    plt.xlabel('$x$')
    plt.ylabel('$J_n(x)$')
    plt.title( r'Bessel functions $J_n(x)$')
    plt.show()
    
def time_bessel_outer2():
    nfunc = 4
    x = np.linspace(0, 20,100000)
    
    for n in range (nfunc):
        y = jn(n,x) # Bessel call
        plt.plot(x,y,label=r'$J_%s(x)$'%n);

    plt.axhline(0,color='black', label='_nolegend_')
    plt.grid()
    plt.legend()
    plt.xlabel('$x$')
    plt.ylabel('$J_n(x)$')
    plt.title( r'Bessel functions $J_n(x)$')
    plt.show()


if __name__ == "__main__":
    # invoke timeit with function arguments
    nf = 4 # argument for profiled function
    iterations = 10
    minTime = timeit(lambda: time_bessel_outer(nf), number = iterations) # use lamda func for passing arg(s)
    print(f'Minimum time: {minTime/iterations: .03f} sec.')
    
    # #invoke timeit without function arguments
    # iterations = 10
    # libs = "from __main__ import time_bessel_outer2"
    # code = "time_bessel_outer2()"
    # minTime = timeit(setup = libs, stmt=code, number = iterations) # use lamda func for passing arg(s)
    # print(f'Minimum time (v2): {minTime/iterations: .03f} sec.')
