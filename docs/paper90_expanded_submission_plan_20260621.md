# Paper 90 Expanded Submission Plan

Date frozen: 2026-06-22 +08:00.

Objective: rebuild Paper 90 into a 25+ page ICLR-style submission-readiness audit, CPU-only and RAM-light, without hiding failures. The output must be a numbered PDF at `C:/Users/wangz/Downloads/90.pdf` only, with no visible Desktop copy. The repository must be pushed to the public GitHub repo after validation.

## Research Bet

Robots should maintain explicit control-authority boundaries: when authority belongs to a learned policy, when a certified/controller layer should take over, when human authority is needed, and when blended authority is safer than a hard handoff.

## Proposed v5 Method

`authority_boundary_v5` scores candidate authority modes using:

- physical consequence risk,
- intent ambiguity,
- control-barrier violation risk,
- human delay and burden,
- recovery feasibility,
- handoff hysteresis,
- boundary uncertainty,
- authority churn penalties.

The v5 audit will report whether this boundary model helps after comparing against simpler and stronger shared-autonomy/control baselines.

## Frozen Experimental Scope

- Seeds: 10.
- Tasks: 6.
- Splits: 8.
- Methods: 13.
- Main episodes per task/split/method/seed: 32.
- Main rollout rows: 199,680.
- Dataset-summary rows: 15,360.
- Ablation variants: 10.
- Ablation rollout rows: 33,600.
- Stress axes: 6.
- Stress levels: 6.
- Stress raw rows: 302,400.
- Fixed-risk raw rows: 69,120.
- Negative cases: 24.

## Tasks

- `fragile_reaching`
- `contact_door_opening`
- `delayed_corridor_navigation`
- `tool_alignment`
- `handoff_tight_corridor`
- `deformable_fixture_alignment`

## Splits

- `nominal_shared_autonomy`
- `intent_ambiguity_shift`
- `contact_mode_shift`
- `human_delay_shift`
- `fragile_object_shift`
- `authority_churn_shift`
- `low_signal_high_risk_shift`
- `combined_authority_stress`

## Methods

- fixed learned policy
- fixed human teleoperation
- confidence threshold shared control
- Bayesian authority allocation
- uncertainty triggered handoff
- CBF safety filter
- MPC risk arbitration
- POMDP handoff policy
- controller fusion prior
- recovery-aware MPC
- `authority_boundary_v4`
- `authority_boundary_v5`
- oracle authority assignment

The manuscript will report all non-oracle references and use oracles only as diagnostic upper bounds.

## Metrics

- task success, higher is better.
- safety violation, lower is better.
- authority regret, lower is better.
- human burden, lower is better.
- late handoff rate, lower is better.
- handoff churn, lower is better.
- recovery success, higher is better.
- intervention cost, lower is better.
- robust utility, higher is better.

Robust utility is frozen before execution and penalizes safety violation, human burden, regret, late handoff, handoff churn, and intervention cost.

## Gates

- Main gate: v5 must beat the best non-oracle success reference on hard aggregate with positive paired lower95, while not worsening safety, burden, regret, late handoff, churn, or utility.
- Mechanism gate: the full v5 method must beat every component-removal ablation by a practical utility margin.
- Stress gate: at maximum combined stress, v5 must be non-dominated by CBF, MPC, Bayesian, POMDP, recovery-aware, and controller-fusion references.
- Fixed-risk gate: at strict safety budget `0.05`, v5 must have nonzero accepted coverage and best feasible accepted utility on hard fixed-risk splits.
- Scope gate: real robot or accepted high-fidelity external benchmark evidence is required for ICLR main readiness.

## Reporting Rule

Do not optimize for pretty results. Optimize for a result that survives hostile review. If the method fails, report `KILL_ARCHIVE` with complete evidence. If it passes locally but lacks external validation, report `STRONG_REVISE`, not ICLR-main ready.

## PDF and Citation Requirements

- Final PDF must be at least 25 pages.
- In-text citations must use bright boxed links that jump to the bibliography.
- The validator must check CSV row counts, PDF page count, Downloads-only placement, required summary tokens, LaTeX citation health, and internal citation-link annotations.
- Do not copy the PDF to the visible Desktop.
