import time
from concurrent.futures import ProcessPoolExecutor, as_completed

def func1(para1, para2):
    time.sleep(para1)
    return para2

def func2(para1, para2, para3):
    time.sleep(para1)
    return para2+para3



if __name__ == '__main__':
    futures = []
    with ProcessPoolExecutor(2) as ex:
        for x in range(6):
            futures.append(ex.submit(func1, x, 'hi '+str(x)))
            futures.append(ex.submit(func2, x+4, 'hello ', 'world '+str(x)))
        
        for i in as_completed(futures):
            print("Future result (as they come): {}".format(i.result()))
    
    print()
    for i in futures:
        print("Future result (in sequence): {}".format(i.result()))
