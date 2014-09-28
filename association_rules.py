from tools import apriori_gen

class RuleMiner(object):
    """A class for mining asociation rules using Apriori algorithm
    """
    def __init__(self, frequent_itemsets, support_data, min_conf=0.7):
        super(RuleMiner, self).__init__()
        self.frequent_itemsets = frequent_itemsets
        self.support_data = support_data
        self.min_conf = min_conf

    def calc_confidence(self, frequent_set, itemset_list, brl):
        pruned_item_list = []
        for conseq in itemset_list:
            conf = self.support_data[frequent_set]/self.support_data[frequent_set - conseq]
            if conf >= self.min_conf:
                brl.append((frequent_set - conseq, conseq, conf))
                pruned_item_list.append(conseq)
        return pruned_item_list

    def rules_from_consequent(self, frequent_set, itemset_list, brl):
        itemset_size = len(itemset_list[0])
        # Try further merging
        if len(frequent_set) > (itemset_size + 1):
            # Create Hm+1 new candidates
            augmented_item_list = apriori_gen(itemset_list, itemset_size+1)
            augmented_item_list = self.calc_confidence(
                frequent_set,
                augmented_item_list,
                brl,
                )
            if len(augmented_item_list) > 1:
                self.rules_from_consequent(
                    frequent_set,
                    augmented_item_list,
                    brl,
                    )

    def generate(self):
        big_rule_list = []
        # Get only sets with two or more items
        for i in range(1, len(self.frequent_itemsets)):
            for frequent_set in self.frequent_itemsets[i]:
                item_list_1 = [frozenset([item]) for item in frequent_set]
                if i > 1:
                    self.rules_from_consequent(
                        frequent_set,
                        item_list_1,
                        big_rule_list,
                        )
                else:
                    self.calc_confidence(
                        frequent_set,
                        item_list_1,
                        big_rule_list,
                        )
        return big_rule_list

def generate_rules(frequent_itemsets, support_data, min_conf=0.7):

    this_miner = RuleMiner(frequent_itemsets, support_data, min_conf)
    return this_miner.generate()
