import unittest
from evaluation import demo, evaluate_cases
from app import dataset, train

class HoldoutTests(unittest.TestCase):
    def test_reports_seen_and_heldout_separately(self):
        p = demo()['partitions']
        self.assertEqual(p['seen_initial_state']['completed'],1)
        self.assertEqual(p['held_out_initial_state']['cases'],2)
        self.assertEqual(p['held_out_initial_state']['handoffs'],2)
        self.assertEqual(p['held_out_initial_state']['invalid_actions'],0)
    def test_duplicate_cases_rejected(self):
        case = {'id':'a','state':{'kind':'access','verified':False,'resolved':False}}
        with self.assertRaises(ValueError):evaluate_cases(train(dataset()),[case,case])
    def test_empty_evaluation_has_zero_counts(self):
        p = evaluate_cases(train(dataset()),[])['partitions']
        self.assertTrue(all(x['cases']==0 for x in p.values()))
