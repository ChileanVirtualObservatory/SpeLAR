"""
This file is part of ChiVO
Copyright (C) Nicolas Miranda

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
from association_rules import RuleMiner, AssociationRule

class treeNode:
    def __init__(self, nameValue, data_dict, parentNode):
        if isinstance(data_dict, int):
            self.count = data_dict
            self.meta_data = {}
        else:
            self.count = data_dict['count']
            self.meta_data = data_dict['meta'].copy()
        self.name = nameValue        
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}
        
    def inc_metadata(self, meta):
        for key in meta:
            if key in self.meta_data:
                self.meta_data[key] += meta[key]
            else:
                self.meta_data[key] = meta[key]

    def inc(self, data_dict):
        self.count  += data_dict['count']
        self.inc_metadata(data_dict['meta'])

    def disp(self, ind=1):
        print '    ' * ind, self.name, ' count: ', self.count, ' meta: ', self.meta_data
        for child in self.children.values():
            child.disp(ind + 1)

def updateHeader(nodeToTest, targetNode):
    while (nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode

def updateTree(items, inTree, headerTable, data_dict):

    if items[0] in inTree.children:
        inTree.children[items[0]].inc(data_dict)
    else:
        inTree.children[items[0]] = treeNode(items[0], data_dict, inTree)
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    if len(items) > 1:
        updateTree(items[1::], inTree.children[items[0]], headerTable, data_dict)

    

def createTree(dataSet, minSup):

    headerTable = {}

    # Create headertable with supports inherited from the initial dataSet dict
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]['count']
    for k in headerTable.keys():
        if headerTable[k] < minSup:
            del(headerTable[k])
    freqItemSet = set(headerTable.keys())

    # Initialize headerTable to its final form and an empty initial tree
    if len(freqItemSet) == 0:
        return None, None
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]
    retTree = treeNode('Null Set', 1, None)
    
    for tranSet, data_dict in dataSet.items():

        count = data_dict['count']
        localD = {}

        # Filter non-frequent itemsets
        for item in tranSet:
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: (p[1], p[0]), reverse=True)]
            #orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[0], reverse=True)]
            updateTree(orderedItems, retTree, headerTable, data_dict)
    return retTree, headerTable

def createInitSet(dataSet):

    retDict = {}

    for trans in dataSet:

        itemset = frozenset(trans['itemlist'])

        if itemset not in retDict:
            meta_dict = {}
            meta_dict[trans['meta']] = 1
            retDict[itemset] = {'count': 1, 'meta': meta_dict}
        else:
            retDict[itemset]['count'] += 1
            if trans['meta'] in retDict[itemset]['meta']:
                retDict[itemset]['meta'][trans['meta']] += 1
            else:
                retDict[itemset]['meta'][trans['meta']] = 1

        #retDict[frozenset(trans['items'])] = {'count': retDict.get(frozenset(trans), 0) + 1}

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
            #condPats[frozenset(prefixPath[1:])] = treeNode.count
            condPats[frozenset(prefixPath[1:])] = {'count': treeNode.count, 'meta': treeNode.meta_data}
        treeNode = treeNode.nodeLink
    return condPats

def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    if not headerTable:
        return

    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: (p[1],p[0]))]

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

def get_meta_data(freqSet, headerTab):

    localD = {}
    for item in freqSet:
        localD[item] = headerTab[item][0]
    ordered_freq_set = [v[0] for v in sorted(localD.items(), key=lambda p: (p[1], p[0]), reverse=True)]

    last_item = ordered_freq_set[-1]
    rest = frozenset(ordered_freq_set[:-1])
    this_node = headerTab[last_item][1]

    this_meta = {}
    while this_node != None:
        prefix_path = []
        ascendTree(this_node, prefix_path)
        this_pattern = frozenset(prefix_path)
        if freqSet.issubset(this_pattern):
            #this_count += this_node.count
            for key in this_node.meta_data:
                if key not in this_meta:
                    this_meta[key] = this_node.meta_data[key]
                else:
                    this_meta[key] += this_node.meta_data[key]
        this_node = this_node.nodeLink

    return this_meta


class RuleMinerForFP(RuleMiner):
    def __init__(self, frequent_itemsets, support_data_struct, num_transactions, min_conf):
        super(RuleMinerForFP, self).__init__(frequent_itemsets, support_data_struct, min_conf)
        self.num_transactions = num_transactions

    def get_support(self, this_set):
        return get_support(this_set, self.support_data_struct, self.num_transactions)

    def get_meta_data(self, this_set):
        return get_meta_data(this_set, self.support_data_struct)

    def calc_confidence(self, frequent_set, itemset_list, brl):
        pruned_item_list = []
        num_items = 4

        for conseq in itemset_list:
            this_rule = AssociationRule(frequent_set - conseq, conseq, self.get_support(frequent_set), self.get_support(frequent_set - conseq), self.get_support(conseq), self.get_meta_data(frequent_set))
            if this_rule.confidence() >= self.min_conf:
                brl.append(this_rule)
                pruned_item_list.append(conseq)

        return pruned_item_list

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
