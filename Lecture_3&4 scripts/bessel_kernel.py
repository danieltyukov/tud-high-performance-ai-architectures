# pure kernel used jointly with CLI timeit:
# %timeit -n 100 -r 1 bessel_kernel(4)

from timeit import timeit
import numpy as np
from scipy.special import jn
import matplotlib.pyplot as plt

def bessel_kernel(nfunc):
    x = np.linspace(0, 20,100000*10)
    
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
    bessel_kernel(4)
    