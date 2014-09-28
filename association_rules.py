from tools import apriori_gen
#from fpgrowth import get_support

class RuleMiner(object):
    """A class for mining asociation rules using Apriori algorithm
    """
    def __init__(self, frequent_itemsets, support_data_struct, min_conf):
        super(RuleMiner, self).__init__()
        self.frequent_itemsets = frequent_itemsets
        self.support_data_struct = support_data_struct
        self.min_conf = min_conf

    def get_confidence(self, antecedent, consequent):
        return self.support_data_struct[antecedent]/self.support_data_struct[antecedent - consequent]

    def calc_confidence(self, frequent_set, itemset_list, brl):
        pruned_item_list = []
        num_items = 4
        for conseq in itemset_list:
            """
            if (type(self.support_data_struct.values()[0]) is float):
                conf = self.support_data_struct[frequent_set]/self.support_data_struct[frequent_set - conseq]
            else:
                support_a = get_support(frequent_set, self.support_data_struct, num_items)
                support_b = get_support(frequent_set - conseq, self.support_data_struct, num_items)
                conf = support_a/support_b
            """
            conf = self.get_confidence(frequent_set, conseq)
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
        for frequent_itemset in self.frequent_itemsets:
            if len(frequent_itemset) >= 2:
                item_list_1 = [frozenset([item]) for item in frequent_itemset]
                if len(frequent_itemset) == 2:
                    self.calc_confidence(frequent_itemset, item_list_1, big_rule_list)
                else:
                    self.rules_from_consequent(frequent_itemset, item_list_1, big_rule_list)
        return big_rule_list

"""
def generate_rules(frequent_itemsets, support_data_struct, min_conf=0.7):

    this_miner = RuleMiner(frequent_itemsets, support_data_struct, min_conf)
    return this_miner.generate()    
"""
