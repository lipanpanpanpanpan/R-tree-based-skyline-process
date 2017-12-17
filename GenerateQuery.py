'''
Arguements: -s <size>, -r <rangeLimit>, -o <outputFile>
Build a set of 100 (default size) range queries
Format:
 x_1 y_1 bitmap_1 10100...0101100
 ......
 x_m y_m bitmap_2 10001...0000110
 ......
'''
# standard libraries
import sys
import getopt
import random
# private libraries
from DatasetBuilder import random_bitmap, random_index


def main():
    fileName = 'queries.txt'
    size = 100
    rangeLimit = 1000 # coordinate range
    
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
        f.write(str(x) + ' ' + str(y) + ' ' + str(bitmap) + ' ' + bin(bitmap)[2:] + '\n')

    f.close()
    print(size,'- Size Query generating finished. Keyword rate =',rate[1],'%')

if __name__ == '__main__':
    main()
