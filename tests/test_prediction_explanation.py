# SPDX-License-Identifier: GPL-3.0-only
import copy
import unittest
from app import dataset, train, predict, predict_decision
from challenge import demo

STATE = {"kind": "billing", "verified": False, "resolved": False}


class PredictionExplanationTests(unittest.TestCase):
    def test_distinct_support_guards_have_no_invented_leaf_evidence(self):
        model = train(dataset())
        for state, reason in [({**STATE, "kind": "new-kind"}, "unknown-kind"),
                              ({**STATE, "resolved": True}, "unseen-state")]:
            with self.subTest(reason=reason):
                result = predict_decision(model, state)
                self.assertEqual((result["action"], result["reason"]), ("handoff", reason))
                self.assertEqual(result["path"], [])
                self.assertIsNone(result["leaf_purity"])
                self.assertIsNone(result["leaf_samples"])

    def test_conflicting_labels_show_leaf_support_and_threshold_boundary(self):
        model = train([{"id": "a", "state": STATE, "action": "verify"},
                       {"id": "b", "state": STATE, "action": "handoff"}])
        result = predict_decision(model, STATE, .6)
        self.assertEqual(result["reason"], "below-threshold")
        self.assertEqual((result["leaf_purity"], result["leaf_samples"]), (.5, 2))
        at_boundary = predict_decision(model, STATE, .5)
        self.assertEqual(at_boundary["reason"], "learned-handoff")
        self.assertEqual(at_boundary["action"], "handoff")

    def test_action_api_matches_report_and_path_uses_only_current_state(self):
        model = train(dataset())
        for row in dataset():
            decision = predict_decision(model, row["state"])
            self.assertEqual(predict(model, row["state"]), decision["action"])
            self.assertEqual(decision["action"], row["action"])
            self.assertEqual(decision["reason"], "selected")
            for branch in decision["path"]:
                self.assertEqual(branch["value"], str(row["state"][branch["feature"]]))

    def test_missing_branch_has_separate_reason_and_no_leaf(self):
        model = train(dataset())
        model["tree"] = {"feature": "kind", "children": {}}
        result = predict_decision(model, STATE)
        self.assertEqual(result["reason"], "missing-branch")
        self.assertEqual(result["path"], [{"feature": "kind", "value": "billing"}])
        self.assertIsNone(result["leaf_samples"])

    def test_explanation_does_not_mutate_model_or_state_and_validates_threshold(self):
        model = train(dataset()); original = copy.deepcopy(model); state = dict(STATE)
        decision = predict_decision(model, state)
        decision["path"].clear()
        self.assertEqual(model, original); self.assertEqual(state, STATE)
        for threshold in (True, float("nan"), -1, 2):
            with self.subTest(threshold=threshold), self.assertRaises(ValueError):
                predict_decision(model, state, threshold)

    def test_challenge_explains_handoffs_without_overriding_environment(self):
        trials = {trial["id"]: trial for trial in demo()["trials"]}
        self.assertEqual(trials["new-kind"]["initial_prediction"]["reason"], "unknown-kind")
        self.assertEqual(trials["unseen-combination"]["initial_prediction"]["reason"], "unseen-state")
        bad = trials["corrupted-teacher"]
        self.assertEqual(bad["initial_prediction"]["reason"], "selected")
        self.assertEqual(bad["status"], "invalid-action")

    def test_missing_sample_metadata_and_nan_leaf_preserve_action_guard(self):
        model = train([{"id": "one", "state": STATE, "action": "verify"}])
        del model["tree"]["samples"]
        self.assertIsNone(predict_decision(model, STATE)["leaf_samples"])
        self.assertEqual(predict(model, STATE), "verify")
        model["tree"]["confidence"] = float("nan")
        self.assertEqual(predict(model, STATE), "handoff")
        self.assertEqual(predict_decision(model, STATE)["reason"], "below-threshold")
