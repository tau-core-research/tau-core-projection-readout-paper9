#!/usr/bin/env python3
"""Build a scoring-readiness dashboard for the UGC12506 beta-closure route.

This is a pre-scoring ledger.  It summarizes the already-built dry-run,
unlock, installer, launcher, launch, formula-freeze, and scoring artifacts so
the next action is visible without weakening the review wall.  It never writes
review decisions, never accepts example-only rows, and never reads observed
rotation curves.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ugc12506_beta_closure_scoring_readiness_dashboard_not_endpoint"


PATHS = {
    "dry_run": DATA / "ugc12506_beta_closure_transfer_scoring_contract_dry_run_summary.csv",
    "unlock": DATA / "ugc12506_beta_closure_transfer_scoring_unlock_packet_summary.csv",
    "installer": DATA / "ugc12506_beta_closure_active_review_response_install_summary.csv",
    "launcher": DATA / "ugc12506_beta_closure_post_review_scoring_launcher_summary.csv",
    "launch": DATA / "ugc12506_beta_closure_scoring_launch_summary.csv",
    "formula": DATA / "ugc12506_beta_closure_transfer_formula_freeze_summary.csv",
    "scoring": DATA / "ugc12506_beta_closure_transfer_scoring_summary.csv",
}


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


def read_first(path: Path) -> pd.Series:
    if not path.exists():
        return pd.Series(dtype=object)
    frame = pd.read_csv(path)
    if frame.empty:
        return pd.Series(dtype=object)
    return frame.iloc[0]


def bool_value(value: object) -> bool:
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes", "y"}
    return bool(value)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.exists() or path.is_relative_to(ROOT) else str(path)


def stage(
    stage_id: str,
    status: str,
    ready: bool,
    blocked: bool,
    artifact: Path,
    evidence: str,
    next_action: str,
    construction_used_vobs: bool = False,
    scoring_used_vobs: bool = False,
) -> dict[str, object]:
    return {
        "stage_id": stage_id,
        "status": status,
        "ready_for_next_stage": ready,
        "blocked": blocked,
        "artifact": rel(artifact),
        "evidence": evidence,
        "next_action": next_action,
        "construction_used_vobs": construction_used_vobs,
        "scoring_used_vobs": scoring_used_vobs,
        "endpoint_scores_allowed": False,
        "endpoint_validation_claim": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    dry_run = read_first(PATHS["dry_run"])
    unlock = read_first(PATHS["unlock"])
    installer = read_first(PATHS["installer"])
    launcher = read_first(PATHS["launcher"])
    launch = read_first(PATHS["launch"])
    formula = read_first(PATHS["formula"])
    scoring = read_first(PATHS["scoring"])

    dry_run_ready = (
        dry_run.get("dry_run_status", "")
        == "U12506_BETA_CLOSURE_TRANSFER_SCORING_CONTRACT_DRY_RUN_READY_REVIEWS_PENDING"
        and int(dry_run.get("n_contract_ready_scenarios", 0)) == 2
        and int(dry_run.get("n_prediction_rows_without_vobs", 0)) > 0
        and not bool_value(dry_run.get("scoring_used_vobs", False))
    )
    unlock_ready = (
        unlock.get("unlock_packet_status", "")
        == "U12506_BETA_CLOSURE_TRANSFER_SCORING_UNLOCK_PACKET_READY_ACTIVE_RESPONSES_PENDING"
        and int(unlock.get("n_required_active_response_files", 0)) == 2
        and int(unlock.get("n_example_only_response_files", 0)) == 3
        and not bool_value(unlock.get("endpoint_scores_allowed", False))
    )
    active_responses_present = int(
        launcher.get(
            "n_active_responses_present",
            installer.get("n_existing_incoming_responses", 0),
        )
    )
    installer_ready = (
        installer.get("active_response_install_status", "")
        == "U12506_BETA_ACTIVE_REVIEW_RESPONSES_INSTALLED_RUN_POST_REVIEW_LAUNCHER"
    )
    launcher_ready = (
        launcher.get("post_review_launcher_status", "")
        == "U12506_BETA_CLOSURE_POST_REVIEW_SCORING_LAUNCHED_CONTROL_ONLY"
    )
    launch_allowed = bool_value(launch.get("beta_cl_transfer_scoring_allowed", False))
    formula_ready = bool_value(formula.get("formula_manifest_ready_for_scoring", False))
    scores_written = bool_value(scoring.get("scores_written", False))
    scoring_used_vobs = bool_value(scoring.get("scoring_used_vobs", False))

    dashboard = pd.DataFrame(
        [
            stage(
                "SCORING_CONTRACT_DRY_RUN",
                str(dry_run.get("dry_run_status", "missing")),
                dry_run_ready,
                not dry_run_ready,
                PATHS["dry_run"],
                (
                    f"{int(dry_run.get('n_contract_ready_scenarios', 0))} scenarios; "
                    f"{int(dry_run.get('n_prediction_rows_without_vobs', 0))} no-vobs predictions"
                ),
                "build_unlock_packet" if dry_run_ready else "rerun_contract_dry_run",
            ),
            stage(
                "REVIEW_UNLOCK_PACKET",
                str(unlock.get("unlock_packet_status", "missing")),
                unlock_ready,
                not unlock_ready,
                PATHS["unlock"],
                (
                    f"{int(unlock.get('n_required_active_response_files', 0))} active responses required; "
                    f"{int(unlock.get('n_example_only_response_files', 0))} example-only rows"
                ),
                "send_unlock_packet_to_independent_reviewer"
                if unlock_ready
                else "rerun_unlock_packet",
            ),
            stage(
                "ACTIVE_RESPONSE_INSTALLER",
                str(installer.get("active_response_install_status", "missing")),
                installer_ready,
                not installer_ready,
                PATHS["installer"],
                (
                    f"{int(installer.get('n_existing_incoming_responses', 0))}/"
                    f"{int(installer.get('n_required_responses', 2))} incoming active responses"
                ),
                "place_completed_review_csvs_in_incoming_dir_then_run_installer",
            ),
            stage(
                "POST_REVIEW_LAUNCHER",
                str(launcher.get("post_review_launcher_status", "missing")),
                launcher_ready,
                not launcher_ready,
                PATHS["launcher"],
                (
                    f"{active_responses_present}/"
                    f"{int(launcher.get('n_required_active_responses', 2))} active responses present; "
                    f"chain_ok={bool_value(launcher.get('chain_returncodes_all_zero', False))}"
                ),
                "run_post_review_launcher_after_active_responses",
            ),
            stage(
                "SCORING_LAUNCH_GATE",
                str(launch.get("scoring_launch_status", "missing")),
                launch_allowed,
                not launch_allowed,
                PATHS["launch"],
                (
                    f"pass_gates={int(launch.get('n_pass_gates', 0))}; "
                    f"blocked_gates={int(launch.get('n_blocked_gates', 0))}"
                ),
                "resolve_review_prefreeze_launch_gates",
            ),
            stage(
                "FORMULA_FREEZE_GATE",
                str(formula.get("formula_freeze_status", "missing")),
                formula_ready,
                not formula_ready,
                PATHS["formula"],
                f"formula_manifest_rows={int(formula.get('n_formula_manifest_rows', 0))}",
                "freeze_nonempty_formula_manifest_before_scoring",
            ),
            stage(
                "TRANSFER_SCORING_RUNNER",
                str(scoring.get("transfer_scoring_status", "missing")),
                scores_written and scoring_used_vobs,
                not (scores_written and scoring_used_vobs),
                PATHS["scoring"],
                (
                    f"scores_written={scores_written}; "
                    f"scoring_used_vobs={scoring_used_vobs}"
                ),
                "review_control_scores_if_runner_executes",
                scoring_used_vobs=scoring_used_vobs,
            ),
        ]
    )

    if scores_written and scoring_used_vobs:
        readiness_status = "U12506_BETA_CLOSURE_SCORING_READINESS_CONTROL_SCORES_WRITTEN_REVIEW_REQUIRED"
        next_action = "review_control_scores_before_any_endpoint_claim"
    elif active_responses_present < 2:
        readiness_status = "U12506_BETA_CLOSURE_SCORING_READINESS_BLOCKED_ACTIVE_RESPONSES_PENDING"
        next_action = "supply_two_active_review_response_csvs_then_run_installer_and_launcher"
    elif not launch_allowed:
        readiness_status = "U12506_BETA_CLOSURE_SCORING_READINESS_BLOCKED_LAUNCH_GATE"
        next_action = "inspect_post_review_intake_prefreeze_and_launch_gates"
    elif not formula_ready:
        readiness_status = "U12506_BETA_CLOSURE_SCORING_READINESS_BLOCKED_FORMULA_FREEZE"
        next_action = "freeze_nonempty_formula_manifest"
    else:
        readiness_status = "U12506_BETA_CLOSURE_SCORING_READINESS_RUNNER_READY"
        next_action = "run_transfer_scoring_runner"

    summary = pd.DataFrame(
        [
            {
                "scoring_readiness_status": readiness_status,
                "n_dashboard_stages": len(dashboard),
                "n_ready_stages": int(dashboard["ready_for_next_stage"].sum()),
                "n_blocked_stages": int(dashboard["blocked"].sum()),
                "dry_run_contract_ready": dry_run_ready,
                "unlock_packet_ready": unlock_ready,
                "active_responses_present": active_responses_present,
                "installer_ready": installer_ready,
                "launcher_control_scores_written": launcher_ready,
                "scoring_launch_allowed": launch_allowed,
                "formula_manifest_ready_for_scoring": formula_ready,
                "scores_written": scores_written,
                "scoring_used_vobs": scoring_used_vobs,
                "endpoint_scores_allowed": False,
                "endpoint_validation_claim": False,
                "next_action": next_action,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    dashboard.to_csv(DATA / "ugc12506_beta_closure_scoring_readiness_dashboard.csv", index=False)
    summary.to_csv(DATA / "ugc12506_beta_closure_scoring_readiness_summary.csv", index=False)

    report = [
        "# UGC12506 Beta-Closure Scoring Readiness Dashboard",
        "",
        "This dashboard condenses the beta-closure transfer path into a single",
        "pre-scoring ledger. It is not an endpoint and it does not read observed",
        "rotation curves.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Stage Ledger",
        "",
        markdown_table(dashboard),
        "",
        "## One Command Path After Independent Review Responses",
        "",
        "Place the completed reviewer files here:",
        "",
        "```text",
        "review_bundles/incoming/ugc12506_beta_closure_transfer_scoring/",
        "```",
        "",
        "Expected filenames:",
        "",
        "```text",
        "ugc12506_beta_closure_spin_proxy_review_response.csv",
        "ugc12506_beta_closure_carrier_review_response.csv",
        "```",
        "",
        "Then run:",
        "",
        "```bash",
        "python scripts/install_ugc12506_beta_closure_active_review_responses.py",
        "python scripts/run_ugc12506_beta_closure_post_review_scoring_launcher.py",
        "python scripts/build_ugc12506_beta_closure_scoring_readiness_dashboard.py",
        "```",
        "",
        "The installer rejects missing, placeholder, example-only, endpoint-flagged,",
        "or residual-leaking response rows. Until both active responses validate,",
        "the scoring runner remains blocked and `vobs` is not read.",
    ]
    (REPORTS / "ugc12506_beta_closure_scoring_readiness_dashboard.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
