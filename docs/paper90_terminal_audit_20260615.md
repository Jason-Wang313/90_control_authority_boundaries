# Paper 90 Terminal Audit

Date: 2026-06-15

Paper: `90_control_authority_boundaries`

Decision: `KILL_ARCHIVE`

## Reproduction

- `python -m py_compile src\run_experiment.py`: passed.
- `python src\run_experiment.py`: passed; log at `logs/90_control_authority_boundaries_continuation_rerun_20260615.log`.
- PDF target: `C:/Users/wangz/Downloads/90.pdf`.
- Visible Desktop copy: not allowed.

## Evidence Files

- `results/rollouts.csv`: 80,640 rows.
- `results/raw_seed_metrics.csv`: 1,260 rows.
- `results/metrics.csv`: 45 rows.
- `results/pairwise_stats.csv`: 1 row.
- `results/ablation_rollouts.csv`: 12,544 rows.
- `results/ablation_seed_metrics.csv`: 196 rows.
- `results/ablation_metrics.csv`: 7 rows.
- `results/stress_sweep_raw.csv`: 47,040 rows.
- `results/stress_sweep.csv`: 42 rows.
- `results/negative_cases.csv`: 3 rows.

## Key Results

Combined authority stress:

- `proposed_authority_boundary`: task success `0.51618 +/- 0.17545`, safety violation `0.57087`, authority regret `0.02647`, human burden `0.85824`.
- `cbf_safety_filter`: task success `0.97991 +/- 0.00702`, safety violation `0.58036`, authority regret `0.02654`, human burden `0.05055`.
- `mpc_risk_arbitration`: task success `0.97600 +/- 0.00695`, safety violation `0.58594`, authority regret `0.02094`, human burden `0.09830`.
- Paired task-success difference versus `cbf_safety_filter`: `-0.46373 +/- 0.17551`.

Ablation:

- Full method task success: `0.50446`.
- `safety_only_boundary` task success: `0.97768`.
- `minus_intent_ambiguity` task success: `0.94587`.

Maximum combined stress:

- `proposed_authority_boundary` task success: `0.50625`.
- `cbf_safety_filter` task success: `0.97946`.
- `mpc_risk_arbitration` task success: `0.97321`.

## Terminal Reason

The local benchmark is useful and reproducible, but the proposed mechanism loses decisively to strong shared-autonomy baselines, imposes high human burden, fails ablation gates, and has no robot hardware or accepted high-fidelity benchmark evidence. The only honest ICLR-main decision is `KILL_ARCHIVE`.

## PDF Verification

- Build command: two-pass `pdflatex -interaction=nonstopmode -halt-on-error main.tex`.
- Canonical PDF: `C:/Users/wangz/Downloads/90.pdf`.
- PDF SHA256: `598EF476CDB8FEED13CCB7484D43310EED380F22DEBAB9FD044D87252E47BA9C`.
- PDF size: 360,914 bytes.
- LaTeX log scan: no document warnings/errors requiring action after the second pass.
- Desktop copy: absent.
