# Skill Foundry

Distill successful agent workflows into small policies that know when to hand control back.

**v0.1 development prototype · Python 3.11+ · GPL-3.0-only**

## What works

Collects expert trajectories in a simulated help desk, trains a compact categorical decision tree, exports the learned policy and compares rollouts with expert rules and an always-close baseline. Unsupported state combinations hand off instead of extrapolating.

## Run

No third-party Python dependencies. Clone this repository and run from its root:

```sh
python app.py
python app.py --input examples/trajectories.json --model-out runs/policy.json
```

For commands using a file under `runs/`, create that directory first (`mkdir runs`). Generated files are ignored by Git. The default demo is offline and uses invented data.

## Test

```sh
python -m unittest discover -s tests -v
```

13 tests passed locally on Python 3.13. Other Python versions have not yet been exercised.

## Architecture

The sandbox separates expert actions, environment preconditions and rollout outcomes. Training chooses decision-tree splits by label entropy. Prediction uses a conservative observed-state support guard and optional leaf-purity threshold. The CLI never overwrites an existing model artifact.

## Reproduced example

The learned policy and expert rules each complete six known scenarios and hand off two unknown types. The always-close baseline produces eight invalid actions. The learned tree comes from labels, verified by a test that changes training labels and observes changed predictions.

See [the captured output](examples/demo-output.json). Rerun `python app.py` to reproduce it.

## Limits

This is small-scale supervised behavior cloning, not LLM distillation. Known evaluation states recur from training: results show execution and handoff, not novel-task generalization. Leaf purity is not calibrated confidence. The conservative support guard intentionally limits generalization.

## Next experiment

Introduce genuinely held-out environment variations and measure coverage/reliability before adding a local LLM teacher.

The [design brief](docs/DESIGN.md) describes the larger goal, including unimplemented milestones.

## Contribute

Describe a repetitive workflow with clear steps and a reliable definition of success. Use invented or openly licensed examples. Include expected outcomes, edge cases and data provenance.

## License

Copyright (c) 2026 Ppetip. Original code is licensed under GNU GPL version 3 only; see [LICENSE](LICENSE).

## Latest development pass

Separate seen-state execution from deliberately held-out initial states.

Run `python evaluation.py`: one seen case completes; both unseen cases hand off. Downstream states can overlap training. This does not demonstrate novel-task generalization.
