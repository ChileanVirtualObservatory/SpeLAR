"""
This file is part of ChiVO
Copyright (C) Nicolas Miranda

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
# -*- coding: utf-8 -*-

"""
Spelar Module

This module contains scripts that receive the commands and options from the
user in order to run the Asociation Rule Analysis of spectral line in the
given spectral line data source.

Example:

    $ python spelar.py -ap test.csv
"""

from arl import apriori, fpgrowth, association_rules
import argparse
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

    group_output = parser.add_mutually_exclusive_group()
    group_output.add_argument('-l', '--latex', help="Path for output table with association rules in LaTeX format")
    group_output.add_argument('-c', '--csv', help="Path for output table with association rules in csv format")

    group_algorithm = parser.add_mutually_exclusive_group(required=True)
    group_algorithm.add_argument('-ap', '--apriori', action="store_true", help="Run with Apriori algorithm for frequent itemset generation")
    group_algorithm.add_argument('-fp', '--fpgrowth', action="store_true", help="Run with FP-Growth algorithm for frequent itemset generation")

    args = parser.parse_args()

    in_file = args.in_file

    spectra = parse_csv(in_file)

    if args.apriori:
        spectra = parse_csv(in_file)
        itemsets, rules = apriori.run(spectra, args.min_sup, args.min_conf)
    elif args.fpgrowth:
        spectra = parse_csv(in_file)
        itemsets, rules = fpgrowth.run(spectra, args.min_sup, args.min_conf)

    num_rules = len(rules)
    num_itemsets = len(itemsets)

    #print "items:\n%s\n" % itemsets

    rules = sorted(rules, key=lambda x: x.lift(), reverse=True)
    rules = sorted(rules, key=lambda x: x.support(), reverse=True)
    #rules = sorted(rules, key=lambda x: x.confidence(), reverse=True)
    

    max_rules = -1
    if (len(rules) > max_rules) and (max_rules > 0):
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

        meta_types = set([])
        for rule in rules:
            for meta_type in rule.meta_data.keys():
                meta_types.add(meta_type)
        #print meta_types
        #print len(meta_types)

        with open(args.latex, 'w') as latex_file:
            latex_file.write("\\begin{longtable}{| c | l | c | c | c | c | c | c | c |}\n")
            latex_file.write("\\hline\n")
            latex_file.write("\\textbf{N} & \\textbf{Rule} & \\textbf{Supp} & \\textbf{Conf} & \\textbf{Lift} & \\textbf{STAR} & \\textbf{GALAXY} & \\textbf{QSO} & \\textbf{STAR_LATE} \\\ \\hline\n")
            for index, rule in enumerate(rules):

                total = sum(rule.meta_data.values())

                latex_file.write(
                    "%d & $\\begin{array}{c c c}\\left\\{\\begin{array}{c}%s\\end{array}\\right\\} & \\Rightarrow & \\left\\{\\begin{array}{c}%s\\end{array}\\right\\}\\end{array}$ & %.2f & %.2f & %.2f & %d & %d & %d & %d \\\ \\hline\n" % (index+1, rule.get_antec_descr_tex().replace("_", "\_"), rule.get_conseq_descr_tex().replace("_", "\_"), rule.support(), rule.confidence(), rule.lift(), rule.meta_data.get('1',0), rule.meta_data.get('2',0), rule.meta_data.get('3',0), rule.meta_data.get('6',0))
                    )
            latex_file.write("\\end{longtable}")

        """
        with open(args.latex, 'w') as latex_file:
            latex_file.write("\\begin{longtable}{| c | l | c | c | c |}\n")
            latex_file.write("\\hline\n")
            latex_file.write("\\textbf{N} & \\textbf{Rule} & \\textbf{Support} & \\textbf{Confidence} & \\textbf{Lift} \\\ \\hline\n")
            for index, rule in enumerate(rules):
                latex_file.write(
                    "%d & $\\begin{array}{c c c}\\left\\{\\begin{array}{c}%s\\end{array}\\right\\} & \\Rightarrow & \\left\\{\\begin{array}{c}%s\\end{array}\\right\\}\\end{array}$ & %.2f & %.2f & %.2f \\\ \\hline\n" % (index+1, rule.get_antec_descr_tex().replace("_", "\_"), rule.get_conseq_descr_tex().replace("_", "\_"), rule.support(), rule.confidence(), rule.lift())
                    )
            latex_file.write("\\end{longtable}")
        """

        """
        with open(args.latex, 'w') as latex_file:
            latex_file.write("\\begin{longtable}{| c | l | c | c | c | c | c | c | c | c | c | c | c | c | c | c | c | c | c | c | c | c | c |}\n")
            latex_file.write("\\hline\n")
            latex_file.write("\\textbf{N} & \\textbf{Rule} & \\textbf{Supp} & \\textbf{Conf} & \\textbf{Lift} & \\textbf{SF} & \\textbf{SSD} & \\textbf{SBD} & \\textbf{QSO} & \\textbf{StB} & \\textbf{SP} & \\textbf{SC} & \\textbf{HS} & \\textbf{SR} & \\textbf{RS} & \\textbf{SWD} & \\textbf{RD} & \\textbf{SD} & \\textbf{SCV} & \\textbf{SRD} & \\textbf{SM} & \\textbf{Gal} & \\textbf{SeB} \\\ \\hline\n")
            for index, rule in enumerate(rules):

                total = sum(rule.meta_data.values())

                latex_file.write(
                    "%d & $\\begin{array}{c c c}\\left\\{\\begin{array}{c}%s\\end{array}\\right\\} & \\Rightarrow & \\left\\{\\begin{array}{c}%s\\end{array}\\right\\}\\end{array}$ & %.2f & %.2f & %.2f & %d & %d & %d & %d & %d & %d & %d & %d & %d & %d & %d & %d & %d & %d & %d & %d & %d & %d \\\ \\hline\n" % (index+1, rule.get_antec_descr_tex().replace("_", "\_"), rule.get_conseq_descr_tex().replace("_", "\_"), rule.support(), rule.confidence(), rule.lift(), rule.meta_data.get('SERENDIPITY_FIRST',0), rule.meta_data.get('STAR_SUB_DWARF',0), rule.meta_data.get('STAR_BROWN_DWARF',0), rule.meta_data.get('QSO',0), rule.meta_data.get('STAR_BHB',0), rule.meta_data.get('STAR_PN',0), rule.meta_data.get('STAR_CARBON',0), rule.meta_data.get('HOT_STD',0), rule.meta_data.get('SERENDIPITY_RED',0), rule.meta_data.get('REDDEN_STD',0), rule.meta_data.get('STAR_WHITE_DWARF',0), rule.meta_data.get('ROSAT_D',0), rule.meta_data.get('SERENDIPITY_DISTANT',0), rule.meta_data.get('STAR_CATY_VAR',0), rule.meta_data.get('STAR_RED_DWARF',0), rule.meta_data.get('SERENDIPITY_MANUAL',0), rule.meta_data.get('GALAXY',0), rule.meta_data.get('SERENDIPITY_BLUE',0))
                    )
            latex_file.write("\\end{longtable}")

        """

    else:
        for rule in rules:
            """
            if 8544 in rule.antecedent:
                print rule
            """
            print rule

    print "\n\nNumber of frequent itemsets: %d" % num_itemsets
    print "Number of rules: %d\n" % num_rules

def parse_csv(in_file, meta=False):
    """
    Args: the path of a csv file with the transaction data

    Returns: a list of transactions (lists)
    """

    transactions = []

    with open(in_file) as this_file:

        reader = csv.reader(this_file)

        for row in reader:
            this_id = row[0]
            #import ipdb;ipdb.set_trace()
            if meta:
                this_meta = row[1]
                this_items = row[2]
            else:
                this_meta = None
                this_items = row[1]

            split_items = this_items.split(',')
            this_trans = {'id': this_id, 'meta': this_meta, 'itemlist': map(float,split_items)}
            transactions.append(this_trans)

        """
        for line in this_file:
            split_content = line.rstrip('\n').split(',')

            if ignore == 0:
                if meta:
                    this_trans = {'id': split_content[0], 'meta': split_content[1], 'items': map(int,split_content[2:])}
                else:
                    this_trans = {'id':split_content[0], ''}
            else:
                this_trans = map(int,split_content[ignore:])

            transactions.append(this_trans)
        """

        #content = this_file.readlines()

    #return [map(int, x.rstrip('\n').split(',')) for x in content]
    return transactions

    #return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]

if __name__ == '__main__':
    main()
