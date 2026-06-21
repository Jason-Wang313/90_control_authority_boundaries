# Paper 90 Terminal Audit 2026-06-21

Terminal action: KILL_ARCHIVE

The v5 expanded-standard run completed the requested plan-first hostile-review protocol for Paper 90. It produced a 29-page manuscript, generated tables and figures, seed-level paired tests, ablations, stress sweeps, fixed-risk checks, negative cases, bright boxed clickable citations, and a validated Downloads-only PDF.

## Validation

- `python -m py_compile src\run_experiment.py`: pass.
- `python src\run_experiment.py`: pass.
- `python scripts\generate_manuscript.py`: pass.
- LaTeX/BibTeX compile: pass.
- `python scripts\validate_submission_artifacts.py`: pass.
- PDF pages: 29.
- PDF SHA256: `7C5590AC45F6E70BC75425A64D7AAB76142C51F528AEA636E16413533AEF9346`.
- Desktop PDF leak: none.

## Decision Rationale

The expanded experiment improves the local evidence base but does not rescue the submission. `authority_boundary_v5` reaches 0.37096 hard-aggregate task success, behind `recovery_aware_mpc` at 0.47370. Its safety violation rate is 0.22734, behind `cbf_safety_filter` at 0.15404. Its robust utility is -0.09423, behind CBF at 0.16009. Its burden and regret are also worse than simple or MPC references.

The result is therefore not a pretty negative result; it is the useful kind. The method is clearer, the paper is larger, and the evidence is harder to dismiss, but the final action remains archive rather than submit.
