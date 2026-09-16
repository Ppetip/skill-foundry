# Status

Stage: v0.1 offline command-line prototype.

Verified: 10 tests pass; default synthetic demo runs.

Current: Collects expert trajectories in a simulated help desk, trains a compact categorical decision tree, exports the learned policy and compares rollouts with expert rules and an always-close baseline. Unsupported state combinations hand off instead of extrapolating.

Next: Introduce genuinely held-out environment variations and measure coverage/reliability before adding a local LLM teacher.

Repository target: https://github.com/Ppetip/skill-foundry
Budget: local/free; no paid APIs or model downloads used.
