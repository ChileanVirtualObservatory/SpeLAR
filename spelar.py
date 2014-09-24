import argparse
import apriori
import fpgrowth

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("in_file")

	args = parser.parse_args()

	in_file = args.in_file

	spectra = parse_csv(in_file)

	L, suppData, ap_rules = apriori.run(spectra)

	print "apriori_items:\n%s\n" % L
	print "apriori_rules:\n%s\n" % ap_rules


	fp_items, fp_rules = fpgrowth.run(spectra)
	print "fp_items:\n%s\n" % fp_items
	print "fp_rules:\n%s\n" % fp_rules

def parse_csv(in_file):
	
	with open(in_file) as f:
		content = f.readlines()

	return [map(float, x.rstrip('\n').split(',')) for x in content]

	#return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]

if __name__ == '__main__':
	main()