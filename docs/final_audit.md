# Final Audit

1. Chosen thesis: Control Authority Boundaries explores `Model where authority should shift between policy, controller, and human.` for shared autonomy and robot control.
2. Rebuild version: v4 deterministic closed-loop evidence audit.
3. ICLR-main decision: KILL_ARCHIVE.
4. Reason: the proposed boundary loses decisively to CBF and MPC on task success, has high human burden, and is contradicted by core ablations.
5. Closest hostile prior work: see `docs/hostile_prior_work.md`, `docs/hostile_prior_work_100_cards.csv`, and `docs/hostile_reviewer_response.md`.
6. Reproducibility: `python -m py_compile src\run_experiment.py` and `python src\run_experiment.py` were rerun on 2026-06-15; the full run log is `logs/90_control_authority_boundaries_continuation_rerun_20260615.log`.
7. Claim-validity status: explicit authority-boundary state is diagnostically interesting but not supported as a submission-ready main mechanism.
8. Evidence coverage: 80,640 main rollouts, 12,544 ablation rollouts, 47,040 stress rollouts, seven seeds, four tasks, five splits, nine methods, seven ablations, and three negative cases.
9. Main result: proposed success `0.51618` versus CBF `0.97991`; paired difference `-0.46373 +/- 0.17551`.
10. Exact Downloads PDF path: `C:/Users/wangz/Downloads/90.pdf`
11. GitHub URL: https://github.com/Jason-Wang313/90_control_authority_boundaries
12. Confirmation: no visible Desktop copy was requested or made.
