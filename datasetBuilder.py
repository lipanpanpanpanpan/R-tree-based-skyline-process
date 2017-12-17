'''
Arguements: -s <size>, -r <rangeLimit>, -o <outputName>
Build a data set
format:
 size
 id_1 x_1 y_1 bitmap_1 attr1_1 attr2_1
 ......
 id_m x_m y_m bitmap_m attr1_m attr2_m
 ......
'''
import sys
import getopt
import random


#随机变量的概率函数
def random_index(rate):  # 参数rate为list<int>
    start = 0
    randnum = random.randint(1, sum(rate))
    for index, item in enumerate(rate):
        start += item
        if randnum <= start:
            break
    return index


# 生成随机bitmap = 10101011100000001000
def random_bitmap(rate):
    '''rate可作为敏感性分析'''
    bitmap = ''
    for i in range(30):
        bitmap += str(random_index(rate))
    bitmap = int(bitmap, 2)  # 用10进制保存 "10101011100000001000"，方便按位取或
    return bitmap

            
# write a rtreePoint
def writePoint(f, rangeLimit):
    x = round(random.uniform(0, rangeLimit),2)
    y = round(random.uniform(0, rangeLimit),2)
    rate = [70, 30]  # 每个子节点含有聚类中30%的keyword
    bitmap = random_bitmap(rate)
    attr1 = round(random.uniform(0, 1), 3)
    attr2 = round(random.uniform(0, 1), 3)
    f.write(str(x) + ' ' + str(y) + ' ' + str(bitmap) + ' '+  str(attr1) + ' ' +str(attr2) + '\n')

# build data set
def buildDataSet(fileName, size, rangeLimit):
    f = open(fileName, 'wt')
    f.write(str(size) + '\n') # first line
    # remained lines
    for i in range(1, size+1):
        f.write(str(i) + ' ')
        writePoint(f, rangeLimit)
    f.close()
    print('Size:', size, ', Coordinate Range:', 0, '~', rangeLimit)

def main():
    fileName = 'dataset.txt'
    size = 100000
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
    
    # build data set
    buildDataSet(fileName, size, rangeLimit)
    
if __name__ == '__main__':
    main()
