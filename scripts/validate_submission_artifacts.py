import csv
import re
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
PAPER = ROOT / "paper"
DOWNLOADS_PDF = Path.home() / "Downloads" / "90.pdf"
DESKTOP_PDF = Path.home() / "Desktop" / "90.pdf"

EXPECTED_COUNTS = {
    "rollouts.csv": 199680,
    "dataset_summary.csv": 15360,
    "raw_seed_metrics.csv": 1040,
    "metrics.csv": 1248,
    "pairwise_stats.csv": 672,
    "hard_aggregate_seed_metrics.csv": 130,
    "hard_aggregate_metrics.csv": 156,
    "hard_aggregate_pairwise_stats.csv": 84,
    "ablation_rollouts.csv": 33600,
    "ablation_seed_metrics.csv": 200,
    "ablation_metrics.csv": 20,
    "ablation_metric_long.csv": 240,
    "stress_sweep_raw.csv": 302400,
    "stress_sweep_seed_metrics.csv": 2520,
    "stress_sweep.csv": 252,
    "stress_sweep_metric_long.csv": 3024,
    "fixed_risk_raw.csv": 69120,
    "fixed_risk_seed_metrics.csv": 480,
    "fixed_risk_metrics.csv": 48,
    "fixed_risk_pairwise.csv": 200,
    "negative_cases.csv": 24,
}

SUMMARY_TOKENS = [
    "Terminal recommendation: KILL_ARCHIVE",
    "proposal_success=0.37096",
    "best_success=0.47370",
    "paired_success_lower95=-0.12094",
    "main_gate=False",
    "mechanism_gate=False",
    "stress_gate=False",
    "fixed_risk_gate=False",
    "scope_gate=False",
]


def csv_count(name):
    with (RESULTS / name).open("r", newline="", encoding="utf-8") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def sha256(path):
    import hashlib

    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def normalized_text(reader):
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return re.sub(r"\s+", " ", text)


def contains_pdf_token(text, token):
    if token in text:
        return True
    compact_text = re.sub(r"[^A-Za-z0-9]+", "", text).upper()
    compact_token = re.sub(r"[^A-Za-z0-9]+", "", token).upper()
    return compact_token in compact_text


def count_internal_citation_links(reader):
    count = 0
    for page in reader.pages:
        for annotation_ref in page.get("/Annots") or []:
            annotation = annotation_ref.get_object()
            if annotation.get("/Subtype") != "/Link":
                continue
            action = annotation.get("/A")
            destination = annotation.get("/Dest")
            if destination and str(destination).startswith("cite."):
                count += 1
            elif action and action.get("/S") == "/GoTo" and str(action.get("/D", "")).startswith("cite."):
                count += 1
    return count


def main():
    for name, expected in EXPECTED_COUNTS.items():
        observed = csv_count(name)
        if observed != expected:
            raise SystemExit(f"{name}: expected {expected}, observed {observed}")
    summary = (RESULTS / "summary.txt").read_text(encoding="utf-8")
    for token in SUMMARY_TOKENS:
        if token not in summary:
            raise SystemExit(f"missing summary token: {token}")
    main_tex = (PAPER / "main.tex").read_text(encoding="utf-8")
    for token in ["citebordercolor={0 1 0}", "colorlinks=false", "pdfborder={0 0 1.8}", "KILL/ARCHIVE", "bibliography{references}"]:
        if token not in main_tex:
            raise SystemExit(f"missing LaTeX token: {token}")
    log = (PAPER / "main.log").read_text(encoding="utf-8", errors="ignore") if (PAPER / "main.log").exists() else ""
    for bad in ["LaTeX Error", "Emergency stop", "Fatal error", "undefined references", "Citation `"]:
        if bad in log:
            raise SystemExit(f"bad LaTeX log token: {bad}")
    if not DOWNLOADS_PDF.exists():
        raise SystemExit(f"missing Downloads PDF: {DOWNLOADS_PDF}")
    if DESKTOP_PDF.exists():
        raise SystemExit(f"Desktop PDF should not exist: {DESKTOP_PDF}")
    reader = PdfReader(str(DOWNLOADS_PDF))
    pages = len(reader.pages)
    if pages < 25:
        raise SystemExit(f"PDF too short: {pages} pages")
    text = normalized_text(reader)
    for token in ["Control Authority Boundaries", "KILL/ARCHIVE", "Fixed-risk", "References"]:
        if not contains_pdf_token(text, token):
            raise SystemExit(f"missing PDF text token: {token}")
    citation_links = count_internal_citation_links(reader)
    if citation_links < 100:
        raise SystemExit(f"too few internal citation links: {citation_links}")
    print(f"validated Paper 90 artifacts: pages={pages}, sha256={sha256(DOWNLOADS_PDF)}")


if __name__ == "__main__":
    main()
