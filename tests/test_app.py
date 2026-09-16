import copy
import unittest
from app import dataset, demo, expert, predict, rollout, step, train


class PolicyTests(unittest.TestCase):
    def setUp(self):
        self.model = train(dataset())

    def test_known_workflow_completes(self):
        for kind in ("access", "billing", "technical"):
            result = rollout({"kind": kind, "verified": False, "resolved": False}, lambda s: predict(self.model, s))
            self.assertEqual(result["status"], "complete")
            self.assertEqual(result["trace"][0]["action"], "verify")

    def test_unknown_kind_handoff(self):
        self.assertEqual(predict(self.model, {"kind": "new", "verified": True, "resolved": True}), "handoff")

    def test_invalid_action_has_no_effect(self):
        state = {"kind": "billing", "verified": False, "resolved": False}
        out, status = step(state, "refund")
        self.assertEqual(status, "invalid-action")
        self.assertEqual(out, state)

    def test_reproducible_training(self):
        self.assertEqual(self.model, train(dataset()))

    def test_labels_affect_learned_policy(self):
        rows = copy.deepcopy(dataset())
        for row in rows:
            row["action"] = "handoff"
        state = {"kind": "billing", "verified": False, "resolved": False}
        self.assertEqual(predict(train(rows), state), "handoff")
        self.assertEqual(predict(self.model, state), "verify")

    def test_unknown_feature_branch_handoff(self):
        rows = [r for r in dataset() if not r["state"]["verified"]]
        # A pure leaf is not evidence of support for an unseen state combination.
        state = {"kind": "billing", "verified": True, "resolved": True}
        self.assertEqual(predict(train(rows), state), "handoff")

    def test_ground_truth_field_rejected(self):
        with self.assertRaises(ValueError):
            expert({"kind": "billing", "verified": False, "resolved": False, "answer": "refund"})

    def test_empty_training_rejected(self):
        with self.assertRaises(ValueError):
            train([])

    def test_trace_does_not_mutate_input(self):
        state = {"kind": "access", "verified": False, "resolved": False}
        old = dict(state)
        rollout(state, expert)
        self.assertEqual(state, old)

    def test_demo_reports_baseline_failures(self):
        result = demo()["comparisons"]
        self.assertEqual(result[0]["completed"], 6)
        self.assertEqual(result[0]["handoffs"], 2)
        self.assertEqual(result[2]["invalid_actions"], 8)


if __name__ == "__main__":
    unittest.main()
