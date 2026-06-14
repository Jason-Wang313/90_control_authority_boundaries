# 90 Control Authority Boundaries

Submission-hardening version: v4

Terminal decision: KILL_ARCHIVE for ICLR main conference.

This repository now contains a deterministic closed-loop shared-autonomy evidence audit for the claim that robots should maintain explicit boundaries over policy, controller, and human control authority. The rebuilt benchmark includes four tasks, five shifts, seven seeds, nine authority-allocation methods, seven ablations, and a combined stress sweep.

## Key Result

On combined authority stress:

- Proposed authority boundary: task success 0.516, safety violation 0.571, authority regret 0.026, human burden 0.858.
- CBF safety filter: task success 0.980, safety violation 0.580, authority regret 0.027, human burden 0.051.
- MPC risk arbitration: task success 0.976, safety violation 0.586, authority regret 0.021, human burden 0.098.
- Paired task-success difference vs strongest non-oracle baseline: -0.464 +/- 0.176.

The proposed method is not submission-ready because it loses decisively to CBF/MPC baselines, imposes high human burden, and is contradicted by ablations. The safety-only ablation reaches 0.978 success and the minus-intent ablation reaches 0.946 success.

## Reproduce Evidence

```powershell
python src\run_experiment.py
```

## Rebuild PDF

```powershell
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Canonical local PDF: `C:/Users/wangz/Downloads/90.pdf`

No PDF should be copied to the visible Desktop.
