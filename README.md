# 90 Control Authority Boundaries

Submission-hardening version: v5 expanded

Terminal decision: KILL_ARCHIVE for ICLR main conference.

This repository contains a deterministic CPU-only, RAM-light hostile-review audit for the claim that robots should keep explicit boundaries over policy, controller, and human control authority. The v5 rebuild expands the old four-page artifact into a 29-page ICLR-style negative archive manuscript with bright boxed clickable citations, generated tables, full CSV evidence, validation scripts, and a Downloads-only canonical PDF.

## Key Result

The proposed `authority_boundary_v5` improves over `authority_boundary_v4`, but it is still not submission-ready:

- Hard-aggregate success: `authority_boundary_v5` 0.37096 versus `recovery_aware_mpc` 0.47370.
- Hard-aggregate safety violation: `authority_boundary_v5` 0.22734 versus `cbf_safety_filter` 0.15404.
- Human burden: `authority_boundary_v5` 0.67510 versus `fixed_policy_authority` 0.26831.
- Authority regret: `authority_boundary_v5` 0.31249 versus `mpc_risk_arbitration` 0.24285.
- Robust utility: `authority_boundary_v5` -0.09423 versus `cbf_safety_filter` 0.16009.
- Paired success lower95 versus the strongest non-oracle baseline: -0.12094.
- Frozen gates: `main_gate=False`, `mechanism_gate=False`, `stress_gate=False`, `fixed_risk_gate=False`, `scope_gate=False`.

The terminal decision stays `KILL_ARCHIVE`: v5 is a stronger and more honest paper, not a main-conference submission. The method fails strong-baseline, safety, mechanism-ablation, maximum-stress, fixed-risk, and external-validation gates.

## Evidence Coverage

- Main rollout rows: 199,680.
- Dataset summary rows: 15,360.
- Main seed-metric rows: 1,040.
- Main aggregate metric rows: 1,248.
- Main paired rows: 672.
- Hard-aggregate seed rows: 130.
- Hard-aggregate metric rows: 156.
- Hard-aggregate paired rows: 84.
- Ablation rollout rows: 33,600.
- Stress raw rows: 302,400.
- Fixed-risk raw rows: 69,120.
- Negative cases: 24.
- Splits: eight authority and deployment-stress splits, including `combined_authority_stress` and `low_signal_high_risk_shift`.
- Methods: thirteen authority-allocation methods, including CBF, MPC, POMDP, recovery-aware MPC, uncertainty handoff, v4, v5, and oracle controls.

## Reproduce Evidence

```powershell
python -m py_compile src\run_experiment.py
python src\run_experiment.py
python scripts\generate_manuscript.py
python scripts\validate_submission_artifacts.py
```

## Rebuild PDF

```powershell
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
Copy-Item -LiteralPath main.pdf -Destination C:\Users\wangz\Downloads\90.pdf -Force
```

Canonical local PDF: `C:/Users/wangz/Downloads/90.pdf`

Validated PDF: 29 pages, SHA256 `7C5590AC45F6E70BC75425A64D7AAB76142C51F528AEA636E16413533AEF9346`.

No PDF should be copied to the visible Desktop.
