# SPDX-License-Identifier: GPL-3.0-only
"""Prevent malformed holdout inputs from silently becoming zero-case evaluations."""
import copy
import unittest
from unittest.mock import patch
from app import dataset, train
from evaluation import evaluate_cases


class HoldoutBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.model = train(dataset())
        self.case = {"id": "known", "state": {"kind": "access", "verified": False, "resolved": False}}

    def test_nonarray_inputs_reject_before_execution_including_generators(self):
        for cases in (None, "", "text", {}, {"id": self.case}, (), iter([self.case]), (c for c in [self.case])):
            with self.subTest(kind=type(cases).__name__), patch("evaluation.rollout") as rollout:
                with self.assertRaisesRegex(ValueError, "array"):
                    evaluate_cases(self.model, cases)
                rollout.assert_not_called()

    def test_invalid_late_case_rejects_entire_batch_before_execution(self):
        invalid = [None, "bad", [], {}, {"id": "missing-state"},
                   {"id": "wrong-state", "state": {"kind": "access"}},
                   {**self.case, "id": ""}, copy.deepcopy(self.case)]
        for last in invalid:
            with self.subTest(case=last), patch("evaluation.rollout") as rollout:
                with self.assertRaises(ValueError):
                    evaluate_cases(self.model, [self.case, last])
                rollout.assert_not_called()

    def test_valid_cases_keep_partition_counts_outcomes_and_input(self):
        cases = [self.case, {"id": "unseen", "state": {"kind": "security", "verified": True, "resolved": False}}]
        before = copy.deepcopy((self.model, cases))
        result = evaluate_cases(self.model, cases)
        seen = result["partitions"]["seen_initial_state"]
        held = result["partitions"]["held_out_initial_state"]
        self.assertEqual((seen["cases"], seen["completed"], seen["handoffs"]), (1, 1, 0))
        self.assertEqual((held["cases"], held["completed"], held["handoffs"]), (1, 0, 1))
        self.assertEqual(seen["trials"][0]["id"], "known")
        self.assertEqual(held["trials"][0]["id"], "unseen")
        self.assertEqual((self.model, cases), before)

    def test_explicit_empty_array_is_zero_cases_without_rollouts(self):
        with patch("evaluation.rollout") as rollout:
            result = evaluate_cases(self.model, [])
            rollout.assert_not_called()
        for partition in result["partitions"].values():
            self.assertEqual(partition, {"cases": 0, "completed": 0, "handoffs": 0,
                                         "invalid_actions": 0, "trials": []})
