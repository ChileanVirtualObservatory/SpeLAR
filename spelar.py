# -*- coding: utf-8 -*-

"""
Spelar Module

This module contains scripts that receive the commands and options from the
user in order to run the Asociation Rule Analysis of spectral line in the
given spectral line data source.

Example:

    $ python spelar.py test.csv
"""

import argparse
import apriori
import fpgrowth

def main():
    """Main function invoked by command line. Receives, processes parameters
    and calls respective algorithms.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("in_file")

    args = parser.parse_args()

    in_file = args.in_file

    spectra = parse_csv(in_file)

    ap_itemsets, support_data, ap_rules = apriori.run(spectra)

    print "apriori_items:\n%s\n" % ap_itemsets
    print "apriori_rules:\n%s\n" % ap_rules


    fp_itemsets, fp_rules = fpgrowth.run(spectra)
    print "fp_items:\n%s\n" % fp_itemsets
    print "fp_rules:\n%s\n" % fp_rules

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
