"""Separate seen-state execution checks from deliberately held-out states."""
import json
from app import dataset, predict, rollout, train, validate_state


def evaluate_cases(model, cases):
    ids = set()
    for case in cases:
        if not isinstance(case.get('id'), str) or not case['id'] or case['id'] in ids:
            raise ValueError('unique case IDs required')
        ids.add(case['id'])
        validate_state(case['state'])
    partitions = {'seen_initial_state': [], 'held_out_initial_state': []}
    for case in cases:
        key = 'seen_initial_state' if json.dumps(case['state'], sort_keys=True) in model['known_states'] else 'held_out_initial_state'
        outcome = rollout(case['state'], lambda state: predict(model, state))
        partitions[key].append({'id': case['id'], **outcome})
    return {'partitions': {key: {'cases': len(trials), 'completed': sum(t['status']=='complete' for t in trials),
            'handoffs': sum(t['status']=='handoff' for t in trials), 'invalid_actions': sum(t['status']=='invalid-action' for t in trials),
            'trials': trials} for key, trials in partitions.items()},
            'limitation': 'Synthetic initial-state holdout. Downstream states may be seen in training. Conservative policy abstains on unseen combinations; this does not demonstrate novel-task generalization.'}


def demo():
    rows = [r for r in dataset() if not (r['state']['kind']=='billing' and not r['state']['verified'])]
    model = train(rows)
    cases = [{'id': 'known-access', 'state': {'kind':'access','verified':False,'resolved':False}},
             {'id': 'held-out-billing', 'state': {'kind':'billing','verified':False,'resolved':False}},
             {'id': 'unknown-kind', 'state': {'kind':'security','verified':True,'resolved':False}}]
    return evaluate_cases(model, cases)


if __name__ == '__main__':
    print(json.dumps(demo(), indent=2))
