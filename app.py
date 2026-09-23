"""Learn a compact decision tree from synthetic expert service-desk trajectories."""
import argparse
import json
import math
from collections import Counter
from pathlib import Path

FEATURES = ("kind", "verified", "resolved")
KINDS = {"access": "reset", "billing": "refund", "technical": "diagnose"}


def validate_state(state):
    if not isinstance(state, dict) or set(state) != set(FEATURES):
        raise ValueError("state must contain exactly kind, verified, resolved")
    if not isinstance(state["kind"], str) or not state["kind"]:
        raise ValueError("kind must be nonempty text")
    if type(state["verified"]) is not bool or type(state["resolved"]) is not bool:
        raise ValueError("verified and resolved must be booleans")


def expert(state):
    validate_state(state)
    if state["kind"] not in KINDS:
        return "handoff"
    if state["resolved"]:
        return "close"
    if not state["verified"]:
        return "verify"
    return KINDS[state["kind"]]


def step(state, action):
    validate_state(state)
    if action == "handoff":
        return dict(state), "handoff"
    # Environment preconditions must not call the teacher being evaluated.
    known = state["kind"] in KINDS
    valid = known and (
        (action == "close" and state["resolved"])
        or (action == "verify" and not state["resolved"] and not state["verified"])
        or (action == KINDS[state["kind"]] and not state["resolved"] and state["verified"])
    )
    if not valid:
        return dict(state), "invalid-action"
    out = dict(state)
    if action == "close":
        return out, "complete"
    if action == "verify":
        out["verified"] = True
    else:
        out["resolved"] = True
    return out, "running"


def entropy(rows):
    counts = Counter(row["action"] for row in rows)
    return -sum((n / len(rows)) * math.log2(n / len(rows)) for n in counts.values())


def tree(rows, features):
    counts = Counter(row["action"] for row in rows)
    action, count = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[0]
    leaf = {"action": action, "confidence": count / len(rows), "samples": len(rows)}
    if len(counts) == 1 or not features:
        return leaf
    choices = []
    for feature in features:
        groups = {}
        for row in rows:
            groups.setdefault(str(row["state"][feature]), []).append(row)
        remainder = sum(len(g) / len(rows) * entropy(g) for g in groups.values())
        choices.append((remainder, feature, groups))
    remainder, feature, groups = min(choices, key=lambda x: (x[0], x[1]))
    if len(groups) == 1:
        return leaf
    return {"feature": feature, "children": {key: tree(group, [f for f in features if f != feature])
                                             for key, group in sorted(groups.items())}}


def train(rows):
    if not isinstance(rows, list) or not rows:
        raise ValueError("training rows must be a nonempty array")
    ids = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("training rows must be objects")
        validate_state(row.get("state"))
        if not isinstance(row.get("id"), str) or not row["id"] or row["id"] in ids:
            raise ValueError("unique training IDs required")
        ids.add(row["id"])
        if not isinstance(row.get("action"), str) or row["action"] not in {"verify", "close", "handoff", *KINDS.values()}:
            raise ValueError("unknown training action")
    return {"schema_version": 1, "algorithm": "categorical decision tree",
            "known_kinds": sorted({r["state"]["kind"] for r in rows}),
            "known_states": sorted({json.dumps(r["state"], sort_keys=True) for r in rows}),
            "tree": tree(rows, list(FEATURES)), "training_rows": len(rows)}


def predict(model, state, threshold=.8):
    validate_state(state)
    if type(threshold) not in (int, float) or not 0 <= threshold <= 1:
        raise ValueError("threshold must be a finite number between zero and one")
    if state["kind"] not in model["known_kinds"] or json.dumps(state, sort_keys=True) not in model["known_states"]:
        return "handoff"
    node = model["tree"]
    while "feature" in node:
        node = node["children"].get(str(state[node["feature"]]))
        if node is None:
            return "handoff"
    return node["action"] if node["confidence"] >= threshold else "handoff"


def rollout(initial, policy, max_steps=4):
    validate_state(initial)
    if type(max_steps) is not int or not 1 <= max_steps <= 1000:
        raise ValueError("max_steps must be an integer between 1 and 1000")
    state = dict(initial)
    trace = []
    for _ in range(max_steps):
        action = policy(dict(state))
        out, status = step(state, action)
        trace.append({"state": state, "action": action, "status": status})
        state = out
        if status != "running":
            return {"status": status, "trace": trace}
    return {"status": "step-limit", "trace": trace}


def dataset():
    rows = []
    for kind in KINDS:
        for verified in (False, True):
            initial = {"kind": kind, "verified": verified, "resolved": False}
            for i, event in enumerate(rollout(initial, expert)["trace"]):
                rows.append({"id": f"train-{kind}-{verified}-{i}", "state": event["state"], "action": event["action"]})
    return rows


def demo():
    rows = dataset()
    model = train(rows)
    scenarios = [{"id": f"eval-{kind}-{verified}", "state": {"kind": kind, "verified": verified, "resolved": False}}
                 for kind in (*KINDS, "unseen-security-review") for verified in (False, True)]
    comparisons = []
    for name, policy in (("learned", lambda s: predict(model, s)), ("expert-rules", expert), ("always-close", lambda s: "close")):
        trials = [{"id": s["id"], **rollout(s["state"], policy)} for s in scenarios]
        comparisons.append({"policy": name, "completed": sum(t["status"] == "complete" for t in trials),
                            "handoffs": sum(t["status"] == "handoff" for t in trials),
                            "invalid_actions": sum(t["status"] == "invalid-action" for t in trials), "trials": trials})
    return {"data": "synthetic-expert-trajectories", "model": model, "comparisons": comparisons,
            "limitation": "Tiny behavior-cloning sandbox, not LLM distillation. Evaluation IDs differ but known state combinations recur from training; this checks execution and unsupported-state handoff, not novel-task generalization. The conservative support guard only accepts previously observed state combinations. Leaf purity is not calibrated confidence."}


def audit_teacher(rows):
    """Check labels against sandbox action preconditions without training."""
    if not isinstance(rows, list):
        raise ValueError("teacher rows must be an array")
    seen, rejected, accepted = set(), [], []
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not row["id"] or row["id"] in seen:
            raise ValueError("unique teacher row IDs required")
        seen.add(row["id"])
        validate_state(row.get("state"))
        action = row.get("action")
        if not isinstance(action, str) or action not in {"verify", "close", "handoff", *KINDS.values()}:
            raise ValueError("unknown teacher action")
        _, status = step(row["state"], action)
        if status == "invalid-action":
            rejected.append({"id":row["id"],"reason":"action precondition violated"})
        else:
            accepted.append(row["id"])
    return {"accepted_ids":accepted,"rejected":rejected,"training_performed":False,
            "limitation":"Sandbox preconditions only; passing labels are not proof of useful teaching or generalization."}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, help="JSON training rows; otherwise run the synthetic demo")
    p.add_argument("--model-out", type=Path, help="Write learned policy JSON to a new file")
    p.add_argument("--audit-teacher", action="store_true", help="Validate labels without training")
    a = p.parse_args()
    if a.audit_teacher and a.model_out:
        p.error("--audit-teacher does not produce a trained model")
    if a.audit_teacher:
        result = audit_teacher(json.loads(a.input.read_text(encoding="utf-8")) if a.input else dataset())
    else:
        result = {"model": train(json.loads(a.input.read_text(encoding="utf-8")))} if a.input else demo()
    if a.model_out:
        with a.model_out.open("x", encoding="utf-8") as out:
            json.dump(result["model"], out, indent=2)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
