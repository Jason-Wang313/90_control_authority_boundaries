# Submission Readiness Audit v4

Date: 2026-06-15

Paper: 90 Control Authority Boundaries

Terminal decision: KILL_ARCHIVE

## Commands Run

```powershell
python -m py_compile src\run_experiment.py
python src\run_experiment.py
```

Both commands completed. The full experiment output was redirected to `logs/90_control_authority_boundaries_continuation_rerun_20260615.log`.

## Evidence Coverage

- Main rollouts: 80,640 rows.
- Main seed metrics: 1,260 rows.
- Main aggregate metrics: 45 rows.
- Pairwise gate rows: 1 row.
- Ablation rollouts: 12,544 rows.
- Ablation seed metrics: 196 rows.
- Ablation aggregate metrics: 7 rows.
- Stress rollouts: 47,040 rows.
- Stress aggregates: 42 rows.
- Negative cases: 3 rows.
- Seeds: 0, 1, 2, 3, 4, 5, 6.
- Tasks: `fragile_reaching`, `contact_door_opening`, `delayed_corridor_navigation`, `tool_alignment`.
- Splits: `nominal_shared_autonomy`, `intent_ambiguity_shift`, `contact_mode_shift`, `human_delay_shift`, `combined_authority_stress`.
- Methods: `fixed_policy_authority`, `fixed_human_authority`, `confidence_threshold_shared_control`, `bayesian_authority_allocation`, `cbf_safety_filter`, `mpc_risk_arbitration`, `controller_fusion_prior`, `proposed_authority_boundary`, `oracle_authority_boundary`.

## Main Gate

On combined authority stress, `proposed_authority_boundary` reaches `0.51618 +/- 0.17545` task success. The strongest non-oracle baseline, `cbf_safety_filter`, reaches `0.97991 +/- 0.00702`. The paired task-success difference is `-0.46373 +/- 0.17551`, which directly fails the primary gate.

## Contradictory Evidence

- Human burden is `0.85824` for the proposed method, versus `0.05055` for CBF and `0.09830` for MPC.
- `safety_only_boundary` reaches `0.97768` task success.
- `minus_intent_ambiguity` reaches `0.94587` task success.
- At maximum combined stress, CBF reaches `0.97946`, MPC reaches `0.97321`, and the proposed method reaches `0.50625`.

## Readiness Judgment

The paper is reproducible as a local negative evidence audit, but not submission-ready for ICLR main. It lacks robot hardware, accepted high-fidelity shared-autonomy benchmark validation, and decisive evidence beyond CBF/MPC/Bayesian baselines.

## Terminal Action

Keep `KILL_ARCHIVE`. Do not submit this paper to ICLR main in the current form.
