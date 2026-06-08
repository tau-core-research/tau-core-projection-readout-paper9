#!/usr/bin/env python3
"""Acquire source-native halo-fit fields for beta-closure transfer candidates.

This acquisition step uses the Li et al. (2020) SPARC halo-model catalogue
through VizieR to fill the pISO-vs-NFW reduced-chi2 closure preference for the
predeclared UGC12506 beta-closure transfer candidates.  It deliberately does
not infer the missing spin or PV/envelope fields, so it does not unlock an
endpoint replay by itself.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
EXTERNAL = ROOT / "data" / "external" / "literature" / "li2020_sparc_halo_catalog"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ugc12506_beta_closure_transfer_halo_fit_acquisition_not_endpoint"
SOURCE_URL = "https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=J/ApJS/247/31/table1&-out.all=1"
SOURCE_CITATION = "Li et al. 2020, ApJS 247, 31; VizieR J/ApJS/247/31"


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


def read_vizier_tsv(path: Path) -> pd.DataFrame:
    lines = path.read_text(encoding="utf-8").splitlines()
    header_index = None
    for index, line in enumerate(lines):
        if line.startswith("recno\tName\tModel"):
            header_index = index
            break
    if header_index is None:
        raise RuntimeError(f"Could not find VizieR table header in {path}")
    rows = []
    for line in lines[header_index + 3 :]:
        if not line.strip() or line.startswith("#"):
            continue
        rows.append(line)
    from io import StringIO

    return pd.read_csv(StringIO("\n".join([lines[header_index], *rows])), sep="\t")


def safe_float(value: object) -> float:
    try:
        text = str(value).strip()
        if not text:
            return float("nan")
        return float(text)
    except Exception:
        return float("nan")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    candidates = pd.read_csv(DATA / "ugc12506_beta_closure_transfer_candidates.csv")
    table_path = EXTERNAL / "table1_vizier.tsv"
    if not table_path.exists():
        raise FileNotFoundError(
            f"Missing {table_path}; cache it from {SOURCE_URL} before running this gate."
        )

    halo = read_vizier_tsv(table_path)
    halo["galaxy"] = halo["Name"].astype(str).str.strip()
    halo["model"] = halo["Model"].astype(str).str.strip()
    halo["chi2_value"] = halo["chi2"].map(safe_float)

    rows = []
    for _, cand in candidates.iterrows():
        galaxy = str(cand["galaxy"])
        sub = halo.loc[halo["galaxy"].eq(galaxy)]
        p_iso = sub.loc[sub["model"].eq("pISO-Flat"), "chi2_value"]
        nfw = sub.loc[sub["model"].eq("NFW-Flat"), "chi2_value"]
        chi2_iso = float(p_iso.iloc[0]) if len(p_iso) else np.nan
        chi2_nfw = float(nfw.iloc[0]) if len(nfw) else np.nan
        if np.isfinite(chi2_iso) and np.isfinite(chi2_nfw) and chi2_nfw > 0:
            ratio = chi2_iso / chi2_nfw
            load = max(ratio - 1.0, 0.0)
            halo_status = "HALO_FIT_FIELDS_FILLED"
        else:
            ratio = np.nan
            load = np.nan
            halo_status = "HALO_FIT_FIELDS_INCOMPLETE"
        rows.append(
            {
                "galaxy": galaxy,
                "predeclared_rank": int(cand["predeclared_rank"]),
                "chi2_ISO": chi2_iso,
                "chi2_NFW": chi2_nfw,
                "chi2_ISO_over_NFW": ratio,
                "nfw_preference_load": load,
                "halo_fit_field_status": halo_status,
                "source": SOURCE_CITATION,
                "source_url": SOURCE_URL,
                "uses_vobs_or_residual_for_selection": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    halo_fields = pd.DataFrame(rows)
    halo_fields.to_csv(
        DATA / "ugc12506_beta_closure_transfer_halo_fit_fields.csv", index=False
    )

    worklist = pd.read_csv(DATA / "ugc12506_beta_closure_transfer_source_worklist.csv")
    status_rows = []
    for _, item in worklist.iterrows():
        galaxy = str(item["galaxy"])
        field = str(item["required_field"])
        halo_row = halo_fields.loc[halo_fields["galaxy"].eq(galaxy)]
        filled = False
        value = ""
        source = ""
        if field == "chi2_NFW" and len(halo_row) and np.isfinite(float(halo_row.iloc[0]["chi2_NFW"])):
            filled = True
            value = float(halo_row.iloc[0]["chi2_NFW"])
            source = SOURCE_CITATION
        elif field == "chi2_ISO" and len(halo_row) and np.isfinite(float(halo_row.iloc[0]["chi2_ISO"])):
            filled = True
            value = float(halo_row.iloc[0]["chi2_ISO"])
            source = SOURCE_CITATION
        status_rows.append(
            {
                **item.to_dict(),
                "field_status_after_halo_acquisition": (
                    "FILLED_FROM_LI2020_VIZIER" if filled else item["field_status"]
                ),
                "source_value": value,
                "source_reference": source,
                "endpoint_scores_allowed_after_halo_acquisition": False,
            }
        )
    worklist_update = pd.DataFrame(status_rows)
    worklist_update.to_csv(
        DATA / "ugc12506_beta_closure_transfer_halo_fit_worklist_update.csv",
        index=False,
    )

    n_candidates = int(len(halo_fields))
    n_halo_complete = int(halo_fields["halo_fit_field_status"].eq("HALO_FIT_FIELDS_FILLED").sum())
    n_still_missing_spin = n_candidates
    n_still_missing_pv = n_candidates
    summary_status = (
        "UGC12506_BETA_CLOSURE_TRANSFER_HALO_FIT_FIELDS_FILLED_SPIN_AND_PV_STILL_BLOCKED"
        if n_halo_complete == n_candidates
        else "UGC12506_BETA_CLOSURE_TRANSFER_HALO_FIT_FIELDS_PARTIAL_SPIN_AND_PV_BLOCKED"
    )
    summary = pd.DataFrame(
        [
            {
                "halo_fit_acquisition_status": summary_status,
                "n_candidates": n_candidates,
                "n_halo_fit_complete": n_halo_complete,
                "n_lambda_spin_still_missing": n_still_missing_spin,
                "n_pv_envelope_still_missing": n_still_missing_pv,
                "n_endpoint_scores_allowed": 0,
                "next_gate": "acquire_or_freeze_source_native_spin_and_pv_envelope_fields",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    summary.to_csv(
        DATA / "ugc12506_beta_closure_transfer_halo_fit_acquisition_summary.csv",
        index=False,
    )

    report = [
        "# UGC12506 Beta-Closure Transfer Halo-Fit Acquisition",
        "",
        "This gate fills only the source-native pISO/NFW reduced-chi2 fields",
        "for the predeclared transfer candidates using the Li et al. (2020)",
        "VizieR catalogue. It does not infer spin, PV/envelope status, or any",
        "endpoint score.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Halo-Fit Fields",
        "",
        markdown_table(halo_fields),
        "",
        "## Remaining Blockers",
        "",
        "The beta-closure replay remains blocked for every candidate until",
        "`lambda_spin` and PV/envelope evidence are source-frozen without using",
        "rotation residuals or endpoint scores.",
    ]
    (REPORTS / "ugc12506_beta_closure_transfer_halo_fit_acquisition.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )

    print(summary.to_string(index=False))
    print(halo_fields.to_string(index=False))


if __name__ == "__main__":
    main()
