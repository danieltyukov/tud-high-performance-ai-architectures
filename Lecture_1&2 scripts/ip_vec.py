import numpy as np
from matplotlib import image
import matplotlib.pyplot as plt
import time
from numba import jit


def compute_energy(image):
    gray = np.dot(image[...,:3], [0.299, 0.587, 0.114])
    
    # Simple gradient approximation (Sobel-like without scipy)
    dx = np.zeros_like(gray)
    dy = np.zeros_like(gray)

    dx[:, 1:-1] = gray[:, 2:] - gray[:, :-2]
    dy[1:-1, :] = gray[2:, :] - gray[:-2, :]

    energy = np.hypot(dx, dy)
    return energy

@jit
def compute_cumulative_energy(energy):
    h, w = energy.shape
    M = energy.copy()
    for i in range(1, h):
        for j in range(w):
            left = M[i-1, j-1] if j > 0 else float('inf')
            up = M[i-1, j]
            right = M[i-1, j+1] if j < w-1 else float('inf')
            M[i, j] += min(left, up, right)
    return M

def find_seam(cum_energy):
    h, w = cum_energy.shape
    seam = np.zeros(h, dtype=np.int32)
    seam[-1] = np.argmin(cum_energy[-1])
    for i in reversed(range(h - 1)):
        j = seam[i + 1]
        options = [j]
        if j > 0:
            options.append(j - 1)
        if j < w - 1:
            options.append(j + 1)
        seam[i] = min(options, key=lambda x: cum_energy[i, x])
    return seam


def remove_seam(image, seam):
    h, w, _ = image.shape
    new_img = np.zeros((h, w - 1, 3), dtype=image.dtype)
    for i in range(h):
        j = seam[i]
        new_img[i] = np.delete(image[i], j, axis=0)
    return new_img


img = image.imread("hq.png")
num_seams = 1
print("Original Image Resoluation:", img.shape[:2])

start = time.time()

for _ in range(num_seams):
        energy = compute_energy(img)
        cum_energy = compute_cumulative_energy(energy)
        seam = find_seam(cum_energy)
        img = remove_seam(img, seam)

exec_time = time.time() - start

print("Resized Image Resoluation:", img.shape[:2])
print(exec_time)
# plt.imshow(img)
# plt.show()
