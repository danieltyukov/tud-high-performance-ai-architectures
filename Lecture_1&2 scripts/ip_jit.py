import time
import math
from PIL import Image
import matplotlib.pyplot as plt
from numba import jit

# @jit
def to_grayscale(image):
    w, h = image.size
    grayscale = [[0] * w for _ in range(h)]
    pixels = image.load()
    for y in range(h):
        for x in range(w):
            r, g, b = pixels[x, y]
            gray = 0.299 * r + 0.587 * g + 0.114 * b
            grayscale[y][x] = gray
    return grayscale

# @jit
def compute_energy(grayscale):
    h = len(grayscale)
    w = len(grayscale[0])
    energy = [[0] * w for _ in range(h)]

    for y in range(h):
        for x in range(w):
            dx = 0
            dy = 0
            if 0 < x < w - 1:
                dx = grayscale[y][x + 1] - grayscale[y][x - 1]
            if 0 < y < h - 1:
                dy = grayscale[y + 1][x] - grayscale[y - 1][x]
            energy[y][x] = math.sqrt(dx * dx + dy * dy)
    return energy

@jit
def compute_cumulative_energy(energy):
    h = len(energy)
    w = len(energy[0])
    cum_energy = energy.copy() #[[0] * w for _ in range(h)]

    # First row is just the energy itself
    for x in range(w):
        cum_energy[0][x] = energy[0][x]

    for y in range(1, h):
        for x in range(w):
            min_above = cum_energy[y - 1][x]
            if x > 0:
                min_above = min(min_above, cum_energy[y - 1][x - 1])
            if x < w - 1:
                min_above = min(min_above, cum_energy[y - 1][x + 1])
            cum_energy[y][x] = energy[y][x] + min_above

    return cum_energy

# @jit
def find_seam(cum_energy):
    h = len(cum_energy)
    w = len(cum_energy[0])
    seam = [0] * h

    # Start from the bottom row
    min_x = 0
    min_val = cum_energy[h - 1][0]
    for x in range(1, w):
        if cum_energy[h - 1][x] < min_val:
            min_val = cum_energy[h - 1][x]
            min_x = x
    seam[h - 1] = min_x

    for y in range(h - 2, -1, -1):
        prev_x = seam[y + 1]
        min_x = prev_x
        min_val = cum_energy[y][prev_x]

        if prev_x > 0 and cum_energy[y][prev_x - 1] < min_val:
            min_val = cum_energy[y][prev_x - 1]
            min_x = prev_x - 1
        if prev_x < w - 1 and cum_energy[y][prev_x + 1] < min_val:
            min_val = cum_energy[y][prev_x + 1]
            min_x = prev_x + 1
        seam[y] = min_x

    return seam

# @jit
def remove_seam(image, seam):
    w, h = image.size
    new_img = Image.new("RGB", (w - 1, h))
    src_pixels = image.load()
    dst_pixels = new_img.load()

    for y in range(h):
        skip_x = seam[y]
        new_x = 0
        for x in range(w):
            if x == skip_x:
                continue
            dst_pixels[new_x, y] = src_pixels[x, y]
            new_x += 1

    return new_img


image = Image.open("lq.png").convert("RGB")
num_seams = 20
print("Original Image Resoluation:", image.shape[:2])

start = time.time()

for _ in range(num_seams):
    gray = to_grayscale(image)
    energy = compute_energy(gray)
    cum_energy = compute_cumulative_energy(energy)
    seam = find_seam(cum_energy)
    image = remove_seam(image, seam)

exec_time = time.time() - start

print("Resized Image Resoluation:", image.shape[:2])
print(exec_time)
plt.imshow(image)
plt.show()