import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


values = range(10**6, 10**7, 10**5)
#values = [x for x in range(10**3, 10**6, 10**3)]
procNo = None  # None (means all), or any positive number
threadNo = None  # None (means all), or any positive number


def counting(n):
    while n > 0:
        n -= 1
    return n


def main():
    for procNo in [1, 2, 4, 8, 16, 32]:
        start = time.time()
        with ProcessPoolExecutor(max_workers=procNo) as ex:
            w = ex.map(counting, values)

        # convert iterable to list for indexing with print(); print just first future (but all futures here should equal zero as this is a count-down function)
        print("For MP pool size: {},".format(procNo), " print 1st output: {}".format(list(w)), " for walltime: {:.2f} sec".format(time.time()-start))
    
    # ALTERNATIVE STYLE
    # futures = []
    # for procNo in [1, 2, 4, 8, 16, 32]:
    #     start = time.time()
    #     with ProcessPoolExecutor(procNo) as ex:
    #         for i in values:
    #             futures.append(ex.submit(counting, i))
    
    # for i in futures:
    #     print("Process output: {}".format(i.result()), " for walltime: {:.2f} sec".format(time.time()-start))
    

    for threadNo in [1, 2, 4, 8, 16, 32]:
        start = time.time()
        with ThreadPoolExecutor(max_workers=threadNo) as ex:
            w = ex.map(counting, values)

        # convert iterable to list for indexing with print(); print just first future (but all futures here should equal zero as this is a count-down function)
        print("For MT pool size: {},".format(threadNo), " print 1st output: {}".format(list(w)[0]), " for walltime: {:.2f} sec".format(time.time()-start))


if __name__ == '__main__':
    main()
