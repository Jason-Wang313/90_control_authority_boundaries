# Submission Readiness Decision

Decision: KILL_ARCHIVE

ICLR main-conference readiness: NO.

Paper 90 was rebuilt as a v4 deterministic closed-loop shared-autonomy evidence audit. The evidence is not enough for an ICLR main submission.

Latest rerun: 2026-06-15 from `src/run_experiment.py`; output redirected to `logs/90_control_authority_boundaries_continuation_rerun_20260615.log`.

Evidence coverage: 80,640 main rollouts, 12,544 ablation rollouts, 47,040 stress rollouts, seven seeds, four tasks, five authority-stress splits, nine methods, seven ablations, and three negative cases.

Reasons:

- The proposed authority-boundary mechanism reaches only 0.516 task success on combined authority stress.
- CBF safety filtering reaches 0.980 task success and MPC risk arbitration reaches 0.976.
- The paired task-success difference against the strongest non-oracle baseline is -0.464 +/- 0.176.
- The proposed method carries high human burden at 0.858.
- Core ablations contradict the mechanism: safety-only reaches 0.978 success and minus-intent reaches 0.946.
- At maximum combined stress, CBF reaches 0.979 success, MPC reaches 0.973, and the proposed method reaches only 0.506.
- No robot hardware, accepted high-fidelity simulator, or external benchmark validation is available.

Honest terminal action: archive/kill for ICLR main. Do not submit this paper to ICLR main in the current form.

Revival condition: a substantially different authority-allocation mechanism that beats CBF, MPC, Bayesian allocation, and controller fusion on external robot evidence.
