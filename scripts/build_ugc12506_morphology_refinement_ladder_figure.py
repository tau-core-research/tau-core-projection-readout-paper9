#!/usr/bin/env python3
"""Build the UGC12506 source-side morphology refinement ladder figure.

This figure is descriptive, not an endpoint promotion.  It uses existing
frozen/control replay artifacts and displays the sequence of increasingly
source-specific readout channels for the UGC12506 stress case.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
FIGURES = ROOT / "figures" / "endpoint_diagnostics" / "ugc12506_morphology_refinement"
PAPER_FIGURES = ROOT / "papers" / "paper2_projection_enriched" / "source" / "figures"


def rmse(obs: pd.Series, pred: pd.Series) -> float:
    return float(((obs - pred) ** 2).mean() ** 0.5)


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    PAPER_FIGURES.mkdir(parents=True, exist_ok=True)

    ladder = pd.read_csv(DATA / "ugc12506_theta_xit_combined_control_replay_points.csv")
    beta = pd.read_csv(DATA / "ugc12506_source_derived_beta_closure_replay_points.csv")

    df = ladder[
        [
            "radius_kpc",
            "vobs_kms",
            "errv_kms",
            "v_baryon_050_kms",
            "v_envelope_positive_prefrozen_kms",
            "v_source_native_nfw_hse_positive_kms",
            "v_projection_history_incremental_positive_kms",
            "v_theta_morph_phase_positive_kms",
            "v_theta_xit_cap_only_control_kms",
        ]
    ].merge(
        beta[["radius_kpc", "v_source_derived_beta_closure_kms"]],
        on="radius_kpc",
        how="left",
    )

    sequence = [
        (
            "BARYONIC_050_CARRIER",
            "baryonic carrier",
            "v_baryon_050_kms",
            "#737373",
            "-",
            "baseline/control carrier",
        ),
        (
            "SOURCE_ENVELOPE_SUPPORT",
            "source envelope",
            "v_envelope_positive_prefrozen_kms",
            "#cc6677",
            "-",
            "source-frozen envelope branch",
        ),
        (
            "SOURCE_NATIVE_NFW_HSE",
            "source-native NFW/HSE",
            "v_source_native_nfw_hse_positive_kms",
            "#aa4499",
            "-",
            "source-native mass/envelope closure",
        ),
        (
            "PROJECTION_HISTORY",
            "projection/history",
            "v_projection_history_incremental_positive_kms",
            "#4477aa",
            "-",
            "observer/projection-history increment",
        ),
        (
            "THETA_MORPH_PHASE",
            r"$\Theta_{\rm morph}$",
            "v_theta_morph_phase_positive_kms",
            "#228833",
            "-",
            "Tau morphology-state phase diagnostic",
        ),
        (
            "THETA_XIT_CAP_CONTROL",
            r"$\Theta_{\rm morph}+\Xi_t$ cap",
            "v_theta_xit_cap_only_control_kms",
            "#ddaa33",
            "-",
            "ledger-strict combined control",
        ),
        (
            "SOURCE_BETA_CLOSURE_CANDIDATE",
            r"source $\beta_{\rm cl}$ closure",
            "v_source_derived_beta_closure_kms",
            "#332288",
            "--",
            "post-diagnostic source-candidate, not endpoint",
        ),
    ]

    rows = []
    for idx, (model_id, label, col, _color, _ls, status) in enumerate(sequence, start=1):
        rows.append(
            {
                "step": idx,
                "model_id": model_id,
                "plot_label": label,
                "rmse_km_s": rmse(df["vobs_kms"], df[col]),
                "status": status,
                "uses_vobs_for_model_construction": False if model_id != "SOURCE_BETA_CLOSURE_CANDIDATE" else False,
                "endpoint_validation_claim": False,
            }
        )
    summary = pd.DataFrame(rows)
    summary.to_csv(DATA / "ugc12506_morphology_refinement_ladder_summary.csv", index=False)

    out_points = df.copy()
    out_points.to_csv(DATA / "ugc12506_morphology_refinement_ladder_points.csv", index=False)

    fig, (ax, axr) = plt.subplots(
        2,
        1,
        figsize=(10.5, 8.2),
        sharex=True,
        gridspec_kw={"height_ratios": [3.1, 1.35], "hspace": 0.08},
    )

    ax.errorbar(
        df["radius_kpc"],
        df["vobs_kms"],
        yerr=df["errv_kms"],
        fmt="o",
        ms=4.5,
        color="black",
        ecolor="#999999",
        elinewidth=0.9,
        capsize=2,
        label="SPARC observed",
        zorder=5,
    )

    for model_id, label, col, color, ls, _status in sequence:
        lw = 2.8 if model_id in {"THETA_XIT_CAP_CONTROL", "SOURCE_BETA_CLOSURE_CANDIDATE"} else 1.9
        alpha = 0.96 if model_id in {"THETA_XIT_CAP_CONTROL", "SOURCE_BETA_CLOSURE_CANDIDATE"} else 0.78
        ax.plot(df["radius_kpc"], df[col], color=color, lw=lw, ls=ls, alpha=alpha, label=label)
        axr.plot(df["radius_kpc"], df["vobs_kms"] - df[col], color=color, lw=lw, ls=ls, alpha=alpha)

    ax.set_title("UGC12506 source-side morphology refinement ladder")
    ax.set_ylabel(r"$v_{\rm rot}$ [km s$^{-1}$]")
    ax.grid(True, alpha=0.22)
    ax.legend(loc="lower right", fontsize=8.2, ncol=2, frameon=True)

    axr.axhline(0.0, color="black", lw=0.8, alpha=0.7)
    axr.set_xlabel("Radius [kpc]")
    axr.set_ylabel(r"$v_{\rm obs}-v_{\rm model}$")
    axr.grid(True, alpha=0.22)

    note = (
        "Ladder uses pre-existing source/control artifacts. "
        r"$\beta_{\rm cl}$ is post-diagnostic candidate, not endpoint validation."
    )
    fig.text(0.01, 0.012, note, fontsize=8.5, color="#444444")

    out = FIGURES / "ugc12506_morphology_refinement_ladder.png"
    fig.savefig(out, dpi=220, bbox_inches="tight")
    paper_out = PAPER_FIGURES / "fig31_ugc12506_morphology_refinement_ladder.png"
    fig.savefig(paper_out, dpi=220, bbox_inches="tight")
    plt.close(fig)

    print(f"wrote {out}")
    print(f"wrote {paper_out}")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
