#!/usr/bin/env python3
"""Build a Bullock-like disk-inferred spin conversion proxy gate.

This gate asks whether a standard angular-momentum proxy can reduce the
missing lambda_spin blocker without using endpoint residuals.  It computes

    j_disk = 2 R_d V_flat
    R_200  = V_200 / (10 H_0)
    lambda'_disk = j_disk / (sqrt(2) R_200 V_200)

for beta-closure transfer candidates with Li et al. (2020) NFW halo fields.
The result is a source-side conversion candidate, not a direct halo spin
measurement and not replay permission.
"""

from __future__ import annotations

import math
from io import StringIO
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
EXTERNAL = ROOT / "data" / "external" / "literature" / "li2020_sparc_halo_catalog"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ugc12506_beta_closure_bullock_spin_conversion_proxy_gate_not_endpoint"
H0_KM_S_MPC = 73.0
LAMBDA_REF = 0.10


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

    master = pd.read_csv(DATA / "external_sparc_master_table.csv")
    transfer = pd.read_csv(DATA / "ugc12506_beta_closure_source_declared_spin_proxy_transfer_queue.csv")
    halo_priority = pd.read_csv(DATA / "ugc12506_beta_closure_transfer_priority_gate.csv")
    table = read_vizier_tsv(EXTERNAL / "table1_vizier.tsv")
    table["galaxy"] = table["Name"].astype(str).str.strip()
    table["model"] = table["Model"].astype(str).str.strip()

    master["galaxy"] = master["Galaxy"].astype(str)
    rows = []
    for _, target in transfer.iterrows():
        galaxy = str(target["galaxy"])
        m = master.loc[master["galaxy"].eq(galaxy)]
        nfw = table.loc[table["galaxy"].eq(galaxy) & table["model"].eq("NFW-Flat")]
        if m.empty or nfw.empty:
            status = "MISSING_SOURCE_FIELDS"
            r_disk = vflat = v200 = r200 = j_disk = lambda_disk = np.nan
        else:
            mrow = m.iloc[0]
            hrow = nfw.iloc[0]
            r_disk = safe_float(mrow["Rdisk_kpc"])
            vflat = safe_float(mrow["Vflat_kms"])
            v200 = safe_float(hrow["V200"])
            r200 = 1000.0 * v200 / (10.0 * H0_KM_S_MPC)
            j_disk = 2.0 * r_disk * vflat
            lambda_disk = j_disk / (math.sqrt(2.0) * r200 * v200)
            status = "CONVERSION_PROXY_COMPUTED_REVIEW_REQUIRED"

        load_row = halo_priority.loc[halo_priority["galaxy"].eq(galaxy)]
        nfw_load = (
            safe_float(load_row.iloc[0]["nfw_preference_load"])
            if not load_row.empty
            else safe_float(target["nfw_preference_load"])
        )
        edgeon_load = safe_float(target["edgeon_load"])
        beta_if_bullock = (
            1.0 + (lambda_disk / LAMBDA_REF) * nfw_load + edgeon_load
            if np.isfinite(lambda_disk) and np.isfinite(nfw_load)
            else np.nan
        )
        rows.append(
            {
                "galaxy": galaxy,
                "conversion_proxy_status": status,
                "Rdisk_kpc": r_disk,
                "Vflat_km_s": vflat,
                "V200_NFW_flat_km_s": v200,
                "R200_NFW_flat_kpc": r200,
                "j_disk_kpc_km_s": j_disk,
                "lambda_bullock_disk_proxy": lambda_disk,
                "lambda_ref": LAMBDA_REF,
                "nfw_preference_load": nfw_load,
                "edgeon_load": edgeon_load,
                "beta_if_bullock_disk_proxy_used": beta_if_bullock,
                "accepted_as_beta_cl_lambda_spin": False,
                "proxy_review_required": True,
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    conversion = pd.DataFrame(rows)
    conversion.to_csv(
        DATA / "ugc12506_beta_closure_bullock_spin_conversion_proxy_values.csv",
        index=False,
    )

    primary = conversion[conversion["galaxy"].isin(["NGC0891", "NGC7331"])].copy()
    comparison = primary.merge(
        transfer[
            [
                "galaxy",
                "lambda_spin_proxy_candidate",
                "spin_envelope_exposure_proxy",
                "transfer_proxy_class",
            ]
        ],
        on="galaxy",
        how="left",
    )
    comparison["exposure_minus_bullock_lambda"] = (
        comparison["lambda_spin_proxy_candidate"]
        - comparison["lambda_bullock_disk_proxy"]
    )
    comparison.to_csv(
        DATA / "ugc12506_beta_closure_bullock_spin_conversion_proxy_comparison.csv",
        index=False,
    )

    checks = pd.DataFrame(
        [
            {
                "check_id": "BSP_BULLOCK_1_DIMENSIONLESS",
                "result": "PASS_FORMULA",
                "reason": "j_disk and R200*V200 both have kpc km/s units",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "check_id": "BSP_BULLOCK_2_RESIDUAL_BLIND",
                "result": "PASS_SOURCE_SIDE",
                "reason": "uses SPARC source fields plus Li2020 NFW V200; no vobs residual or endpoint score",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "check_id": "BSP_BULLOCK_3_ASSUMPTION_DEPENDENCE",
                "result": "REVIEW_REQUIRED",
                "reason": "requires disk specific angular momentum to trace the relevant halo/envelope closure-normalization slot",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "check_id": "BSP_BULLOCK_4_REPLAY_PERMISSION",
                "result": "BLOCKED",
                "reason": "conversion proxy is not accepted as beta_cl lambda_spin without independent review",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    checks.to_csv(
        DATA / "ugc12506_beta_closure_bullock_spin_conversion_proxy_checks.csv",
        index=False,
    )

    summary = pd.DataFrame(
        [
            {
                "bullock_conversion_proxy_status": (
                    "BULLOCK_DISK_INFERRED_SPIN_PROXY_COMPUTED_REVIEW_REQUIRED"
                ),
                "n_targets_computed": int(conversion["lambda_bullock_disk_proxy"].notna().sum()),
                "ngc0891_lambda_bullock_disk_proxy": float(
                    comparison.loc[
                        comparison["galaxy"].eq("NGC0891"),
                        "lambda_bullock_disk_proxy",
                    ].iloc[0]
                ),
                "ngc7331_lambda_bullock_disk_proxy": float(
                    comparison.loc[
                        comparison["galaxy"].eq("NGC7331"),
                        "lambda_bullock_disk_proxy",
                    ].iloc[0]
                ),
                "accepted_as_beta_cl_lambda_spin": False,
                "proxy_review_required": True,
                "beta_cl_replay_allowed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "next_gate": (
                    "independent_review_choose_exposure_proxy_or_bullock_conversion_or_direct_spin_source"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    summary.to_csv(
        DATA / "ugc12506_beta_closure_bullock_spin_conversion_proxy_summary.csv",
        index=False,
    )

    report = [
        "# UGC12506 Beta-Closure Bullock-Like Spin Conversion Proxy Gate",
        "",
        "This gate computes a source-side, Bullock-like disk-inferred spin proxy",
        "for beta_cl transfer candidates. It is a conditional conversion proxy,",
        "not a direct halo/envelope spin measurement and not replay permission.",
        "",
        "## Formula",
        "",
        "\\[",
        "j_{\\rm disk}=2R_dV_{\\rm flat},\\quad",
        "R_{200}=V_{200}/(10H_0),\\quad",
        "\\lambda'_{\\rm disk}={j_{\\rm disk}\\over \\sqrt{2}R_{200}V_{200}}.",
        "\\]",
        "",
        "The formula is dimensionless and residual-blind. Its open assumption is",
        "whether the disk-inferred specific angular momentum can stand in for the",
        "Tau-side halo/envelope closure-normalization slot.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Primary Comparison",
        "",
        markdown_table(comparison),
        "",
        "## Checks",
        "",
        markdown_table(checks),
        "",
        "## Claim Boundary",
        "",
        "The gate produces a more standard spin-proxy candidate than the exposure",
        "load proxy, but it does not promote either candidate. An independent",
        "review must choose or reject the conversion before any beta_cl preflight",
        "or replay.",
    ]
    (REPORTS / "ugc12506_beta_closure_bullock_spin_conversion_proxy_gate.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )
    print(summary.to_string(index=False))
    print(comparison[[
        "galaxy",
        "lambda_bullock_disk_proxy",
        "lambda_spin_proxy_candidate",
        "beta_if_bullock_disk_proxy_used",
        "transfer_proxy_class",
    ]].to_string(index=False))


if __name__ == "__main__":
    main()
