from tools import apriori_gen
#from fpgrowth import get_support

def add_descriptions(rules, descriptions):
    for rule in rules:
        rule.descriptions = descriptions

def format_description(description):
    if description:
        return ' (' + description + ')'
    else:
        return ''

class AssociationRule(object):

    def __init__(self, antecedent, consequent, support, confidence):
        super(AssociationRule, self).__init__()
        self.antecedent = frozenset(antecedent)
        self.consequent = frozenset(consequent)
        self.support = support
        self.confidence = confidence
        self.descriptions = None

    def __hash__(self):
        return hash(hash(self.antecedent) + hash(self.consequent) + self.support + self.confidence)

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
            and self.antecedent == other.antecedent \
            and self.consequent == other.consequent \
            and self.support == other.support \
            and self.confidence == other.confidence

    def format_itemset(self, itemset):
        items_repr = []
        for item in sorted(list(itemset)):
            if self.descriptions:
                this_repr = "%s%s" % (item, format_description(self.descriptions.get(str(item))))
            else:
                this_repr = item.__str__()
            items_repr.append(this_repr)
        return ", ".join(items_repr)

    def get_antec_descr(self):
        return self.format_itemset(self.antecedent)

    def get_conseq_descr(self):
        return self.format_itemset(self.consequent)

    def __str__(self):
        return "<%s => %s | sup: %.2f | conf: %.2f>" % (self.get_antec_descr(), self.get_conseq_descr(), self.support, self.confidence)

class RuleMiner(object):
    """A class for mining asociation rules using Apriori algorithm
    """
    def __init__(self, frequent_itemsets, support_data_struct, min_conf):
        super(RuleMiner, self).__init__()
        self.frequent_itemsets = frequent_itemsets
        self.support_data_struct = support_data_struct
        self.min_conf = min_conf

    def get_support(self, this_set):
        return self.support_data_struct[this_set]

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
                #brl.append((frequent_set - conseq, conseq, conf))
                this_rule = AssociationRule(frequent_set - conseq, conseq, self.get_support(frequent_set), conf)
                brl.append(this_rule)
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
