import time
import numpy as np
import cupy as cp

datasize = 32768

# numpy code  (CPU)
tic = time.time()
x1_cpu = np.array(range(datasize))
x2_cpu = np.array(range(datasize))
y_cpu = x1_cpu * x2_cpu + x1_cpu * x2_cpu * x2_cpu
print(f"CPU walltime: {(time.time() - tic):.2f} sec")

# CuPy code (GPU)
for i in range(4):
	tic = time.time()
	x1_gpu = cp.array(range(datasize))
	x2_gpu = cp.array(range(datasize))
	y2_gpu = x1_gpu * x2_gpu + x1_gpu * x2_gpu * x2_gpu
	y2_cpu = y2_gpu.get()
	print(f"GPU walltime {i} sec: {(time.time() - tic):.2f}")
