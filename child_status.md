# Child Status 90

Current stage: expanded-standard v5 terminal audit
Last update: 2026-06-22 03:35:00 +08:00
PDF: C:/Users/wangz/Downloads/90.pdf
PDF SHA256: 7C5590AC45F6E70BC75425A64D7AAB76142C51F528AEA636E16413533AEF9346
PDF pages: 29
GitHub: https://github.com/Jason-Wang313/90_control_authority_boundaries
Submission-hardening version: v5 expanded
Terminal decision: KILL_ARCHIVE
ICLR main ready: no

Latest rerun: `python -m py_compile src\run_experiment.py`, full `python src\run_experiment.py`, `python scripts\generate_manuscript.py`, LaTeX/BibTeX compilation, and `python scripts\validate_submission_artifacts.py` completed on 2026-06-22.

Evidence inventory: 199,680 main rollouts, 15,360 dataset-summary rows, 1,040 seed-metric rows, 1,248 aggregate metric rows, 672 paired rows, 130 hard-aggregate seed rows, 156 hard-aggregate metric rows, 84 hard-aggregate paired rows, 33,600 ablation rows, 302,400 stress rows, 69,120 fixed-risk rows, and 24 negative cases.

Reason: `authority_boundary_v5` improves over v4 but remains dominated under the frozen hostile-review gates. It reaches 0.37096 hard-aggregate task success versus 0.47370 for `recovery_aware_mpc`, has worse safety than `cbf_safety_filter` (0.22734 versus 0.15404 violation), worse robust utility than CBF (-0.09423 versus 0.16009), higher burden than fixed policy authority, and zero fixed-risk coverage at budget 0.05 on the hard fixed-risk splits. No robot hardware or accepted high-fidelity simulator validation is available.
