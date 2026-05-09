from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random

def fct(variableA, variableB):
   time.sleep(random.randint(1,5))
   return variableA+1, variableB+1

myvar1 = [1,2,3,4]
myvar2 = [7,8,9,0]

with ThreadPoolExecutor(max_workers = 8) as executor:
    for out in as_completed([executor.submit(fct,*vars) for vars in zip(myvar1, myvar2)]):
        print(out.result())


# You can still get the output in the original order this way. You just need to save the list you give to as_completed:
#with ThreadPoolExecutor(max_workers = 8) as executor:
#    jobs = [executor.submit(fct, *vars)
#
#for vars in zip(myvar1, myvar2)]
#    for out in as_completed(jobs):
#        print(out.result())
#    results = [r.result() for r in jobs]
#    print(results)
