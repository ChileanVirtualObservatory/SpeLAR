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
import csv

def main():
    """Main function invoked by command line. Receives, processes parameters
    and calls respective algorithms.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("in_file", help="CSV input file")
    parser.add_argument("min_sup", help="Minimum support", type=float)
    parser.add_argument("min_conf", help="Minimum confidence", type=float)
    parser.add_argument('-d', '--descriptions', help="CSV with item IDs and descriptions to display")
    parser.add_argument('-tex', '--latex', help="Output table with association rules in LaTeX format")

    group_algorithm = parser.add_mutually_exclusive_group(required=True)
    group_algorithm.add_argument('-ap', '--apriori', action="store_true", help="Run with Apriori algorithm for frequent itemset generation")
    group_algorithm.add_argument('-fp', '--fpgrowth', action="store_true", help="Run with FP-Growth algorithm for frequent itemset generation")

    args = parser.parse_args()

    in_file = args.in_file

    spectra = parse_csv(in_file)

    if args.apriori:
        itemsets, rules = apriori.run(spectra, args.min_sup, args.min_conf)
    elif args.fpgrowth:
        itemsets, rules = fpgrowth.run(spectra, args.min_sup, args.min_conf)

    num_rules = len(rules)
    num_itemsets = len(itemsets)

    #print "items:\n%s\n" % itemsets

    #rules = sorted(rules, key=lambda x: x.support(), reverse=True)
    #rules = sorted(rules, key=lambda x: x.confidence(), reverse=True)
    rules = sorted(rules, key=lambda x: x.lift(), reverse=True)

    max_rules = 250
    if len(rules) > max_rules:
        rules = rules[:max_rules]

    if args.descriptions:
        ids_descriptions = dict()
        with open(args.descriptions, 'r') as descr_file:
            reader = csv.reader(descr_file)
            next(reader, None)
            for row in reader:
                ids_descriptions[row[1]] = row[0]
        association_rules.add_descriptions(rules, ids_descriptions)
    
    if args.latex:
        with open(args.latex, 'w') as latex_file:
            latex_file.write("\\begin{longtable}{| c | l | c | c | c |}\n")
            latex_file.write("\\hline\n")
            latex_file.write("\\textbf{N} & \\textbf{Rule} & \\textbf{Support} & \\textbf{Confidence} & \\textbf{Lift} \\\ \\hline\n")
            for index, rule in enumerate(rules):
                latex_file.write(
                    "%d & $\\begin{array}{c c c}\\left\\{\\begin{array}{c}%s\\end{array}\\right\\} & \\Rightarrow & \\left\\{\\begin{array}{c}%s\\end{array}\\right\\}\\end{array}$ & %.2f & %.2f & %.2f \\\ \\hline\n" % (index+1, rule.get_antec_descr_tex().replace("_", "\_"), rule.get_conseq_descr_tex().replace("_", "\_"), rule.support(), rule.confidence(), rule.lift())
                    )
            latex_file.write("\\end{longtable}")

    else:
        for rule in rules:
            print rule

    print "\n\nNumber of frequent itemsets: %d" % num_itemsets
    print "Number of rules: %d\n" % num_rules

def parse_csv(in_file):
    """
    Args: the path of a csv file with the transaction data

    Returns: a list of transactions (lists)
    """

    with open(in_file) as this_file:
        content = this_file.readlines()

    return [map(int, x.rstrip('\n').split(',')) for x in content]

    #return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]

if __name__ == '__main__':
    main()
