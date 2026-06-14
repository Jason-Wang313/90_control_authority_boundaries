# Paper 90 Rebuild Plan: Control Authority Boundaries

Timestamp: 2026-06-14 13:58:00 +01:00

## Starting Point

Paper 90 is currently a v3 archive for ICLR main. The original bet is:

> Model where authority should shift between policy, controller, and human.

The hostile prior-work pressure is severe: shared autonomy already has Bayesian authority allocation, confidence-based shared control, game-theoretic haptic shared control, nonlinear MPC with adaptive impedance, control barrier functions, barrier-pair safe shared autonomy, controller fusion, and seamless autonomy-transition systems. A submission-ready rebuild cannot claim novelty from "uncertainty plus arbitration." It must test whether an explicit authority-boundary state changes closed-loop outcomes under physically meaningful failures.

## Rebuilt Claim Under Test

The strongest defensible claim is:

> A controller should maintain an explicit boundary state over which actor has safe and effective authority--policy, low-level controller, or human--and should switch authority only when predicted physical consequence, user intent ambiguity, and recovery burden jointly justify the handoff.

This is not a claim of real deployment. It is a local evidence audit of whether the mechanism survives strong baselines.

## Benchmark Design

I will replace the template success-rate generator with a deterministic closed-loop shared-autonomy benchmark. Each episode simulates a robot executing under hidden physical and human-intent modes. The simulator will track state evolution, collisions, human override timing, autonomy burden, and recovery after authority changes.

Tasks:

1. Assisted reaching through clutter with fragile obstacles.
2. Shared-control door/drawer opening with contact-mode transitions.
3. Mobile manipulator corridor navigation with delayed human input.
4. Tool-use alignment where low-level servoing can recover but policy-level autonomy may overcommit.

Splits:

1. `nominal_shared_autonomy`
2. `intent_ambiguity_shift`
3. `contact_mode_shift`
4. `human_delay_shift`
5. `combined_authority_stress`

## Methods To Compare

Baselines must be strong enough to kill the paper if they match the proposed method:

1. `fixed_policy_authority`: robot policy keeps authority unless a hard failure occurs.
2. `fixed_human_authority`: human stays in charge; safe but slow and high-burden.
3. `confidence_threshold_shared_control`: switches by policy confidence only.
4. `bayesian_authority_allocation`: belief-filter arbitration over human intent and autonomy confidence.
5. `cbf_safety_filter`: policy authority with control-barrier safety override.
6. `mpc_risk_arbitration`: nonlinear-MPC-style handoff based on predicted constraint violation and cost.
7. `controller_fusion_prior`: fuses policy and controller priors with uncertainty weighting.
8. `proposed_authority_boundary`: explicit actor-authority boundary using consequence, intent ambiguity, recovery burden, and handoff hysteresis.
9. `oracle_authority_boundary`: upper bound with access to hidden mode and true human intent.

## Metrics

Primary metrics:

1. Task success.
2. Safety violation rate.
3. Authority regret: cost gap to the best actor for the realized hidden mode.
4. Unnecessary handoff rate.
5. Late handoff rate.
6. Human burden: cumulative time under human authority and intervention frequency.
7. Recovery success after a wrong initial authority assignment.
8. Smoothness and completion time.

Statistical reporting:

1. Seven deterministic seeds.
2. Per-task and per-split means with 95 percent confidence intervals.
3. Paired seed-level differences against the strongest non-oracle baseline.
4. Explicit terminal recommendation in `results/summary.txt`.

## Ablations

The full method must beat its own stripped versions:

1. `full_authority_boundary`
2. `minus_consequence_model`
3. `minus_intent_ambiguity`
4. `minus_recovery_burden`
5. `minus_handoff_hysteresis`
6. `confidence_only_boundary`
7. `safety_only_boundary`

If any core ablation improves task success without a clear safety/burden tradeoff, the main claim is not submission-ready.

## Stress Tests

Stress axes:

1. Human command delay.
2. Intent ambiguity.
3. Contact-mode unpredictability.
4. Fragile obstacle density.
5. Controller tracking noise.
6. Combined maximum stress.

The proposed method must not win only at a tuned operating point. I will generate stress curves and identify negative cases where authority boundaries fail.

## Paper Rewrite Requirements

After the evidence run:

1. Rewrite `paper/main.tex` as either a strong-revise evidence report or a negative evidence audit.
2. Replace template claims with measured claims only.
3. Include tables for combined stress, ablations, and failure cases.
4. Include figures for success/safety/burden, authority quality, ablations, and stress curves.
5. Update README, child status, and root reports.
6. Build only `C:/Users/wangz/Downloads/90.pdf`; do not copy anything to Desktop.
7. Commit and push to `https://github.com/Jason-Wang313/90_control_authority_boundaries` as a public repo.

## Terminal Gate

Mark `STRONG_REVISE` only if all of the following are true:

1. `proposed_authority_boundary` beats the strongest non-oracle baseline on combined-stress task success with a paired CI that does not make the gain look like noise.
2. It also improves either safety violation or authority regret without materially increasing human burden.
3. Core ablations degrade in the expected directions.
4. Maximum-stress curves do not reverse in favor of CBF, MPC, Bayesian allocation, or controller fusion.
5. The paper honestly states that evidence is local/simulated and not hardware validation.

Otherwise mark `KILL_ARCHIVE`. A promising but non-decisive local result is not ICLR-main ready.
