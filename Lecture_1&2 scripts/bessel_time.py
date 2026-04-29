# Bessel function profiled both as a whole (outer) and kernel-only (inner) via the time() function

from time import time
import numpy as np
from scipy.special import jn
import matplotlib.pyplot as plt


if __name__ == "__main__":
    nfunc = 4
    x = np.linspace(0, 20,100000)
    minTime = float('inf'); # set to sth very high
    
    tic1 = time() # overall snapshot    
    for n in range (nfunc):
        tic2 = time() # function snapshot
        y = jn(n,x) # Bessel call
        plt.plot(x,y,label=r'$J_%s(x)$'%n)
        toc2 = time() - tic2 # function snapshot
        minTime = min(toc2, minTime)

    plt.axhline(0,color='black', label='_nolegend_')
    plt.grid()
    plt.legend()
    plt.xlabel('$x$')
    plt.ylabel('$J_n(x)$')
    plt.title( r'Bessel functions $J_n(x)$')
    plt.show()
    
    print(f'Minimum time: {minTime: .03f} sec.')
    toc1 = time() - tic1
    execTime = toc1
    print(f'Execution time: {execTime: .03f} sec.')