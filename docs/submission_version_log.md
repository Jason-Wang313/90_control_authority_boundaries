# Submission Version Log

## v1 - Generated Draft
- Original continuation-batch generated paper and toy single-seed experiment.

## v2 - Submission Hardening
- Added hostile reviewer attack log and response docs.
- Replaced the toy experiment with seven-seed metrics, stronger baselines, ablations, stress tests, and negative cases.
- Narrowed claims to synthetic diagnostic evidence.
- Recompiled canonical PDF at `C:/Users/wangz/Downloads/90.pdf`.
- Terminal decision: WORKSHOP_ONLY.

## v3 - ICLR Main Gate Archive
- Applied the stricter ICLR-main-conference standard.
- Re-read local paper, docs, experiments, prior-work artifacts, PDF state, and repo state.
- Determined that missing real-robot/high-fidelity evidence, template-generated experiments, and unresolved novelty threats are not recoverable from local artifacts.
- Recompiled the canonical PDF with `Submission-hardening version: v3`.
- Terminal decision: KILL_ARCHIVE.

## v4 - Paper-Specific Authority-Boundary Rebuild
- Replaced the generic archive framing with a deterministic closed-loop shared-autonomy benchmark.
- Added four tasks, five authority-stress splits, nine methods, seven seeds, ablations, stress sweep, negative cases, and figures.
- Reported 80,640 main rollouts, 12,544 ablation rollouts, and 47,040 stress rollouts.
- Found that the proposed authority-boundary mechanism loses decisively to CBF and MPC baselines and fails ablation gates.
- Terminal decision: KILL_ARCHIVE.

## v4.1 - 2026-06-15 Rerun Audit
- Re-ran `python -m py_compile src\run_experiment.py` and the full `python src\run_experiment.py`.
- Confirmed the paired task-success difference versus `cbf_safety_filter` is `-0.46373 +/- 0.17551`.
- Confirmed high human burden, ablation contradiction, and maximum-stress failure.
- Updated child docs and paper source to keep the v4 KILL_ARCHIVE decision evidence-bound.

## v5 - Expanded-Standard Submission Audit
- Froze a plan-first hostile-review protocol before execution.
- Rebuilt the benchmark with ten seeds, six tasks, eight splits, thirteen methods, 199,680 main rollouts, 15,360 dataset-summary rows, 1,040 seed-metric rows, 1,248 aggregate metric rows, 672 paired rows, 130 hard-aggregate seed rows, 156 hard-aggregate metric rows, 84 hard-aggregate paired rows, 33,600 ablation rows, 302,400 stress rows, 69,120 fixed-risk rows, and 24 negative cases.
- Added stronger CBF, MPC, POMDP, uncertainty-triggered, recovery-aware, v4, v5, and oracle references.
- Added generated tables, paper-specific figures, split-level paired checks, ablation utility, stress sweep, fixed-risk analysis, and negative cases.
- Generated a 29-page ICLR-style manuscript with bright boxed clickable citations and a 120-entry bibliography.
- Validated the canonical Downloads-only PDF at `C:/Users/wangz/Downloads/90.pdf`; SHA256 `7C5590AC45F6E70BC75425A64D7AAB76142C51F528AEA636E16413533AEF9346`.
- Terminal decision remains KILL_ARCHIVE because `authority_boundary_v5` fails hard-aggregate success, safety, burden, regret, utility, mechanism-ablation, maximum-stress, fixed-risk, and external-validation gates.
