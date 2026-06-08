#!/usr/bin/env python3
"""Declare a residual-blind spin/envelope exposure proxy for beta transfer.

The UGC12506 beta-closure replay needs a source-side spin/envelope
normalization.  Direct literature spin values are not cached for the transfer
targets.  This gate therefore defines a candidate proxy from SPARC source
fields only, without scoring rotation curves.  The proxy is not promoted to an
accepted lambda_spin measurement here; endpoint replay remains blocked until an
independent review accepts the proxy rule or supplies direct spin values.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ugc12506_beta_closure_source_declared_spin_proxy_gate_not_endpoint"
LAMBDA_REF = 0.10


def safe_div(num: pd.Series, den: pd.Series) -> pd.Series:
    return num / den.replace(0, np.nan)


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


def build_source_proxy(master: pd.DataFrame, galaxies: list[str]) -> pd.DataFrame:
    df = master.copy()
    df["galaxy"] = df["Galaxy"].astype(str)
    df = df[df["galaxy"].isin(galaxies)].copy()

    df["inclination_deg"] = pd.to_numeric(df["Inc_deg"], errors="coerce")
    df["rhi_over_rdisk"] = safe_div(
        pd.to_numeric(df["RHI_kpc"], errors="coerce"),
        pd.to_numeric(df["Rdisk_kpc"], errors="coerce"),
    )
    df["mhi_1e9_msun"] = pd.to_numeric(df["MHI_1e9Msun"], errors="coerce")
    df["vflat_km_s"] = pd.to_numeric(df["Vflat_kms"], errors="coerce")
    df["lum36_1e9_lsun"] = pd.to_numeric(df["L36_1e9Lsun"], errors="coerce")
    df["gas_to_l36"] = safe_div(df["mhi_1e9_msun"], df["lum36_1e9_lsun"])

    # Dimensionless source loads. These are deliberately bounded protocol
    # observables, not fitted amplitudes.
    df["extent_load"] = np.clip((df["rhi_over_rdisk"] - 4.0) / 8.0, 0.0, 1.0)
    df["velocity_load"] = np.clip((df["vflat_km_s"] - 160.0) / 160.0, 0.0, 1.0)
    df["gas_load"] = np.clip(np.log1p(df["mhi_1e9_msun"]) / np.log1p(35.0), 0.0, 1.0)
    df["edgeon_load"] = np.clip((df["inclination_deg"] - 75.0) / 15.0, 0.0, 1.0)

    df["spin_envelope_exposure_proxy"] = (
        0.35 * df["extent_load"]
        + 0.25 * df["velocity_load"]
        + 0.25 * df["gas_load"]
        + 0.15 * df["edgeon_load"]
    )
    df["lambda_spin_proxy_candidate"] = LAMBDA_REF * (
        1.0 + df["spin_envelope_exposure_proxy"]
    )

    return df[
        [
            "galaxy",
            "inclination_deg",
            "rhi_over_rdisk",
            "mhi_1e9_msun",
            "vflat_km_s",
            "gas_to_l36",
            "extent_load",
            "velocity_load",
            "gas_load",
            "edgeon_load",
            "spin_envelope_exposure_proxy",
            "lambda_spin_proxy_candidate",
        ]
    ].sort_values("spin_envelope_exposure_proxy", ascending=False)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    candidates = pd.read_csv(DATA / "ugc12506_beta_closure_transfer_candidates.csv")
    halo = pd.read_csv(DATA / "ugc12506_beta_closure_transfer_halo_fit_fields.csv")
    master = pd.read_csv(DATA / "external_sparc_master_table.csv")

    galaxies = ["UGC12506", *candidates["galaxy"].astype(str).tolist()]
    proxy = build_source_proxy(master, galaxies)
    proxy = proxy.merge(
        halo[["galaxy", "nfw_preference_load", "chi2_ISO_over_NFW"]],
        on="galaxy",
        how="left",
    )
    proxy["nfw_preference_load"] = proxy["nfw_preference_load"].fillna(np.nan)
    proxy["proxy_status"] = "SOURCE_PROXY_DECLARED_NOT_ACCEPTED_LAMBDA_SPIN"
    proxy["uses_vobs_or_residual"] = False
    proxy["endpoint_scores_allowed"] = False
    proxy["claim_boundary"] = CLAIM_BOUNDARY

    transfer = proxy[proxy["galaxy"].ne("UGC12506")].copy()
    transfer["transfer_proxy_priority"] = (
        transfer["spin_envelope_exposure_proxy"]
        * np.clip(transfer["nfw_preference_load"].fillna(0.0), 0.0, None)
    )
    transfer["transfer_proxy_class"] = np.where(
        transfer["transfer_proxy_priority"].ge(0.08),
        "PRIMARY_PROXY_TRANSFER_REVIEW_TARGET",
        np.where(
            transfer["transfer_proxy_priority"].gt(0.0),
            "SECONDARY_PROXY_TRANSFER_REVIEW_TARGET",
            "CONTROL_OR_ALTERNATIVE_BRANCH",
        ),
    )
    transfer = transfer.sort_values(
        ["transfer_proxy_priority", "spin_envelope_exposure_proxy"],
        ascending=[False, False],
    )
    transfer["proxy_rank"] = np.arange(1, len(transfer) + 1)

    proxy.to_csv(
        DATA / "ugc12506_beta_closure_source_declared_spin_proxy_fields.csv",
        index=False,
    )
    transfer.to_csv(
        DATA / "ugc12506_beta_closure_source_declared_spin_proxy_transfer_queue.csv",
        index=False,
    )

    primary = transfer[
        transfer["transfer_proxy_class"].eq("PRIMARY_PROXY_TRANSFER_REVIEW_TARGET")
    ]
    secondary = transfer[
        transfer["transfer_proxy_class"].eq("SECONDARY_PROXY_TRANSFER_REVIEW_TARGET")
    ]
    summary = pd.DataFrame(
        [
            {
                "spin_proxy_gate_status": (
                    "UGC12506_BETA_CLOSURE_SOURCE_DECLARED_SPIN_PROXY_BUILT_ENDPOINT_BLOCKED"
                ),
                "n_proxy_rows": int(len(proxy)),
                "n_transfer_rows": int(len(transfer)),
                "n_primary_proxy_review_targets": int(len(primary)),
                "n_secondary_proxy_review_targets": int(len(secondary)),
                "primary_targets": ";".join(primary["galaxy"].astype(str)),
                "secondary_targets": ";".join(secondary["galaxy"].astype(str).head(5)),
                "lambda_ref": LAMBDA_REF,
                "proxy_formula": (
                    "lambda_spin_proxy=lambda_ref*(1 + 0.35*extent_load + "
                    "0.25*velocity_load + 0.25*gas_load + 0.15*edgeon_load)"
                ),
                "proxy_promotion_status": "not_accepted_as_lambda_spin_measurement",
                "endpoint_scores_allowed": False,
                "next_gate": (
                    "independent_review_or_direct_spin_values_before_beta_cl_transfer_replay"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    summary.to_csv(
        DATA / "ugc12506_beta_closure_source_declared_spin_proxy_gate_summary.csv",
        index=False,
    )

    report = [
        "# UGC12506 Beta-Closure Source-Declared Spin Proxy Gate",
        "",
        "This gate declares a residual-blind spin/envelope exposure proxy for",
        "the beta-closure transfer route. It is a protocol candidate, not an",
        "accepted literature spin measurement and not an endpoint replay.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Proxy Definition",
        "",
        "All loads are dimensionless source observables from SPARC master-table",
        "fields. The protocol candidate is",
        "",
        "`lambda_spin_proxy = lambda_ref * (1 + 0.35 extent_load + 0.25 velocity_load + 0.25 gas_load + 0.15 edgeon_load)`,",
        "",
        f"with `lambda_ref = {LAMBDA_REF}`. The loads use only RHI/Rdisk, Vflat,",
        "H I mass, and inclination. No rotation residual, endpoint score,",
        "wrong-family rank, or best-fit Tau family enters the construction.",
        "",
        "## Transfer Queue",
        "",
        markdown_table(
            transfer[
                [
                    "proxy_rank",
                    "galaxy",
                    "spin_envelope_exposure_proxy",
                    "lambda_spin_proxy_candidate",
                    "nfw_preference_load",
                    "transfer_proxy_priority",
                    "transfer_proxy_class",
                ]
            ]
        ),
        "",
        "## Claim Boundary",
        "",
        "This gate reduces the blocker from an undefined spin slot to a declared",
        "source-only proxy candidate. It does not promote the proxy to an accepted",
        "lambda_spin measurement. Beta-closure replay and endpoint scoring remain",
        "blocked until an independent source review accepts this proxy rule or",
        "direct source-native spin values are acquired.",
    ]
    (REPORTS / "ugc12506_beta_closure_source_declared_spin_proxy_gate.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )

    print(summary.to_string(index=False))
    print(
        transfer[
            [
                "proxy_rank",
                "galaxy",
                "spin_envelope_exposure_proxy",
                "lambda_spin_proxy_candidate",
                "nfw_preference_load",
                "transfer_proxy_priority",
                "transfer_proxy_class",
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()
