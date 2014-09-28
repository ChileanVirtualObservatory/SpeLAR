
class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}

    def inc(self, numOccur):
        self.count  += numOccur

    def disp(self, ind=1):
        print '    ' * ind, self.name, ' ', self.count
        for child in self.children.values():
            child.disp(ind + 1)

def updateHeader(nodeToTest, targetNode):
    while (nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode

def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count)
    else:
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    if len(items) > 1:
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)

def createTree(dataSet, minSup=1):
    headerTable = {}
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    for k in headerTable.keys():
        if headerTable[k] < minSup:
            del(headerTable[k])
    freqItemSet = set(headerTable.keys())
    if len(freqItemSet) == 0:
        return None, None
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]
    retTree = treeNode('Null Set', 1, None)
    for tranSet, count in dataSet.items():
        localD = {}
        #import ipdb; ipdb.set_trace()
        for item in tranSet:
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
            #orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[0], reverse=True)]
            updateTree(orderedItems, retTree, headerTable, count)
    return retTree, headerTable

def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict

def ascendTree(leafNode, prefixPath):
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)

def findPrefixPath(basePat, treeNode):
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats

def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    bigL = [v[0] for v in sorted (headerTable.items(), key=lambda p: p[1])]

    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        myCondTree, myHead = createTree(condPattBases, minSup)
        if myHead != None:
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)

def get_support(freqSet, headerTab, num_items):
    """
    if len(freqSet) == 1:
        return float(headerTab[freqSet][0]) / num_items
    else:
    """

    localD = {}
    for item in freqSet:
        localD[item] = headerTab[item][0]
    ordered_freq_set = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]

    last_item = ordered_freq_set[-1]
    rest = frozenset(ordered_freq_set[:-1])
    this_node = headerTab[last_item][1]

    this_count = 0
    while this_node != None:
        prefix_path = []
        ascendTree(this_node, prefix_path)
        this_pattern = frozenset(prefix_path)
        if freqSet.issubset(this_pattern):
            this_count += this_node.count
        this_node = this_node.nodeLink

    return float(this_count) / num_items

def calcConf(freqSet, H, brl, headerTab, num_items, minConf):
    prunedH = []
    for conseq in H:
        support_a = get_support(freqSet, headerTab, num_items)
        support_b = get_support(freqSet - conseq, headerTab, num_items)
        #print "itemset_a: %s\nsupport_a: %f\nitemset_b: %s\nsupport_b: %f\n" % (freqSet, support_a, freqSet - conseq, support_b)
        conf = support_a/support_b
        if conf >= minConf:
            brl.append((freqSet - conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH

def aprioriGen(Lk, k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk):
            L1 = list(Lk[i])[:k-2]
            L2 = list(Lk[j])[:k-2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])

    return retList

def rulesFromConseq(freqSet, H, brl, headerTab, num_items, minConf):
    m = len(H[0])
    if (len(freqSet) > (m + 1)):
        Hmp1 = aprioriGen(H, m+1)
        Hmp1 = calcConf(freqSet, Hmp1, brl, headerTab, num_items, minConf)
        if (len(Hmp1) > 1):
            rulesFromConseq(freqSet, Hmp1, brl, headerTab, num_items, minConf)

def generateRules(freqItems, headerTab, num_items, minConf=0.7,):
    bigRuleList = []
    for freqSet in freqItems:
        if len(freqSet) >= 2:
            H1 = [frozenset([item]) for item in freqSet]
            if len(freqSet) == 2:
                calcConf(freqSet, H1, bigRuleList, headerTab, num_items, minConf)
            else:
                rulesFromConseq(freqSet, H1, bigRuleList, headerTab, num_items, minConf)
    return bigRuleList


def run(dataSet, minsup=0.5):

    abs_minsup = minsup * len(dataSet)

    initSet = createInitSet(dataSet)

    myFPTree, myHeaderTab = createTree(initSet, abs_minsup)

    #myFPTree.disp()
    #print myHeaderTab

    freqItems = []
    mineTree(myFPTree, myHeaderTab, abs_minsup, set([]), freqItems)

    #import ipdb; ipdb.set_trace()
    #rules = generateRules(freqItems, myHeaderTab, float(len(dataSet)))
    #rules = generateRules(freqItems, myHeaderTab)

    #return freqItems, rules
    return freqItems, myHeaderTab