"""
apriori module

This module contains an implementation of the Apriori algorithm for
association rule learning.

Example:

    frequent_items, support_info, association_rules = apriori.run(data_set)
"""

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

def apriori_gen(frequent_itemsets, k):
    """Generates frequent itemsets of size k from a list of itemsets of size k-1

    Args:
        frequent_itemsets: a list of frequent itemsets
        k: the size of the frequent itemsets to generate

    Returns:
        ret_list: a list of the frequent itemsets of size k
    """
    ret_list = []
    len_freq_itemsets = len(frequent_itemsets)
    for i in range(len_freq_itemsets):
        for j in range(i+1, len_freq_itemsets):
            # Join sets if first k-2 items are equal
            set_1 = list(frequent_itemsets[i])[:k-2]
            set_2 = list(frequent_itemsets[j])[:k-2]
            set_1.sort()
            set_2.sort()
            if set_1 == set_2:
                ret_list.append(frequent_itemsets[i] | frequent_itemsets[j])

    return ret_list

def apriori(dataset, min_support=0.5):
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
    return frequent_itemsets, support_data

def calc_confidence(frequent_set, itemset_list, support_data, brl, min_conf):
    """Evaluates a set of candidate rules by calculating their confidence and
    saving the ones that meet the minimum confidence

    Args:
        frequent_set: a frequent set from which to generate the rules
        itemset_list: a list of itemsets from which to generate the consecuent
            of the rules
        support_data: dictionary with the number of times each item is present
            in the dataset
        brl: a list to which the generated rules will be appended
        min_conf: minimum confidence the generated rules must meet

    Returns:
        pruned_item_list: a list of possible rule generating items to be
            mined still
    """
    pruned_item_list = []
    for conseq in itemset_list:
        conf = support_data[frequent_set]/support_data[frequent_set - conseq]
        if conf >= min_conf:
            brl.append((frequent_set - conseq, conseq, conf))
            pruned_item_list.append(conseq)
    return pruned_item_list

def rules_from_consequent(
    frequent_set,
    itemset_list,
    support_data,
    brl,
    min_conf):
    """Generates association rules recursively using a frequent itemset
    as consecuent.

    Args:
        frequent_set: a frequent itemset
        itemset_list: a list of items that could be on the consecuent of
            the rule
        support_data: dictionary with the number of times each frequent
            itemset is present in the dataset
        brl: a list to which the generated rules will be appended
        min_conf: minimum confidence the generated rules must meet
    """
    itemset_size = len(itemset_list[0])
    # Try further merging
    if len(frequent_set) > (itemset_size + 1):
        # Create Hm+1 new candidates
        augmented_item_list = apriori_gen(itemset_list, itemset_size+1)
        augmented_item_list = calc_confidence(
            frequent_set,
            augmented_item_list,
            support_data,
            brl,
            min_conf
            )
        if len(augmented_item_list) > 1:
            rules_from_consequent(
                frequent_set,
                augmented_item_list,
                support_data,
                brl,
                min_conf
                )

def generate_rules(frequent_itemsets, support_data, min_conf=0.7):
    """Generates association rules from a set of frequent itemsets

    Args:
        frequent_itemsets: a set of frequent itemsets
        support_data: dictionary with the number of times each frequent
            itemset is present in the dataset
        min_conf: minimum confidence the generated rules must meet
    """
    big_rule_list = []
    # Get only sets with two or more items
    for i in range(1, len(frequent_itemsets)):
        for frequent_set in frequent_itemsets[i]:
            item_list_1 = [frozenset([item]) for item in frequent_set]
            if i > 1:
                rules_from_consequent(
                    frequent_set,
                    item_list_1,
                    support_data,
                    big_rule_list,
                    min_conf
                    )
            else:
                calc_confidence(
                    frequent_set,
                    item_list_1,
                    support_data,
                    big_rule_list,
                    min_conf
                    )
    return big_rule_list

def run(dataset):
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

    frequent_itemsets, support_data = apriori(dataset, min_support=0.5)
    rules = generate_rules(frequent_itemsets, support_data, min_conf=0.7)

    return frequent_itemsets, support_data, rules
