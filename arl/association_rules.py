#This file is part of ChiVO, the Chilean Virtual Observatory
#A project sponsored by FONDEF (D11I1060)
#Copyright (C) 2015 Universidad Tecnica Federico Santa Maria Mauricio Solar
#                                                            Marcelo Mendoza
#                   Universidad de Chile                     Diego Mardones
#                   Pontificia Universidad Catolica          Karim Pichara
#                   Universidad de Concepcion                Ricardo Contreras
#                   Universidad de Santiago                  Victor Parada
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from tools import apriori_gen
#from fpgrowth import get_support

def add_descriptions(rules, descriptions):
    for rule in rules:
        rule.descriptions = descriptions

def format_description(description):
    if description:
        return ' (' + description + ')'
    else:
        return ' (UNIDENTIFIED)'

class AssociationRule(object):

    def __init__(self, antecedent, consequent, support, supp_antecedent, supp_consequent, meta_data=None):
        super(AssociationRule, self).__init__()
        self.antecedent = frozenset(antecedent)
        self.consequent = frozenset(consequent)
        self.supp = support
        self.supp_antecedent = supp_antecedent
        self.supp_consequent = supp_consequent
        self.descriptions = None
        self.meta_data = meta_data

    def __hash__(self):
        return hash(hash(self.antecedent) + hash(self.consequent) + self.supp + self.supp_antecedent + self.supp_consequent)

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
            and self.antecedent == other.antecedent \
            and self.consequent == other.consequent \
            and self.supp == other.supp \
            and self.supp_antecedent == other.supp_consequent \
            and self.supp_consequent == other.supp_consequent

    def support(self):
        return self.supp

    def confidence(self):
        return self.supp / self.supp_antecedent

    def lift(self):
        return self.supp / (self.supp_antecedent * self.supp_consequent)

    def get_itemsets_desctiptions(self):
        antecedent = []
        consequent = []
        for item in self.antecedent:
            if self.descriptions:
                this_description = self.descriptions.get(str(item), "")
            else:
                this_description = ""
            this_tuple = (item, this_description)
            antecedent.append(this_tuple)
        for item in self.consequent:
            if self.descriptions:
                this_description = self.descriptions.get(str(item), "")
            else:
                this_description = ""
            this_tuple = (item, this_description)
            consequent.append(this_tuple)
        return antecedent, consequent

    def format_itemset(self, itemset):
        items_repr = []
        for item in sorted(list(itemset)):
            if self.descriptions:
                this_repr = "%s%s" % (item, format_description(self.descriptions.get(str(item))))
            else:
                this_repr = item.__str__()
            items_repr.append(this_repr)
        return ", ".join(items_repr)

    def format_itemset_tex(self, itemset):
        items_repr = []
        for item in sorted(list(itemset)):
            if self.descriptions:
                this_repr = "%s%s" % (item, format_description(self.descriptions.get(str(item))))
            else:
                this_repr = item.__str__()
            items_repr.append(this_repr)
        return " \\\ ".join(items_repr)

    def get_antec_descr(self):
        return self.format_itemset(self.antecedent)

    def get_antec_descr_tex(self):
        return self.format_itemset_tex(self.antecedent)

    def get_conseq_descr(self):
        return self.format_itemset(self.consequent)

    def get_conseq_descr_tex(self):
        return self.format_itemset_tex(self.consequent)

    def __str__(self):
        return "<%s => %s | sup: %.2f | conf: %.2f | meta: %s>" % (self.get_antec_descr(), self.get_conseq_descr(), self.support(), self.confidence(), self.meta_data)

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

    def calc_confidence(self, frequent_set, itemset_list, brl):
        pruned_item_list = []
        num_items = 4

        for conseq in itemset_list:
            this_rule = AssociationRule(frequent_set - conseq, conseq, self.get_support(frequent_set), self.get_support(frequent_set - conseq), self.get_support(conseq))
            if this_rule.confidence() >= self.min_conf:
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
