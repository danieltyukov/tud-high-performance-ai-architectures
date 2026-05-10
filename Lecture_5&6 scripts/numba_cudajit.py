from numba import cuda
import numpy as np

@cuda.jit()
def doCalcGpu(x1,x2,y):
    i = cuda.grid(1)
    y[i] = x1[i] + x2[i]
  
size = 32768
x1 = np.array(range(size))
x2 = np.array(range(size))
y  = np.zeros(x1.shape)

threadsperblock = (1024,1,1)
blockspergrid = (int(size/1024),1,1)

doCalcGpu[blockspergrid,threadsperblock](x1,x2,y)
print(y)
