'''
rtreeNN.py
Arguements: -d <datasetFile>, -q <queryFile>, -b <Bvalue>
'''

# standard libraries
import time
import getopt
import sys
import math
import random
# private libraries
import RtreeBuilder
import Rtree

# the nearest neighbors
global results


# in a leaf, find all points which have the topk least score
def getTopK(leaf, query, k, Enough):
    global results

    query_result = []
    for point in leaf.childList:
        Scr = NodeScore(point, query)
        query_result.append((Scr, point))
    query_result = sorted(query_result, key = lambda x: x[0])
    #score = query_result[0][0]
    if len(query_result) > k:
        query_result = query_result[:k]
        if Enough: # 如果前一个query已经足够topk，则把results列表清空
            results.clear()
            query_result = query_result[:k]
        results += query_result
        enough = True
        return enough
    else:
        if Enough:  # 如果前一个query已经足够topk，则把results列表清空
            results.clear()
        results += query_result
        enough = False
        return enough
        
    
def findLeaf(tupleList, query):
    while isinstance(tupleList[0][1], Rtree.Branch):
        node = tupleList[0][1]
        del tupleList[0]
        for child in node.childList:
            tupleList.append((NodeScore(child, query), child))
        tupleList = sorted(tupleList, key=lambda x: x[0])
    if isinstance(tupleList[0][1], Rtree.Leaf):
        return tupleList

def scoreFirst(tupleList, query, k):  # tuplelist = [(score, node)]
    global results
    enough = False
    if isinstance(tupleList[0][1], Rtree.Branch):
        node = tupleList[0][1]
        del tupleList[0]
        for child in node.childList:
            tupleList.append((NodeScore(child, query), child))
        tupleList = sorted(tupleList, key=lambda x: x[0])
    elif isinstance(tupleList[0][1], Rtree.Leaf):
        node = tupleList[0][1]
        del tupleList[0]
        enough = getTopK(node, query, k, True)
        while not enough:
            tupleList = findLeaf(tupleList, query)
            node = tupleList[0][1]
            enough = getTopK(node, query, k - len(results), enough)
    if enough:
        return

    # implement scoreFirst algorithm resursively
    scoreFirst(tupleList, query, k)

def NodeScore(node, query):
    score = 0
    Sa = float('inf')
    # 参数
    a = 0.8
    b = 0.6
    maxSd = 100.0
    maxSk = 10
    qA1 = 0.5
    qA2 = 0.5
    if isinstance(node, Rtree.Point):
        x = node.x
        y = node.y
        Sa = qA1 * node.attribute[0] + qA2 * node.attribute[1]
    else:  # leaf & branch
        x = node.centre[0]
        y = node.centre[1]
        for attrtuple in node.attribute:
            temp = qA1 * attrtuple[0] + qA2 * attrtuple[1]
            if temp < Sa:
                Sa = temp
    #Sd, Sk (Sa is given above)
    Sd = math.sqrt((query[0] - x)**2 + (query[1] - y)**2) / maxSd
    Sk = 1 - (bin(query[2] & node.bitmap)[2:].count('1') / maxSk)
    word2vec()
    # 加权
    score = a*b*Sd+(1-b)*Sk+(1-a)*b*Sa
    return score


'''模拟一波计算向量距离，那个词向量太烦了，找不到合适的数据集提取关键词，用随机生成的bitmap来模拟关键词匹配
用这个函数来模拟计算词向量距离的时间复杂度'''
def word2vec():
    dissum = 0
    for i in range(200):
        a = round(random.uniform(-2, 2), 6)
        b = round(random.uniform(-2, 2), 6)
        dissum += (a-b)**2
    dis = math.sqrt(dissum)
    return



# answer all the queries using "Best First" algorithm with a given r-tree
def answerNnQueries(root, queries, k):
    global results

    resultFile = 'results.txt'
    # the start time
    timeStart = time.time()
    f = open(resultFile, 'wt')
    for query in queries:
        # initialize global variables
        results = []
        # answer query
        scoreFirst([(0, root)], query, k)
        i = 0
        for resultuple in results:
            result = resultuple[1]
            i += 1
            f.write('top'+str(i)+': x='+str(result.x) + ',y=' + str(result.y) +
                    ',keword=' + str(bin(query[2] & result.bitmap).count('1')) + ',' + str(result.attribute))
        f.write('\r')
    # the end time
    timeEnd = time.time()
    f.close()
    i = len(queries)
    print('TopK=',k,'Queries finished. Average time: ' + str((timeEnd-timeStart)/i))


# read all queries
def readNn(queryFile):
    fileHandle = open(queryFile, 'rt')
    queries = []
    nextLine = fileHandle.readline()
    while nextLine == '\n':
        nextLine = fileHandle.readline()
    while nextLine != '':
        queries.append(getQuery(nextLine))
        nextLine = fileHandle.readline()
        while nextLine == '\n':
            nextLine = fileHandle.readline()
    fileHandle.close()
    return queries   # return一个二维列表，每一行是一个query

# read a single query from a line of text

def getQuery(nextLine):
    # split the string with whitespace
    content = nextLine.strip('\n').split(' ')
    while content.count('') != 0:
        content.remove('')
    result = []
    for i in [0, 1]:
        result.append(float(content[i]))
    result.append(int(content[2]))
    return result

def main():
    datasetFile = 'demoset.txt'
    queryFile = 'queries.txt'
    Bvalue = None
    
    # parse arguments
    options,args = getopt.getopt(sys.argv[1:],"d:q:b:")
    for opt, para in options:
        if opt == '-d':
            datasetFile = para
        if opt == '-q':
            queryFile = para
        if opt == '-b':
            Bvalue = int(para)
    
    # build r-tree
    startbuild = time.time()
    root = RtreeBuilder.buildRtree(datasetFile, Bvalue)
    RtreeBuilder.checkRtree(root)
    endbuild = time.time()
    print('Building time:', str(endbuild - startbuild))
    # answer NN queries
    queries = readNn(queryFile)
    # topk query
    for k in [25,50]:
        answerNnQueries(root, queries, k)
    
if __name__ == '__main__':
    main()
