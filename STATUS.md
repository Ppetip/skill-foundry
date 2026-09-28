# Status

Stage: command-line prototype with optional live Jev integration.
Verified: 55 tests and five offline CLI paths pass locally; hosted checks for this change pending. Jev smoke results remain historical; no new live calls.

Latest: Decision reports distinguish handoff reasons and show traversed branches and leaf support.

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

2026-09-23 06:53 UTC: Training now rejects malformed JSON containers, row objects,
missing states and non-string action labels with ValueError before building a tree.
Teacher audits reject missing states consistently. Prediction rejects boolean,
non-numeric and non-finite thresholds. Five new regressions cover validation before
training, input preservation, valid threshold endpoints, and absence of model output
after invalid CLI input. Common-runner checks pass: 46 tests and five offline CLI
checks. Hosted verification passed on all four OS/Python combinations. No live calls or provider
spending; tests train only the existing tiny synthetic decision-tree fixtures.

2026-09-23 10:54 UTC verification follow-up: Published code and all four hosted jobs verified after the earlier approval-review usage-limit interruption. Existing check suites were not rerun solely to create history. Run: https://github.com/Ppetip/skill-foundry/actions/runs/35829403189

2026-09-23 14:55 UTC: Added guidance for interpreting saved-check freshness in the optional local Codex runner. A current check validates training, prediction and environment behavior on controlled fixtures. It does not certify a separately trained model or novel-task performance. The shared runner now records check-source fingerprints and provides read-only status. All five current app checks passed (234 tests total), along with 24 local runner regressions. Run ID: 811900b822db42e390b5e1714afbbe25. App implementation unchanged; this documentation update skips redundant hosted CI. No live calls or new performance claim.

2026-09-26 19:00 UTC: Added predict_decision and challenge initial_prediction reports. The action-only predict API uses the same guarded rule. Explanations distinguish support guards, threshold abstention, learned handoff and selected action, without bypassing environment checks. Local check 714606230df04ac7b9a8eb07260ef4c2 passed. All four hosted Windows/Linux Python 3.11/3.13 jobs pass. No Jev calls or deployment.

Prediction-explanation verification: https://github.com/Ppetip/skill-foundry/actions/runs/36264821411

2026-09-27 07:00 UTC: Shared-runner routing changes passed the existing policy, handoff and precondition checks; no model deployment or changed-environment performance is claimed. All five common-runner check routes passed (280 app tests and 28 CLI paths total), plus 32 shared-runner regressions. Check run ffd76d632c9246f4969e0cbbbacb538f. Shared integration is local to the AI Lab workspace, not included in a standalone repository clone. Existing app-source hosted results remain applicable; this documentation update skips redundant hosted CI. No paid calls.

2026-09-27 19:00 UTC: The shared-runner change passes existing policy, explanation and precondition checks; no changed-environment performance or deployment is claimed. All five common checks pass (288 app tests, 29 CLI paths), plus 38 shared-runner regressions. Check run 6cbc7ab369f64438ac08e746849d49a7. Shared integration stays local to the AI Lab workspace. App-source hosted evidence is unchanged; documentation-only update skips redundant CI. No live calls.

2026-09-28 15:00 UTC: Official TypeSafe model pricing rechecked; the pinned Jev rate and free output are unchanged. Review window refreshed to September 28 through October 4 UTC, failing closed October 5. One-cent permanent reservation and the existing shared $3 cap/ledger remain unchanged. Added two mocked date-boundary tests; existing mocked calls now use the review-start date. Local check 10d3bcc5c43a42b1b5bbf4b998834a5e passed. Hosted verification pending. No live calls or ledger access during this update; historical smoke results remain historical.
