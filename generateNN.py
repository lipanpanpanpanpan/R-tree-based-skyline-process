'''
nnGenerator.py
Arguements: -s <size>, -r <rangeLimit>, -o <outputFile>
Build a set of 100 (default size) range queries
Format:
 x_1 y_1
 ......
 x_m y_m
 ......
'''
# standard libraries
import sys
import getopt
import random
# private libraries
import datasetBuilder


def random_index(rate):
    '''随机变量的概率函数'''
    # 参数rate为list<int>
    start = 0
    randnum = random.randint(1, sum(rate))
    for index, item in enumerate(rate):
        start += item
        if randnum <= start:
            break
    return index


def random_bitmap(rate):  # 生成随机bitmap = [0,1,0,1,1,0,0,0,0,1,0,1,....]
    '''rate可作为敏感性分析'''
    bitmap = ''
    for i in range(30):
        bitmap += str(random_index(rate))
    bitmap = int(bitmap, 2)  # 用10进制保存 "0101011100000001000"，方便按位取或
    return bitmap



def main():
    fileName = 'queriesNN.txt'
    size = 100
    rangeLimit = 1000
    
    # parse arguements
    options,args = getopt.getopt(sys.argv[1:],"s:r:o:")
    for opt, para in options:
        if opt == '-s':
            size = int(para)
        if opt == '-r':
            rangeLimit = int(para)
        if opt == '-o':
            fileName = para

    f = open(fileName, 'wt')
    for i in range(1, size+1):
        x = round(random.uniform(0, rangeLimit), 2)
        y = round(random.uniform(0, rangeLimit), 2)
        rate = [80, 20]  # 每个查询q含有聚类中20%的keyword
        bitmap = random_bitmap(rate)
        f.write(str(x) + ' ' + str(y) + ' ' + str(bitmap) + '\n')

    
    f.close()
    print('Finished')

if __name__ == '__main__':
    main()
