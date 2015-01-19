"""
apriori module

This module contains an implementation of the Apriori algorithm for
association rule learning.

Example:

    frequent_items, support_info, association_rules = apriori.run(data_set)
"""

from tools import apriori_gen
from association_rules import RuleMiner

def one_item_sets(data_set):
    """Creates a superset containing a set for each one of the items in a
    transaction data set; in other words, a set of candidate itemsets
    of size one.

    Args:
        data_set (iterable (iterable)): a set of transactions

    Returns:
        A list with all the one-item sets as frozensets
    """
    result = []
    for transaction in data_set:
        for item in transaction:
            if not [item] in result:
                result.append([item])
    result.sort()
    return map(frozenset, result)

def scan_data(dataset, candidate_sets, min_support):
    """Generates frecuent itemsets from candidate sets by scanning over
    the transaction dataset.

    Args:
        dataset (list (iterable)): a dataset of transactions
        candidate_sets (list (hashable)): a list of candidate sets
        min_support: minimum support

    Returns:
        ret_list: a list of frequent itemsets
        support_data: a dictionary with counts for each itemset
    """
    candidate_count = {}
    for tid in dataset:
        for can in candidate_sets:
            if can.issubset(tid):
                if not candidate_count.has_key(can):
                    candidate_count[can] = 1
                else:
                    candidate_count[can] += 1
    num_items = float(len(dataset))
    ret_list = []
    support_data = {}
    for key in candidate_count:
        # Calculate support for every itemset
        support = candidate_count[key]/num_items
        if support >= min_support:
            ret_list.insert(0, key)
        support_data[key] = support
    return ret_list, support_data

def apriori(dataset, min_support):
    """
    Args:
        dataset (iterable (iterable)): a dataset of transactions
        min_support: minimum support of itemsets to generate

    Returns:
        frequent_itemsets: a set of the itemsets with support over minimum
        support_data: dictionary with the number of times each item is present
            in the dataset
    """
    this_one_itemsets = one_item_sets(dataset)
    this_dataset = map(set, dataset)
    len_1_freq_itemsets, support_data = scan_data(
        this_dataset,
        this_one_itemsets,
        min_support
        )
    frequent_itemsets = [len_1_freq_itemsets]
    k = 2
    while len(frequent_itemsets[k-2]) > 0:
        candidate_sets = apriori_gen(frequent_itemsets[k-2], k)
        # Scan data set to get frequent itemsets from candidate sets
        freq_itemsets_k, supp_data_k = scan_data(
            this_dataset,
            candidate_sets,
            min_support
            )
        support_data.update(supp_data_k)
        frequent_itemsets.append(freq_itemsets_k)
        k += 1

    frequent_itemsets = [x for itemset in frequent_itemsets for x in itemset]

    return frequent_itemsets, support_data

def generate_rules(frequent_itemsets, support_data, min_conf):

    this_miner = RuleMiner(frequent_itemsets, support_data, min_conf)
    return this_miner.generate()

def run(dataset, min_support, min_conf):
    """Runs the apriori algorithm for frequent itemset and asociation
    rule generation.

    Args:
        dataset: a dataset of transactions from which to find frequent itemsets
            and association rules

    Returns:
        frequent_itemsets: a set of frequent itemsets found
        support_data: dictionary with the number of times each frequent
            itemset is present in the dataset
        rules: a set of association rules mined from the dataset
    """

    flat_dataset = [trans['itemlist'] for trans in dataset]

    frequent_itemsets, support_data = apriori(flat_dataset, min_support)

    rules = generate_rules(frequent_itemsets, support_data, min_conf)

    return frequent_itemsets, rules
