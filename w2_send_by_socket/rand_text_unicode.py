# coding=UTF-8
import random

def rndUnicode():
    val = random.randint(0x4e00, 0x9fbf)
    return chr(val)

string = ''
file = open('test_50MB.txt', 'w', encoding='utf-8')
for i in range(0, int(4096*32*50)):
    string += str(i).encode('utf-8').decode('utf-8')
    string += rndUnicode()
file.write(string)
file.close()
