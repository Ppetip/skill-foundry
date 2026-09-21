# Reading policy results

A successful CLI command means training/evaluation code completed, not that the learned policy completed every task.

- For each entry of `comparisons`, read `completed`, `handoffs`, and `invalid_actions` together. Handoff is an abstention, not a completed task.
- The default learned-policy synthetic demo completes six cases and hands off two. Known state combinations recur from training; this does not demonstrate generalization.
- `evaluation.py` separates seen and held-out initial states. The held-out synthetic fixture has two cases, zero completions and two handoffs. Later states may still overlap training.
- A result containing only `model` provides training metadata; it contains no evaluation evidence.

Check independent action preconditions and shifted cases before accepting teacher labels. No real LLM distillation, production reliability, or transfer benefit is established by these small fixtures.
