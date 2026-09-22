# SPDX-License-Identifier: GPL-3.0-only
import unittest
from unittest.mock import patch
from app import audit_teacher, step, rollout

class IndependentEnvironmentTests(unittest.TestCase):
    def test_faulty_teacher_is_rejected_by_environment(self):
        state={'kind':'billing','verified':False,'resolved':False}
        with patch('app.expert',return_value='refund'):
            result=rollout(state,lambda s:'refund')
            self.assertEqual(result['status'],'invalid-action')
            audit=audit_teacher([{'id':'bad','state':state,'action':'refund'}])
            self.assertEqual(audit['accepted_ids'],[])
            self.assertEqual(len(audit['rejected']),1)

    def test_transitions_work_without_calling_teacher(self):
        with patch('app.expert',side_effect=AssertionError('environment called teacher')):
            state={'kind':'billing','verified':False,'resolved':False}
            state,status=step(state,'verify');self.assertEqual(status,'running')
            state,status=step(state,'refund');self.assertEqual(status,'running')
            state,status=step(state,'close');self.assertEqual(status,'complete')

    def test_unknown_kind_and_wrong_domain_actions_cannot_complete(self):
        for kind,action in [('unknown','close'),('billing','reset'),('access','refund')]:
            state={'kind':kind,'verified':True,'resolved':False}
            unchanged,status=step(state,action)
            self.assertEqual(status,'invalid-action');self.assertEqual(unchanged,state)
            self.assertEqual(step(state,'handoff')[1],'handoff')
