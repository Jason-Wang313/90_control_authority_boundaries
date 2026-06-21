# Submission Readiness Decision

Decision: KILL_ARCHIVE

ICLR main-conference readiness: NO.

Paper 90 was rebuilt as a v5 expanded-standard deterministic shared-autonomy audit. The artifact is much stronger than the old draft and meets the requested 25+ page manuscript bar, but the evidence still does not justify an ICLR main submission.

Latest rerun: 2026-06-22 from `src/run_experiment.py`, followed by generated manuscript rebuild and `scripts/validate_submission_artifacts.py`.

Evidence coverage: 199,680 main rollouts, 15,360 dataset-summary rows, 1,040 seed-metric rows, 1,248 aggregate metric rows, 672 paired rows, 130 hard-aggregate seed rows, 156 hard-aggregate metric rows, 84 hard-aggregate paired rows, 33,600 ablation rows, 302,400 stress rows, 69,120 fixed-risk rows, and 24 negative cases.

Reasons:

- Hard-aggregate task success is 0.37096 for `authority_boundary_v5` versus 0.47370 for `recovery_aware_mpc`.
- Safety violation is 0.22734 for `authority_boundary_v5` versus 0.15404 for `cbf_safety_filter`.
- Human burden remains high at 0.67510 versus 0.26831 for `fixed_policy_authority`.
- Authority regret is worse than `mpc_risk_arbitration` (0.31249 versus 0.24285).
- Robust utility is worse than `cbf_safety_filter` (-0.09423 versus 0.16009).
- Paired task-success lower95 against the strongest non-oracle baseline is -0.12094.
- The best removed-component ablation is `safety_only_boundary`, so the mechanism gate fails.
- Maximum combined stress is dominated by `cbf_safety_filter`, so the stress gate fails.
- Fixed-risk budget 0.05 coverage is zero on the hard fixed-risk splits.
- No robot hardware, accepted high-fidelity simulator, trained deployed controller, or external benchmark validation is available.

Honest terminal action: archive/kill for ICLR main. Do not submit this paper to ICLR main in the current form.

Revival condition: a substantially different authority-allocation mechanism that beats CBF, MPC, recovery-aware MPC, POMDP handoff, and simple controller policies under external robot or accepted high-fidelity benchmark evidence, with preregistered fixed-risk and stress gates cleared after freezing the protocol.
