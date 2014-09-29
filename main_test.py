import unittest
import spelar
import apriori
import fpgrowth

class TestMainApp(unittest.TestCase):

	def setUp(self):
		self.spectra = [
			[84.03675, 84.58818, 84.83367],
			[84.03675, 84.32088, 84.58818, 84.52117, 84.83367],
			[84.03675, 84.58818, 84.53117, 84.83367],
			[84.37009, 84.47945]
		]

		self.frequent_itemsets = set([
			frozenset([84.58818]),
			frozenset([84.03675]),
			frozenset([84.83367]),
			frozenset([84.03675, 84.83367]),
			frozenset([84.03675, 84.58818]),
			frozenset([84.83367, 84.58818]),
			frozenset([84.03675, 84.83367, 84.58818])
		])

		self.rules = set([
			(frozenset([84.83367]),frozenset([84.03675]), 1.0),
			(frozenset([84.03675]), frozenset([84.83367]), 1.0),
			#(frozenset([84.58818]), frozenset([84.03675]), 1.0),
			(frozenset([84.03675]), frozenset([84.58818]), 1.0),
			(frozenset([84.58818]), frozenset([84.83367]), 1.0),
			(frozenset([84.83367]), frozenset([84.58818]), 1.0),
			(frozenset([84.58818]), frozenset([84.03675, 84.83367]), 1.0),
			(frozenset([84.83367]), frozenset([84.03675, 84.58818]), 1.0),
			(frozenset([84.03675]), frozenset([84.83367, 84.58818]), 1.0)
		])


	def test_apriori(self):
		this_itemsets, this_rules = apriori.run(self.spectra)
		self.assertTrue(set(this_itemsets) == self.frequent_itemsets)
		self.assertTrue(set(this_rules) == self.rules)

	def test_fpgrowth(self):
		this_itemsets, this_rules = fpgrowth.run(self.spectra)
		self.assertTrue(set(this_rules) == self.rules)
		self.assertTrue(set(this_itemsets) == self.frequent_itemsets)