'''
rtreeNN.py
Arguements: -d <datasetFile>, -q <queryFile>, -b <Bvalue>
'''

# standard libraries
import time
import getopt
import sys
import math
# private libraries
import rtreeBuilder
import Rtree

# the nearest neighbors
global results


# in a leaf, find all points which have the topk least score
def getNN(leaf, query, k, Enough):
    global results
    ''' top1:
    for point in leaf.childList:
        newScr = NodeScore(point, query)
        if newScr < score:
            score = newScr
            results.clear()
            results.append(point)
        elif newScr == score:
            results.append(point)
    '''
    # top k
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
        enough = getNN(node, query, k, True)
        while not enough:
            tupleList = findLeaf(tupleList, query)
            node = tupleList[0][1]
            enough = getNN(node, query, k - len(results), enough)
    if enough:
        return
    '''# in this case, the NN has been found
    if score < tupleList[0][0]:
        return'''
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
    # 加权
    score = a*b*Sd+(1-b)*Sk+(1-a)*b*Sa
    return score


# answer all the queries using "Best First" algorithm with a given r-tree
def answerNnQueries(root, queries):
    global results
    # topk query
    k = 15

    resultFile = 'resultNN.txt'
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
    print('Queries finished. Average time: ' + str((timeEnd-timeStart)/i))


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
    datasetFile = 'dataset.txt'
    queryFile = 'queriesNN.txt'
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
    root = rtreeBuilder.buildRtree(datasetFile, Bvalue)
    rtreeBuilder.checkRtree(root)
    endbuild = time.time()
    print('Building time:', str(endbuild - startbuild))
    # answer NN queries
    queries = readNn(queryFile)
    answerNnQueries(root, queries)
    
if __name__ == '__main__':
    main()
