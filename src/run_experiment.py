import csv
import hashlib
import math
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

BASE_SEED = 90090090
SEEDS = list(range(10))
MAIN_EPISODES_PER_TASK = 32
ABLATION_EPISODES_PER_TASK = 28
STRESS_EPISODES_PER_TASK = 20
FIXED_EPISODES_PER_TASK = 24

TASKS = [
    {
        "task": "fragile_reaching",
        "difficulty": 0.38,
        "hazard": 0.48,
        "contact": 0.24,
        "ambiguity": 0.42,
        "delay": 0.18,
        "fragility": 0.62,
        "policy_skill": 0.34,
        "controller_skill": 0.28,
        "human_skill": 0.31,
    },
    {
        "task": "contact_door_opening",
        "difficulty": 0.43,
        "hazard": 0.34,
        "contact": 0.60,
        "ambiguity": 0.36,
        "delay": 0.20,
        "fragility": 0.30,
        "policy_skill": 0.30,
        "controller_skill": 0.39,
        "human_skill": 0.27,
    },
    {
        "task": "delayed_corridor_navigation",
        "difficulty": 0.41,
        "hazard": 0.56,
        "contact": 0.28,
        "ambiguity": 0.50,
        "delay": 0.42,
        "fragility": 0.46,
        "policy_skill": 0.33,
        "controller_skill": 0.31,
        "human_skill": 0.33,
    },
    {
        "task": "tool_alignment",
        "difficulty": 0.46,
        "hazard": 0.30,
        "contact": 0.44,
        "ambiguity": 0.58,
        "delay": 0.24,
        "fragility": 0.38,
        "policy_skill": 0.29,
        "controller_skill": 0.33,
        "human_skill": 0.35,
    },
    {
        "task": "handoff_tight_corridor",
        "difficulty": 0.45,
        "hazard": 0.54,
        "contact": 0.36,
        "ambiguity": 0.44,
        "delay": 0.48,
        "fragility": 0.40,
        "policy_skill": 0.31,
        "controller_skill": 0.36,
        "human_skill": 0.30,
    },
    {
        "task": "deformable_fixture_alignment",
        "difficulty": 0.49,
        "hazard": 0.38,
        "contact": 0.58,
        "ambiguity": 0.46,
        "delay": 0.28,
        "fragility": 0.55,
        "policy_skill": 0.28,
        "controller_skill": 0.34,
        "human_skill": 0.34,
    },
]

SPLITS = {
    "nominal_shared_autonomy": {
        "hazard": 0.00,
        "contact": 0.00,
        "ambiguity": 0.00,
        "delay": 0.00,
        "noise": 0.08,
        "fragility": 0.00,
        "churn": 0.04,
        "low_signal": 0.02,
    },
    "intent_ambiguity_shift": {
        "hazard": 0.03,
        "contact": 0.02,
        "ambiguity": 0.28,
        "delay": 0.06,
        "noise": 0.11,
        "fragility": 0.02,
        "churn": 0.10,
        "low_signal": 0.10,
    },
    "contact_mode_shift": {
        "hazard": 0.10,
        "contact": 0.30,
        "ambiguity": 0.06,
        "delay": 0.04,
        "noise": 0.12,
        "fragility": 0.08,
        "churn": 0.09,
        "low_signal": 0.06,
    },
    "human_delay_shift": {
        "hazard": 0.08,
        "contact": 0.04,
        "ambiguity": 0.14,
        "delay": 0.34,
        "noise": 0.12,
        "fragility": 0.05,
        "churn": 0.12,
        "low_signal": 0.08,
    },
    "fragile_object_shift": {
        "hazard": 0.16,
        "contact": 0.10,
        "ambiguity": 0.10,
        "delay": 0.08,
        "noise": 0.13,
        "fragility": 0.34,
        "churn": 0.08,
        "low_signal": 0.08,
    },
    "authority_churn_shift": {
        "hazard": 0.10,
        "contact": 0.12,
        "ambiguity": 0.24,
        "delay": 0.18,
        "noise": 0.18,
        "fragility": 0.10,
        "churn": 0.36,
        "low_signal": 0.14,
    },
    "low_signal_high_risk_shift": {
        "hazard": 0.26,
        "contact": 0.22,
        "ambiguity": 0.24,
        "delay": 0.18,
        "noise": 0.22,
        "fragility": 0.22,
        "churn": 0.18,
        "low_signal": 0.36,
    },
    "combined_authority_stress": {
        "hazard": 0.25,
        "contact": 0.26,
        "ambiguity": 0.26,
        "delay": 0.28,
        "noise": 0.22,
        "fragility": 0.24,
        "churn": 0.30,
        "low_signal": 0.28,
    },
}

HARD_SPLITS = [
    "fragile_object_shift",
    "authority_churn_shift",
    "low_signal_high_risk_shift",
    "combined_authority_stress",
]
FIXED_SPLITS = ["low_signal_high_risk_shift", "combined_authority_stress"]
ABLATION_SPLITS = ["low_signal_high_risk_shift", "combined_authority_stress"]

METHODS = [
    "fixed_policy_authority",
    "fixed_human_teleoperation",
    "confidence_threshold_shared_control",
    "bayesian_authority_allocation",
    "uncertainty_triggered_handoff",
    "cbf_safety_filter",
    "mpc_risk_arbitration",
    "pomdp_handoff_policy",
    "controller_fusion_prior",
    "recovery_aware_mpc",
    "authority_boundary_v4",
    "authority_boundary_v5",
    "oracle_authority_assignment",
]

STRESS_METHODS = [
    "confidence_threshold_shared_control",
    "bayesian_authority_allocation",
    "cbf_safety_filter",
    "mpc_risk_arbitration",
    "pomdp_handoff_policy",
    "recovery_aware_mpc",
    "authority_boundary_v5",
]

FIXED_METHODS = [
    "bayesian_authority_allocation",
    "cbf_safety_filter",
    "mpc_risk_arbitration",
    "pomdp_handoff_policy",
    "recovery_aware_mpc",
    "authority_boundary_v5",
]

ABLATIONS = [
    "full_authority_boundary_v5",
    "minus_consequence_risk_model",
    "minus_intent_ambiguity_gate",
    "minus_human_burden_model",
    "minus_handoff_hysteresis",
    "minus_boundary_uncertainty",
    "minus_recovery_feasibility",
    "confidence_only_boundary",
    "safety_only_boundary",
    "mpc_only_boundary",
]

METRICS = [
    "task_success",
    "safety_violation",
    "authority_regret",
    "human_burden",
    "late_handoff",
    "handoff_churn",
    "recovery_success",
    "intervention_cost",
    "boundary_calibration_error",
    "override_precision",
    "unsafe_autonomy",
    "robust_utility",
]

PAIRWISE_REFERENCES = [
    "bayesian_authority_allocation",
    "uncertainty_triggered_handoff",
    "cbf_safety_filter",
    "mpc_risk_arbitration",
    "pomdp_handoff_policy",
    "recovery_aware_mpc",
    "authority_boundary_v4",
]

FIXED_PAIRWISE_METRICS = ["coverage", "accepted_success", "accepted_safety_violation", "accepted_regret", "accepted_utility"]
STRESS_AXES = ["intent_ambiguity", "contact_mode", "human_delay", "fragility", "authority_churn", "combined"]
STRESS_LEVELS = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
RISK_BUDGETS = [0.02, 0.05, 0.10, 0.20]
PROPOSAL = "authority_boundary_v5"

PROFILES = {
    "fixed_policy_authority": dict(success=-0.20, safety=0.36, burden=0.02, regret=0.24, late=0.24, churn=0.04, recovery=0.18, cost=0.03, calib=0.25, precision=0.20),
    "fixed_human_teleoperation": dict(success=-0.07, safety=0.22, burden=0.88, regret=0.08, late=0.13, churn=0.03, recovery=0.54, cost=0.24, calib=0.16, precision=0.60),
    "confidence_threshold_shared_control": dict(success=-0.04, safety=0.25, burden=0.62, regret=0.11, late=0.11, churn=0.19, recovery=0.50, cost=0.16, calib=0.18, precision=0.52),
    "bayesian_authority_allocation": dict(success=0.10, safety=0.20, burden=0.48, regret=0.06, late=0.07, churn=0.13, recovery=0.67, cost=0.18, calib=0.12, precision=0.64),
    "uncertainty_triggered_handoff": dict(success=0.07, safety=0.19, burden=0.55, regret=0.07, late=0.06, churn=0.22, recovery=0.63, cost=0.17, calib=0.15, precision=0.62),
    "cbf_safety_filter": dict(success=0.23, safety=0.12, burden=0.08, regret=0.05, late=0.03, churn=0.06, recovery=0.76, cost=0.10, calib=0.11, precision=0.71),
    "mpc_risk_arbitration": dict(success=0.25, safety=0.15, burden=0.13, regret=0.03, late=0.02, churn=0.07, recovery=0.83, cost=0.16, calib=0.09, precision=0.74),
    "pomdp_handoff_policy": dict(success=0.18, safety=0.17, burden=0.31, regret=0.04, late=0.04, churn=0.11, recovery=0.77, cost=0.19, calib=0.10, precision=0.70),
    "controller_fusion_prior": dict(success=-0.11, safety=0.31, burden=0.20, regret=0.20, late=0.10, churn=0.16, recovery=0.36, cost=0.08, calib=0.19, precision=0.42),
    "recovery_aware_mpc": dict(success=0.24, safety=0.16, burden=0.18, regret=0.04, late=0.02, churn=0.08, recovery=0.88, cost=0.20, calib=0.10, precision=0.73),
    "authority_boundary_v4": dict(success=0.08, safety=0.20, burden=0.61, regret=0.07, late=0.05, churn=0.16, recovery=0.68, cost=0.18, calib=0.13, precision=0.65),
    "authority_boundary_v5": dict(success=0.15, safety=0.18, burden=0.46, regret=0.06, late=0.04, churn=0.14, recovery=0.74, cost=0.19, calib=0.12, precision=0.68),
    "oracle_authority_assignment": dict(success=0.32, safety=0.09, burden=0.18, regret=0.01, late=0.01, churn=0.05, recovery=0.94, cost=0.18, calib=0.04, precision=0.86),
    "full_authority_boundary_v5": dict(success=0.15, safety=0.18, burden=0.46, regret=0.06, late=0.04, churn=0.14, recovery=0.74, cost=0.19, calib=0.12, precision=0.68),
    "minus_consequence_risk_model": dict(success=0.09, safety=0.24, burden=0.43, regret=0.09, late=0.05, churn=0.13, recovery=0.68, cost=0.17, calib=0.15, precision=0.62),
    "minus_intent_ambiguity_gate": dict(success=0.20, safety=0.19, burden=0.27, regret=0.04, late=0.03, churn=0.09, recovery=0.76, cost=0.16, calib=0.13, precision=0.69),
    "minus_human_burden_model": dict(success=0.17, safety=0.19, burden=0.65, regret=0.05, late=0.04, churn=0.15, recovery=0.75, cost=0.22, calib=0.13, precision=0.67),
    "minus_handoff_hysteresis": dict(success=0.16, safety=0.18, burden=0.48, regret=0.06, late=0.05, churn=0.28, recovery=0.73, cost=0.21, calib=0.12, precision=0.66),
    "minus_boundary_uncertainty": dict(success=0.13, safety=0.21, burden=0.43, regret=0.08, late=0.05, churn=0.16, recovery=0.70, cost=0.17, calib=0.17, precision=0.63),
    "minus_recovery_feasibility": dict(success=0.12, safety=0.18, burden=0.43, regret=0.07, late=0.04, churn=0.13, recovery=0.58, cost=0.16, calib=0.13, precision=0.65),
    "confidence_only_boundary": dict(success=-0.02, safety=0.25, burden=0.58, regret=0.12, late=0.11, churn=0.20, recovery=0.50, cost=0.14, calib=0.19, precision=0.50),
    "safety_only_boundary": dict(success=0.23, safety=0.13, burden=0.08, regret=0.05, late=0.03, churn=0.06, recovery=0.77, cost=0.11, calib=0.12, precision=0.70),
    "mpc_only_boundary": dict(success=0.24, safety=0.15, burden=0.14, regret=0.04, late=0.02, churn=0.07, recovery=0.84, cost=0.17, calib=0.10, precision=0.73),
}


def stable_int(*parts):
    payload = "|".join(str(p) for p in parts).encode("utf-8")
    return int.from_bytes(hashlib.sha256(payload).digest()[:8], "little") % (2**32)


def stable_rng(*parts):
    return np.random.default_rng(stable_int(BASE_SEED, *parts))


def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, float(x)))


def ci95(values):
    vals = np.asarray(values, dtype=float)
    if len(vals) <= 1:
        return 0.0
    return float(1.96 * vals.std(ddof=1) / math.sqrt(len(vals)))


def write_rows(path, fields, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def stress_params(split, stress_axis=None, stress_level=0.0):
    params = dict(SPLITS[split])
    level = float(stress_level)
    if stress_axis is None:
        return params
    if stress_axis == "intent_ambiguity":
        params["ambiguity"] = 0.06 + 0.56 * level
        params["low_signal"] = max(params["low_signal"], 0.06 + 0.34 * level)
    elif stress_axis == "contact_mode":
        params["contact"] = 0.06 + 0.58 * level
        params["hazard"] = max(params["hazard"], 0.08 + 0.30 * level)
    elif stress_axis == "human_delay":
        params["delay"] = 0.04 + 0.62 * level
        params["ambiguity"] = max(params["ambiguity"], 0.05 + 0.25 * level)
    elif stress_axis == "fragility":
        params["fragility"] = 0.06 + 0.58 * level
        params["hazard"] = max(params["hazard"], 0.07 + 0.36 * level)
    elif stress_axis == "authority_churn":
        params["churn"] = 0.05 + 0.64 * level
        params["noise"] = max(params["noise"], 0.08 + 0.40 * level)
    elif stress_axis == "combined":
        params["hazard"] = 0.08 + 0.48 * level
        params["contact"] = 0.08 + 0.50 * level
        params["ambiguity"] = 0.08 + 0.50 * level
        params["delay"] = 0.06 + 0.52 * level
        params["noise"] = 0.08 + 0.42 * level
        params["fragility"] = 0.08 + 0.48 * level
        params["churn"] = 0.06 + 0.54 * level
        params["low_signal"] = 0.08 + 0.48 * level
    return {k: clamp(v) for k, v in params.items()}


def episode_context(task_cfg, split, seed, episode, stress_axis=None, stress_level=0.0):
    params = stress_params(split, stress_axis, stress_level)
    rng = stable_rng("context", task_cfg["task"], split, seed, episode, stress_axis or "main", stress_level)
    phase = 0.5 + 0.5 * math.sin((episode + 1) * math.pi / MAIN_EPISODES_PER_TASK)
    context = {}
    for key in ["hazard", "contact", "ambiguity", "delay", "fragility"]:
        base = task_cfg[key] + params[key]
        if key in ["hazard", "contact"]:
            base += 0.06 * phase
        if key == "ambiguity":
            base += 0.05 * (1.0 - phase)
        if key == "delay":
            base += 0.03 * rng.random()
        context[key] = clamp(base + rng.normal(0.0, 0.035))
    context["noise"] = clamp(params["noise"] + rng.normal(0.0, 0.030))
    context["churn_pressure"] = clamp(params["churn"] + 0.45 * context["ambiguity"] + 0.22 * context["noise"] + rng.normal(0.0, 0.025))
    context["low_signal"] = clamp(params["low_signal"] + 0.32 * context["ambiguity"] + rng.normal(0.0, 0.025))
    context["difficulty"] = clamp(
        task_cfg["difficulty"]
        + 0.20 * context["hazard"]
        + 0.17 * context["contact"]
        + 0.16 * context["ambiguity"]
        + 0.11 * context["delay"]
        + 0.11 * context["fragility"]
        + rng.normal(0.0, 0.025)
    )
    context["policy_skill"] = task_cfg["policy_skill"]
    context["controller_skill"] = task_cfg["controller_skill"]
    context["human_skill"] = task_cfg["human_skill"]
    context["latent_risk"] = clamp(
        0.18 * context["hazard"]
        + 0.14 * context["contact"]
        + 0.13 * context["fragility"]
        + 0.08 * context["noise"]
        + 0.06 * context["low_signal"]
    )
    return context


def rollout_metrics(context, method, rng):
    profile = PROFILES[method]
    hard = context["difficulty"]
    authority_mismatch = clamp(
        0.45 * context["ambiguity"]
        + 0.25 * context["low_signal"]
        + 0.18 * context["churn_pressure"]
        + 0.12 * context["delay"]
    )
    control_hazard = clamp(
        0.38 * context["hazard"]
        + 0.24 * context["contact"]
        + 0.18 * context["fragility"]
        + 0.10 * context["noise"]
    )
    success_p = clamp(
        0.80
        + profile["success"]
        - 0.50 * hard
        - 0.20 * authority_mismatch
        - 0.12 * context["delay"]
        + 0.07 * profile["recovery"]
        + rng.normal(0.0, 0.018)
    )
    safety_p = clamp(
        profile["safety"] * (0.45 + 1.12 * control_hazard)
        + 0.035 * context["low_signal"]
        + 0.026 * context["churn_pressure"]
        + rng.normal(0.0, 0.010),
        0.005,
        0.95,
    )
    burden = clamp(
        profile["burden"]
        + 0.20 * context["ambiguity"]
        + 0.18 * context["delay"]
        + 0.08 * context["low_signal"]
        - 0.06 * profile["recovery"]
        + rng.normal(0.0, 0.018)
    )
    late = clamp(
        profile["late"]
        + 0.30 * context["delay"]
        + 0.18 * context["ambiguity"]
        + 0.10 * context["low_signal"]
        - 0.08 * profile["recovery"]
        + rng.normal(0.0, 0.012)
    )
    churn = clamp(
        profile["churn"]
        + 0.32 * context["churn_pressure"]
        + 0.14 * context["ambiguity"]
        + rng.normal(0.0, 0.015)
    )
    regret = clamp(
        profile["regret"]
        + 0.26 * (1.0 - success_p)
        + 0.18 * safety_p
        + 0.08 * late
        + 0.06 * churn
        + rng.normal(0.0, 0.010)
    )
    recovery = clamp(
        profile["recovery"]
        + 0.10 * (1.0 - hard)
        - 0.22 * late
        - 0.12 * safety_p
        - 0.08 * churn
        + rng.normal(0.0, 0.014)
    )
    intervention_cost = clamp(
        profile["cost"]
        + 0.15 * burden
        + 0.08 * churn
        + 0.08 * context["delay"]
        + rng.normal(0.0, 0.010)
    )
    calibration = clamp(
        profile["calib"]
        + 0.16 * context["low_signal"]
        + 0.10 * context["noise"]
        + 0.08 * context["ambiguity"]
        + rng.normal(0.0, 0.010)
    )
    precision = clamp(
        profile["precision"]
        - 0.18 * context["low_signal"]
        - 0.10 * context["ambiguity"]
        - 0.05 * context["noise"]
        + rng.normal(0.0, 0.014)
    )
    unsafe_autonomy = clamp(
        safety_p * (1.0 - min(0.80, burden))
        + 0.10 * (method == "fixed_policy_authority")
        + 0.05 * (method == "controller_fusion_prior")
    )
    task_success = 1.0 if rng.random() < success_p else 0.0
    safety_violation = 1.0 if rng.random() < safety_p else 0.0
    robust_utility = (
        task_success
        - 0.62 * safety_violation
        - 0.24 * burden
        - 0.25 * regret
        - 0.16 * late
        - 0.12 * churn
        - 0.10 * intervention_cost
        + 0.08 * recovery
    )
    risk_estimate = clamp(safety_p + 0.22 * calibration + 0.05 * context["low_signal"] + rng.normal(0.0, 0.008))
    return {
        "task_success": task_success,
        "safety_violation": safety_violation,
        "authority_regret": regret,
        "human_burden": burden,
        "late_handoff": late,
        "handoff_churn": churn,
        "recovery_success": recovery,
        "intervention_cost": intervention_cost,
        "boundary_calibration_error": calibration,
        "override_precision": precision,
        "unsafe_autonomy": unsafe_autonomy,
        "robust_utility": robust_utility,
        "risk_estimate": risk_estimate,
    }


def dataset_rows():
    rows = []
    for seed in SEEDS:
        for task_cfg in TASKS:
            for split in SPLITS:
                for episode in range(MAIN_EPISODES_PER_TASK):
                    context = episode_context(task_cfg, split, seed, episode)
                    rows.append(
                        {
                            "seed": seed,
                            "task": task_cfg["task"],
                            "split": split,
                            "episode": episode,
                            "difficulty": f"{context['difficulty']:.6f}",
                            "hazard": f"{context['hazard']:.6f}",
                            "contact": f"{context['contact']:.6f}",
                            "ambiguity": f"{context['ambiguity']:.6f}",
                            "delay": f"{context['delay']:.6f}",
                            "fragility": f"{context['fragility']:.6f}",
                            "low_signal": f"{context['low_signal']:.6f}",
                            "latent_risk": f"{context['latent_risk']:.6f}",
                        }
                    )
    return rows


def make_rollouts(methods, episodes_per_task, tag, splits=None, stress_axis=None, stress_level=0.0):
    rows = []
    active_splits = list(splits or SPLITS.keys())
    for seed in SEEDS:
        for split in active_splits:
            for task_cfg in TASKS:
                for method in methods:
                    for episode in range(episodes_per_task):
                        context = episode_context(task_cfg, split, seed, episode, stress_axis, stress_level)
                        rng = stable_rng(tag, seed, split, task_cfg["task"], method, episode, stress_axis or "main", stress_level)
                        metrics = rollout_metrics(context, method, rng)
                        row = {
                            "seed": seed,
                            "split": split,
                            "task": task_cfg["task"],
                            "method": method,
                            "episode": episode,
                            "stress_axis": stress_axis or "",
                            "stress_level": f"{float(stress_level):.2f}",
                        }
                        for metric in METRICS:
                            row[metric] = f"{metrics[metric]:.6f}"
                        row["risk_estimate"] = f"{metrics['risk_estimate']:.6f}"
                        rows.append(row)
    return rows


def make_ablation_rollouts():
    rows = []
    for seed in SEEDS:
        for split in ABLATION_SPLITS:
            for task_cfg in TASKS:
                for ablation in ABLATIONS:
                    for episode in range(ABLATION_EPISODES_PER_TASK):
                        context = episode_context(task_cfg, split, seed, episode)
                        rng = stable_rng("ablation", seed, split, task_cfg["task"], ablation, episode)
                        metrics = rollout_metrics(context, ablation, rng)
                        row = {
                            "seed": seed,
                            "split": split,
                            "task": task_cfg["task"],
                            "ablation": ablation,
                            "episode": episode,
                        }
                        for metric in METRICS:
                            row[metric] = f"{metrics[metric]:.6f}"
                        row["risk_estimate"] = f"{metrics['risk_estimate']:.6f}"
                        rows.append(row)
    return rows


def make_stress_rollouts():
    rows = []
    for axis in STRESS_AXES:
        for level in STRESS_LEVELS:
            for seed in SEEDS:
                for task_cfg in TASKS:
                    for method in STRESS_METHODS:
                        for episode in range(STRESS_EPISODES_PER_TASK):
                            context = episode_context(task_cfg, "combined_authority_stress", seed, episode, axis, level)
                            rng = stable_rng("stress", axis, level, seed, task_cfg["task"], method, episode)
                            metrics = rollout_metrics(context, method, rng)
                            row = {
                                "seed": seed,
                                "stress_axis": axis,
                                "stress_level": f"{float(level):.2f}",
                                "task": task_cfg["task"],
                                "method": method,
                                "episode": episode,
                            }
                            for metric in METRICS:
                                row[metric] = f"{metrics[metric]:.6f}"
                            row["risk_estimate"] = f"{metrics['risk_estimate']:.6f}"
                            rows.append(row)
    return rows


def make_fixed_risk_rows():
    rows = []
    for seed in SEEDS:
        for split in FIXED_SPLITS:
            for budget in RISK_BUDGETS:
                for task_cfg in TASKS:
                    for method in FIXED_METHODS:
                        for episode in range(FIXED_EPISODES_PER_TASK):
                            context = episode_context(task_cfg, split, seed, episode)
                            rng = stable_rng("fixed", seed, split, budget, task_cfg["task"], method, episode)
                            metrics = rollout_metrics(context, method, rng)
                            accepted = 1.0 if metrics["risk_estimate"] <= budget else 0.0
                            accepted_utility = (
                                metrics["task_success"]
                                - 0.62 * metrics["safety_violation"]
                                - 0.24 * metrics["human_burden"]
                                - 0.25 * metrics["authority_regret"]
                                - 0.12 * metrics["intervention_cost"]
                            ) if accepted else 0.0
                            row = {
                                "seed": seed,
                                "split": split,
                                "budget": f"{float(budget):.2f}",
                                "task": task_cfg["task"],
                                "method": method,
                                "episode": episode,
                                "risk_estimate": f"{metrics['risk_estimate']:.6f}",
                                "accepted": f"{accepted:.6f}",
                                "accepted_success": f"{accepted * metrics['task_success']:.6f}",
                                "accepted_safety_violation": f"{accepted * metrics['safety_violation']:.6f}",
                                "accepted_regret": f"{accepted * metrics['authority_regret']:.6f}",
                                "accepted_utility": f"{accepted_utility:.6f}",
                            }
                            rows.append(row)
    return rows


def mean_float(rows, key):
    return float(np.mean([float(row[key]) for row in rows])) if rows else 0.0


def seed_metric_rows(rows, group_keys, method_key="method", metrics=METRICS):
    groups = defaultdict(list)
    for row in rows:
        key = tuple(row[k] for k in group_keys)
        groups[key].append(row)
    out = []
    for key, group in sorted(groups.items()):
        row = {k: v for k, v in zip(group_keys, key)}
        row["n"] = len(group)
        for metric in metrics:
            row[metric] = f"{mean_float(group, metric):.6f}"
        out.append(row)
    return out


def metric_long_rows(seed_rows, group_keys, metrics=METRICS):
    groups = defaultdict(list)
    for row in seed_rows:
        key = tuple(row[k] for k in group_keys)
        groups[key].append(row)
    out = []
    for key, group in sorted(groups.items()):
        for metric in metrics:
            vals = [float(row[metric]) for row in group]
            out.append(
                {
                    **{k: v for k, v in zip(group_keys, key)},
                    "metric": metric,
                    "mean": f"{float(np.mean(vals)):.6f}",
                    "ci95": f"{ci95(vals):.6f}",
                    "n": len(vals),
                }
            )
    return out


def metric_wide_rows(seed_rows, group_keys, metrics=METRICS):
    groups = defaultdict(list)
    for row in seed_rows:
        key = tuple(row[k] for k in group_keys)
        groups[key].append(row)
    out = []
    for key, group in sorted(groups.items()):
        row = {k: v for k, v in zip(group_keys, key)}
        row["n"] = len(group)
        for metric in metrics:
            vals = [float(item[metric]) for item in group]
            row[metric] = f"{float(np.mean(vals)):.6f}"
            row[f"{metric}_ci95"] = f"{ci95(vals):.6f}"
        out.append(row)
    return out


def pairwise_rows(seed_rows, group_keys, proposal_key=PROPOSAL, reference_key="method", references=PAIRWISE_REFERENCES, metrics=METRICS):
    by_group = defaultdict(dict)
    for row in seed_rows:
        key = tuple(row[k] for k in group_keys) + (row["seed"],)
        by_group[key][row[reference_key]] = row
    grouped = defaultdict(list)
    for key, methods in by_group.items():
        if proposal_key not in methods:
            continue
        output_key = key[:-1]
        for reference in references:
            if reference not in methods:
                continue
            for metric in metrics:
                diff = float(methods[proposal_key][metric]) - float(methods[reference][metric])
                grouped[(output_key, reference, metric)].append(diff)
    out = []
    for (key, reference, metric), diffs in sorted(grouped.items()):
        mean = float(np.mean(diffs))
        band = ci95(diffs)
        out.append(
            {
                **{k: v for k, v in zip(group_keys, key)},
                "reference": reference,
                "metric": metric,
                "mean_diff": f"{mean:.6f}",
                "ci95": f"{band:.6f}",
                "lower95": f"{mean - band:.6f}",
                "upper95": f"{mean + band:.6f}",
                "n": len(diffs),
            }
        )
    return out


def hard_aggregate_seed_rows(raw_seed_rows):
    groups = defaultdict(list)
    for row in raw_seed_rows:
        if row["split"] in HARD_SPLITS:
            groups[(row["method"], row["seed"])].append(row)
    out = []
    for (method, seed), group in sorted(groups.items()):
        row = {"method": method, "seed": seed, "n": len(group)}
        for metric in METRICS:
            row[metric] = f"{float(np.mean([float(item[metric]) for item in group])):.6f}"
        out.append(row)
    return out


def fixed_seed_rows(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[(row["split"], row["budget"], row["method"], row["seed"])].append(row)
    out = []
    for (split, budget, method, seed), group in sorted(groups.items()):
        coverage = mean_float(group, "accepted")
        row = {"split": split, "budget": budget, "method": method, "seed": seed, "n": len(group), "coverage": f"{coverage:.6f}"}
        for metric in ["accepted_success", "accepted_safety_violation", "accepted_regret", "accepted_utility"]:
            row[metric] = f"{mean_float(group, metric):.6f}"
        out.append(row)
    return out


def fixed_pairwise_rows(fixed_seed):
    refs = [m for m in FIXED_METHODS if m != PROPOSAL]
    by_group = defaultdict(dict)
    for row in fixed_seed:
        by_group[(row["split"], row["budget"], row["seed"])][row["method"]] = row
    grouped = defaultdict(list)
    for (split, budget, seed), methods in by_group.items():
        if PROPOSAL not in methods:
            continue
        for ref in refs:
            if ref not in methods:
                continue
            for metric in FIXED_PAIRWISE_METRICS:
                grouped[(split, budget, ref, metric)].append(float(methods[PROPOSAL][metric]) - float(methods[ref][metric]))
    out = []
    for (split, budget, ref, metric), diffs in sorted(grouped.items()):
        mean = float(np.mean(diffs))
        band = ci95(diffs)
        out.append(
            {
                "split": split,
                "budget": budget,
                "reference": ref,
                "metric": metric,
                "mean_diff": f"{mean:.6f}",
                "lower95": f"{mean - band:.6f}",
                "upper95": f"{mean + band:.6f}",
                "n": len(diffs),
            }
        )
    return out


def lookup_metric(rows, selectors, metric):
    for row in rows:
        if row.get("metric") == metric and all(row.get(k) == v for k, v in selectors.items()):
            return float(row["mean"]), float(row["ci95"])
    raise KeyError((selectors, metric))


def lookup_wide(rows, selectors):
    for row in rows:
        if all(row.get(k) == v for k, v in selectors.items()):
            return row
    raise KeyError(selectors)


def make_negative_cases():
    cases = [
        ("low_signal_high_risk_shift", "authority_boundary_v5", "boundary confidence is high while obstacle hazard is under-observed", "late controller takeover and avoidable safety violation"),
        ("combined_authority_stress", "authority_boundary_v5", "human delay and ambiguity both high", "handoff burden rises without recovering MPC-level success"),
        ("authority_churn_shift", "authority_boundary_v5", "hysteresis suppresses rapid but useful control transfer", "task completion trails recovery-aware MPC"),
        ("fragile_object_shift", "authority_boundary_v5", "fragility dominates authority scoring", "CBF prevents contact better with lower burden"),
        ("contact_mode_shift", "authority_boundary_v4", "old boundary over-trusts intent confidence", "contact-mode slip causes high regret"),
        ("human_delay_shift", "fixed_human_teleoperation", "operator authority is always granted", "burden saturates and late actions accumulate"),
    ]
    rows = []
    for i in range(24):
        split, method, trigger, failure = cases[i % len(cases)]
        rows.append(
            {
                "case_id": f"neg90_{i+1:02d}",
                "split": split,
                "method": method,
                "trigger": trigger,
                "failure_mode": failure,
                "reviewer_attack": "A hostile reviewer can ask why a simpler certified or MPC authority rule is not enough.",
                "terminal_effect": "Counts against ICLR-main readiness.",
            }
        )
    return rows


def plot_outputs(hard_metrics, ablation_metrics, stress_metrics, fixed_metrics):
    labels = [m for m in METHODS if not m.startswith("oracle")]
    success = [lookup_metric(hard_metrics, {"method": m}, "task_success")[0] for m in labels]
    safety = [lookup_metric(hard_metrics, {"method": m}, "safety_violation")[0] for m in labels]
    burden = [lookup_metric(hard_metrics, {"method": m}, "human_burden")[0] for m in labels]
    utility = [lookup_metric(hard_metrics, {"method": m}, "robust_utility")[0] for m in labels]

    plt.figure(figsize=(10, 4.8))
    plt.bar(range(len(labels)), success, color="#2f6f9f")
    plt.xticks(range(len(labels)), [x.replace("_", "\n") for x in labels], rotation=0, fontsize=7)
    plt.ylabel("Hard aggregate success")
    plt.title("Paper 90 hard aggregate task success")
    plt.tight_layout()
    plt.savefig(FIGURES / "authority_boundary_hard_success_v5.png", dpi=180)
    plt.close()

    x = np.arange(len(labels))
    width = 0.28
    plt.figure(figsize=(10, 4.8))
    plt.bar(x - width, safety, width, label="Safety violation")
    plt.bar(x, burden, width, label="Human burden")
    plt.bar(x + width, [max(0.0, -u) for u in utility], width, label="Utility deficit")
    plt.xticks(x, [m.replace("_", "\n") for m in labels], fontsize=7)
    plt.legend(fontsize=8)
    plt.title("Failure pressure: safety, burden, and utility")
    plt.tight_layout()
    plt.savefig(FIGURES / "authority_boundary_failures_v5.png", dpi=180)
    plt.close()

    ab_labels = [row["ablation"] for row in ablation_metrics if row["split"] == "combined_authority_stress"]
    ab_utils = [float(row["robust_utility"]) for row in ablation_metrics if row["split"] == "combined_authority_stress"]
    plt.figure(figsize=(9, 4.5))
    plt.bar(range(len(ab_labels)), ab_utils, color="#a56b2a")
    plt.xticks(range(len(ab_labels)), [a.replace("_", "\n") for a in ab_labels], fontsize=7)
    plt.ylabel("Robust utility")
    plt.title("Combined authority-stress ablation utility")
    plt.tight_layout()
    plt.savefig(FIGURES / "authority_boundary_ablation_v5.png", dpi=180)
    plt.close()

    curve_rows = []
    plt.figure(figsize=(8.5, 5.0))
    for method in STRESS_METHODS:
        xs, ys = [], []
        for level in STRESS_LEVELS:
            row = lookup_wide(stress_metrics, {"stress_axis": "combined", "stress_level": f"{level:.2f}", "method": method})
            xs.append(level)
            ys.append(float(row["task_success"]))
            curve_rows.append({"method": method, "stress_level": f"{level:.2f}", "task_success": f"{float(row['task_success']):.6f}"})
        plt.plot(xs, ys, marker="o", linewidth=1.6, label=method.replace("_", " "))
    plt.xlabel("Combined stress level")
    plt.ylabel("Task success")
    plt.title("Combined authority stress sweep")
    plt.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(FIGURES / "authority_boundary_stress_sweep_v5.png", dpi=180)
    plt.close()
    write_rows(FIGURES / "stress_curve_data_v5.csv", ["method", "stress_level", "task_success"], curve_rows)

    plt.figure(figsize=(8.5, 5.0))
    for method in FIXED_METHODS:
        xs, ys = [], []
        for budget in RISK_BUDGETS:
            row = lookup_wide(fixed_metrics, {"split": "combined_authority_stress", "budget": f"{budget:.2f}", "method": method})
            xs.append(budget)
            ys.append(float(row["coverage"]))
        plt.plot(xs, ys, marker="o", linewidth=1.6, label=method.replace("_", " "))
    plt.xlabel("Risk budget")
    plt.ylabel("Accepted coverage")
    plt.title("Fixed-risk coverage on combined authority stress")
    plt.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(FIGURES / "authority_boundary_fixed_risk_v5.png", dpi=180)
    plt.close()

    plt.figure(figsize=(7.5, 5.2))
    for m, s, safe, bur, util in zip(labels, success, safety, burden, utility):
        plt.scatter(safe + bur, s, s=40 + 140 * max(0.0, util), label=m.replace("_", " "))
        plt.text(safe + bur + 0.003, s + 0.003, m.replace("_", "\n"), fontsize=6)
    plt.xlabel("Safety violation + human burden")
    plt.ylabel("Hard aggregate success")
    plt.title("Success-safety-burden Pareto view")
    plt.tight_layout()
    plt.savefig(FIGURES / "authority_boundary_pareto_v5.png", dpi=180)
    plt.close()


def write_summary(
    raw_rows,
    dataset,
    seed_rows_main,
    metrics_long,
    pairwise,
    hard_seed,
    hard_metrics,
    hard_pairwise,
    ablation_rows,
    ablation_seed,
    ablation_metrics,
    stress_rows,
    stress_seed,
    stress_metrics,
    fixed_rows,
    fixed_seed,
    fixed_metrics,
    fixed_pairwise,
    negative_cases,
):
    non_oracle = [m for m in METHODS if "oracle" not in m]
    hard_success = {m: lookup_metric(hard_metrics, {"method": m}, "task_success")[0] for m in non_oracle}
    hard_safety = {m: lookup_metric(hard_metrics, {"method": m}, "safety_violation")[0] for m in non_oracle}
    hard_burden = {m: lookup_metric(hard_metrics, {"method": m}, "human_burden")[0] for m in non_oracle}
    hard_regret = {m: lookup_metric(hard_metrics, {"method": m}, "authority_regret")[0] for m in non_oracle}
    hard_utility = {m: lookup_metric(hard_metrics, {"method": m}, "robust_utility")[0] for m in non_oracle}
    best_success_ref = max(hard_success, key=hard_success.get)
    safest_ref = min(hard_safety, key=hard_safety.get)
    lowest_burden_ref = min(hard_burden, key=hard_burden.get)
    lowest_regret_ref = min(hard_regret, key=hard_regret.get)
    best_utility_ref = max(hard_utility, key=hard_utility.get)

    paired_success = [
        row
        for row in hard_pairwise
        if row["reference"] == best_success_ref and row["metric"] == "task_success"
    ][0]
    paired_safety = [
        row
        for row in hard_pairwise
        if row["reference"] == safest_ref and row["metric"] == "safety_violation"
    ][0]

    proposal_success = hard_success[PROPOSAL]
    proposal_safety = hard_safety[PROPOSAL]
    proposal_burden = hard_burden[PROPOSAL]
    proposal_regret = hard_regret[PROPOSAL]
    proposal_utility = hard_utility[PROPOSAL]

    ablation_combined = [row for row in ablation_metrics if row["split"] == "combined_authority_stress"]
    full_ablation_utility = float([row for row in ablation_combined if row["ablation"] == "full_authority_boundary_v5"][0]["robust_utility"])
    best_removed = max([row for row in ablation_combined if row["ablation"] != "full_authority_boundary_v5"], key=lambda r: float(r["robust_utility"]))

    max_stress_rows = [
        row
        for row in stress_metrics
        if row["stress_axis"] == "combined" and row["stress_level"] == "1.00" and row["method"] != PROPOSAL
    ]
    proposal_stress = lookup_wide(stress_metrics, {"stress_axis": "combined", "stress_level": "1.00", "method": PROPOSAL})
    stress_best = max(max_stress_rows, key=lambda r: float(r["robust_utility"]))

    fixed_005 = [row for row in fixed_metrics if row["budget"] == "0.05"]
    fixed_summary_parts = []
    fixed_gate = True
    for split in FIXED_SPLITS:
        proposal_row = lookup_wide(fixed_metrics, {"split": split, "budget": "0.05", "method": PROPOSAL})
        best_feasible = max([row for row in fixed_005 if row["split"] == split], key=lambda r: float(r["accepted_utility"]))
        fixed_summary_parts.append(
            f"{split}: v5_coverage={float(proposal_row['coverage']):.5f}, best_feasible_coverage={float(best_feasible['coverage']):.5f}, "
            f"v5_success={float(proposal_row['accepted_success']):.5f}, best_feasible_success={float(best_feasible['accepted_success']):.5f}, "
            f"v5_safety={float(proposal_row['accepted_safety_violation']):.5f}, best_feasible_safety={float(best_feasible['accepted_safety_violation']):.5f}"
        )
        if float(proposal_row["coverage"]) <= 0.0 or float(proposal_row["accepted_utility"]) < float(best_feasible["accepted_utility"]) - 0.01:
            fixed_gate = False

    main_gate = (
        proposal_success >= hard_success[best_success_ref] + 0.02
        and float(paired_success["lower95"]) > 0.0
        and proposal_safety <= hard_safety[safest_ref] + 0.01
        and proposal_burden <= hard_burden[lowest_burden_ref] + 0.05
        and proposal_utility >= hard_utility[best_utility_ref] + 0.02
    )
    mechanism_gate = full_ablation_utility >= float(best_removed["robust_utility"]) + 0.02
    stress_gate = float(proposal_stress["robust_utility"]) >= float(stress_best["robust_utility"]) - 0.005
    scope_gate = False

    lines = [
        "Paper 90 control_authority_boundaries v5 expanded audit",
        "Terminal recommendation: KILL_ARCHIVE",
        "ICLR main ready: no",
        "Reason: expanded CPU-only control-authority audit adds stronger CBF, MPC, POMDP, recovery-aware, uncertainty, ablation, stress, and fixed-risk tests, but no real robot or accepted high-fidelity deployment benchmark evidence exists.",
        f"Main rollout rows: {len(raw_rows)}",
        f"Dataset summary rows: {len(dataset)}",
        f"Main seed-metric rows: {len(seed_rows_main)}",
        f"Main metric rows: {len(metrics_long)}",
        f"Main pairwise rows: {len(pairwise)}",
        f"Hard aggregate seed rows: {len(hard_seed)}",
        f"Hard aggregate metric rows: {len(hard_metrics)}",
        f"Hard aggregate pairwise rows: {len(hard_pairwise)}",
        f"Ablation rollout rows: {len(ablation_rows)}",
        f"Ablation seed rows: {len(ablation_seed)}",
        f"Ablation metric rows: {len(ablation_metrics)}",
        f"Stress raw rows: {len(stress_rows)}",
        f"Stress seed rows: {len(stress_seed)}",
        f"Stress metric rows: {len(stress_metrics)}",
        f"Fixed-risk raw rows: {len(fixed_rows)}",
        f"Fixed-risk seed rows: {len(fixed_seed)}",
        f"Fixed-risk metric rows: {len(fixed_metrics)}",
        f"Fixed-risk pairwise rows: {len(fixed_pairwise)}",
        f"Negative cases: {len(negative_cases)}",
        "",
        "Frozen hard-aggregate gate:",
        f"best_success_reference={best_success_ref}",
        f"safest_reference={safest_ref}",
        f"lowest_burden_reference={lowest_burden_ref}",
        f"lowest_regret_reference={lowest_regret_ref}",
        f"best_utility_reference={best_utility_ref}",
        f"proposal_success={proposal_success:.5f}",
        f"best_success={hard_success[best_success_ref]:.5f}",
        f"proposal_safety={proposal_safety:.5f}",
        f"safest_safety={hard_safety[safest_ref]:.5f}",
        f"proposal_burden={proposal_burden:.5f}",
        f"lowest_burden={hard_burden[lowest_burden_ref]:.5f}",
        f"proposal_regret={proposal_regret:.5f}",
        f"lowest_regret={hard_regret[lowest_regret_ref]:.5f}",
        f"proposal_utility={proposal_utility:.5f}",
        f"best_utility={hard_utility[best_utility_ref]:.5f}",
        f"paired_success_lower95={float(paired_success['lower95']):.5f}",
        f"paired_safety_upper95={float(paired_safety['upper95']):.5f}",
        f"main_gate={main_gate}",
        f"mechanism_gate={mechanism_gate}",
        f"mechanism_best_removed={best_removed['ablation']}",
        f"stress_gate={stress_gate}",
        f"stress_dominated_by={stress_best['method']}",
        f"fixed_risk_gate={fixed_gate}",
        f"scope_gate={scope_gate}",
        " | ".join(fixed_summary_parts),
        "",
        "Hard aggregate metrics:",
    ]
    for method in METHODS:
        row = {metric: lookup_metric(hard_metrics, {"method": method}, metric)[0] for metric in METRICS}
        lines.append(
            f"{method} task_success={row['task_success']:.5f} safety={row['safety_violation']:.5f} burden={row['human_burden']:.5f} "
            f"regret={row['authority_regret']:.5f} late={row['late_handoff']:.5f} churn={row['handoff_churn']:.5f} utility={row['robust_utility']:.5f}"
        )
    lines.extend(["", "Key paired hard-aggregate differences:"])
    for row in hard_pairwise:
        if row["reference"] in [best_success_ref, safest_ref, best_utility_ref, "authority_boundary_v4"] and row["metric"] in [
            "task_success",
            "safety_violation",
            "human_burden",
            "authority_regret",
            "robust_utility",
        ]:
            lines.append(
                f"v5_minus_{row['reference']} {row['metric']}: mean={float(row['mean_diff']):.5f} ci95={float(row['ci95']):.5f} "
                f"lower95={float(row['lower95']):.5f} upper95={float(row['upper95']):.5f}"
            )
    lines.extend(["", "Ablation utility:"])
    for row in ablation_combined:
        lines.append(
            f"{row['ablation']} success={float(row['task_success']):.5f} safety={float(row['safety_violation']):.5f} "
            f"burden={float(row['human_burden']):.5f} utility={float(row['robust_utility']):.5f}"
        )
    lines.extend(["", "Maximum combined stress:"])
    for row in [lookup_wide(stress_metrics, {"stress_axis": "combined", "stress_level": "1.00", "method": method}) for method in STRESS_METHODS]:
        lines.append(
            f"{row['method']} task_success={float(row['task_success']):.5f} safety={float(row['safety_violation']):.5f} "
            f"burden={float(row['human_burden']):.5f} utility={float(row['robust_utility']):.5f}"
        )
    lines.extend(["", "Fixed-risk budget 0.05:"])
    for row in fixed_005:
        lines.append(
            f"{row['split']} {row['method']} coverage={float(row['coverage']):.5f} accepted_success={float(row['accepted_success']):.5f} "
            f"accepted_safety={float(row['accepted_safety_violation']):.5f} accepted_regret={float(row['accepted_regret']):.5f}"
        )
    lines.extend(["", f"Negative cases: {len(negative_cases)}", "terminal=KILL_ARCHIVE"])
    (RESULTS / "summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    dataset = dataset_rows()
    raw_rows = make_rollouts(METHODS, MAIN_EPISODES_PER_TASK, "main")
    seed_rows_main = seed_metric_rows(raw_rows, ["split", "method", "seed"])
    metrics_long = metric_long_rows(seed_rows_main, ["split", "method"])
    pairwise = pairwise_rows(seed_rows_main, ["split"])
    hard_seed = hard_aggregate_seed_rows(seed_rows_main)
    hard_metrics = metric_long_rows(hard_seed, ["method"])
    hard_pairwise = pairwise_rows(hard_seed, [], references=PAIRWISE_REFERENCES)

    ablation_rows = make_ablation_rollouts()
    ablation_seed = seed_metric_rows(ablation_rows, ["split", "ablation", "seed"], method_key="ablation")
    ablation_metrics = metric_wide_rows(ablation_seed, ["split", "ablation"])
    ablation_long = metric_long_rows(ablation_seed, ["split", "ablation"])

    stress_rows = make_stress_rollouts()
    stress_seed = seed_metric_rows(stress_rows, ["stress_axis", "stress_level", "method", "seed"])
    stress_metrics = metric_wide_rows(stress_seed, ["stress_axis", "stress_level", "method"])
    stress_long = metric_long_rows(stress_seed, ["stress_axis", "stress_level", "method"])

    fixed_rows = make_fixed_risk_rows()
    fixed_seed = fixed_seed_rows(fixed_rows)
    fixed_metrics = metric_wide_rows(fixed_seed, ["split", "budget", "method"], metrics=FIXED_PAIRWISE_METRICS)
    fixed_pairwise = fixed_pairwise_rows(fixed_seed)
    negative_cases = make_negative_cases()

    write_rows(RESULTS / "dataset_summary.csv", list(dataset[0].keys()), dataset)
    write_rows(RESULTS / "rollouts.csv", list(raw_rows[0].keys()), raw_rows)
    write_rows(RESULTS / "raw_seed_metrics.csv", list(seed_rows_main[0].keys()), seed_rows_main)
    write_rows(RESULTS / "metrics.csv", list(metrics_long[0].keys()), metrics_long)
    write_rows(RESULTS / "pairwise_stats.csv", list(pairwise[0].keys()), pairwise)
    write_rows(RESULTS / "hard_aggregate_seed_metrics.csv", list(hard_seed[0].keys()), hard_seed)
    write_rows(RESULTS / "hard_aggregate_metrics.csv", list(hard_metrics[0].keys()), hard_metrics)
    write_rows(RESULTS / "hard_aggregate_pairwise_stats.csv", list(hard_pairwise[0].keys()), hard_pairwise)
    write_rows(RESULTS / "ablation_rollouts.csv", list(ablation_rows[0].keys()), ablation_rows)
    write_rows(RESULTS / "ablation_seed_metrics.csv", list(ablation_seed[0].keys()), ablation_seed)
    write_rows(RESULTS / "ablation_metrics.csv", list(ablation_metrics[0].keys()), ablation_metrics)
    write_rows(RESULTS / "ablation_metric_long.csv", list(ablation_long[0].keys()), ablation_long)
    write_rows(RESULTS / "stress_sweep_raw.csv", list(stress_rows[0].keys()), stress_rows)
    write_rows(RESULTS / "stress_sweep_seed_metrics.csv", list(stress_seed[0].keys()), stress_seed)
    write_rows(RESULTS / "stress_sweep.csv", list(stress_metrics[0].keys()), stress_metrics)
    write_rows(RESULTS / "stress_sweep_metric_long.csv", list(stress_long[0].keys()), stress_long)
    write_rows(RESULTS / "fixed_risk_raw.csv", list(fixed_rows[0].keys()), fixed_rows)
    write_rows(RESULTS / "fixed_risk_seed_metrics.csv", list(fixed_seed[0].keys()), fixed_seed)
    write_rows(RESULTS / "fixed_risk_metrics.csv", list(fixed_metrics[0].keys()), fixed_metrics)
    write_rows(RESULTS / "fixed_risk_pairwise.csv", list(fixed_pairwise[0].keys()), fixed_pairwise)
    write_rows(RESULTS / "negative_cases.csv", list(negative_cases[0].keys()), negative_cases)

    plot_outputs(hard_metrics, ablation_metrics, stress_metrics, fixed_metrics)
    write_summary(
        raw_rows,
        dataset,
        seed_rows_main,
        metrics_long,
        pairwise,
        hard_seed,
        hard_metrics,
        hard_pairwise,
        ablation_rows,
        ablation_seed,
        ablation_metrics,
        stress_rows,
        stress_seed,
        stress_metrics,
        fixed_rows,
        fixed_seed,
        fixed_metrics,
        fixed_pairwise,
        negative_cases,
    )


if __name__ == "__main__":
    main()
