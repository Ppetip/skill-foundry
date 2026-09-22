# SPDX-License-Identifier: GPL-3.0-only
import unittest
from challenge import demo
from app import dataset

class ChallengeTests(unittest.TestCase):
    def test_corrupted_teacher_cannot_refund_before_verification(self):
        trial=next(t for t in demo()['trials'] if t['id']=='corrupted-teacher')
        self.assertEqual(trial['status'],'invalid-action')
        self.assertEqual(len(trial['trace']),1)
        self.assertFalse(trial['trace'][0]['state']['verified'])
        self.assertEqual(trial['trace'][0]['action'],'refund')
    def test_changed_states_handoff_without_action(self):
        trials={t['id']:t for t in demo()['trials']}
        for name in ['unseen-combination','new-kind']:
            self.assertEqual(trials[name]['status'],'handoff')
            self.assertEqual(len(trials[name]['trace']),1)
        self.assertEqual(trials['known']['status'],'complete')
    def test_challenge_does_not_pollute_expert_dataset(self):
        before=dataset();demo();self.assertEqual(dataset(),before)
