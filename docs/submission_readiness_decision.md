# Submission Readiness Decision

Decision: KILL_ARCHIVE

ICLR main-conference readiness: NO.

Paper 90 was rebuilt as a v4 deterministic closed-loop shared-autonomy evidence audit. The evidence is not enough for an ICLR main submission.

Reasons:

- The proposed authority-boundary mechanism reaches only 0.516 task success on combined authority stress.
- CBF safety filtering reaches 0.980 task success and MPC risk arbitration reaches 0.976.
- The paired task-success difference against the strongest non-oracle baseline is -0.464 +/- 0.176.
- The proposed method carries high human burden at 0.858.
- Core ablations contradict the mechanism: safety-only reaches 0.978 success and minus-intent reaches 0.946.
- No robot hardware, accepted high-fidelity simulator, or external benchmark validation is available.

Honest terminal action: archive/kill for ICLR main. Do not submit this paper to ICLR main in the current form.

Revival condition: a substantially different authority-allocation mechanism that beats CBF, MPC, Bayesian allocation, and controller fusion on external robot evidence.
