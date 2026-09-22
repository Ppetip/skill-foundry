# Status

Stage: command-line prototype with optional live Jev integration.
Verified: 38 offline tests pass; dry run and live synthetic Jev workflow pass.

Latest: The environment now validates action preconditions independently of the expert teacher function.

Next: Evaluate teacher trajectories on shifted environments with independent outcomes.

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

2026-09-22 10:48 UTC: The environment now validates action preconditions independently of the expert teacher function. A deliberately faulty teacher that refunds before verification fails both rollout and the teacher audit. Handoff remains permitted, and the existing known-kind/verification/resolution rules are unchanged. Independence here means separate code paths within the same synthetic task specification, not external review or real-world validation. Local tests pass; publication and hosted verification pending. No new Jev calls.
