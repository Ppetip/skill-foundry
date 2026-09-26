# Skill Foundry

Distill successful agent workflows into small policies that know when to hand control back.

**v0.1 development prototype Ãƒâ€šÃ‚Â· Python 3.11+ Ãƒâ€šÃ‚Â· GPL-3.0-only**

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

53 tests and five offline CLI paths pass on Windows and Linux with Python 3.11 and 3.13 (GitHub Actions).

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

## Optional Jev workflow

Run `python jev_workflow.py` to preview the synthetic request without network access.
To opt into live calls, create a local `.env` using `.env.example`, set your TypeSafe key,
and point `JEV_BUDGET_DB` at one absolute SQLite path shared by all five projects.
Then run `python jev_workflow.py --live --env-file /absolute/path/to/.env`.
Do not commit the real configuration. No packages or model downloads are required.

The adapter pins `jev-1.13.0` and sends only the built-in synthetic fixture in this CLI.
Agent Black Box makes four replay calls; each other workflow makes one. The reusable
`Client.evaluate(state, questions)` interface supports bounded Choice questions.
Treat low-confidence decisions as abstentions; its 0.8 cutoff is a heuristic, not calibrated certainty.

The shared ledger allows at most $3 in cumulative reservations: one cent is permanently
reserved **before each attempt**, including timeouts and failed requests. It never retries
automatically. Concurrent processes share an atomic SQLite reservation. Never reset,
delete, replace or split the ledger to regain budget. This guard covers this client,
not unrelated account use. Provider billing remains authoritative.

[Official TypeSafe pricing](https://docs.typesafe.ai/models) checked 2026-09-21 lists
$0.042 per million input tokens and free output. One cent exceeds a full 65,536-input-token
request at that rate; the client also limits serialized input to 16KB. Estimates use
reported input tokens and exclude unknown failed-request usage. Calls fail closed on
2026-09-28 until pricing and the reservation bound are reviewed. Never extend the review
date without checking the provider's current terms.

[The HTTP API](https://docs.typesafe.ai/api) uses the fixed official TypeSafe endpoint.
Redirects are refused, responses are schema-checked, and error bodies/credentials are
not logged. Tests mock the provider and do not spend money.

`examples/jev-live-smoke.json` records a real 2026-09-21 model response on synthetic input.
It is a connectivity and workflow smoke check, not a quality benchmark or evidence of
training, generalization, speed or production reliability. Re-running it may change results.

Jev proposes verify before refund; the environment rejects unsafe teacher actions.

## Continuous verification

[Offline checks](https://github.com/Ppetip/skill-foundry/actions/workflows/offline.yml) run tests and JSON CLI smoke checks on Windows/Linux with Python 3.11/3.13 for pushes and pull requests. Run `python verify_demos.py` locally. Actions are pinned to immutable commits, use read-only permissions, and receive no provider secrets. Jev tests use mocks; the CLI check uses its default dry run. The workflow does not run live inference.

### First-time budget setup and recovery

For a genuinely new allowance only, run `python jev_client.py --init-budget /absolute/path/to/jev-budget.sqlite3` once, then use that exact path in `JEV_BUDGET_DB` for every app. Initialization refuses existing files, including empty files. Do not initialize a new ledger to replace lost spending history. Existing users keep their existing ledger and skip setup.

Live clients now open existing ledgers only, including at reservation time. A missing, mistyped, or empty ledger stops calls instead of silently recreating a zero balance. Restore missing history from a trusted backup; do not reset it. This prevents accidental recreation, not deliberate administrator modification or substitution of a different valid database.

## Latest reliability improvement

`rollout(initial, policy, max_steps=4)` now rejects malformed initial states and invalid step limits before invoking the policy. Exhausting a valid bound returns `step-limit` with the recorded trace. No new teacher inference or policy training was performed in this pass.

See [Reading results](docs/RESULTS.md) for outcome fields, denominators, abstentions and the limits of command success.

## New evaluation path

Run `python app.py --audit-teacher`, optionally with `--input trajectories.json`. The audit returns accepted IDs and rejected IDs/reasons; invalid row schemas are errors. Conservative handoff is allowed. Passing means only that the action satisfies this sandbox, not that it is an optimal teacher label. No training happens and `--model-out` is incompatible with audit mode.

## Evaluation reliability

The environment now validates action preconditions independently of the expert teacher function. A deliberately faulty teacher that refunds before verification fails both rollout and the teacher audit. Handoff remains permitted, and the existing known-kind/verification/resolution rules are unchanged. Independence here means separate code paths within the same synthetic task specification, not external review or real-world validation.

## Extended evaluation

Run `python challenge.py` (Codex route `challenge`). Two tiny decision trees are trained locally on original and deliberately corrupted synthetic teacher rows. The known task completes, two changed initial states hand off, and a premature refund from the corrupted teacher is caught as an invalid action. All four expected outcomes match; that means detection and handoff worked, not four tasks completed. Environment transition rules are unchanged, so this is not a changed-environment transfer test or LLM distillation. See `examples/extended-evaluation.json`.

## Input validation

Training requires a nonempty JSON array of objects with unique nonempty string IDs,
valid `state` objects, and recognized string action labels. Missing states and
malformed action values raise `ValueError` before tree construction. Teacher audits
also report missing states as validation errors. Prediction thresholds must be finite
numbers from zero to one; booleans are rejected. Invalid CLI training input does not
create the requested model artifact. These are input-shape checks, not proof that
teacher labels are correct; use the separate teacher audit for action preconditions.

## Explain a learned action or handoff

Call `predict_decision(model, state, threshold=0.8)` to inspect the action, reason, threshold, traversed feature/value path, `leaf_purity` and `leaf_samples`. `predict` still returns only the action using the same decision rule. Reasons distinguish `unknown-kind`, `unseen-state`, `missing-branch`, `below-threshold`, `learned-handoff` and `selected`. Checks stop at the first applicable guard. When no leaf is reached, leaf fields are null; models lacking optional sample metadata also report null samples.

Leaf purity is the fraction of training rows at that leaf carrying its majority label; samples count rows, including repeated states. Neither is calibrated probability or independent evidence of success. An explicitly learned handoff differs from a support guard rejecting a state. A selected action still has to satisfy the separate environment preconditions.

`python challenge.py` now includes `initial_prediction` for each synthetic case. It explains only that case's starting decision, not every later rollout step. The deliberately corrupted teacher can still produce a selected but invalid refund; the environment rejects it. This report makes that distinction visible without changing the environment rules. The example trains tiny local decision trees, not an LLM, and is not a production reliability benchmark.

Prediction only reads the caller-supplied in-memory model and state; it does not execute tools, train, deploy or write files. State and threshold validation remain in place. Models are trusted structures produced by this prototype; the explanation API does not certify arbitrary model artifacts or sandbox caller code.
