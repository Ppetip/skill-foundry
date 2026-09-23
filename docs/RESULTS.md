# Reading policy results

A successful CLI command means training/evaluation code completed, not that the learned policy completed every task.

- For each entry of `comparisons`, read `completed`, `handoffs`, and `invalid_actions` together. Handoff is an abstention, not a completed task.
- The default learned-policy synthetic demo completes six cases and hands off two. Known state combinations recur from training; this does not demonstrate generalization.
- `evaluation.py` separates seen and held-out initial states. The held-out synthetic fixture has two cases, zero completions and two handoffs. Later states may still overlap training.
- A result containing only `model` provides training metadata; it contains no evaluation evidence.

Check independent action preconditions and shifted cases before accepting teacher labels. No real LLM distillation, production reliability, or transfer benefit is established by these small fixtures.

## Saved-check freshness in the local AI Lab workflow

When using the optional AI Lab workspace integration, run `python lab.py status` from the workspace root. This reads saved results without rerunning tests or inference and lists the latest checks for every tool. The shared runner is a local integration, not part of a standalone clone of this repository; standalone checks remain documented in README.

`check_passed` records command/test completion. `freshness` is separate:

- `current`: the explicit source inputs and Python runtime match the completed check.
- `source-or-runtime-changed`: rerun checks after relevant code or runtime changes.
- `changed-during-checks`: inputs changed while checks ran; that run cannot verify one stable version.
- `unverified-legacy`: an older result has no source fingerprint.
- `not-run`: no saved check exists for this tool.

Fingerprints cover project Python files, tests, checked-in example JSON/JSONL paths, workflow YAML and shared runner Python files. They omit documentation, .env, databases, private run outputs and arbitrary analysis input files. Current does not prove unchanged external dependencies or OS state. Saved reports are private local cache records, not signed attestations. A later demo never replaces a check result, and a current failing check is still a failure.

A current check validates training, prediction and environment behavior on controlled fixtures. It does not certify a separately trained model or novel-task performance.
