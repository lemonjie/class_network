from multiprocessing import Array
import multiprocessing.process

init_list = []
for i in range(0, 42):
    init_list.append('耶')
final_list = Array('u', init_list)

input_list01 = ['伊', '睨', '山', '勢', '舞', '流', '溪']
input_list02 = ['獨', '攬', '梅', '花', '舒', '臘', '雪']
input_list03 = ['椰', '碧', '洗', '滌', '宜', '福', '居']
input_list04 = ['一', '二', '三', '四', '五', '六', '七']
input_list05 = ['朵', '瑞', '咪', '發', '索', '拉', '西']
input_list06 = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def worker(num, arr):
    for i in range(len(arr)):
        final_list[num * len(arr) + i] = arr[i]

if __name__ == '__main__':
    process1 = multiprocessing.Process(target=worker, args=[0,input_list01])
    process2 = multiprocessing.Process(target=worker, args=[1,input_list02])
    process3 = multiprocessing.Process(target=worker, args=[2,input_list03])
    process4 = multiprocessing.Process(target=worker, args=[3,input_list04])
    process5 = multiprocessing.Process(target=worker, args=[4,input_list05])
    process6 = multiprocessing.Process(target=worker, args=[5,input_list06])

    process1.start()
    process2.start()
    process3.start()
    process4.start()
    process5.start()
    process6.start()
    process1.join()
    process2.join()
    process3.join()
    process4.join()
    process5.join()
    process6.join()

    print(final_list[:])

'''
from multiprocessing import Array
import multiprocessing.process

init_list = []
for i in range(0, 42):
    init_list.append('耶')
final_list = Array('u', init_list)

input_list01 = ['伊', '睨', '山', '勢', '舞', '流', '溪']
input_list02 = ['獨', '攬', '梅', '花', '舒', '臘', '雪']
input_list03 = ['椰', '碧', '洗', '滌', '宜', '福', '居']
input_list04 = ['一', '二', '三', '四', '五', '六', '七']
input_list05 = ['朵', '瑞', '咪', '發', '索', '拉', '西']
input_list06 = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

input_list = []
input_list.append(input_list01)
input_list.append(input_list02)
input_list.append(input_list03)
input_list.append(input_list04)
input_list.append(input_list05)
input_list.append(input_list06)

def worker(num, arr):
    for i in range(len(arr)):
        final_list[num * len(arr) + i] = arr[i]

if __name__ == '__main__':
    process_list = []
    for i in range(0,6):
        process_list.append( multiprocessing.Process(target=worker, args=[i,input_list[i]]) )

    for i in range(0,6):
        process_list[i].start()

    for i in range(0,6):
        process_list[i].join()

    print(final_list[:])
'''