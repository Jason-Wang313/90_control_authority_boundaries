# Paper 90 ICLR-Main Submission-Readiness Execution Plan

Date: 2026-06-15

Paper: `90_control_authority_boundaries`

Target venue standard: ICLR main conference, evidence-first. The paper can advance only if explicit control-authority boundary state improves closed-loop shared-autonomy outcomes over strong CBF, MPC, Bayesian allocation, confidence, controller-fusion, human-only, policy-only, and oracle baselines. A diagnostic concept is not enough if task success, human burden, or ablations fail.

## Current State

The repository currently reports a v4 terminal decision of `KILL_ARCHIVE`. The core claim is that a robot should maintain explicit boundaries over whether authority belongs to a learned policy, low-level controller, or human. The prior v4 evidence is strongly negative: the proposed method loses task success to CBF and MPC baselines, imposes high human burden, and is contradicted by safety-only and minus-intent ablations.

## Execution Order

1. Verify repository hygiene before touching evidence.
   - Confirm worktree status.
   - Record current commit and remote.
   - Confirm the existing Downloads PDF and Desktop exclusion state.

2. Re-run the evidence generator from source.
   - Compile-check `src/run_experiment.py`.
   - Run `python src/run_experiment.py`.
   - Preserve generated CSVs, figures, and `results/summary.txt`.

3. Audit evidence completeness.
   - Confirm seven seeds.
   - Confirm all tasks, shifts, methods, ablations, stress axes, pairwise stats, and negative cases.
   - Confirm row counts and schemas for rollout, seed-level, aggregate, pairwise, ablation, stress, and negative-case outputs.

4. Apply the ICLR-main decision gate.
   - Require the proposed method to beat the strongest non-oracle baseline on combined authority-stress task success with paired uncertainty.
   - Require safety violation or authority regret improvement without excessive human burden.
   - Require ablations to degrade when consequence modeling, intent ambiguity, recovery burden, and handoff hysteresis are removed.
   - Require stress tests to preserve the same conclusion under human delay, intent ambiguity, contact-mode shift, fragile obstacles, controller noise, and combined stress.

5. Decide honestly.
   - If all local gates pass but evidence remains local synthetic only, mark at most `STRONG_REVISE`.
   - If CBF, MPC, Bayesian allocation, controller fusion, or any core ablation beats the proposed method on primary criteria, preserve `KILL_ARCHIVE`.
   - Do not claim ICLR-main readiness without robot hardware or accepted high-fidelity shared-autonomy benchmark validation.

6. Update child documentation and paper.
   - Align `README.md`, `child_status.md`, `plan.md`, readiness decision, final audit, hostile reviewer response, attack log, version log, and checklists with the rerun.
   - Add terminal audit docs with exact row counts, seed coverage, metric conclusions, PDF hash, and artifact-location checks.

7. Build and verify the PDF.
   - Build `paper/main.pdf` twice with LaTeX.
   - Copy only to `C:/Users/wangz/Downloads/90.pdf`.
   - Do not copy any PDF to the visible Desktop.
   - Scan the LaTeX log for warnings or errors that affect quality.

8. Update root ledgers.
   - Update `GLOBAL_POOL_STATUS.md`, `BATCH_STATUS.md`, `SUBMISSION_STATUS.md`, `MASTER_REPORT.md`, and `MASTER_SUBMISSION_REPORT.md`.

9. Commit, push, and verify.
   - Commit only Paper 90 child-repo files inside its repo.
   - Push `main` to the public GitHub repo.
   - Verify local `HEAD` equals `origin/main`.
   - Verify `C:/Users/wangz/Downloads/90.pdf` exists and `C:/Users/wangz/Desktop/90.pdf` does not.

## Expected Outcome Risk

The likely terminal decision is `KILL_ARCHIVE`. The previous v4 evidence reports a decisive negative task-success gap versus CBF, high human burden, ablation contradiction, and stress failure. The rerun will still be performed end-to-end, and the final decision will be evidence-bound.
