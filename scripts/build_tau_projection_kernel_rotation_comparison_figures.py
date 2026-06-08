#!/usr/bin/env python3
"""Build comparison rotation-curve figures for Tau projection kernel variants.

The figure compares, where available:

- simple Tau morphology kernel,
- observer/projection-enriched Tau kernel,
- morphology-history/observer-projection-enriched Tau kernel,
- Newtonian, TPG/v6, and MOND baselines.

An explicit RMOND curve is not present in the currently used point artifacts,
so the figure does not relabel any existing baseline as RMOND.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
FIGURES = ROOT / "figures" / "endpoint_diagnostics"
CLAIM_BOUNDARY = "tau_projection_kernel_rotation_comparison_not_population_validation"


def rmse(obs: np.ndarray, pred: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(pred - obs))))


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for column in display.columns:
        if pd.api.types.is_float_dtype(display[column]):
            display[column] = display[column].map(lambda value: f"{value:.6g}")
        else:
            display[column] = display[column].astype(str)
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[column]) for column in display.columns) + " |")
    return "\n".join(lines)


def prior_baselines(galaxy: str) -> pd.DataFrame:
    points = pd.read_csv(DATA / "multigalaxy_fit_inspection_points.csv")
    points = points.loc[points["galaxy"].eq(galaxy)].copy()
    piv = points.pivot_table(
        index="r_kpc",
        columns="model_id",
        values="vpred_kms",
        aggfunc="first",
    ).reset_index()
    obs = points.loc[points["model_id"].eq("NEWTONIAN_vn"), ["r_kpc", "vobs_kms"]].drop_duplicates()
    piv = piv.merge(obs, on="r_kpc", how="left")
    return piv.rename(
        columns={
            "r_kpc": "r",
            "vobs_kms": "vobs",
            "NEWTONIAN_vn": "Newtonian",
            "TPG_V6": "TPG/v6",
            "MOND": "MOND",
        }
    )


def maybe_merge(base: pd.DataFrame, other: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    keep = ["r"] + [c for c in columns if c in other.columns]
    return base.merge(other[keep], on="r", how="left")


def load_ugc12506() -> tuple[pd.DataFrame, dict[str, str]]:
    base = prior_baselines("UGC12506")
    env = pd.read_csv(DATA / "ugc12506_source_envelope_support_replay_points.csv").rename(
        columns={
            "radius_kpc": "r",
            "v_envelope_positive_prefrozen_kms": "Tau simple",
        }
    )
    eea = pd.read_csv(DATA / "ugc12506_edgeon_envelope_asymmetry_replay_points.csv").rename(
        columns={
            "radius_kpc": "r",
            "v_eea_positive_prefrozen_kms": "Tau observer projection",
        }
    )
    ph = pd.read_csv(DATA / "ugc12506_projection_history_incremental_replay_points.csv").rename(
        columns={
            "radius_kpc": "r",
            "v_projection_history_incremental_positive_kms": "Tau morph-observer projection",
            "v_source_native_nfw_hse_positive_kms": "Tau source-native NFW/HSE",
            "errv_kms": "errv",
        }
    )
    df = maybe_merge(base, env, ["Tau simple"])
    df = maybe_merge(df, eea, ["Tau observer projection"])
    df = maybe_merge(df, ph, ["Tau morph-observer projection", "Tau source-native NFW/HSE", "errv"])
    return df, {
        "simple": "source-envelope support",
        "observer": "edge-on/envelope/asymmetry projection",
        "morph_observer": "source-native NFW/HSE + incremental projection-history",
    }


def load_ngc5907() -> tuple[pd.DataFrame, dict[str, str]]:
    simple = pd.read_csv(DATA / "ngc5907_projection_accepted_endpoint_points.csv").rename(
        columns={
            "v_K_thick_flared": "Tau simple",
            "v_projection_accepted": "Tau observer projection",
        }
    )
    mixed = pd.read_csv(DATA / "ngc5907_expdisk_projection_mixed_accepted_endpoint_points.csv").rename(
        columns={"v_mixed_population": "Tau morph-observer projection"}
    )
    df = simple[["r", "vobs", "errv", "vn", "v_v6", "v_mond", "Tau simple", "Tau observer projection"]].rename(
        columns={"vn": "Newtonian", "v_v6": "TPG/v6", "v_mond": "MOND"}
    )
    df = maybe_merge(df, mixed, ["Tau morph-observer projection"])
    return df, {
        "simple": "thick/flared Tau proxy",
        "observer": "accepted projection endpoint",
        "morph_observer": "mixed exponential/projection readout",
    }


def load_ngc4013() -> tuple[pd.DataFrame, dict[str, str]]:
    wvo = pd.read_csv(DATA / "ngc4013_warp_vertical_overlay_endpoint_points.csv").rename(
        columns={
            "v_K_exponential_disk": "Tau simple",
            "v_wvo_endpoint": "Tau observer projection",
        }
    )
    mixed = pd.read_csv(DATA / "ngc4013_expdisk_wvo_frozen_protocol_points.csv").rename(
        columns={"v_expdisk_wvo_frozen": "Tau morph-observer projection"}
    )
    df = wvo[["r", "vobs", "errv", "vn", "v_v6", "v_mond", "Tau simple", "Tau observer projection"]].rename(
        columns={"vn": "Newtonian", "v_v6": "TPG/v6", "v_mond": "MOND"}
    )
    df = maybe_merge(df, mixed, ["Tau morph-observer projection"])
    return df, {
        "simple": "exponential-disk Tau proxy",
        "observer": "warp/vertical-overlay endpoint",
        "morph_observer": "expdisk + WVO frozen protocol",
    }


def load_ngc7331() -> tuple[pd.DataFrame, dict[str, str]]:
    v3 = pd.read_csv(DATA / "ngc7331_v2_v3_replay_holdout_endpoint_points.csv").rename(
        columns={
            "v_K_exponential_disk": "Tau simple",
            "v_v1_broad_window_accepted_reference": "Tau observer projection",
            "v_v3_source_sharpened_replay": "Tau morph-observer projection",
        }
    )
    df = v3[
        [
            "r",
            "vobs",
            "errv",
            "vn",
            "v_v6",
            "v_mond",
            "Tau simple",
            "Tau observer projection",
            "Tau morph-observer projection",
        ]
    ].rename(columns={"vn": "Newtonian", "v_v6": "TPG/v6", "v_mond": "MOND"})
    return df, {
        "simple": "exponential-disk Tau proxy",
        "observer": "broad outer-warp window",
        "morph_observer": "source-sharpened vertical/outer-warp replay",
    }


def load_ngc4088() -> tuple[pd.DataFrame, dict[str, str]]:
    pts = pd.read_csv(DATA / "ngc4088_warp_history_accepted_endpoint_points.csv").rename(
        columns={
            "v_K_thick_flared": "Tau simple",
            "v_warp_history_formula_freeze_km_s": "Tau morph-observer projection",
            "vn": "Newtonian",
            "v_v6": "TPG/v6",
            "v_mond": "MOND",
        }
    )
    df = pts[
        [
            "r",
            "vobs",
            "Newtonian",
            "TPG/v6",
            "MOND",
            "Tau simple",
            "Tau morph-observer projection",
        ]
    ].copy()
    df["errv"] = np.nan
    df["Tau observer projection"] = np.nan
    return df, {
        "simple": "thick/flared Tau proxy",
        "observer": "not separately frozen in this artifact",
        "morph_observer": "warp-history accepted endpoint",
    }


LOADERS = {
    "UGC12506": load_ugc12506,
    "NGC5907": load_ngc5907,
    "NGC4013": load_ngc4013,
    "NGC7331": load_ngc7331,
    "NGC4088": load_ngc4088,
}


STYLE = {
    "Newtonian": dict(color="#777777", lw=1.7, ls="-"),
    "TPG/v6": dict(color="#4c78a8", lw=1.7, ls="--"),
    "MOND": dict(color="#59a14f", lw=1.7, ls=":"),
    "Tau simple": dict(color="#f28e2b", lw=1.9, ls="-"),
    "Tau source-native NFW/HSE": dict(color="#b2182b", lw=1.5, ls="-."),
    "Tau observer projection": dict(color="#9c755f", lw=2.0, ls="-"),
    "Tau morph-observer projection": dict(color="#5e3c99", lw=2.5, ls="-"),
}


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    rows = []
    loaded = {}
    notes = {}
    for galaxy, loader in LOADERS.items():
        df, note = loader()
        df = df.sort_values("r").reset_index(drop=True)
        loaded[galaxy] = df
        notes[galaxy] = note
        obs = df["vobs"].to_numpy(dtype=float)
        for col in [
            "Newtonian",
            "TPG/v6",
            "MOND",
            "Tau simple",
            "Tau source-native NFW/HSE",
            "Tau observer projection",
            "Tau morph-observer projection",
        ]:
            if col in df.columns and df[col].notna().any():
                rows.append(
                    {
                        "galaxy": galaxy,
                        "curve": col,
                        "rmse_km_s": rmse(obs, df[col].to_numpy(dtype=float)),
                        "n_points": int(df[col].notna().sum()),
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )

    scores = pd.DataFrame(rows)
    scores.to_csv(DATA / "tau_projection_kernel_rotation_comparison_scores.csv", index=False)

    fig, axes = plt.subplots(3, 2, figsize=(15.2, 15.6), constrained_layout=False)
    axes = axes.flatten()
    for ax, (galaxy, df) in zip(axes, loaded.items()):
        err = df["errv"].to_numpy(dtype=float) if "errv" in df.columns else np.full(len(df), np.nan)
        if np.isfinite(err).any():
            ax.errorbar(df["r"], df["vobs"], yerr=err, fmt="o", ms=3.2, lw=0.6, color="black", label="observed")
        else:
            ax.plot(df["r"], df["vobs"], "o", ms=3.2, color="black", label="observed")
        for col in [
            "Newtonian",
            "TPG/v6",
            "MOND",
            "Tau simple",
            "Tau source-native NFW/HSE",
            "Tau observer projection",
            "Tau morph-observer projection",
        ]:
            if col in df.columns and df[col].notna().any():
                ax.plot(df["r"], df[col], label=col, **STYLE[col])
        ax.set_title(galaxy, pad=8)
        ax.set_xlabel("Radius [kpc]")
        ax.set_ylabel("Rotation speed [km/s]")
        ax.grid(True, alpha=0.25)
        ax.legend(frameon=False, fontsize=6.8, ncol=2, loc="best")
    axes[-1].axis("off")
    axes[-1].text(
        0.02,
        0.98,
        "\n".join(
            [
                "Notes",
                "- Explicit RMOND prediction curves are not present in these point artifacts.",
                "- UGC12506 PH curve is a caveated control replay, not endpoint validation.",
                "- NGC4013 protocol is retrospective/blocker-marked.",
                "- NGC4088 is a single-object caveated warp-history endpoint.",
                "- Curves are compared only where already frozen/scored artifacts exist.",
            ]
        ),
        va="top",
        ha="left",
        fontsize=10,
        wrap=True,
    )
    fig.suptitle(
        "Tau Core kernel comparison: simple, projection, morphology-history projection, and baselines",
        y=0.985,
        fontsize=14,
    )
    fig.tight_layout(rect=[0.0, 0.0, 1.0, 0.955], h_pad=2.0, w_pad=1.6)
    multi_path = FIGURES / "tau_projection_kernel_rotation_comparison_grid.png"
    fig.savefig(multi_path, dpi=190)
    plt.close(fig)

    for galaxy, df in loaded.items():
        fig, ax = plt.subplots(figsize=(8.8, 5.4))
        err = df["errv"].to_numpy(dtype=float) if "errv" in df.columns else np.full(len(df), np.nan)
        if np.isfinite(err).any():
            ax.errorbar(df["r"], df["vobs"], yerr=err, fmt="o", ms=4, lw=0.7, color="black", label="observed")
        else:
            ax.plot(df["r"], df["vobs"], "o", ms=4, color="black", label="observed")
        for col in [
            "Newtonian",
            "TPG/v6",
            "MOND",
            "Tau simple",
            "Tau source-native NFW/HSE",
            "Tau observer projection",
            "Tau morph-observer projection",
        ]:
            if col in df.columns and df[col].notna().any():
                ax.plot(df["r"], df[col], label=col, **STYLE[col])
        ax.set_title(f"{galaxy}: Tau projection-kernel comparison")
        ax.set_xlabel("Radius [kpc]")
        ax.set_ylabel("Rotation speed [km/s]")
        ax.grid(True, alpha=0.25)
        ax.legend(frameon=False, fontsize=8, ncol=2)
        fig.tight_layout()
        fig.savefig(FIGURES / f"{galaxy.lower()}_tau_projection_kernel_comparison.png", dpi=190)
        plt.close(fig)

    notes_df = pd.DataFrame(
        [
            {
                "galaxy": galaxy,
                "simple_tau_definition": note["simple"],
                "observer_projection_definition": note["observer"],
                "morph_observer_projection_definition": note["morph_observer"],
                "rmond_curve_status": "not_available_as_explicit_curve_in_current_artifacts",
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for galaxy, note in notes.items()
        ]
    )
    notes_df.to_csv(DATA / "tau_projection_kernel_rotation_comparison_notes.csv", index=False)

    report = [
        "# Tau Projection Kernel Rotation Comparison",
        "",
        "This report compares available simple Tau, observer/projection Tau,",
        "morphology-history observer/projection Tau, and baseline rotation curves.",
        "The current artifacts provide Newtonian, TPG/v6, and MOND curves. They do",
        "not provide a separate explicit RMOND curve, so no RMOND line is drawn.",
        "",
        "## Curve Definitions",
        "",
        markdown_table(notes_df),
        "",
        "## RMSE Scores",
        "",
        markdown_table(scores.sort_values(["galaxy", "rmse_km_s"])),
        "",
        f"![Tau projection kernel comparison grid]({multi_path})",
        "",
        "## Claim Boundary",
        "",
        "This is a visualization and already-existing artifact comparison. It is",
        "not a new population validation and does not promote caveated replays to",
        "accepted endpoints.",
        "",
    ]
    (REPORTS / "tau_projection_kernel_rotation_comparison.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print(scores.sort_values(["galaxy", "rmse_km_s"]).to_string(index=False))
    print(multi_path)


if __name__ == "__main__":
    main()
