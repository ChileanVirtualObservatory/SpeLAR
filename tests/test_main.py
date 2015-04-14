import unittest
from arl import apriori, fpgrowth
from arl.association_rules import AssociationRule

class TestMainApp(unittest.TestCase):

	def setUp(self):
		self.spectra = [
			{'id': 1, 'itemlist': [84.03675,84.58818,84.83367], "meta": None},
			{'id': 2, 'itemlist': [84.03675,84.32088,84.58818,84.52117,84.83367], "meta": None},
			{'id': 3, 'itemlist': [84.03675,84.58818,84.53117,84.83367], "meta": None},
			{'id': 4, 'itemlist': [84.37009,84.47945], "meta": None}
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
		"""
		self.rules = set([
			(frozenset([84.83367]),frozenset([84.03675]), 1.0),
			(frozenset([84.03675]), frozenset([84.83367]), 1.0),
			(frozenset([84.58818]), frozenset([84.03675]), 1.0),
			(frozenset([84.03675]), frozenset([84.58818]), 1.0),
			(frozenset([84.58818]), frozenset([84.83367]), 1.0),
			(frozenset([84.83367]), frozenset([84.58818]), 1.0),
			(frozenset([84.58818]), frozenset([84.03675, 84.83367]), 1.0),
			(frozenset([84.83367]), frozenset([84.03675, 84.58818]), 1.0),
			(frozenset([84.03675]), frozenset([84.83367, 84.58818]), 1.0)
		])
		"""
		self.rules = set([
			AssociationRule([84.83367],[84.03675],0.75, 0.75, 0.75),
			AssociationRule([84.03675],[84.83367],0.75, 0.75, 0.75),
			AssociationRule([84.58818],[84.03675],0.75, 0.75, 0.75),
			AssociationRule([84.03675],[84.58818],0.75, 0.75, 0.75),
			AssociationRule([84.58818],[84.83367],0.75, 0.75, 0.75),
			AssociationRule([84.83367],[84.58818],0.75, 0.75, 0.75),
			AssociationRule([84.58818],[84.03675, 84.83367],0.75, 0.75, 0.75),
			AssociationRule([84.83367],[84.03675, 84.58818],0.75, 0.75, 0.75),
			AssociationRule([84.03675],[84.83367, 84.58818],0.75, 0.75, 0.75)
		])


	def test_apriori(self):
		this_itemsets, this_rules = apriori.run(self.spectra, 0.5, 0.5)
		self.assertTrue(set(this_itemsets) == self.frequent_itemsets)
		self.assertTrue(set(this_rules) == self.rules)

	def test_fpgrowth(self):
		this_itemsets, this_rules = fpgrowth.run(self.spectra, 0.5, 0.5)
		self.assertTrue(set(this_rules) == self.rules)
		self.assertTrue(set(this_itemsets) == self.frequent_itemsets)

if __name__ == '__main__':
    unittest.main()