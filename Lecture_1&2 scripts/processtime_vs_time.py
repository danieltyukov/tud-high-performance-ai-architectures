# Adapted from: https://stackoverflow.com/questions/56127719/is-pythons-time-process-time-including-the-cpu-time-spent-by-child-processes
# Next year: Also use https://github.com/sumerc/yappi/

import time
from concurrent.futures import ProcessPoolExecutor
from numpy import mean

def f(x):
    i = 0
    for j in range(x ** 8):
        i += j
    return i

def processtime():
    clock_t0 = time.time()
    t0 = time.process_time()
    result = f(9)
    print('Result:', result, end='\t')
    t1 = time.process_time()
    clock_t1 = time.time()
    print('CPU time: ', t1 - t0, end='\t')
    print('Clock time: ', clock_t1 - clock_t0)
    return t1 - t0

def multiprocessing_processtime():
    clock_t0 = time.time()
    t0 = time.process_time()
    with ProcessPoolExecutor() as executor:
        result = executor.map(f, [9])
    result = list(result) # convert to list else: TypeError: 'generator' object is not subscriptable
    print('Result:', result[0], end='\t')
    t1 = time.process_time()
    clock_t1 = time.time()
    print('CPU time: ', t1 - t0, end='\t')
    print('Clock time: ', clock_t1 - clock_t0)
    return t1 - t0


if __name__ == '__main__':
    print('\nProcessing in Parent Process')
    print('Mean CPU processing time:', mean([processtime() for _ in range(5)]), 'sec')

    print('\nProcessing in Child Process')
    print('Mean CPU processing time:', mean([multiprocessing_processtime() for _ in range(5)]), 'sec')
