# Child Status 90

Current stage: ICLR main v4 evidence audit terminal
Last update: 2026-06-15 11:08:30 +01:00
PDF: C:/Users/wangz/Downloads/90.pdf
GitHub: https://github.com/Jason-Wang313/90_control_authority_boundaries
Submission-hardening version: v4
Terminal decision: KILL_ARCHIVE
ICLR main ready: no

Latest rerun: `python -m py_compile src\run_experiment.py` and full `python src\run_experiment.py` completed on 2026-06-15 with output redirected to `logs/90_control_authority_boundaries_continuation_rerun_20260615.log`.

Evidence inventory: 80,640 main rollouts, 12,544 ablation rollouts, 47,040 stress rollouts, seven seeds, four tasks, five authority-stress splits, nine methods, seven ablations, six stress levels, and three negative cases.

Reason: deterministic closed-loop shared-autonomy benchmark added and rerun. The proposed authority boundary loses task success to CBF and MPC baselines (`0.51618` vs `0.97991` and `0.97600`), carries much higher human burden (`0.85824`), and is contradicted by safety-only and minus-intent ablations. No robot hardware or accepted high-fidelity simulator validation is available.
