# IO-network CPU kernel. -march=native for AVX2/FMA, -ffast-math so the
# poly-exp and the reductions vectorise. -fopenmp for the cell-parallel loop.
CC      = gcc
CFLAGS  = -O3 -march=native -ffast-math -funroll-loops -fopenmp -Wall
LDFLAGS = -lm -fopenmp

io_sim: io_sim.c
	$(CC) $(CFLAGS) io_sim.c -o io_sim $(LDFLAGS)

# show which loops the vectoriser accepted
vec: io_sim.c
	$(CC) $(CFLAGS) -fopt-info-vec-optimized io_sim.c -o io_sim $(LDFLAGS) 2>&1 | grep -Ei "io_sim.c:.*loop vectorized" | head -30

clean:
	rm -f io_sim

.PHONY: vec clean
