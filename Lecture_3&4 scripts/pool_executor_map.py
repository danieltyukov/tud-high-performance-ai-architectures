# Example of calling map and not iterating the results
# Adapted from: https://superfastpython.com/threadpoolexecutor-in-python/#Step_2_Submit_Tasks_to_the_Thread_Pool
from time import sleep
from random import random
from concurrent.futures import ThreadPoolExecutor

def task(value):  # sleep for a variable amount of time
    sleep(random())
    print(f'Task called: {value}')
    return value

def main():
    # start the process pool
    with ThreadPoolExecutor() as executor:
        # submit all tasks
        future = executor.map(task, range(5))
    print('All done!')
    for fut in future:
        print(f'Task done: {fut}')

if __name__ == '__main__':
    main()
