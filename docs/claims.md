# Claims

- Mechanism claim tested: explicit authority boundaries should reduce unsafe or late handoff decisions by tracking policy, controller, and human authority as separate action-critical variables.
- Evidence claim supported: the v5 CPU-only benchmark is reproducible and includes strong local baselines, seed-level paired tests, ablations, stress sweeps, fixed-risk checks, and negative cases.
- Evidence claim not supported: `authority_boundary_v5` is not stronger than the best CBF/MPC/recovery-aware baselines on frozen hard-aggregate success, safety, burden, regret, utility, stress, or fixed-risk gates.
- Scope claim: the artifact supports a reproducible negative archive, not real-robot deployment or ICLR-main submission.
- Unsupported claims explicitly avoided: no claim of SOTA robot performance, no claim of hardware validation, and no claim that the proposed mechanism is necessary under strong ablations.
