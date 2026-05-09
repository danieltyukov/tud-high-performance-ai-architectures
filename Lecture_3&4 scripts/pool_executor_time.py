# Adapted from: https://stackoverflow.com/questions/56127719/is-pythons-time-process-time-including-the-cpu-time-spent-by-child-processes

from time import process_time, time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from numpy import mean


def f(x):
    i = 0
    for j in range(x ** 8):
        i += j
    return i


def sequential_process_time():
    clock_t0 = time(); t0 = process_time()
    result = f(9)

    t1 = process_time(); clock_t1 = time()
    
    print(f"CPU time: {t1 - t0: .3f} sec, Wallclock time: {clock_t1 - clock_t0:.3f} sec")
    return t1 - t0


def multiprocessing_process_time():
    clock_t0 = time(); t0 = process_time()
    with ProcessPoolExecutor(10) as pool:
        pool.map(f, [9])

    t1 = process_time(); clock_t1 = time()

    print(f"CPU time: {t1 - t0: .3f} sec, Wallclock time: {clock_t1 - clock_t0:.3f} sec")
    return t1 - t0

def multithreading_process_time():
    clock_t0 = time(); t0 = process_time()
    with ThreadPoolExecutor(10) as pool:
        pool.map(f, [9])

    t1 = process_time(); clock_t1 = time()

    print(f"CPU time: {t1 - t0: .3f} sec, Wallclock time: {clock_t1 - clock_t0:.3f} sec")
    return t1 - t0


if __name__ == '__main__':
    print('Processing in Parent Process')
    print(f"Mean CPU processing time: {mean([sequential_process_time() for _ in range(5)]):.3f} sec")

    print('\nProcessing in Child Process')
    print(f"Mean CPU processing time: {mean([multiprocessing_process_time() for _ in range(5)]):.3f} sec")

    print('\nProcessing in Child Thread')
    print(f"Mean CPU processing time: {mean([multithreading_process_time() for _ in range(5)]):.3f} sec")