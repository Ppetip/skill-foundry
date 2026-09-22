# Status

Stage: command-line prototype with optional live Jev integration.
Verified: 41 offline tests pass; dry run and live synthetic Jev workflow pass.

Latest: Run `python challenge.py` (Codex route `challenge`).

Next: Evaluate a separately specified transition change before claiming adaptation to changed environments.

Repository: https://github.com/Ppetip/skill-foundry
Budget: one shared $3 cumulative Jev allowance across the portfolio, never per project or cycle.
No other paid compute authorized. Eight initial calls across all projects used 3,303 input tokens;
estimated total $0.000138726, with $0.08 conservatively reserved. See README for limits.
Live smoke responses are not production benchmarks. No model training performed.

2026-09-21 CI pass: added pinned, read-only Windows/Linux Python 3.11/3.13 checks for unit tests and offline CLI contracts. Local checks and all four hosted Windows/Linux Python 3.11/3.13 jobs pass. No additional Jev calls.

Hosted verification: https://github.com/Ppetip/skill-foundry/actions/runs/35590287159

2026-09-21 14:42 UTC budget fix: live clients require an existing ledger; explicit initialization refuses overwrite. Added four regression cases for missing/deleted/empty ledgers and preserved spending. All local tests, CLI checks, and four hosted Windows/Linux Python 3.11/3.13 jobs pass. No additional Jev calls.

Budget-fix hosted verification: https://github.com/Ppetip/skill-foundry/actions/runs/35614396787

2026-09-21 18:44 UTC: Rollouts validate the initial state and require an integer step bound from 1 to 1,000 before calling a policy. Local tests, offline CLI checks, and all four hosted matrix jobs pass. No additional Jev calls.

Feature-pass verification: https://github.com/Ppetip/skill-foundry/actions/runs/35640907538

2026-09-21 22:45 UTC: documented how to interpret this tool's outcomes separately from command success. The local Codex runner now shows a concise outcome summary for this project. Verified through common-runner checks and synthetic demo output; histories stay local.

2026-09-22 02:46 UTC: Teacher-label audit checks sandbox preconditions without training or accepting labels automatically. Common-runner checks, new route and all four hosted jobs pass. No new Jev calls.

Evaluation-path verification: https://github.com/Ppetip/skill-foundry/actions/runs/35681205403

2026-09-22 10:48 UTC: The environment now validates action preconditions independently of the expert teacher function. A deliberately faulty teacher that refunds before verification fails both rollout and the teacher audit. Handoff remains permitted, and the existing known-kind/verification/resolution rules are unchanged. Independence here means separate code paths within the same synthetic task specification, not external review or real-world validation. Published and verified: local checks and all four hosted matrix jobs pass. No new Jev calls.

Reliability verification: https://github.com/Ppetip/skill-foundry/actions/runs/35718655877

2026-09-22 22:50 UTC: Run `python challenge.py` (Codex route `challenge`). Two tiny decision trees are trained locally on original and deliberately corrupted synthetic teacher rows. The known task completes, two changed initial states hand off, and a premature refund from the corrupted teacher is caught as an invalid action. All four expected outcomes match; that means detection and handoff worked, not four tasks completed. Environment transition rules are unchanged, so this is not a changed-environment transfer test or LLM distillation. See `examples/extended-evaluation.json`. Common-runner checks pass. Published and verified: all four hosted Windows/Linux Python 3.11/3.13 jobs pass. No new Jev calls.

Extended evaluation verification: https://github.com/Ppetip/skill-foundry/actions/runs/35795076069
