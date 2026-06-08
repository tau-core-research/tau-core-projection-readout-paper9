#!/usr/bin/env python3
"""Run the UGC12506 beta-closure post-review scoring launcher.

This launcher is the mechanical bridge from independent review responses to
the existing scoring runner.  It does not write reviewer responses and does not
accept example-only rows.  It simply checks whether the two active response
files exist, runs the standard intake/prefreeze/formula/scoring chain, and
records whether scoring stayed blocked or executed.

If the active response files are absent, the launcher remains a blocked
pre-scoring artifact and does not read observed rotation curves.
"""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ugc12506_beta_closure_post_review_scoring_launcher_not_endpoint"

SPIN_ACTIVE_RESPONSE = DATA / "ugc12506_beta_closure_spin_proxy_review_response.csv"
CARRIER_ACTIVE_RESPONSE = DATA / "ugc12506_beta_closure_carrier_review_response.csv"

CHAIN = [
    "scripts/run_ugc12506_beta_closure_spin_proxy_review_response_intake.py",
    "scripts/build_ugc12506_beta_closure_spin_route_prefreeze_gate.py",
    "scripts/build_ugc12506_beta_closure_spin_route_decision_matrix.py",
    "scripts/run_ugc12506_beta_closure_carrier_review_response_intake.py",
    "scripts/build_ugc12506_beta_closure_transfer_carrier_freeze_gate.py",
    "scripts/build_ugc12506_beta_closure_scoring_launch_gate.py",
    "scripts/build_ugc12506_beta_closure_transfer_formula_freeze_gate.py",
    "scripts/run_ugc12506_beta_closure_transfer_scoring.py",
]


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for column in display.columns:
        if pd.api.types.is_float_dtype(display[column]):
            display[column] = display[column].map(
                lambda value: "" if pd.isna(value) else f"{value:.6g}"
            )
        else:
            display[column] = display[column].astype(str)
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[column]) for column in display.columns) + " |")
    return "\n".join(lines)


def bool_value(value: object) -> bool:
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes", "y"}
    return bool(value)


def run_script(script: str) -> dict[str, object]:
    result = subprocess.run(
        [sys.executable, script],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    return {
        "script": script,
        "returncode": result.returncode,
        "stdout_tail": result.stdout.strip().splitlines()[-1] if result.stdout.strip() else "",
        "stderr_tail": result.stderr.strip().splitlines()[-1] if result.stderr.strip() else "",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def read_first(path: Path) -> pd.Series:
    if not path.exists():
        return pd.Series(dtype=object)
    df = pd.read_csv(path)
    if df.empty:
        return pd.Series(dtype=object)
    return df.iloc[0]


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    active_inputs = pd.DataFrame(
        [
            {
                "active_response": str(SPIN_ACTIVE_RESPONSE.relative_to(ROOT)),
                "response_type": "spin_route_review",
                "exists": SPIN_ACTIVE_RESPONSE.exists(),
                "example_only_accepted": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "active_response": str(CARRIER_ACTIVE_RESPONSE.relative_to(ROOT)),
                "response_type": "carrier_review",
                "exists": CARRIER_ACTIVE_RESPONSE.exists(),
                "example_only_accepted": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    chain_results = pd.DataFrame([run_script(script) for script in CHAIN])

    spin_intake = read_first(DATA / "ugc12506_beta_closure_spin_proxy_review_response_intake_summary.csv")
    carrier_intake = read_first(DATA / "ugc12506_beta_closure_carrier_review_response_intake_summary.csv")
    prefreeze = read_first(DATA / "ugc12506_beta_closure_spin_route_prefreeze_summary.csv")
    carrier_freeze = read_first(DATA / "ugc12506_beta_closure_transfer_carrier_freeze_summary.csv")
    launch = read_first(DATA / "ugc12506_beta_closure_scoring_launch_summary.csv")
    formula = read_first(DATA / "ugc12506_beta_closure_transfer_formula_freeze_summary.csv")
    scoring = read_first(DATA / "ugc12506_beta_closure_transfer_scoring_summary.csv")

    active_responses_present = active_inputs["exists"].all()
    chain_ok = chain_results["returncode"].eq(0).all()
    scoring_executed = bool_value(scoring.get("scores_written", False)) and bool_value(
        scoring.get("scoring_used_vobs", False)
    )

    if scoring_executed:
        status = "U12506_BETA_CLOSURE_POST_REVIEW_SCORING_LAUNCHED_CONTROL_ONLY"
        next_gate = "review_control_only_scores_before_any_endpoint_claim"
    elif active_responses_present:
        status = "U12506_BETA_CLOSURE_POST_REVIEW_SCORING_STILL_BLOCKED_AFTER_ACTIVE_RESPONSES"
        next_gate = "inspect_failed_intake_or_freeze_gate"
    else:
        status = "U12506_BETA_CLOSURE_POST_REVIEW_SCORING_BLOCKED_ACTIVE_RESPONSES_PENDING"
        next_gate = "external_reviewer_supplies_active_response_files"

    summary = pd.DataFrame(
        [
            {
                "post_review_launcher_status": status,
                "n_required_active_responses": len(active_inputs),
                "n_active_responses_present": int(active_inputs["exists"].sum()),
                "chain_returncodes_all_zero": chain_ok,
                "spin_intake_status": spin_intake.get("review_intake_status", "missing"),
                "carrier_intake_status": carrier_intake.get("carrier_review_intake_status", "missing"),
                "spin_prefreeze_status": prefreeze.get("spin_route_prefreeze_status", "missing"),
                "carrier_freeze_status": carrier_freeze.get("carrier_freeze_status", "missing"),
                "scoring_launch_status": launch.get("scoring_launch_status", "missing"),
                "formula_freeze_status": formula.get("formula_freeze_status", "missing"),
                "transfer_scoring_status": scoring.get("transfer_scoring_status", "missing"),
                "scores_written": bool_value(scoring.get("scores_written", False)),
                "scoring_used_vobs": bool_value(scoring.get("scoring_used_vobs", False)),
                "endpoint_scores_allowed": False,
                "endpoint_validation_claim": False,
                "next_gate": next_gate,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    active_inputs.to_csv(
        DATA / "ugc12506_beta_closure_post_review_scoring_launcher_active_inputs.csv",
        index=False,
    )
    chain_results.to_csv(
        DATA / "ugc12506_beta_closure_post_review_scoring_launcher_chain.csv",
        index=False,
    )
    summary.to_csv(
        DATA / "ugc12506_beta_closure_post_review_scoring_launcher_summary.csv",
        index=False,
    )

    report = [
        "# UGC12506 Beta-Closure Post-Review Scoring Launcher",
        "",
        "This launcher runs the standard post-review chain if active response",
        "files are present. It never writes review responses and it never treats",
        "example-only rows as active decisions.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Active Inputs",
        "",
        markdown_table(active_inputs),
        "",
        "## Chain Results",
        "",
        markdown_table(chain_results),
        "",
        "## Claim Boundary",
        "",
        "If active responses are absent, this is only a blocked pre-scoring",
        "artifact. If scoring later executes, it remains a control-only scoring",
        "run until separately reviewed; no endpoint validation claim is made here.",
    ]
    (REPORTS / "ugc12506_beta_closure_post_review_scoring_launcher.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
