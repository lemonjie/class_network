from multiprocessing import Pool
import time
def worker(p):
       print(p)
       time.sleep(3)
if __name__=="__main__":
    pool = Pool(processes=7)
    for i  in range(50):
        pool.apply(worker, args=(i,)) # number of working processes is 7
    print('worker')
    pool.close()
    pool.join()