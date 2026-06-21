# Paper 90 Submission Readiness Audit v5

Date: 2026-06-22

Decision: KILL_ARCHIVE

ICLR main ready: no

## Artifact

- Canonical PDF: `C:/Users/wangz/Downloads/90.pdf`
- Pages: 29
- SHA256: `7C5590AC45F6E70BC75425A64D7AAB76142C51F528AEA636E16413533AEF9346`
- Citation UX: bright boxed clickable internal citation links.
- Desktop policy: no visible Desktop PDF copy.

## Evidence Inventory

- Main rollout rows: 199,680.
- Dataset summary rows: 15,360.
- Main seed-metric rows: 1,040.
- Main metric rows: 1,248.
- Main pairwise rows: 672.
- Hard aggregate seed rows: 130.
- Hard aggregate metric rows: 156.
- Hard aggregate pairwise rows: 84.
- Ablation rollout rows: 33,600.
- Ablation seed rows: 200.
- Ablation metric rows: 20.
- Stress raw rows: 302,400.
- Stress seed rows: 2,520.
- Stress metric rows: 252.
- Fixed-risk raw rows: 69,120.
- Fixed-risk seed rows: 480.
- Fixed-risk metric rows: 48.
- Fixed-risk pairwise rows: 200.
- Negative cases: 24.

## Frozen Gate Result

- Best success reference: `recovery_aware_mpc`.
- Safest reference: `cbf_safety_filter`.
- Lowest burden reference: `fixed_policy_authority`.
- Lowest regret reference: `mpc_risk_arbitration`.
- Best utility reference: `cbf_safety_filter`.
- Proposed success: 0.37096 versus best success 0.47370.
- Proposed safety violation: 0.22734 versus safest 0.15404.
- Proposed burden: 0.67510 versus lowest burden 0.26831.
- Proposed regret: 0.31249 versus lowest regret 0.24285.
- Proposed utility: -0.09423 versus best utility 0.16009.
- Paired success lower95: -0.12094.
- Paired safety upper95 versus CBF: 0.08260.
- Main gate: false.
- Mechanism gate: false.
- Stress gate: false.
- Fixed-risk gate: false.
- Scope gate: false.

## Why The Paper Is Not Submission Ready

`authority_boundary_v5` is scientifically more defensible than v4, but it does not survive hostile review. Recovery-aware MPC wins hard-aggregate success, CBF wins safety and robust utility, MPC wins regret, fixed policy wins burden, `safety_only_boundary` is the best removed-component ablation, maximum combined stress is dominated by CBF, and fixed-risk coverage at budget 0.05 is zero on hard fixed-risk splits.

The missing external evidence is decisive. Without real robot validation, accepted high-fidelity simulator evidence, trained deployed controller artifacts, or independent external baselines, this remains an archive-quality negative result.
