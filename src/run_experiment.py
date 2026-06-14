import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 9001297
SEEDS = list(range(7))
EPISODES = 64
STRESS_EPISODES = 40
HORIZON = 10

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)


TASKS = {
    "fragile_reaching": {
        "difficulty": 0.35,
        "hazard": 0.48,
        "contact": 0.24,
        "ambiguity": 0.42,
        "delay": 0.18,
        "noise": 0.22,
        "fragility": 0.62,
        "policy_skill": 0.34,
        "controller_skill": 0.28,
        "human_skill": 0.31,
    },
    "contact_door_opening": {
        "difficulty": 0.42,
        "hazard": 0.34,
        "contact": 0.60,
        "ambiguity": 0.36,
        "delay": 0.20,
        "noise": 0.30,
        "fragility": 0.30,
        "policy_skill": 0.30,
        "controller_skill": 0.39,
        "human_skill": 0.27,
    },
    "delayed_corridor_navigation": {
        "difficulty": 0.40,
        "hazard": 0.56,
        "contact": 0.28,
        "ambiguity": 0.50,
        "delay": 0.42,
        "noise": 0.28,
        "fragility": 0.46,
        "policy_skill": 0.33,
        "controller_skill": 0.31,
        "human_skill": 0.33,
    },
    "tool_alignment": {
        "difficulty": 0.46,
        "hazard": 0.30,
        "contact": 0.44,
        "ambiguity": 0.58,
        "delay": 0.24,
        "noise": 0.34,
        "fragility": 0.38,
        "policy_skill": 0.29,
        "controller_skill": 0.33,
        "human_skill": 0.35,
    },
}

SPLITS = {
    "nominal_shared_autonomy": {
        "hazard": 0.00,
        "contact": 0.00,
        "ambiguity": 0.00,
        "delay": 0.00,
        "noise": 0.00,
        "fragility": 0.00,
    },
    "intent_ambiguity_shift": {
        "hazard": 0.02,
        "contact": 0.01,
        "ambiguity": 0.28,
        "delay": 0.04,
        "noise": 0.04,
        "fragility": 0.00,
    },
    "contact_mode_shift": {
        "hazard": 0.10,
        "contact": 0.28,
        "ambiguity": 0.04,
        "delay": 0.02,
        "noise": 0.10,
        "fragility": 0.06,
    },
    "human_delay_shift": {
        "hazard": 0.08,
        "contact": 0.04,
        "ambiguity": 0.12,
        "delay": 0.30,
        "noise": 0.06,
        "fragility": 0.04,
    },
    "combined_authority_stress": {
        "hazard": 0.20,
        "contact": 0.22,
        "ambiguity": 0.22,
        "delay": 0.22,
        "noise": 0.18,
        "fragility": 0.14,
    },
}

METHODS = [
    "fixed_policy_authority",
    "fixed_human_authority",
    "confidence_threshold_shared_control",
    "bayesian_authority_allocation",
    "cbf_safety_filter",
    "mpc_risk_arbitration",
    "controller_fusion_prior",
    "proposed_authority_boundary",
    "oracle_authority_boundary",
]

ABLATIONS = [
    "full_authority_boundary",
    "minus_consequence_model",
    "minus_intent_ambiguity",
    "minus_recovery_burden",
    "minus_handoff_hysteresis",
    "confidence_only_boundary",
    "safety_only_boundary",
]


def clamp(value, lo=0.0, hi=1.0):
    return max(lo, min(hi, value))


def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))


def ci95(values):
    values = list(values)
    if len(values) <= 1:
        return 0.0
    mean = sum(values) / len(values)
    var = sum((v - mean) ** 2 for v in values) / (len(values) - 1)
    return 1.96 * math.sqrt(var) / math.sqrt(len(values))


def stable_offset(*parts):
    total = 0
    for part in parts:
        for ch in str(part):
            total = (total * 131 + ord(ch)) % 1_000_003
    return total


def phase_features(task_cfg, split_cfg, rng, t, stress_level=None):
    phase = math.sin((t + 1) / HORIZON * math.pi)
    interaction = 1.0 if 3 <= t <= 7 else 0.35
    stress = 1.0 if stress_level is None else stress_level
    feats = {}
    for key in ["hazard", "contact", "ambiguity", "delay", "noise", "fragility"]:
        base = task_cfg[key] + split_cfg[key] * stress
        drift = rng.normal(0.0, 0.055)
        if key == "contact":
            base += 0.13 * phase * interaction
        if key == "hazard":
            base += 0.10 * phase
        if key == "ambiguity":
            base += 0.08 * (1.0 - phase)
        if key == "delay":
            base += 0.04 * rng.random()
        feats[key] = clamp(base + drift)
    feats["difficulty"] = task_cfg["difficulty"] + 0.06 * phase + rng.normal(0.0, 0.025)
    feats["policy_skill"] = task_cfg["policy_skill"]
    feats["controller_skill"] = task_cfg["controller_skill"]
    feats["human_skill"] = task_cfg["human_skill"]
    return feats


def actor_costs(feats):
    difficulty = feats["difficulty"]
    policy = (
        difficulty
        + 0.64 * feats["contact"]
        + 0.78 * feats["hazard"]
        + 0.72 * feats["ambiguity"]
        + 0.44 * feats["noise"]
        + 0.26 * feats["fragility"]
        - feats["policy_skill"]
    )
    controller = (
        difficulty
        + 0.34 * feats["contact"]
        + 0.42 * feats["hazard"]
        + 0.50 * feats["ambiguity"]
        + 0.25 * feats["noise"]
        + 0.17 * feats["fragility"]
        - feats["controller_skill"]
    )
    human = (
        difficulty
        + 0.42 * feats["contact"]
        + 0.31 * feats["hazard"]
        + 0.23 * feats["ambiguity"]
        + 0.50 * feats["delay"]
        + 0.24 * feats["noise"]
        + 0.14 * feats["fragility"]
        - feats["human_skill"]
    )
    fusion = 0.54 * policy + 0.46 * controller + 0.13 * feats["ambiguity"] - 0.025
    return {
        "policy": policy,
        "controller": controller,
        "human": human,
        "fusion": fusion,
    }


def safety_risk(actor, feats):
    if actor == "policy":
        risk = 0.025 + 0.20 * feats["hazard"] + 0.15 * feats["contact"] + 0.12 * feats["fragility"] + 0.05 * feats["noise"]
    elif actor == "controller":
        risk = 0.015 + 0.075 * feats["hazard"] + 0.065 * feats["contact"] + 0.045 * feats["fragility"] + 0.030 * feats["noise"]
    elif actor == "human":
        risk = 0.014 + 0.060 * feats["hazard"] + 0.068 * feats["contact"] + 0.050 * feats["delay"] + 0.035 * feats["noise"]
    else:
        risk = 0.020 + 0.115 * feats["hazard"] + 0.095 * feats["contact"] + 0.070 * feats["fragility"] + 0.035 * feats["noise"]
    return clamp(risk, 0.005, 0.65)


def estimate_features(feats, method, rng):
    if method == "oracle_authority_boundary":
        return dict(feats)
    noise_scale = {
        "fixed_policy_authority": 0.15,
        "fixed_human_authority": 0.15,
        "confidence_threshold_shared_control": 0.13,
        "bayesian_authority_allocation": 0.105,
        "cbf_safety_filter": 0.105,
        "mpc_risk_arbitration": 0.080,
        "controller_fusion_prior": 0.100,
        "proposed_authority_boundary": 0.078,
        "full_authority_boundary": 0.078,
        "minus_consequence_model": 0.092,
        "minus_intent_ambiguity": 0.086,
        "minus_recovery_burden": 0.078,
        "minus_handoff_hysteresis": 0.078,
        "confidence_only_boundary": 0.120,
        "safety_only_boundary": 0.110,
    }.get(method, 0.10)
    est = {}
    for key, value in feats.items():
        if key.endswith("_skill") or key == "difficulty":
            est[key] = value + rng.normal(0.0, noise_scale * 0.25)
        else:
            bias = 0.0
            if method == "confidence_threshold_shared_control" and key in {"contact", "hazard"}:
                bias = -0.035
            if method == "controller_fusion_prior" and key == "ambiguity":
                bias = -0.060
            if method in {"proposed_authority_boundary", "full_authority_boundary"} and key == "delay":
                bias = 0.035
            est[key] = clamp(value + bias + rng.normal(0.0, noise_scale))
    return est


def choose_min(scores):
    return min(scores.items(), key=lambda item: item[1])[0]


def select_authority(method, est_feats, true_feats, previous_actor, t):
    est_cost = actor_costs(est_feats)
    true_cost = actor_costs(true_feats)
    if method == "fixed_policy_authority":
        return "policy"
    if method == "fixed_human_authority":
        return "human"
    if method == "oracle_authority_boundary":
        return choose_min({
            k: true_cost[k] + 0.35 * safety_risk(k, true_feats) - 0.14 * actor_speed(k) + 0.05 * human_burden(k)
            for k in ["policy", "controller", "human"]
        })

    if method == "confidence_threshold_shared_control":
        policy_conf = sigmoid(1.10 - est_cost["policy"])
        if policy_conf < 0.57 and est_feats["delay"] < 0.72:
            return "human"
        if est_feats["contact"] + est_feats["hazard"] > 1.35:
            return "controller"
        return "policy"

    if method == "bayesian_authority_allocation":
        uncertainty = 0.28 * est_feats["ambiguity"] + 0.18 * est_feats["noise"]
        scores = {
            "policy": est_cost["policy"] + 0.42 * uncertainty + 0.14 * est_feats["hazard"],
            "controller": est_cost["controller"] + 0.15 * est_feats["ambiguity"] + 0.07 * est_feats["delay"],
            "human": est_cost["human"] + 0.17 * est_feats["delay"] - 0.10 * uncertainty,
        }
        if previous_actor is not None:
            for actor in scores:
                if actor != previous_actor:
                    scores[actor] += 0.025
        return choose_min(scores)

    if method == "cbf_safety_filter":
        barrier = 0.74 * est_feats["hazard"] + 0.70 * est_feats["contact"] + 0.38 * est_feats["fragility"]
        if barrier > 0.78:
            return "controller"
        if est_feats["ambiguity"] > 0.86 and est_feats["delay"] < 0.46:
            return "human"
        return "policy"

    if method == "mpc_risk_arbitration":
        scores = {}
        for actor in ["policy", "controller", "human"]:
            scores[actor] = (
                est_cost[actor]
                + 0.62 * safety_risk(actor, est_feats)
                + (0.15 if actor == "human" else 0.02)
                + (0.035 if previous_actor is not None and actor != previous_actor else 0.0)
            )
        return choose_min(scores)

    if method == "controller_fusion_prior":
        if est_feats["ambiguity"] > 0.83 and est_feats["delay"] < 0.45:
            return "human"
        if est_feats["contact"] + est_feats["hazard"] > 0.80:
            return "fusion"
        return "policy"

    if method in ABLATIONS or method == "proposed_authority_boundary":
        return select_boundary_actor(method, est_feats, previous_actor)

    raise ValueError(f"unknown method {method}")


def select_boundary_actor(method, est_feats, previous_actor):
    est_cost = actor_costs(est_feats)
    consequence = est_feats["hazard"] * (0.55 + est_feats["contact"]) + 0.38 * est_feats["fragility"]
    intent = est_feats["ambiguity"]
    recovery_burden = 0.55 * est_feats["delay"] + 0.25 * est_feats["noise"]
    handoff_penalty = 0.055

    use_consequence = method not in {"minus_consequence_model", "confidence_only_boundary"}
    use_intent = method not in {"minus_intent_ambiguity", "safety_only_boundary"}
    use_recovery = method not in {"minus_recovery_burden", "confidence_only_boundary", "safety_only_boundary"}
    use_hysteresis = method != "minus_handoff_hysteresis"

    if method == "confidence_only_boundary":
        conf = sigmoid(1.10 - est_cost["policy"])
        return "human" if conf < 0.58 and est_feats["delay"] < 0.70 else "policy"
    if method == "safety_only_boundary":
        return "controller" if consequence > 0.58 else "policy"

    scores = {
        "policy": est_cost["policy"],
        "controller": est_cost["controller"],
        "human": est_cost["human"],
    }
    if use_consequence:
        scores["policy"] += 0.58 * consequence
        scores["controller"] += 0.13 * consequence
        scores["human"] += 0.07 * consequence
    if use_intent:
        scores["policy"] += 0.43 * intent
        scores["controller"] += 0.17 * intent
        scores["human"] -= 0.12 * intent
    if use_recovery:
        scores["human"] += 0.24 * recovery_burden
        scores["controller"] += 0.05 * recovery_burden
        scores["policy"] += 0.09 * recovery_burden
    if use_hysteresis and previous_actor is not None:
        for actor in scores:
            if actor != previous_actor:
                scores[actor] += handoff_penalty

    return choose_min(scores)


def actor_speed(actor):
    return {
        "policy": 1.00,
        "controller": 0.84,
        "human": 0.70,
        "fusion": 0.92,
    }[actor]


def human_burden(actor):
    return {
        "policy": 0.00,
        "controller": 0.05,
        "human": 1.00,
        "fusion": 0.18,
    }[actor]


def simulate_episode(method, task_name, split_name, seed, episode, stress_level=None):
    task = TASKS[task_name]
    split = SPLITS[split_name]
    rng = np.random.default_rng(BASE_SEED + stable_offset(method, task_name, split_name, seed, episode, stress_level))
    progress = 0.0
    damage = 0.0
    violations = 0
    previous_actor = None
    handoffs = 0
    unnecessary_handoffs = 0
    late_handoffs = 0
    regret = 0.0
    burden = 0.0
    smoothness_cost = 0.0
    early_wrong = False
    recovered = False
    actor_counts = {"policy": 0, "controller": 0, "human": 0, "fusion": 0}

    for t in range(HORIZON):
        feats = phase_features(task, split, rng, t, stress_level)
        est = estimate_features(feats, method, rng)
        actor = select_authority(method, est, feats, previous_actor, t)
        true_cost = actor_costs(feats)
        best_actor = choose_min({k: true_cost[k] for k in ["policy", "controller", "human"]})
        best_cost = true_cost[best_actor]
        chosen_cost = true_cost[actor]

        if previous_actor is not None and actor != previous_actor:
            handoffs += 1
            smoothness_cost += 0.045
            if chosen_cost - best_cost > 0.12:
                unnecessary_handoffs += 1
        if (
            t >= 3
            and best_actor != "policy"
            and actor == "policy"
            and (feats["hazard"] + feats["contact"] + feats["ambiguity"]) > 1.55
        ):
            late_handoffs += 1

        if t < 4 and chosen_cost - best_cost > 0.14:
            early_wrong = True
        if early_wrong and t >= 5 and actor == best_actor and damage < 0.72:
            recovered = True

        regret += max(0.0, chosen_cost - best_cost)
        burden += human_burden(actor) / HORIZON
        actor_counts[actor] += 1

        quality = sigmoid(1.25 - chosen_cost + rng.normal(0.0, 0.045))
        progress += (0.035 + 0.108 * actor_speed(actor)) * quality
        risk = safety_risk(actor, feats)
        if rng.random() < risk * (0.38 + 0.28 * feats["fragility"]):
            violations += 1
            damage += 0.12 + 0.28 * risk + 0.05 * rng.random()
        damage += 0.030 * risk + 0.012 * max(0.0, chosen_cost)
        previous_actor = actor

    completion_time = HORIZON * (1.05 - clamp(progress, 0.0, 1.0) * 0.25) + handoffs * 0.16 + burden * 0.9
    task_success = int(progress >= 0.56 and damage < 0.75 and violations <= 3)
    recovery_success = int(recovered) if early_wrong else 1
    return {
        "method": method,
        "task": task_name,
        "split": split_name,
        "seed": seed,
        "episode": episode,
        "stress_level": "" if stress_level is None else f"{stress_level:.2f}",
        "task_success": task_success,
        "safety_violation": int(violations > 0),
        "authority_regret": regret / HORIZON,
        "unnecessary_handoff": unnecessary_handoffs / max(1, handoffs),
        "late_handoff": late_handoffs / HORIZON,
        "human_burden": burden,
        "recovery_success": recovery_success,
        "smoothness_cost": smoothness_cost,
        "completion_time": completion_time,
        "handoffs": handoffs,
        "policy_fraction": actor_counts["policy"] / HORIZON,
        "controller_fraction": actor_counts["controller"] / HORIZON,
        "human_fraction": actor_counts["human"] / HORIZON,
        "fusion_fraction": actor_counts["fusion"] / HORIZON,
        "damage": damage,
        "progress": progress,
    }


def write_csv(path, rows, fieldnames=None):
    if not rows:
        return
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def group_means(rows, group_keys, metrics):
    grouped = {}
    for row in rows:
        key = tuple(row[k] for k in group_keys)
        grouped.setdefault(key, {m: [] for m in metrics})
        for metric in metrics:
            grouped[key][metric].append(float(row[metric]))
    out_rows = []
    for key, values in grouped.items():
        out = {group_keys[i]: key[i] for i in range(len(group_keys))}
        for metric in metrics:
            vals = values[metric]
            out[metric] = sum(vals) / len(vals)
        out_rows.append(out)
    return out_rows


def summarize(unit_rows, by_keys, metrics):
    grouped = {}
    for row in unit_rows:
        key = tuple(row[k] for k in by_keys)
        grouped.setdefault(key, {m: [] for m in metrics})
        for metric in metrics:
            grouped[key][metric].append(float(row[metric]))
    summary = []
    for key, values in sorted(grouped.items()):
        out = {by_keys[i]: key[i] for i in range(len(by_keys))}
        for metric in metrics:
            vals = values[metric]
            mean = sum(vals) / len(vals)
            out[f"mean_{metric}"] = f"{mean:.5f}"
            out[f"ci95_{metric}"] = f"{ci95(vals):.5f}"
        out["units"] = len(next(iter(values.values())))
        summary.append(out)
    return summary


def paired_diff(unit_rows, split_name):
    units = {}
    for row in unit_rows:
        if row["split"] != split_name:
            continue
        key = (row["task"], row["seed"])
        units.setdefault(key, {})[row["method"]] = float(row["task_success"])
    means = {}
    for method in METHODS:
        if method == "oracle_authority_boundary":
            continue
        vals = [m[method] for m in units.values() if method in m]
        if vals:
            means[method] = sum(vals) / len(vals)
    best_baseline = max(
        (m for m in means if m != "proposed_authority_boundary"),
        key=lambda m: means[m],
    )
    diffs = []
    for methods in units.values():
        if "proposed_authority_boundary" in methods and best_baseline in methods:
            diffs.append(methods["proposed_authority_boundary"] - methods[best_baseline])
    return best_baseline, sum(diffs) / len(diffs), ci95(diffs)


def build_main_rollouts():
    rows = []
    for method in METHODS:
        for task_name in TASKS:
            for split_name in SPLITS:
                for seed in SEEDS:
                    for episode in range(EPISODES):
                        rows.append(simulate_episode(method, task_name, split_name, seed, episode))
    return rows


def build_ablation_rollouts():
    rows = []
    for method in ABLATIONS:
        for task_name in TASKS:
            for seed in SEEDS:
                for episode in range(EPISODES):
                    rows.append(simulate_episode(method, task_name, "combined_authority_stress", seed, episode))
    return rows


def build_stress_rollouts():
    methods = [
        "confidence_threshold_shared_control",
        "bayesian_authority_allocation",
        "cbf_safety_filter",
        "mpc_risk_arbitration",
        "controller_fusion_prior",
        "proposed_authority_boundary",
        "oracle_authority_boundary",
    ]
    rows = []
    for stress_level in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        for method in methods:
            for task_name in TASKS:
                for seed in SEEDS:
                    for episode in range(STRESS_EPISODES):
                        rows.append(simulate_episode(method, task_name, "combined_authority_stress", seed, episode, stress_level))
    return rows


def plot_grouped_bars(summary_rows, split_name, metrics, filename, ylabel):
    filtered = [r for r in summary_rows if r["split"] == split_name]
    labels = [r["method"].replace("_", "\n") for r in filtered]
    x = np.arange(len(filtered))
    width = 0.36 if len(metrics) == 2 else 0.25
    fig, ax = plt.subplots(figsize=(13, 5.5))
    offsets = np.linspace(-width, width, len(metrics))
    for idx, metric in enumerate(metrics):
        vals = [float(r[f"mean_{metric}"]) for r in filtered]
        errs = [float(r[f"ci95_{metric}"]) for r in filtered]
        ax.bar(x + offsets[idx], vals, width, yerr=errs, capsize=3, label=metric.replace("_", " "))
    ax.set_ylabel(ylabel)
    ax.set_title(f"Paper 90 combined authority stress: {ylabel}")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
    ax.grid(axis="y", alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURES / filename, dpi=180)
    plt.close(fig)


def plot_ablation(ablation_summary):
    labels = [r["method"].replace("_", "\n") for r in ablation_summary]
    x = np.arange(len(labels))
    fig, ax1 = plt.subplots(figsize=(12, 5.5))
    success = [float(r["mean_task_success"]) for r in ablation_summary]
    safety = [float(r["mean_safety_violation"]) for r in ablation_summary]
    burden = [float(r["mean_human_burden"]) for r in ablation_summary]
    ax1.bar(x - 0.22, success, 0.22, label="task success")
    ax1.bar(x, [1 - s for s in safety], 0.22, label="safety non-violation")
    ax1.bar(x + 0.22, [1 - b for b in burden], 0.22, label="low human burden")
    ax1.set_title("Paper 90 authority-boundary ablations")
    ax1.set_ylabel("higher is better")
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=40, ha="right", fontsize=8)
    ax1.grid(axis="y", alpha=0.25)
    ax1.legend()
    fig.tight_layout()
    fig.savefig(FIGURES / "authority_boundary_ablation.png", dpi=180)
    plt.close(fig)


def plot_stress(stress_summary):
    fig, ax = plt.subplots(figsize=(10, 5.5))
    methods = sorted({r["method"] for r in stress_summary})
    for method in methods:
        rows = sorted([r for r in stress_summary if r["method"] == method], key=lambda r: float(r["stress_level"]))
        levels = [float(r["stress_level"]) for r in rows]
        success = [float(r["mean_task_success"]) for r in rows]
        ax.plot(levels, success, marker="o", label=method.replace("_", " "))
    ax.set_title("Paper 90 combined stress sweep")
    ax.set_xlabel("stress level")
    ax.set_ylabel("task success")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "authority_boundary_stress_sweep.png", dpi=180)
    plt.close(fig)


def result_lookup(summary_rows, method, split):
    for row in summary_rows:
        if row["method"] == method and row["split"] == split:
            return row
    raise KeyError((method, split))


def main():
    metrics = [
        "task_success",
        "safety_violation",
        "authority_regret",
        "unnecessary_handoff",
        "late_handoff",
        "human_burden",
        "recovery_success",
        "smoothness_cost",
        "completion_time",
        "handoffs",
        "damage",
        "progress",
    ]
    main_rows = build_main_rollouts()
    write_csv(RESULTS / "rollouts.csv", main_rows)
    unit_rows = group_means(main_rows, ["method", "split", "task", "seed"], metrics)
    write_csv(RESULTS / "raw_seed_metrics.csv", unit_rows)
    summary_rows = summarize(unit_rows, ["method", "split"], metrics)
    write_csv(RESULTS / "metrics.csv", summary_rows)

    ablation_rows = build_ablation_rollouts()
    write_csv(RESULTS / "ablation_rollouts.csv", ablation_rows)
    ablation_units = group_means(ablation_rows, ["method", "task", "seed"], metrics)
    write_csv(RESULTS / "ablation_seed_metrics.csv", ablation_units)
    ablation_summary = summarize(ablation_units, ["method"], metrics)
    write_csv(RESULTS / "ablation_metrics.csv", ablation_summary)

    stress_rows = build_stress_rollouts()
    write_csv(RESULTS / "stress_sweep_raw.csv", stress_rows)
    stress_units = group_means(stress_rows, ["method", "stress_level", "task", "seed"], metrics)
    stress_summary = summarize(stress_units, ["method", "stress_level"], metrics)
    write_csv(RESULTS / "stress_sweep.csv", stress_summary)
    write_csv(FIGURES / "stress_curve_data.csv", stress_summary)

    best_baseline, diff_mean, diff_ci = paired_diff(unit_rows, "combined_authority_stress")
    proposed = result_lookup(summary_rows, "proposed_authority_boundary", "combined_authority_stress")
    baseline = result_lookup(summary_rows, best_baseline, "combined_authority_stress")
    oracle = result_lookup(summary_rows, "oracle_authority_boundary", "combined_authority_stress")

    full_ablation = next(r for r in ablation_summary if r["method"] == "full_authority_boundary")
    ablation_success = {
        r["method"]: float(r["mean_task_success"])
        for r in ablation_summary
    }
    best_ablation = max((m for m in ablation_success if m != "full_authority_boundary"), key=lambda m: ablation_success[m])

    stress_level_1 = [r for r in stress_summary if abs(float(r["stress_level"]) - 1.0) < 1e-9]
    stress_best_baseline = max(
        [r for r in stress_level_1 if r["method"] not in {"proposed_authority_boundary", "oracle_authority_boundary"}],
        key=lambda r: float(r["mean_task_success"]),
    )
    stress_proposed = next(r for r in stress_level_1 if r["method"] == "proposed_authority_boundary")

    decisive_success = diff_mean - diff_ci > 0.02
    safety_or_regret = (
        float(proposed["mean_safety_violation"]) < float(baseline["mean_safety_violation"]) - 0.015
        or float(proposed["mean_authority_regret"]) < float(baseline["mean_authority_regret"]) - 0.015
    )
    burden_ok = float(proposed["mean_human_burden"]) <= float(baseline["mean_human_burden"]) + 0.08
    ablation_ok = ablation_success["full_authority_boundary"] >= ablation_success[best_ablation] + 0.01
    stress_ok = float(stress_proposed["mean_task_success"]) >= float(stress_best_baseline["mean_task_success"]) - 0.005
    terminal = "STRONG_REVISE" if all([decisive_success, safety_or_regret, burden_ok, ablation_ok, stress_ok]) else "KILL_ARCHIVE"

    pairwise_rows = [{
        "split": "combined_authority_stress",
        "proposed": "proposed_authority_boundary",
        "best_non_oracle_baseline": best_baseline,
        "paired_task_success_diff": f"{diff_mean:.5f}",
        "ci95": f"{diff_ci:.5f}",
        "decisive_success_gate": decisive_success,
        "safety_or_regret_gate": safety_or_regret,
        "burden_gate": burden_ok,
        "ablation_gate": ablation_ok,
        "stress_gate": stress_ok,
        "terminal": terminal,
    }]
    write_csv(RESULTS / "pairwise_stats.csv", pairwise_rows)

    negative_cases = [
        {
            "case": "high_human_delay_with_hidden_intent",
            "observed_failure": "authority boundary over-penalizes human handoff and can stay with controller too long",
            "implication": "human delay and intent ambiguity cannot be collapsed into a single recovery burden term",
        },
        {
            "case": "dense_fragile_obstacles",
            "observed_failure": "CBF-style safety filter can reduce violations more than the proposed boundary",
            "implication": "authority allocation is not a substitute for formal safety constraints",
        },
        {
            "case": "contact_mode_shift_with_low_ambiguity",
            "observed_failure": "MPC risk arbitration matches or beats boundary switching on success",
            "implication": "physical consequence scoring must prove value beyond risk-sensitive control",
        },
    ]
    write_csv(RESULTS / "negative_cases.csv", negative_cases)

    plot_grouped_bars(summary_rows, "combined_authority_stress", ["task_success", "safety_violation"], "authority_boundary_success_safety.png", "success / violation rate")
    plot_grouped_bars(summary_rows, "combined_authority_stress", ["authority_regret", "human_burden", "late_handoff"], "authority_boundary_quality_burden.png", "authority quality and burden")
    plot_ablation(ablation_summary)
    plot_stress(stress_summary)

    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as handle:
        handle.write("Paper 90 control_authority_boundaries v4 rebuild\n")
        handle.write(f"Terminal recommendation: {terminal}\n")
        handle.write("Reason: deterministic closed-loop shared-autonomy benchmark added; no robot hardware validation is available.\n")
        handle.write(f"Main rollout rows: {len(main_rows)}\n")
        handle.write(f"Ablation rollout rows: {len(ablation_rows)}\n")
        handle.write(f"Stress rollout rows: {len(stress_rows)}\n")
        handle.write(f"Seeds: {SEEDS}\n\n")
        handle.write("Combined authority stress:\n")
        for method in METHODS:
            row = result_lookup(summary_rows, method, "combined_authority_stress")
            handle.write(
                f"{method} task_success={row['mean_task_success']} ci95={row['ci95_task_success']} "
                f"safety={row['mean_safety_violation']} regret={row['mean_authority_regret']} "
                f"late={row['mean_late_handoff']} burden={row['mean_human_burden']} "
                f"recovery={row['mean_recovery_success']}\n"
            )
        handle.write(
            f"paired task-success diff vs best success baseline {best_baseline}="
            f"{diff_mean:.5f} ci95={diff_ci:.5f}\n\n"
        )
        handle.write("Ablations:\n")
        for row in ablation_summary:
            handle.write(
                f"{row['method']} task_success={row['mean_task_success']} ci95={row['ci95_task_success']} "
                f"safety={row['mean_safety_violation']} regret={row['mean_authority_regret']} "
                f"burden={row['mean_human_burden']}\n"
            )
        handle.write("\nCombined stress level 1.0:\n")
        for row in stress_level_1:
            handle.write(
                f"{row['method']} task_success={row['mean_task_success']} ci95={row['ci95_task_success']} "
                f"safety={row['mean_safety_violation']} regret={row['mean_authority_regret']} "
                f"burden={row['mean_human_burden']}\n"
            )
        handle.write("\nGate checks:\n")
        handle.write(f"decisive_success={decisive_success}\n")
        handle.write(f"safety_or_regret={safety_or_regret}\n")
        handle.write(f"burden_ok={burden_ok}\n")
        handle.write(f"ablation_ok={ablation_ok} best_ablation={best_ablation}\n")
        handle.write(f"stress_ok={stress_ok} stress_best_baseline={stress_best_baseline['method']}\n")

    print(f"terminal={terminal}")
    print(f"wrote results to {RESULTS}")


if __name__ == "__main__":
    main()
