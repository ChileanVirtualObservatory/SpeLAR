# -*- coding: utf-8 -*-

"""
Spelar Module

This module contains scripts that receive the commands and options from the
user in order to run the Asociation Rule Analysis of spectral line in the
given spectral line data source.

Example:

    $ python spelar.py -ap test.csv
"""

import apriori
import argparse
import fpgrowth
import association_rules

def main():
    """Main function invoked by command line. Receives, processes parameters
    and calls respective algorithms.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("in_file")

    group_algorithm = parser.add_mutually_exclusive_group(required=True)
    group_algorithm.add_argument('-ap', '--apriori', action="store_true", help="Run with Apriori algorithm for frequent itemset generation")
    group_algorithm.add_argument('-fp', '--fpgrowth', action="store_true", help="Run with FP-Growth algorithm for frequent itemset generation")

    args = parser.parse_args()

    in_file = args.in_file

    spectra = parse_csv(in_file)

    if args.apriori:
        itemsets, rules = apriori.run(spectra)
    elif args.fpgrowth:
        itemsets, rules = fpgrowth.run(spectra)

    print "items:\n%s\n" % itemsets
    print "rules:\n%s\n" % rules

def parse_csv(in_file):
    """
    Args: the path of a csv file with the transaction data

    Returns: a list of transactions (lists)
    """

    with open(in_file) as this_file:
        content = this_file.readlines()

    return [map(float, x.rstrip('\n').split(',')) for x in content]

    #return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]

if __name__ == '__main__':
    main()
