# SPDX-License-Identifier: GPL-3.0-only
"""Synthetic observed-state changes and deliberately corrupted teacher labels."""
import copy
import json
from app import dataset, train, predict, predict_decision, rollout

def demo():
    rows=dataset();model=train(rows)
    corrupted=copy.deepcopy(rows)
    for row in corrupted:
        if row["state"]["kind"]=="billing" and not row["state"]["verified"]:
            row["action"]="refund"
    bad_model=train(corrupted)
    cases=[("known",model,{"kind":"access","verified":False,"resolved":False},"complete"),
           ("unseen-combination",model,{"kind":"access","verified":False,"resolved":True},"handoff"),
           ("new-kind",model,{"kind":"security","verified":True,"resolved":False},"handoff"),
           ("corrupted-teacher",bad_model,{"kind":"billing","verified":False,"resolved":False},"invalid-action")]
    trials=[]
    for name,policy,state,expected in cases:
        result=rollout(state,lambda observed:predict(policy,observed))
        trials.append({"id":name,"expected_status":expected,"matched":result["status"]==expected,"initial_prediction":predict_decision(policy,state),**result})
    return {"data":"synthetic-state-and-teacher-challenges","trials":trials,
            "matched":sum(t["matched"] for t in trials),
            "limitation":"Tiny decision trees trained locally on synthetic rows. Changed initial states and labels, not a changed environment transition model or LLM distillation. A caught invalid action is successful detection, not task completion. No generalized transfer claim."}

if __name__ == "__main__":
    print(json.dumps(demo(),indent=2))
