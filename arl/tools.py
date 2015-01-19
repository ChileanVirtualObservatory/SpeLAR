
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