from association_rules import RuleMiner

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

def createTree(dataSet, minSup):

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

        for item in tranSet:
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: (p[1], p[0]), reverse=True)]
            #orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[0], reverse=True)]
            updateTree(orderedItems, retTree, headerTable, count)
    return retTree, headerTable

def createInitSet(dataSet):

    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = retDict.get(frozenset(trans), 0) + 1
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
    if not headerTable:
        return

    bigL = [v[0] for v in sorted (headerTable.items(), key=lambda p: (p[1],p[0]))]

    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        myCondTree, myHead = createTree(condPattBases, minSup)
        if myHead != None:
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)

def get_support(freqSet, headerTab, num_items):

    localD = {}
    for item in freqSet:
        localD[item] = headerTab[item][0]
    ordered_freq_set = [v[0] for v in sorted(localD.items(), key=lambda p: (p[1], p[0]), reverse=True)]

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


class RuleMinerForFP(RuleMiner):
    def __init__(self, frequent_itemsets, support_data_struct, num_transactions, min_conf):
        super(RuleMinerForFP, self).__init__(frequent_itemsets, support_data_struct, min_conf)
        self.num_transactions = num_transactions

    def get_support(self, this_set):
        return get_support(this_set, self.support_data_struct, self.num_transactions)

    def get_confidence(self, antecedent, consequent):
        support_a = get_support(antecedent, self.support_data_struct, self.num_transactions)
        support_b = get_support(antecedent - consequent, self.support_data_struct, self.num_transactions)
        return support_a/support_b

def generate_rules(frequent_itemsets, support_data_struct, num_transactions, min_conf):

    this_miner = RuleMinerForFP(frequent_itemsets, support_data_struct, num_transactions, min_conf)
    return this_miner.generate()

def run(dataSet, min_support, min_conf):

    abs_minsup = min_support * len(dataSet)

    initSet = createInitSet(dataSet)

    myFPTree, myHeaderTab = createTree(initSet, abs_minsup)

    freqItems = []

    mineTree(myFPTree, myHeaderTab, abs_minsup, set([]), freqItems)
    freqItems = map(frozenset,freqItems)

    rules = generate_rules(freqItems, myHeaderTab, len(dataSet), min_conf)

    return freqItems, rules