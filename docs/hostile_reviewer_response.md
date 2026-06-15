# Hostile Reviewer Response

Paper: 90 Control Authority Boundaries

## Strongest Technical Threats
- Safety-Critical Control for Human-Robot Interaction in Shared Workspaces using Control Barrier Functions (2026)
- Adaptive Impedance Control for the Haptic Shared Driving Task Based on Nonlinear MPC (2020)
- Bayesian Controller Fusion: Leveraging Control Priors in Deep Reinforcement Learning for Robotics (2021)
- A Shared Control Approach Based on First-Order Dynamical Systems and Closed-Loop Variable Stiffness Control (2023)
- Haptic Shared Control for Human-Robot Collaboration: A Game-Theoretical Approach (2020)
- A Barrier Pair Method for Safe Human-Robot Shared Autonomy (2021)
- Online Hybrid Model Predictive Controller Design for Cruise Control of Automobiles (2017)
- Towards Explainable Co-Robots: Developing Confidence-Based Shared Control Paradigms (2020)

## ICLR Main Response
A hostile ICLR reviewer would be correct to reject this as a main-conference submission. The v4 paper has a deterministic closed-loop shared-autonomy benchmark, seven seeds, strong CBF/MPC/Bayesian/controller-fusion baselines, ablations, stress sweeps, and negative cases. Even so, the proposed method loses combined authority-stress success to CBF by `-0.46373 +/- 0.17551`, imposes high human burden, and is contradicted by safety-only and minus-intent ablations. The paper also lacks robot hardware or accepted high-fidelity shared-autonomy benchmark validation.

## Honest Action
The paper is marked `KILL_ARCHIVE`. This avoids converting a useful negative audit into an overstated main-conference claim.

## What Would Be Needed To Revive
- Real robot or accepted high-fidelity shared-autonomy benchmark experiments.
- A substantially different authority-allocation mechanism that beats CBF, MPC, Bayesian allocation, and controller fusion.
- Manual full-paper related-work audit.
- Paper-specific qualitative rollout analysis.
- Evidence that authority boundaries improve task success, safety/regret, and human burden under deployment shift.
