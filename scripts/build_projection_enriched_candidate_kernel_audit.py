#!/usr/bin/env python3
"""Summarize approximate projection-enriched kernel candidate endpoint status.

This script is intentionally an audit/summary builder, not a scorer.  It reads
already frozen endpoint outputs for the four path/projection-enriched candidate
galaxies discussed in the paper and writes a compact ledger plus a reviewer-
facing report.  No observed velocities or residuals are read here.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"


def markdown_table(df: pd.DataFrame) -> str:
    """Write a compact markdown table without optional pandas dependencies."""
    cols = list(df.columns)
    lines = [
        "| " + " | ".join(cols) + " |",
        "| " + " | ".join(["---"] * len(cols)) + " |",
    ]
    for _, row in df.iterrows():
        vals = []
        for col in cols:
            val = row[col]
            if pd.isna(val):
                vals.append("")
            elif isinstance(val, float):
                vals.append(f"{val:.6g}")
            else:
                vals.append(str(val))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def read_one(path: str) -> pd.Series:
    p = DERIVED / path
    if not p.exists():
        raise FileNotFoundError(p)
    df = pd.read_csv(p)
    if len(df) != 1:
        raise ValueError(f"expected one row in {p}, got {len(df)}")
    return df.iloc[0]


def main() -> None:
    rows: list[dict[str, object]] = []

    ngc4013 = read_one("ngc4013_warp_vertical_overlay_endpoint_scores.csv")
    rows.append(
        {
            "galaxy": "NGC4013",
            "projection_enriched_lane": "expdisk_warp_vertical_overlay",
            "status": ngc4013["endpoint_status"],
            "n_points": int(ngc4013["n_points"]),
            "matched_rmse_km_s": ngc4013["rmse_warp_vertical_overlay"],
            "best_baseline_model": "TPG_V6_v_v6",
            "best_baseline_rmse_km_s": ngc4013["rmse_tpg_v6"],
            "matched_minus_best_baseline_km_s": ngc4013["wvo_minus_tpg_v6"],
            "wrong_family_mean_rmse_km_s": ngc4013["rmse_wrong_family_mean"],
            "matched_minus_wrong_mean_km_s": ngc4013["rmse_warp_vertical_overlay"]
            - ngc4013["rmse_wrong_family_mean"],
            "matched_beats_all_baselines": True,
            "matched_beats_all_wrong_families": pd.NA,
            "construction_used_vobs": False,
            "endpoint_scores_allowed": bool(ngc4013["endpoint_scores_allowed"]),
            "interpretation": "retrospective/caveated mixed-reference case; useful proof-of-concept, not fresh population validation",
        }
    )

    ngc5907 = read_one("ngc5907_expdisk_projection_mixed_accepted_endpoint_summary.csv")
    rows.append(
        {
            "galaxy": "NGC5907",
            "projection_enriched_lane": "expdisk_projection_vertical_warp_context",
            "status": ngc5907["endpoint_status"],
            "n_points": int(ngc5907["n_points"]),
            "matched_rmse_km_s": ngc5907["rmse_mixed_accepted"],
            "best_baseline_model": ngc5907["best_baseline_model"],
            "best_baseline_rmse_km_s": ngc5907["best_baseline_rmse_km_s"],
            "matched_minus_best_baseline_km_s": ngc5907[
                "matched_minus_best_baseline_rmse_km_s"
            ],
            "wrong_family_mean_rmse_km_s": ngc5907["wrong_mixed_mean_rmse_km_s"],
            "matched_minus_wrong_mean_km_s": ngc5907[
                "matched_minus_wrong_mixed_mean_rmse_km_s"
            ],
            "matched_beats_all_baselines": bool(ngc5907["matched_beats_all_baselines"]),
            "matched_beats_all_wrong_families": bool(
                ngc5907["matched_beats_all_wrong_mixed_families"]
            ),
            "construction_used_vobs": bool(ngc5907["construction_used_vobs"]),
            "endpoint_scores_allowed": bool(ngc5907["endpoint_scores_allowed"]),
            "interpretation": "strongest fresh projection-enriched freeze target; single-galaxy preliminary control result",
        }
    )

    ngc7331 = read_one("ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint_summary.csv")
    rows.append(
        {
            "galaxy": "NGC7331",
            "projection_enriched_lane": "expdisk_vertical_outer_warp_overlay",
            "status": ngc7331["endpoint_status"],
            "n_points": int(ngc7331["n_points"]),
            "matched_rmse_km_s": ngc7331["rmse_mixed_accepted"],
            "best_baseline_model": ngc7331["best_baseline_model"],
            "best_baseline_rmse_km_s": ngc7331["best_baseline_rmse_km_s"],
            "matched_minus_best_baseline_km_s": ngc7331[
                "matched_minus_best_baseline_rmse_km_s"
            ],
            "wrong_family_mean_rmse_km_s": ngc7331["wrong_mixed_mean_rmse_km_s"],
            "matched_minus_wrong_mean_km_s": ngc7331[
                "matched_minus_wrong_mixed_mean_rmse_km_s"
            ],
            "matched_beats_all_baselines": bool(ngc7331["matched_beats_all_baselines"]),
            "matched_beats_all_wrong_families": bool(
                ngc7331["matched_beats_all_wrong_mixed_families"]
            ),
            "construction_used_vobs": bool(ngc7331["construction_used_vobs"]),
            "endpoint_scores_allowed": bool(ngc7331["endpoint_scores_allowed"]),
            "interpretation": "caveated accepted mixed endpoint; outer-warp projection still broad-window caveated",
        }
    )

    ngc4088 = read_one("ngc4088_warp_history_accepted_endpoint_summary.csv")
    rows.append(
        {
            "galaxy": "NGC4088",
            "projection_enriched_lane": "warp_history_asymmetric_projection",
            "status": ngc4088["endpoint_status"],
            "n_points": int(ngc4088["n_points"]),
            "matched_rmse_km_s": ngc4088["rmse_warp_history_accepted"],
            "best_baseline_model": ngc4088["best_baseline_model"],
            "best_baseline_rmse_km_s": ngc4088["best_baseline_rmse_km_s"],
            "matched_minus_best_baseline_km_s": ngc4088[
                "matched_minus_best_baseline_rmse_km_s"
            ],
            "wrong_family_mean_rmse_km_s": ngc4088["wrong_family_mean_rmse_km_s"],
            "matched_minus_wrong_mean_km_s": ngc4088[
                "matched_minus_wrong_family_mean_rmse_km_s"
            ],
            "matched_beats_all_baselines": bool(ngc4088["matched_beats_all_baselines"]),
            "matched_beats_all_wrong_families": bool(
                ngc4088["matched_beats_all_wrong_families"]
            ),
            "construction_used_vobs": bool(ngc4088["construction_used_vobs"]),
            "endpoint_scores_allowed": bool(ngc4088["endpoint_scores_allowed"]),
            "interpretation": "visually strong caveated control endpoint; q/memory/epsilon and normalization caveats remain important",
        }
    )

    out = pd.DataFrame(rows)

    # Attach the stricter small-N replay/holdout warning where available.
    replay_path = DERIVED / "mixed_readout_replay_holdout_control_by_galaxy.csv"
    if replay_path.exists():
        replay = pd.read_csv(replay_path).set_index("galaxy")
        out["strict_replay_wrong_label_result"] = out["galaxy"].map(
            lambda g: (
                "not_run"
                if g not in replay.index
                else (
                    "beats_all_wrong_labels"
                    if bool(replay.loc[g, "matched_beats_all_wrong_labels"])
                    else f"does_not_beat_best_wrong_label; margin={replay.loc[g, 'matched_minus_wrong_best']:.4f} km/s"
                )
            )
        )

    summary = {
        "n_candidates": len(out),
        "n_endpoint_scores_allowed": int(out["endpoint_scores_allowed"].sum()),
        "n_matched_beats_all_baselines": int(out["matched_beats_all_baselines"].sum()),
        "n_matched_beats_all_wrong_families_single_case": int(
            out["matched_beats_all_wrong_families"].map(lambda x: bool(x) if pd.notna(x) else False).sum()
        ),
        "mean_matched_minus_best_baseline_km_s": float(
            out["matched_minus_best_baseline_km_s"].mean()
        ),
        "mean_matched_minus_wrong_mean_km_s": float(
            out["matched_minus_wrong_mean_km_s"].mean()
        ),
        "claim_boundary": "projection_enriched_candidate_kernel_audit_not_population_validation",
    }

    out_path = DERIVED / "projection_enriched_candidate_kernel_audit.csv"
    summary_path = DERIVED / "projection_enriched_candidate_kernel_audit_summary.csv"
    report_path = REPORTS / "projection_enriched_candidate_kernel_audit.md"

    out.to_csv(out_path, index=False)
    pd.DataFrame([summary]).to_csv(summary_path, index=False)

    report = [
        "# Projection-Enriched Candidate Kernel Audit",
        "",
        "This audit summarizes already frozen single-galaxy endpoint/control outputs for the four galaxies proposed as approximate path-aware projection-kernel development targets. It is not a new scorer and does not read observed velocities.",
        "",
        "## Summary",
        "",
        markdown_table(pd.DataFrame([summary])),
        "",
        "## Candidate ledger",
        "",
        markdown_table(out),
        "",
        "## Interpretation",
        "",
        "- All four candidate lanes are encouraging in the single-galaxy accepted/caveated endpoint summaries: the matched projection-enriched readout beats the best listed baseline in each row.",
        "- NGC5907 and NGC7331 remain the cleanest next source-side development targets, but the stricter replay/holdout wrong-label check shows that their margins against the best wrong mixed labels are small and currently negative.",
        "- NGC4013 is useful as a mixed-reference proof-of-concept, but it is not a fresh independent holdout.",
        "- NGC4088 is the visually strongest caveated case, but source-review and law-level caveats must stay visible.",
        "- Therefore the correct claim is kernel-development evidence, not population validation and not a final path-aware Tau Core kernel.",
    ]
    report_path.write_text("\\n".join(report) + "\\n", encoding="utf-8")

    print(out.to_string(index=False))
    print(f"\nwrote {out_path}")
    print(f"wrote {summary_path}")
    print(f"wrote {report_path}")


if __name__ == "__main__":
    main()
