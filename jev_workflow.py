# SPDX-License-Identifier: GPL-3.0-only
import argparse
import json
from pathlib import Path
from jev_client import Client, JevError, MODEL, choice, selected
import app

def request_data():
    return {"kind": "billing", "verified": False, "resolved": False}, choice(
        "Choose the next service-desk action. Unknown ticket kind requires handoff. Resolved tickets close. Otherwise verify identity first, then reset access, refund billing, or diagnose technical issues.",
        {"verify": "Unverified unresolved known ticket", "refund": "Verified unresolved billing ticket", "reset": "Verified unresolved access ticket", "diagnose": "Verified unresolved technical ticket", "close": "Resolved known ticket", "handoff": "Unknown kind or uncertainty"})

def guarded_action(state, proposed):
    _, status = app.step(state, proposed)
    return "handoff" if status == "invalid-action" else proposed

def run(client):
    state, questions = request_data()
    response = client.evaluate(state, questions)
    proposed = selected(response, "handoff")
    action = guarded_action(state, proposed)
    next_state, status = app.step(state, action)
    return {"proposed_action": proposed, "guarded_action": action, "rules_baseline": app.expert(state),
            "next_state": next_state, "status": status, "usage": [response["usage"]],
            "limitation": "One synthetic teacher decision with independent precondition enforcement. No labels automatically accepted for training; no distillation claim."}

def main():
    parser = argparse.ArgumentParser(description="Preview the synthetic Jev request; --live explicitly opts into paid calls.")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--env-file", type=Path)
    args = parser.parse_args()
    if not args.live:
        state, questions = request_data()
        print(json.dumps({"mode": "dry-run-no-network", "model": MODEL, "state": state, "questions": questions}, indent=2))
        return
    if args.env_file is None:
        parser.error("--live requires --env-file with the shared budget ledger")
    try:
        client = Client(args.env_file)
        result = run(client)
        print(json.dumps({"mode": "live-model-on-synthetic-data", "model": MODEL, **result, "budget": client.budget.summary()}, indent=2))
    except JevError as exc:
        parser.exit(1, str(exc) + "\n")

if __name__ == "__main__":
    main()
