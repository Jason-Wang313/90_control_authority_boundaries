# Final Audit

1. Chosen thesis: Control Authority Boundaries explores `Model where authority should shift between policy, controller, and human.` for shared autonomy and robot control.
2. Rebuild version: v5 expanded-standard deterministic closed-loop evidence audit.
3. ICLR-main decision: KILL_ARCHIVE.
4. Reason: `authority_boundary_v5` improves over v4 but fails the frozen hostile-review gates against CBF, MPC, recovery-aware MPC, simple authority policies, ablations, stress tests, fixed-risk checks, and external-validation requirements.
5. Closest hostile prior work: see `docs/hostile_prior_work.md`, `docs/hostile_prior_work_100_cards.csv`, `docs/hostile_reviewer_response.md`, and the generated 120-reference bibliography in `paper/references.bib`.
6. Reproducibility: `python -m py_compile src\run_experiment.py`, `python src\run_experiment.py`, `python scripts\generate_manuscript.py`, LaTeX/BibTeX compilation, and `python scripts\validate_submission_artifacts.py` completed on 2026-06-22.
7. Claim-validity status: explicit authority-boundary state is diagnostically interesting but not supported as a submission-ready main mechanism.
8. Evidence coverage: 199,680 main rollouts, 15,360 dataset-summary rows, 1,040 seed-metric rows, 1,248 aggregate metric rows, 672 paired rows, 130 hard-aggregate seed rows, 156 hard-aggregate metric rows, 84 hard-aggregate paired rows, 33,600 ablation rows, 302,400 stress rows, 69,120 fixed-risk rows, and 24 negative cases.
9. Main result: hard-aggregate `authority_boundary_v5` success `0.37096` versus `0.47370` for `recovery_aware_mpc`; paired success lower95 `-0.12094`.
10. Safety result: `authority_boundary_v5` violation `0.22734` versus `0.15404` for `cbf_safety_filter`; paired safety upper95 against CBF `0.08260`.
11. Mechanism result: the best removed-component ablation is `safety_only_boundary`; `mechanism_gate=False`.
12. Stress result: maximum combined stress is dominated by `cbf_safety_filter`; `stress_gate=False`.
13. Fixed-risk result: budget 0.05 coverage is zero on both hard fixed-risk splits; `fixed_risk_gate=False`.
14. Exact Downloads PDF path: `C:/Users/wangz/Downloads/90.pdf`
15. PDF validation: 29 pages, SHA256 `7C5590AC45F6E70BC75425A64D7AAB76142C51F528AEA636E16413533AEF9346`, bright boxed internal citation links validated.
16. GitHub URL: https://github.com/Jason-Wang313/90_control_authority_boundaries
17. Confirmation: no visible Desktop copy was requested or made.
