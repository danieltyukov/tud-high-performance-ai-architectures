import time
import concurrent.futures
import os


value = [x for x in range(10**3, 10**6, 10**3)]
# for i in value:
#     print(i)


def counting(n):
    start = time.time()
    while n > 0:
        n -= 1
    return time.time() - start


def main():
    for i in range(11,-1,-1):
        start = time.time()
        with concurrent.futures.ProcessPoolExecutor(os.cpu_count()*4) as executor:
            executor.map(counting, value, chunksize=2**i) # increment chunk size in powers of 2
        print(f"MP Total time taken for {(len(value)/2**i):.3f} chunk(s) is: {(time.time() - start):.3f} sec.")
            

if __name__ == '__main__':
    main()
