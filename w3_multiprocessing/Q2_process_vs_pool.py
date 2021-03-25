from multiprocessing import Pool
import multiprocessing.process
import time
import os
def worker(p):
    p = p**2
    print(p, end=' ')
    print(os.getpid())
    return p
def show(result):
    #res = result*2
    print('-', result)

if __name__=="__main__":

    num = 1000
    
    #pool apply
    time_start = time.time()
    pool_apply = Pool(None) #None -> use number from os.cpu_count()
    for i in range(num):
        pool_apply.apply(worker, args=(i,))
    print('apply trigger')
    pool_apply.close()
    pool_apply.join()
    time_end = time.time()
    spend_time = time_end - time_start
    print('pool apply spend time: ', spend_time, ' sec')
    print()
    
    #pool apply_async
    time_start = time.time()
    pool_apply_async = Pool(None)
    for i in range(num):
        pool_apply_async.apply_async(worker, args=(i,), callback=show)
    print('apply_async trigger')
    pool_apply_async.close()
    pool_apply_async.join()
    time_end = time.time()
    spend_time = time_end - time_start
    print('pool apply_async spend time: ', spend_time, ' sec')
    print()
    
    #pool map
    time_start = time.time()
    pool_map = Pool(None)
    res = pool_map.map(worker, [*range(0,num)])
    print('map trigger')
    pool_map.close()
    pool_map.join()
    time_end = time.time()
    spend_time = time_end - time_start
    print('pool map spend time: ', spend_time, ' sec')
    print()

    #pool map_async
    time_start = time.time()
    pool_map_async = Pool(None)
    res = pool_map_async.map_async(worker, [*range(0,num)], callback=show)
    print('map_async trigger')
    pool_map_async.close()
    pool_map_async.join()
    time_end = time.time()
    spend_time = time_end - time_start
    print('pool map_async spend time: ', spend_time, ' sec')
    print()

    #pool imap
    time_start = time.time()
    pool_imap = Pool(None)
    res = pool_imap.imap(worker, [*range(0,num)])
    print('imap trigger')
    pool_imap.close()
    pool_imap.join()
    time_end = time.time()
    spend_time = time_end - time_start
    print('pool imap spend time: ', spend_time, ' sec')
    print()

    #pool map
    time_start = time.time()
    pool_imap_unordered = Pool(None)
    res = pool_imap_unordered.imap_unordered(worker, [*range(0,num)])
    print('imap_unordered trigger')
    pool_imap_unordered.close()
    pool_imap_unordered.join()
    time_end = time.time()
    spend_time = time_end - time_start
    print('pool imap_unordered spend time: ', spend_time, ' sec')
    print()

    #process
    time_start = time.time()
    num = 1000
    process_list = []
    for i in range(0,num):
        process_list.append( multiprocessing.Process(target=worker, args=(i,)) )
    for i in range(0,num):
        process_list[i].start()
    for i in range(0,num):
        process_list[i].join()
    time_end = time.time()
    spend_time = time_end - time_start
    print('process spend time: ', spend_time, ' sec')
