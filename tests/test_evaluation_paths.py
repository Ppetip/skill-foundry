# SPDX-License-Identifier: GPL-3.0-only
import copy
import unittest
from unittest.mock import patch
from app import audit_teacher

class TeacherAuditTests(unittest.TestCase):
    def rows(self):return [{'id':'bad','state':{'kind':'billing','verified':False,'resolved':False},'action':'refund'},{'id':'good','state':{'kind':'billing','verified':False,'resolved':False},'action':'verify'}]
    def test_unsafe_label_rejected_without_training_or_mutation(self):
        rows=self.rows();before=copy.deepcopy(rows)
        with patch('app.train') as train:r=audit_teacher(rows);train.assert_not_called()
        self.assertEqual(rows,before);self.assertEqual(r['accepted_ids'],['good']);self.assertEqual(r['rejected'][0]['id'],'bad');self.assertFalse(r['training_performed'])
    def test_handoff_is_allowed_conservative_label(self):
        rows=self.rows()[:1];rows[0]['action']='handoff';self.assertEqual(audit_teacher(rows)['accepted_ids'],['bad'])
    def test_duplicate_or_unknown_action_rejected(self):
        with self.assertRaises(ValueError):audit_teacher(self.rows()*2)
        rows=self.rows();rows[0]['action']='send-money'
        with self.assertRaises(ValueError):audit_teacher(rows)
