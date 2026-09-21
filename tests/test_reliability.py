# SPDX-License-Identifier: GPL-3.0-only
import unittest
from app import rollout,expert

class RolloutBoundTests(unittest.TestCase):
    def test_invalid_limits_reject_before_policy(self):
        state={'kind':'billing','verified':False,'resolved':False}
        calls=[]
        for limit in (0,-1,True,1.5,1001):
            with self.assertRaises(ValueError): rollout(state,lambda s:calls.append(s),limit)
        self.assertEqual(calls,[])
    def test_truncated_rollout_retains_progress(self):
        state={'kind':'billing','verified':False,'resolved':False}
        result=rollout(state,expert,1)
        self.assertEqual(result['status'],'step-limit')
        self.assertEqual(result['trace'][0]['action'],'verify')
        self.assertFalse(state['verified'])
    def test_invalid_initial_state_rejected_before_policy(self):
        calls=[]
        with self.assertRaises(ValueError): rollout({'kind':'billing'},lambda s:calls.append(s))
        self.assertEqual(calls,[])
