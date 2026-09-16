# Skill Foundry

Distill successful agent workflows into small policies that know when to hand control back.

## Problem

Repeated multi-step LLM calls are expensive, but blindly replaying a successful trace is brittle.

## Approach

Collect sandbox trajectories, learn a compact policy from observable state, validate action preconditions and fall back when out of distribution. Compare behavior cloning, hand-written rules and a full agent.

## Demo concept

Train a small policy to navigate a simulated service desk; introduce an unseen ticket type and show safe handoff rather than a confident wrong action.

## First implementation

A deterministic ticket-routing environment, expert trajectories, a small supervised policy, held-out scenario split, confidence-based abstention and trace export. This is policy learning, not LLM distillation yet.

## Evaluation

Report held-out task completion, policy size, inference time, handoff coverage, recovery and failures under shifted scenarios. Separate teacher-generated labels from independent outcome checks.

## Milestones

1. Sandbox, rules baseline and trajectory schema
2. Behavior-cloning policy and held-out evaluation
3. Abstention and perturbed environment tests
4. Optional LLM teacher plus reproducible distillation study

## Your contribution

Describe a repetitive workflow with clear steps and a reliable definition of success.

## Status and license

Design brief only; no implementation or measured results yet. Original code will use GPL-3.0-only.
