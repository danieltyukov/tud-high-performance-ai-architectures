# Adapted from: https://blog.finxter.com/python-profilers-how-to-speed-up-your-python-app/

import random
import cProfile
import pstats


def guess():
    ''' Returns a random number '''
    return random.randint(2, 1000)

def is_prime(x):
    ''' Checks whether x is prime '''
    for i in range(x):
        for j in range(x):
            if i * j == x:
                return False
    return True

def is_prime2(x):
    ''' Checks whether x is prime '''
    for i in range(2,int(x**0.5)+1):
        if x % i == 0:
            return False
    return True

def find_primes(num):
    primes = []
    for i in range(num):
        p = guess()
        while not is_prime(p): # <- change to is_prime2(p) for optimization
            p = guess()
        primes += [p]
    return primes


if __name__ == '__main__':
    #print(find_primes(100)) # original function call
    
    #cProfile.run('print(find_primes(100))') # profiled function call
    
    cProfile.run('print(find_primes(100))',"output.dat") # profiled function call with pstats enabled
    p = pstats.Stats("output.dat")
    p.print_stats(p.sort_stats("calls")) # arrange by most function calls
    p.strip_dirs() # improve readability
    p.print_stats(p.sort_stats("tottime")) # arrange by largest exec time