# SPDX-License-Identifier: GPL-3.0-only
"""Regression checks for supplied JSON rows and prediction options."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from app import audit_teacher, dataset, predict, train


class InputBoundaryTests(unittest.TestCase):
    def test_training_rejects_malformed_json_before_building_tree(self):
        valid = dataset()[0]
        malformed = [None, {}, "rows", [None], [7], [{}],
                     [{**valid, "state": None}], [{**valid, "action": []}],
                     [{**valid, "action": {}}], [{**valid, "id": False}]]
        with patch("app.tree") as build:
            for rows in malformed:
                with self.subTest(rows=rows), self.assertRaises(ValueError):
                    train(rows)
            build.assert_not_called()

    def test_audit_missing_state_is_a_validation_error(self):
        with self.assertRaisesRegex(ValueError, "state must contain"):
            audit_teacher([{"id": "missing-state", "action": "handoff"}])

    def test_threshold_rejects_boolean_and_nonnumeric_values(self):
        model = train(dataset())
        state = dataset()[0]["state"]
        for threshold in (True, False, None, "0.8", [], {}, float("nan"),
                          float("inf"), -float("inf"), -.1, 1.1):
            with self.subTest(threshold=threshold), self.assertRaises(ValueError):
                predict(model, state, threshold)
        for threshold in (0, 0.0, .8, 1, 1.0):
            self.assertEqual(predict(model, state, threshold), "verify")

    def test_training_preserves_input_rows(self):
        rows = dataset()
        before = copy.deepcopy(rows)
        train(rows)
        audit_teacher(rows)
        self.assertEqual(rows, before)

    def test_cli_invalid_input_does_not_create_model(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "invalid.json"
            output = Path(directory) / "policy.json"
            source.write_text(json.dumps([{"id": "broken", "action": "verify"}]),
                              encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "app.py", "--input", str(source), "--model-out", str(output)],
                cwd=Path(__file__).resolve().parents[1], capture_output=True, text=True,
                timeout=10)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("ValueError: state must contain", result.stderr)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
