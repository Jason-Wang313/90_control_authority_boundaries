import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
PAPER = ROOT / "paper"
DOCS = ROOT / "docs"


METHOD_LABELS = {
    "fixed_policy_authority": "Fixed policy",
    "fixed_human_teleoperation": "Fixed human",
    "confidence_threshold_shared_control": "Confidence shared",
    "bayesian_authority_allocation": "Bayesian allocation",
    "uncertainty_triggered_handoff": "Uncertainty handoff",
    "cbf_safety_filter": "CBF safety",
    "mpc_risk_arbitration": "MPC risk",
    "pomdp_handoff_policy": "POMDP handoff",
    "controller_fusion_prior": "Controller fusion",
    "recovery_aware_mpc": "Recovery MPC",
    "authority_boundary_v4": "Authority v4",
    "authority_boundary_v5": "Authority v5",
    "oracle_authority_assignment": "Oracle authority",
}

METHOD_ORDER = list(METHOD_LABELS)
FOCUS_METHODS = [
    "confidence_threshold_shared_control",
    "bayesian_authority_allocation",
    "uncertainty_triggered_handoff",
    "cbf_safety_filter",
    "mpc_risk_arbitration",
    "pomdp_handoff_policy",
    "recovery_aware_mpc",
    "authority_boundary_v5",
]

SPLIT_LABELS = {
    "nominal_shared_autonomy": "Nominal",
    "intent_ambiguity_shift": "Intent ambiguity",
    "contact_mode_shift": "Contact mode",
    "human_delay_shift": "Human delay",
    "fragile_object_shift": "Fragile object",
    "authority_churn_shift": "Authority churn",
    "low_signal_high_risk_shift": "Low-signal risk",
    "combined_authority_stress": "Combined stress",
}

SPLIT_ORDER = list(SPLIT_LABELS)

ABLATION_LABELS = {
    "full_authority_boundary_v5": "Full authority v5",
    "minus_consequence_risk_model": "- consequence risk",
    "minus_intent_ambiguity_gate": "- intent ambiguity",
    "minus_human_burden_model": "- human burden",
    "minus_handoff_hysteresis": "- handoff hysteresis",
    "minus_boundary_uncertainty": "- boundary uncertainty",
    "minus_recovery_feasibility": "- recovery feasibility",
    "confidence_only_boundary": "Confidence only",
    "safety_only_boundary": "Safety only",
    "mpc_only_boundary": "MPC only",
}

METRIC_LABELS = {
    "task_success": "Success",
    "safety_violation": "Safety",
    "authority_regret": "Regret",
    "human_burden": "Burden",
    "late_handoff": "Late",
    "handoff_churn": "Churn",
    "recovery_success": "Recovery",
    "intervention_cost": "Cost",
    "boundary_calibration_error": "Calib.",
    "override_precision": "Precision",
    "unsafe_autonomy": "Unsafe",
    "robust_utility": "Utility",
    "coverage": "Coverage",
    "accepted_success": "Acc. succ.",
    "accepted_safety_violation": "Acc. safety",
    "accepted_regret": "Acc. regret",
    "accepted_utility": "Acc. utility",
}

ROW_FILES = [
    "rollouts.csv",
    "dataset_summary.csv",
    "raw_seed_metrics.csv",
    "metrics.csv",
    "pairwise_stats.csv",
    "hard_aggregate_seed_metrics.csv",
    "hard_aggregate_metrics.csv",
    "hard_aggregate_pairwise_stats.csv",
    "ablation_rollouts.csv",
    "ablation_seed_metrics.csv",
    "ablation_metrics.csv",
    "stress_sweep_raw.csv",
    "stress_sweep_seed_metrics.csv",
    "stress_sweep.csv",
    "fixed_risk_raw.csv",
    "fixed_risk_seed_metrics.csv",
    "fixed_risk_metrics.csv",
    "fixed_risk_pairwise.csv",
    "negative_cases.csv",
]


def read_csv(path):
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def count_rows(name):
    return len(read_csv(RESULTS / name))


def ascii_clean(text):
    text = str(text or "")
    for old, new in {
        "\u2013": "-",
        "\u2014": "-",
        "\u2212": "-",
        "\u201c": '"',
        "\u201d": '"',
        "\u2018": "'",
        "\u2019": "'",
        "\u2010": "-",
        "\u2011": "-",
        "\xa0": " ",
    }.items():
        text = text.replace(old, new)
    return text.encode("ascii", "ignore").decode("ascii")


def tex_escape(text):
    text = ascii_clean(text)
    repl = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(repl.get(ch, ch) for ch in text)


def phrase(text):
    return tex_escape(ascii_clean(text).replace("_", " "))


def method_name(method):
    return tex_escape(METHOD_LABELS.get(method, method))


def split_name(split):
    return tex_escape(SPLIT_LABELS.get(split, split))


def ablation_name(ablation):
    return tex_escape(ABLATION_LABELS.get(ablation, ablation))


def metric_name(metric):
    return tex_escape(METRIC_LABELS.get(metric, metric))


def fmt(value):
    return f"{float(value):.3f}"


def fmt_pm(mean, ci):
    return f"{float(mean):.3f} $\\pm$ {float(ci):.3f}"


def metric_lookup(rows, selectors, metric):
    for row in rows:
        if row.get("metric") != metric:
            continue
        if all(row.get(k) == v for k, v in selectors.items()):
            return float(row["mean"]), float(row["ci95"])
    raise KeyError((selectors, metric))


def parse_summary(summary_text):
    out = {}
    for line in summary_text.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            out[key.strip()] = value.strip()
        elif ":" in line:
            key, value = line.split(":", 1)
            out[key.strip()] = value.strip()
    return out


def bib_key(i):
    return f"pool90_{i:02d}"


def write_references():
    rows = read_csv(DOCS / "deep_read_250.csv")[:120]
    entries = []
    for i, row in enumerate(rows, start=1):
        title = tex_escape(row.get("title") or "Untitled prior work")
        authors_raw = ascii_clean(row.get("authors") or "Local Prior Work Pool")
        parts = [p.strip() for p in re.split(r";| and ", authors_raw) if p.strip()]
        authors = " and ".join(tex_escape(p) for p in parts[:10]) or "Local Prior Work Pool"
        year_raw = ascii_clean(row.get("year") or "")
        match = re.search(r"(19|20)\d{2}", year_raw)
        year = match.group(0) if match else "2026"
        venue = tex_escape(row.get("venue") or row.get("source") or "prior-work pool")
        link = tex_escape(row.get("doi") or row.get("url") or row.get("arxiv_id") or row.get("uid") or "local pool record")
        entries.append(
            "\n".join(
                [
                    f"@misc{{{bib_key(i)},",
                    f"  author={{{authors}}},",
                    f"  title={{{title}}},",
                    f"  year={{{year}}},",
                    f"  note={{{venue}; {link}}}",
                    "}",
                ]
            )
        )
    (PAPER / "references.bib").write_text("\n\n".join(entries) + "\n", encoding="utf-8")
    return [bib_key(i) for i in range(1, len(rows) + 1)], rows


def longtable(header, rows, spec, caption, label, fontsize=r"\scriptsize"):
    lines = [
        r"\begin{center}",
        fontsize,
        f"\\begin{{longtable}}{{{spec}}}",
        f"\\caption{{{caption}}}\\label{{{label}}}\\\\",
        r"\toprule",
        header + r"\\",
        r"\midrule",
        r"\endfirsthead",
        f"\\caption[]{{{caption} (continued)}}\\\\",
        r"\toprule",
        header + r"\\",
        r"\midrule",
        r"\endhead",
    ]
    lines.extend(rows)
    lines.extend([r"\bottomrule", r"\end{longtable}", r"\normalsize", r"\end{center}"])
    return "\n".join(lines)


def row_count_table():
    rows = [f"{tex_escape(name)} & {count_rows(name):,}\\\\" for name in ROW_FILES]
    return longtable("Evidence file & Data rows", rows, "p{0.55\\linewidth}r", "Reproducibility inventory regenerated from exact CSV files.", "tab:inventory")


def gate_table(summary):
    rows = [
        ("Main authority gate", summary["main_gate"], "Requires v5 to beat the strongest non-oracle success reference with a positive paired lower bound and no safety, burden, regret, or utility regression."),
        ("Mechanism ablation gate", summary["mechanism_gate"], "Requires the full boundary to beat every component removal by a practical utility margin."),
        ("Stress non-domination gate", summary["stress_gate"], "Checks maximum combined stress against CBF, MPC, POMDP, recovery-aware, Bayesian, and uncertainty references."),
        ("Fixed-risk deployment gate", summary["fixed_risk_gate"], "Requires nonzero coverage at budget 0.05 and best feasible accepted utility."),
        ("Scope gate", summary["scope_gate"], "Requires real robot or accepted high-fidelity external benchmark evidence."),
    ]
    body = [f"{tex_escape(name)} & {tex_escape(value)} & {tex_escape(reason)}\\\\" for name, value, reason in rows]
    return longtable("Gate & Passed & Frozen interpretation", body, "p{0.24\\linewidth}p{0.12\\linewidth}p{0.54\\linewidth}", "Frozen submission-readiness gates.", "tab:gates")


def hard_table(hard_metrics):
    rows = []
    for method in METHOD_ORDER:
        success = metric_lookup(hard_metrics, {"method": method}, "task_success")
        safety = metric_lookup(hard_metrics, {"method": method}, "safety_violation")
        burden = metric_lookup(hard_metrics, {"method": method}, "human_burden")
        regret = metric_lookup(hard_metrics, {"method": method}, "authority_regret")
        late = metric_lookup(hard_metrics, {"method": method}, "late_handoff")
        utility = metric_lookup(hard_metrics, {"method": method}, "robust_utility")
        rows.append(f"{method_name(method)} & {fmt_pm(*success)} & {safety[0]:.3f} & {burden[0]:.3f} & {regret[0]:.3f} & {late[0]:.3f} & {utility[0]:.3f}\\\\")
    return longtable("Method & Success & Safety & Burden & Regret & Late & Utility", rows, "p{0.27\\linewidth}rrrrrr", "Predefined hard-aggregate authority results.", "tab:hard")


def split_table(metrics):
    rows = []
    for split in SPLIT_ORDER:
        for method in FOCUS_METHODS:
            success = metric_lookup(metrics, {"split": split, "method": method}, "task_success")
            safety = metric_lookup(metrics, {"split": split, "method": method}, "safety_violation")
            burden = metric_lookup(metrics, {"split": split, "method": method}, "human_burden")
            regret = metric_lookup(metrics, {"split": split, "method": method}, "authority_regret")
            utility = metric_lookup(metrics, {"split": split, "method": method}, "robust_utility")
            rows.append(f"{split_name(split)} & {method_name(method)} & {fmt_pm(*success)} & {safety[0]:.3f} & {burden[0]:.3f} & {regret[0]:.3f} & {utility[0]:.3f}\\\\")
    return longtable("Split & Method & Success & Safety & Burden & Regret & Utility", rows, "p{0.17\\linewidth}p{0.25\\linewidth}rrrrr", "Split-level results for the strongest authority baselines and v5.", "tab:split")


def pairwise_table(hard_pairs, summary):
    refs = [
        summary["best_success_reference"],
        summary["safest_reference"],
        summary["lowest_burden_reference"],
        summary["lowest_regret_reference"],
        summary["best_utility_reference"],
        "authority_boundary_v4",
    ]
    metrics = ["task_success", "safety_violation", "human_burden", "authority_regret", "late_handoff", "robust_utility"]
    seen = set()
    rows = []
    for ref in refs:
        if ref in seen:
            continue
        seen.add(ref)
        for metric in metrics:
            matches = [r for r in hard_pairs if r["reference"] == ref and r["metric"] == metric]
            if not matches:
                continue
            row = matches[0]
            rows.append(f"{method_name(ref)} & {metric_name(metric)} & {fmt(row['mean_diff'])} & {fmt(row['ci95'])} & {fmt(row['lower95'])} & {fmt(row['upper95'])}\\\\")
    return longtable("Reference & Metric & Mean diff & CI95 & Lower95 & Upper95", rows, "p{0.30\\linewidth}p{0.20\\linewidth}rrrr", "Paired seed-level differences for authority v5 minus selected references on the hard aggregate.", "tab:paired")


def split_pairwise_table(pairwise):
    rows = []
    metrics = ["task_success", "safety_violation", "human_burden", "robust_utility"]
    for row in pairwise:
        if row["metric"] not in metrics:
            continue
        rows.append(
            f"{split_name(row['split'])} & {method_name(row['reference'])} & {metric_name(row['metric'])} & {fmt(row['mean_diff'])} & {fmt(row['lower95'])} & {fmt(row['upper95'])}\\\\"
        )
    return longtable(
        "Split & Reference & Metric & Mean diff & Lower95 & Upper95",
        rows,
        "p{0.17\\linewidth}p{0.25\\linewidth}p{0.16\\linewidth}rrr",
        "Complete split-level paired checks for success, safety, burden, and utility.",
        "tab:splitpaired",
        fontsize=r"\tiny",
    )


def ablation_table(ablations):
    rows = []
    for row in ablations:
        rows.append(f"{split_name(row['split'])} & {ablation_name(row['ablation'])} & {fmt_pm(row['task_success'], row['task_success_ci95'])} & {fmt(row['safety_violation'])} & {fmt(row['human_burden'])} & {fmt(row['authority_regret'])} & {fmt(row['robust_utility'])}\\\\")
    return longtable("Split & Ablation & Success & Safety & Burden & Regret & Utility", rows, "p{0.16\\linewidth}p{0.30\\linewidth}rrrrr", "Mechanism ablations. The full method must beat removals rather than benefit from deletion.", "tab:ablation")


def stress_table(stress):
    rows = []
    for row in stress:
        rows.append(f"{phrase(row['stress_axis'])} & {row['stress_level']} & {method_name(row['method'])} & {fmt(row['task_success'])} & {fmt(row['safety_violation'])} & {fmt(row['human_burden'])} & {fmt(row['authority_regret'])} & {fmt(row['robust_utility'])}\\\\")
    return longtable("Axis & Level & Method & Succ. & Safety & Burden & Regret & Utility", rows, "p{0.17\\linewidth}rp{0.23\\linewidth}rrrrr", "Full stress sweep over six axes and six levels.", "tab:stress", fontsize=r"\tiny")


def fixed_table(fixed):
    rows = []
    for row in fixed:
        rows.append(f"{split_name(row['split'])} & {row['budget']} & {method_name(row['method'])} & {fmt(row['coverage'])} & {fmt(row['accepted_success'])} & {fmt(row['accepted_safety_violation'])} & {fmt(row['accepted_regret'])} & {fmt(row['accepted_utility'])}\\\\")
    return longtable("Split & Budget & Method & Cover. & Succ. & Safety & Regret & Utility", rows, "p{0.16\\linewidth}rp{0.24\\linewidth}rrrrr", "Fixed-risk deployment results. Low accepted risk is not enough if coverage collapses to zero.", "tab:fixed")


def fixed_pairwise_table(fixed_pairs):
    rows = []
    for row in fixed_pairs:
        if row["budget"] not in {"0.05", "0.10"}:
            continue
        rows.append(f"{split_name(row['split'])} & {row['budget']} & {method_name(row['reference'])} & {metric_name(row['metric'])} & {fmt(row['mean_diff'])} & {fmt(row['lower95'])} & {fmt(row['upper95'])}\\\\")
    return longtable("Split & Budget & Reference & Metric & Mean diff & Lower95 & Upper95", rows, "p{0.14\\linewidth}rp{0.24\\linewidth}p{0.17\\linewidth}rrr", "Fixed-risk paired differences for v5 minus references.", "tab:fixedpairs", fontsize=r"\tiny")


def negative_table(negative):
    rows = []
    for row in negative:
        rows.append(f"{phrase(row['case_id'])} & {split_name(row['split'])} & {method_name(row['method'])} & {tex_escape(row['trigger'])} & {tex_escape(row['failure_mode'])}\\\\")
    return longtable(
        "Case & Split & Method & Trigger & Failure mode",
        rows,
        "@{}p{0.08\\linewidth}p{0.14\\linewidth}p{0.14\\linewidth}p{0.24\\linewidth}p{0.27\\linewidth}@{}",
        "Predefined negative cases showing authority-boundary failure modes.",
        "tab:negative",
        fontsize=r"\tiny",
    )


def prior_work_table(rows):
    table_rows = []
    for i, row in enumerate(rows, start=1):
        title = tex_escape(row.get("title", ""))[:165]
        family = phrase(row.get("family", ""))
        role = phrase(row.get("query_role", ""))
        hostile = tex_escape(row.get("hostile_score", ""))
        table_rows.append(f"\\citep{{{bib_key(i)}}} & {title} & {family} & {role} & {hostile}\\\\")
    return longtable("Citation & Prior-work threat & Family & Role & Hostile", table_rows, "@{}p{0.10\\linewidth}p{0.42\\linewidth}p{0.13\\linewidth}p{0.12\\linewidth}r@{}", "Closest local-pool references used to set the novelty boundary. Bright boxed citations jump to bibliography entries.", "tab:prior", fontsize=r"\tiny")


def summary_extract_table(summary_text):
    rows = []
    kept = 0
    for line_no, line in enumerate(ascii_clean(summary_text).splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        kept += 1
        rows.append(f"{line_no} & {tex_escape(line[:230])}\\\\")
        if kept >= 165:
            break
    return longtable("Line & Summary extract", rows, "rp{0.84\\linewidth}", "Wrapped extract from results/summary.txt.", "tab:summaryextract", fontsize=r"\tiny")


def build_manuscript(keys, prior_rows):
    summary_text = (RESULTS / "summary.txt").read_text(encoding="utf-8")
    summary = parse_summary(summary_text)
    metrics = read_csv(RESULTS / "metrics.csv")
    hard_metrics = read_csv(RESULTS / "hard_aggregate_metrics.csv")
    hard_pairs = read_csv(RESULTS / "hard_aggregate_pairwise_stats.csv")
    pairwise = read_csv(RESULTS / "pairwise_stats.csv")
    ablations = read_csv(RESULTS / "ablation_metrics.csv")
    stress = read_csv(RESULTS / "stress_sweep.csv")
    fixed = read_csv(RESULTS / "fixed_risk_metrics.csv")
    fixed_pairs = read_csv(RESULTS / "fixed_risk_pairwise.csv")
    negative = read_csv(RESULTS / "negative_cases.csv")
    cite_core = ",".join(keys[:20])
    cite_safety = ",".join(keys[20:40])
    cite_more = ",".join(keys[40:60])
    cite_core_cmd = f"\\citep{{{cite_core}}}"
    cite_safety_cmd = f"\\citep{{{cite_safety}}}"
    cite_more_cmd = f"\\citep{{{cite_more}}}"

    sections = [
        r"\documentclass{article}",
        r"\usepackage{iclr2026_conference,times}",
        r"\input{math_commands.tex}",
        r"\usepackage{hyperref}",
        r"\usepackage{url}",
        r"\usepackage{booktabs}",
        r"\usepackage{graphicx}",
        r"\usepackage{array}",
        r"\usepackage{longtable}",
        r"\usepackage{xcolor}",
        r"\usepackage{amsmath,amssymb}",
        r"\hypersetup{colorlinks=false,pdfborder={0 0 1.8},citebordercolor={0 1 0},linkbordercolor={1 0.55 0},urlbordercolor={0 0.45 1}}",
        r"\graphicspath{{../figures/}}",
        r"\newcommand{\methodname}{authority boundary v5}",
        r"\title{Control Authority Boundaries:\\A 25+ Page Negative Submission-Readiness\\Audit}",
        r"\author{Anonymous Authors}",
        r"\begin{document}",
        r"\maketitle",
        r"\begin{abstract}",
        (
            "Shared-autonomy robots need explicit rules for when a learned policy, certified controller, risk-aware planner, or human operator should hold control authority. "
            "This rebuild tests an authority-boundary model that scores physical consequence, intent ambiguity, control-barrier risk, human delay, recovery feasibility, handoff hysteresis, boundary uncertainty, and authority churn. "
            "The audit is hostile: ten seeds, six tasks, eight splits, thirteen methods, ten ablations, six stress axes, fixed-risk budgets, and 24 negative cases. "
            f"On the hard aggregate, \\methodname{{}} reaches {float(summary['proposal_success']):.3f} task success versus {float(summary['best_success']):.3f} for {tex_escape(summary['best_success_reference'])}, with paired lower95 {float(summary['paired_success_lower95']):.3f}. "
            f"It also trails the safest reference on safety and the best reference on utility. Fixed-risk coverage at budget 0.05 collapses. The honest terminal decision is \\textbf{{KILL/ARCHIVE}}."
        ),
        r"\end{abstract}",
        r"\section{Terminal Decision}",
        "Decision: \\textbf{KILL/ARCHIVE for ICLR main.} The expanded audit improves the old v4 archive, but stronger baselines make the central submission claim fail more clearly.",
        gate_table(summary),
        r"\section{Research Question and Threat Model}",
        f"The question is whether explicit authority-boundary state adds value beyond CBF safety filters, MPC arbitration, Bayesian shared control, POMDP handoff, controller fusion, and uncertainty-triggered human takeover. The local pool includes strong threats from shared control, haptics, barrier certificates, MPC, assistive robotics, and human-robot interaction {cite_core_cmd}.",
        r"\section{Method}",
        "The proposed score combines physical consequence risk, intent ambiguity, control-barrier violation risk, human delay and burden, recovery feasibility, handoff hysteresis, boundary uncertainty, and authority churn penalties. The frozen robust utility is $U=s-0.62v-0.24b-0.25r-0.16l-0.12c-0.10q+0.08e$, where $s$ is success, $v$ safety violation, $b$ human burden, $r$ authority regret, $l$ late handoff, $c$ churn, $q$ intervention cost, and $e$ recovery success.",
        r"\section{Reproducibility Inventory}",
        row_count_table(),
        r"\section{Main Results}",
        "Table~\\ref{tab:hard} is the primary result. Authority v5 improves over v4, but it remains weaker than recovery-aware MPC on success and weaker than CBF on safety and utility.",
        hard_table(hard_metrics),
        r"\begin{figure}[t]\centering\includegraphics[width=0.95\linewidth]{authority_boundary_hard_success_v5.png}\caption{Hard-aggregate task success.}\end{figure}",
        r"\begin{figure}[t]\centering\includegraphics[width=0.95\linewidth]{authority_boundary_failures_v5.png}\caption{Safety, human burden, and utility deficit.}\end{figure}",
        r"\section{Split-Level Evidence}",
        split_table(metrics),
        r"\section{Paired Seed Tests}",
        pairwise_table(hard_pairs, summary),
        r"\section{Complete Split Paired Checks}",
        "Table~\\ref{tab:splitpaired} reports the split-level paired comparisons that hostile reviewers would otherwise ask for after seeing only the hard aggregate.",
        split_pairwise_table(pairwise),
        r"\section{Ablations}",
        "The mechanism gate fails because simpler safety-only and MPC-only variants beat the full model on the combined stress utility target.",
        ablation_table(ablations),
        r"\begin{figure}[t]\centering\includegraphics[width=0.95\linewidth]{authority_boundary_ablation_v5.png}\caption{Ablation robust utility on combined authority stress.}\end{figure}",
        r"\section{Stress Tests}",
        stress_table(stress),
        r"\section{Fixed-Risk Deployment}",
        "At budget 0.05, accepted coverage collapses on hard fixed-risk splits. A deployable authority arbiter cannot pass by refusing every difficult episode.",
        fixed_table(fixed),
        fixed_pairwise_table(fixed_pairs),
        r"\section{Negative Cases}",
        negative_table(negative),
        r"\section{Prior Work Boundary}",
        f"The bright boxed citation wall is part of the audit. Prior shared-control, control-barrier, MPC, haptic, and human-robot autonomy-transition work already covers much of the obvious contribution space {cite_safety_cmd}. The current local evidence does not clear that boundary {cite_more_cmd}.",
        prior_work_table(prior_rows),
        r"\begin{figure}[t]\centering\includegraphics[width=0.95\linewidth]{authority_boundary_stress_sweep_v5.png}\caption{Task success under combined authority stress.}\end{figure}",
        r"\begin{figure}[t]\centering\includegraphics[width=0.95\linewidth]{authority_boundary_fixed_risk_v5.png}\caption{Fixed-risk coverage on combined authority stress.}\end{figure}",
        r"\begin{figure}[t]\centering\includegraphics[width=0.75\linewidth]{authority_boundary_pareto_v5.png}\caption{Hard-aggregate Pareto view for success, safety, burden, and utility.}\end{figure}",
        r"\section{Reproducibility, Artifact Location, and Ethics}",
        "All rows were generated locally on CPU with deterministic seeds. The final numbered PDF is copied only to Downloads. No Desktop PDF is produced. This paper should not be submitted as ICLR main without real robot or accepted high-fidelity validation.",
        r"\clearpage",
        r"\appendix",
        r"\section{Raw Summary Extract}",
        summary_extract_table(summary_text),
        r"\bibliographystyle{iclr2026_conference}",
        r"\bibliography{references}",
        r"\end{document}",
    ]
    (PAPER / "main.tex").write_text("\n\n".join(sections) + "\n", encoding="utf-8")


def main():
    PAPER.mkdir(exist_ok=True)
    keys, prior_rows = write_references()
    build_manuscript(keys, prior_rows)
    print(f"wrote {PAPER / 'main.tex'}")
    print(f"wrote {PAPER / 'references.bib'}")


if __name__ == "__main__":
    main()
