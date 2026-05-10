from numba import cuda
import numpy as np

@cuda.jit()
def doCalcGpu(x1,x2,y):
    i = cuda.grid(1)
    y[i] = x1[i] + x2[i]
    
size = 32768
# Allocate and transfer a numpy ndarray or structured scalar to the device
x1 = cuda.to_device(np.array(range(size)))
x2 = cuda.to_device(np.array(range(size)))
y  = cuda.device_array(x1.shape)

threadsperblock = (1024,1,1)
blockspergrid = (int(size/1024),1,1)

doCalcGpu[blockspergrid,threadsperblock](x1,x2,y)
print(y.copy_to_host())
