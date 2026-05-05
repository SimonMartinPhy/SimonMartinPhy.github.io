"""
Analyse des résultats MC LINAC :
  - Extraction PDD et profils transversaux depuis le fichier .mhd
  - Fit des paramètres du modèle analytique WebLinac
  - Figures de comparaison MC vs analytique
  - Schéma 2D de la géométrie (option --vis, sans Geant4)

Prérequis : linac_phase2.py doit avoir produit les fichiers .mhd de dose.

Produit :
  output_mc/e{energy}/phase2/pdd_profiles_fs{N}cm.json
  output_mc/e{energy}/phase2/comparison_{energy}_fs{N}cm.png
  output_mc/e{energy}/phase2/fitted_params_{energy}MV.json

Utilisation :
  python linac_analysis.py --fs 10
  python linac_analysis.py --fs 5 10 20 30 --energy 6
  python linac_analysis.py --vis --fs 10 20 --energy 6fff

Dépendances : pip install itk scipy numpy matplotlib
"""

import argparse
import json
import pathlib

import numpy as np

from linac_config import (
    cm, mm,
    BEAM_PARAMS, SAD_MM, SSD_MM,
    TARGET_Z_TOP, TARGET_THICKNESS, TARGET_RADIUS,
    PRIM_Z_TOP, PRIM_Z_BOT, PRIM_INNER_R_TOP, PRIM_INNER_R_BOT, PRIM_OUTER_R,
    FF_Z_TOP, FF_Z_BOT, FF_TIP_R, FF_BASE_R,
    PHSP1_Z,
    IC_Z_CENTER, IC_THICKNESS, IC_R,
    JAW_Y_Z_TOP, JAW_Y_Z_BOT, JAW_Y_W,
    JAW_X_Z_TOP, JAW_X_Z_BOT, JAW_X_W,
    PHANTOM_SURFACE_Z, PHANTOM_DEPTH, PHANTOM_XY,
    jaw_half_opening, make_dirs,
)


# ═════════════════════════════════════════════════════════════════════════════
#  EXTRACTION PDD ET PROFILS
# ═════════════════════════════════════════════════════════════════════════════

def extract_pdd_profiles(dose_mhd_path: str,
                         field_size_cm: float,
                         ssd_cm: float = 100.0,
                         output_dir: pathlib.Path = None) -> dict:
    """
    Lit le volume de dose 3D (.mhd) et extrait le PDD + profils transversaux.

    Retourne un dict JSON-compatible avec :
      pdd        : depths_cm, dose_percent, dmax_cm
      profiles   : profils X et Y à dmax, 5, 10, 20 cm
    """
    try:
        import itk
    except ImportError:
        raise ImportError("itk est requis pour lire les .mhd : pip install itk")

    dose_img = itk.imread(dose_mhd_path)
    dose_arr = itk.array_view_from_image(dose_img)   # shape (nz, ny, nx)
    spacing  = dose_img.GetSpacing()
    origin   = dose_img.GetOrigin()

    nz, ny, nx = dose_arr.shape
    cx, cy     = nx // 2, ny // 2

    pdd_raw  = dose_arr[:, cy, cx].astype(float)
    pdd_max  = pdd_raw.max()
    pdd_norm = (pdd_raw / pdd_max * 100.0) if pdd_max > 0 else pdd_raw.copy()

    # origin[2] est en coordonnées locales du fantôme (centre = 0).
    # On ajoute PHANTOM_DEPTH/2 pour ramener le zéro à la surface d'entrée.
    depths_cm = [(origin[2] + PHANTOM_DEPTH / 2.0 + k * spacing[2]) / 10.0 for k in range(nz)]
    dmax_idx  = int(np.argmax(pdd_raw))
    dmax_cm   = depths_cm[dmax_idx]

    profiles = {}
    for d_cm in [dmax_cm, 5.0, 10.0, 20.0]:
        iz = int(round(d_cm * 10.0 / spacing[2]))
        if not (0 <= iz < nz):
            continue
        prof_x = dose_arr[iz, cy, :].astype(float)
        prof_y = dose_arr[iz, :, cx].astype(float)
        x_pos  = [(origin[0] + j * spacing[0]) / 10.0 for j in range(nx)]
        y_pos  = [(origin[1] + j * spacing[1]) / 10.0 for j in range(ny)]
        p0x = prof_x[cx] if prof_x[cx] > 0 else prof_x.max()
        p0y = prof_y[cy] if prof_y[cy] > 0 else prof_y.max()
        profiles[f"{d_cm:.1f}cm"] = {
            "x_cm":      x_pos,
            "profile_x": (prof_x / p0x).tolist() if p0x > 0 else prof_x.tolist(),
            "y_cm":      y_pos,
            "profile_y": (prof_y / p0y).tolist() if p0y > 0 else prof_y.tolist(),
        }

    result = {
        "field_size_cm": field_size_cm,
        "ssd_cm":        ssd_cm,
        "pdd": {
            "depths_cm":    depths_cm,
            "dose_percent": pdd_norm.tolist(),
            "dmax_cm":      dmax_cm,
        },
        "profiles": profiles,
    }

    if output_dir is not None:
        out = output_dir / f"pdd_profiles_fs{field_size_cm:.0f}cm.json"
        with open(out, "w") as f:
            json.dump(result, f, indent=2)
        print(f"  [PDD/Profils] → {out}")

    return result


# ═════════════════════════════════════════════════════════════════════════════
#  FIT DU MODÈLE ANALYTIQUE WEBLINAC
# ═════════════════════════════════════════════════════════════════════════════

def fit_analytical_params(mc_results: dict, energy_key: str = "6") -> dict:
    """
    Ajuste les paramètres du modèle analytique WebLinac aux données MC.

    Modèle PDD (d >= dmax) :
      100 × [(SSD+dmax)/(SSD+d)]² × exp(-mu×(d-dmax)) × scatter

    Modèle profil (FF) :
      0.5×[erf((a-x)/M) + erf((a+x)/M)] × (1 + horn×r²) + 0.018×(1-pen)
    """
    try:
        from scipy.optimize import curve_fit
        from scipy.special import erf as scipy_erf
    except ImportError:
        raise ImportError("scipy est requis : pip install scipy")

    ssd_cm = mc_results.get("ssd_cm", 100.0)
    sad_cm = 100.0
    fs_cm  = mc_results["field_size_cm"]
    is_fff = BEAM_PARAMS[energy_key]["FFF"]

    depths = np.array(mc_results["pdd"]["depths_cm"])
    dose   = np.array(mc_results["pdd"]["dose_percent"])
    dmax   = mc_results["pdd"]["dmax_cm"]

    ds_mc = (dose[0] / 100.0 if depths[0] < 0.3
             else np.interp(0.0, depths, dose) / 100.0)

    # Fit exponentiel du PDD (d >= dmax)
    mask  = depths >= dmax
    d_fit = depths[mask]
    p_fit = dose[mask]

    def pdd_model(d, mu):
        scatter = 1.0 + 1.5e-3 * (fs_cm - 10.0) * (d - dmax)
        isl     = ((ssd_cm + dmax) / (ssd_cm + d)) ** 2
        return 100.0 * isl * np.exp(-mu * (d - dmax)) * scatter

    try:
        popt, _ = curve_fit(pdd_model, d_fit, p_fit, p0=[0.033], bounds=([0.01], [0.10]))
        mu_fit  = float(popt[0])
    except Exception:
        mu_fit = 0.033

    # Fit du profil à dmax (pénombre + cornes)
    prof_key = f"{dmax:.1f}cm"
    if prof_key not in mc_results["profiles"]:
        keys     = list(mc_results["profiles"].keys())
        d_keys   = [float(k.replace("cm", "")) for k in keys]
        prof_key = keys[int(np.argmin(np.abs(np.array(d_keys) - dmax)))]

    prof  = mc_results["profiles"][prof_key]
    x_arr = np.array(prof["x_cm"])
    px    = np.array(prof["profile_x"])
    d_p   = float(prof_key.replace("cm", ""))
    a_cm  = (fs_cm / 2.0) * (ssd_cm + d_p) / sad_cm

    def profile_ff(x, sig0, horn):
        sig = sig0 + 0.012 * d_p + 0.004 * (fs_cm - 10.0)
        M   = np.sqrt(2.0) * sig
        pen = 0.5 * (scipy_erf((a_cm - x) / M) + scipy_erf((a_cm + x) / M))
        r   = np.abs(x) / a_cm if a_cm > 0 else np.zeros_like(x)
        return pen * np.where(r < 1.0, 1.0 + horn * r**2, 1.0) + 0.018 * (1.0 - pen)

    def profile_fff(x, sig0, sigma_fff):
        sig   = sig0 + 0.012 * d_p + 0.004 * (fs_cm - 10.0)
        M     = np.sqrt(2.0) * sig
        pen   = 0.5 * (scipy_erf((a_cm - x) / M) + scipy_erf((a_cm + x) / M))
        x_src = np.abs(x) * sad_cm / (ssd_cm + d_p)
        return pen / (1.0 + (x_src / sigma_fff)**2) + 0.018 * (1.0 - pen)

    try:
        if is_fff:
            popt, _ = curve_fit(profile_fff, x_arr, px, p0=[0.36, 13.0],
                                bounds=([0.10, 2.0], [1.0, 30.0]))
            sig0_fit, sigma_fff_fit, horn_fit = float(popt[0]), float(popt[1]), 0.0
        else:
            popt, _ = curve_fit(profile_ff, x_arr, px, p0=[0.35, 0.05],
                                bounds=([0.05, 0.0], [1.0, 0.5]))
            sig0_fit, horn_fit, sigma_fff_fit = float(popt[0]), float(popt[1]), None
    except Exception:
        sig0_fit, horn_fit = 0.35, 0.05
        sigma_fff_fit = 13.0 if is_fff else None

    fitted = {
        "energy":     energy_key,
        "field_size": fs_cm,
        "dmax":       round(dmax,     3),
        "mu":         round(mu_fit,   5),
        "Ds":         round(ds_mc,    4),
        "sig0":       round(sig0_fit, 4),
        "horn":       round(horn_fit, 4),
    }
    if sigma_fff_fit is not None:
        fitted["sigma_fff"] = round(sigma_fff_fit, 3)
    return fitted


# ═════════════════════════════════════════════════════════════════════════════
#  COMPARAISON MC vs MODÈLE ANALYTIQUE
# ═════════════════════════════════════════════════════════════════════════════

def compare_with_analytical(mc_results: dict, fitted_params: dict,
                             output_dir: pathlib.Path = None):
    """Génère les figures PDD + profils : MC (points) vs analytique (tirets)."""
    try:
        import matplotlib.pyplot as plt
        from scipy.special import erf as scipy_erf
    except ImportError:
        print("  [Comparaison] matplotlib ou scipy absent.")
        return

    p      = fitted_params
    fs     = p["field_size"]
    ssd    = mc_results.get("ssd_cm", 100.0)
    sad    = 100.0
    dmax   = p["dmax"]
    mu     = p["mu"]
    Ds     = p["Ds"]
    sig0   = p["sig0"]
    horn   = p["horn"]
    s_fff  = p.get("sigma_fff")
    is_fff = BEAM_PARAMS.get(p["energy"], {}).get("FFF", False)

    def pdd_anal(d):
        if d <= 0:
            return Ds * 100.0
        if d < dmax:
            t = d / dmax
            return 100.0 * (Ds + (1.0 - Ds) * (3*t*t - 2*t*t*t))
        return (100.0 * ((ssd + dmax) / (ssd + d))**2
                * np.exp(-mu * (d - dmax))
                * (1.0 + 1.5e-3 * (fs - 10.0) * (d - dmax)))

    def prof_anal(x, d_cm):
        a   = (fs / 2.0) * (ssd + d_cm) / sad
        sig = sig0 + 0.012 * d_cm + 0.004 * (fs - 10.0)
        M   = np.sqrt(2.0) * sig
        pen = 0.5 * (scipy_erf((a - x) / M) + scipy_erf((a + x) / M))
        if is_fff and s_fff:
            horns = 1.0 / (1.0 + (np.abs(x) * sad / (ssd + d_cm) / s_fff)**2)
        else:
            r     = np.abs(x) / a if a > 0 else np.zeros_like(x)
            horns = np.where(r < 1.0, 1.0 + horn * r**2, 1.0)
        return pen * horns + 0.018 * (1.0 - pen)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f"MC vs Modèle analytique — {p['energy']} MV — FS = {fs:.0f}×{fs:.0f} cm")

    ax = axes[0]
    d_mc = np.array(mc_results["pdd"]["depths_cm"])
    p_mc = np.array(mc_results["pdd"]["dose_percent"])
    d_an = np.linspace(0.0, 30.0, 300)
    ax.plot(d_mc, p_mc, "o-", ms=3, label="Monte Carlo", color="#38bdf8")
    ax.plot(d_an, [pdd_anal(d) for d in d_an], "--", label="Analytique", color="#fb923c")
    ax.axvline(dmax, ls=":", color="yellow", lw=1, label=f"dmax = {dmax:.2f} cm")
    ax.set_xlabel("Profondeur (cm)")
    ax.set_ylabel("PDD (%)")
    ax.set_title("Rendement en profondeur")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    ax = axes[1]
    colors = ["#38bdf8", "#4ade80", "#fb923c", "#e879f9"]
    for i, (key, prof) in enumerate(mc_results["profiles"].items()):
        col  = colors[i % len(colors)]
        d_cm = float(key.replace("cm", ""))
        x_mc = np.array(prof["x_cm"])
        x_an = np.linspace(-20.0, 20.0, 400)
        ax.plot(x_mc, np.array(prof["profile_x"]), "o", ms=2, color=col, alpha=0.7)
        ax.plot(x_an, prof_anal(x_an, d_cm), "--", color=col, label=f"d = {d_cm:.1f} cm")
    ax.set_xlabel("Position latérale (cm)")
    ax.set_ylabel("Dose normalisée")
    ax.set_title("Profils transversaux (MC : points, Analytique : tirets)")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    if output_dir:
        fig_path = output_dir / f"comparison_{p['energy']}_fs{fs:.0f}cm.png"
        plt.savefig(fig_path, dpi=150, bbox_inches="tight")
        print(f"  [Comparaison] Figure → {fig_path}")
    plt.close(fig)


# ═════════════════════════════════════════════════════════════════════════════
#  SCHÉMA 2D DE LA GÉOMÉTRIE (matplotlib — sans Geant4)
# ═════════════════════════════════════════════════════════════════════════════

def draw_geometry(energy_key: str = "6",
                  field_size_cm: float = 10.0,
                  output_dir: pathlib.Path = None):
    """
    Génère un schéma 2D (coupe r-z) de la géométrie LINAC.

    Ne requiert pas Geant4. Produit un PNG avec :
      - Panel gauche : tête LINAC (z = 0 … 450 mm)
      - Panel droit  : vue d'ensemble jusqu'au fantôme d'eau
    """
    try:
        import matplotlib.pyplot as plt
        from matplotlib.patches import Polygon, Rectangle
    except ImportError:
        print("  [Géométrie] matplotlib absent.")
        return

    bp    = BEAM_PARAMS[energy_key]
    fs_mm = field_size_cm * 10.0

    _EDGE = dict(ec="#374151", lw=0.5)

    def _rect(ax, z1, z2, r1, r2, label=None, **kw):
        kw = {**_EDGE, **kw}
        ax.add_patch(Rectangle((z1, r1),  z2 - z1, r2 - r1, label=label, **kw))
        ax.add_patch(Rectangle((z1, -r2), z2 - z1, r2 - r1, **kw))

    def _trap(ax, z1, z2, ri1, ri2, ro1, ro2, label=None, **kw):
        kw = {**_EDGE, **kw}
        pts_p = np.array([[z1, ri1], [z2, ri2], [z2, ro2], [z1, ro1]])
        pts_n = pts_p.copy(); pts_n[:, 1] = -pts_n[:, 1]
        ax.add_patch(Polygon(pts_p, label=label, **kw))
        ax.add_patch(Polygon(pts_n, **kw))

    def _cone(ax, z1, z2, r_tip, r_base, label=None, **kw):
        kw = {**_EDGE, **kw}
        pts_p = np.array([[z1, r_tip], [z2, r_base], [z2, 0.0], [z1, 0.0]])
        pts_n = pts_p.copy(); pts_n[:, 1] = -pts_n[:, 1]
        ax.add_patch(Polygon(pts_p, label=label, **kw))
        ax.add_patch(Polygon(pts_n, **kw))

    def _jaw(ax, z1, z2, r_near, thick, label=None, **kw):
        kw = {**_EDGE, **kw}
        ax.add_patch(Rectangle((z1,  r_near),           z2 - z1, thick, label=label, **kw))
        ax.add_patch(Rectangle((z1, -(r_near + thick)), z2 - z1, thick, **kw))

    CW  = "#6b7280"
    CA  = "#7dd3fc"
    CW2 = "#4b5563"
    CWA = "#2563eb"
    CPH = "#f59e0b"
    CFD = "#fbbf24"
    CIS = "#a78bfa"

    jaw_y_z = (JAW_Y_Z_TOP + JAW_Y_Z_BOT) / 2.0
    jaw_x_z = (JAW_X_Z_TOP + JAW_X_Z_BOT) / 2.0
    jaw_y_h = jaw_half_opening(jaw_y_z, fs_mm)
    jaw_x_h = jaw_half_opening(jaw_x_z, fs_mm)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7),
                                   gridspec_kw={"width_ratios": [2, 3]})
    fig.patch.set_facecolor("#111827")
    fig.suptitle(
        f"Géométrie LINAC — {energy_key} MV {'[FFF]' if bp['FFF'] else '[FF]'} — "
        f"FS = {field_size_cm:.0f}×{field_size_cm:.0f} cm",
        fontsize=13, color="#f9fafb",
    )

    for ax in (ax1, ax2):
        ax.set_facecolor("#1f2937")
        ax.tick_params(colors="#d1d5db")
        ax.xaxis.label.set_color("#d1d5db")
        ax.yaxis.label.set_color("#d1d5db")
        ax.title.set_color("#f9fafb")
        for sp in ax.spines.values():
            sp.set_edgecolor("#374151")
        ax.grid(True, alpha=0.15, color="#9ca3af")
        ax.axhline(0, color="#9ca3af", lw=0.5, ls=":")

    # ── Panel gauche : tête LINAC ─────────────────────────────────────────────
    _rect(ax1, TARGET_Z_TOP, TARGET_Z_TOP + TARGET_THICKNESS,
          0, TARGET_RADIUS, label="Cible W", color=CW, alpha=0.95)
    ro_clip = min(PRIM_OUTER_R, 95.0)
    _trap(ax1, PRIM_Z_TOP, PRIM_Z_BOT,
          PRIM_INNER_R_TOP, PRIM_INNER_R_BOT, ro_clip, ro_clip,
          label="Collimateur primaire", color=CW, alpha=0.85)
    if not bp["FFF"]:
        _cone(ax1, FF_Z_TOP, FF_Z_BOT, FF_TIP_R, FF_BASE_R,
              label="Cône égalisateur", color=CW, alpha=0.90)
    ax1.axvline(PHSP1_Z, color=CPH, ls="--", lw=1.5, label=f"PhSp1  z = {PHSP1_Z:.0f} mm")
    _rect(ax1, IC_Z_CENTER - IC_THICKNESS / 2, IC_Z_CENTER + IC_THICKNESS / 2,
          0, IC_R, label="Chambre moniteur", color=CA, alpha=0.55)
    _jaw(ax1, JAW_Y_Z_TOP, JAW_Y_Z_BOT, jaw_y_h, JAW_Y_W,
         label="Mâchoires Y", color=CW, alpha=0.85)
    _jaw(ax1, JAW_X_Z_TOP, JAW_X_Z_BOT, jaw_x_h, JAW_X_W,
         label="Mâchoires X", color=CW2, alpha=0.85)
    ax1.annotate(f"Ouverture\n±{jaw_x_h:.1f} mm",
                 xy=(jaw_x_z, jaw_x_h), xytext=(380, 70),
                 color="#f9fafb", fontsize=7,
                 arrowprops=dict(arrowstyle="->", color="#f9fafb", lw=0.7))
    ax1.set_xlim(-5, 450)
    ax1.set_ylim(-105, 105)
    ax1.set_xlabel("z (mm) depuis la cible")
    ax1.set_ylabel("r (mm)")
    ax1.set_title("Tête LINAC")
    ax1.legend(fontsize=7, loc="upper right", framealpha=0.3,
               labelcolor="#f9fafb", facecolor="#374151", edgecolor="#374151")

    # ── Panel droit : vue d'ensemble ──────────────────────────────────────────
    _jaw(ax2, JAW_Y_Z_TOP, JAW_Y_Z_BOT, jaw_y_h, JAW_Y_W, label="Mâchoires Y",
         color=CW, alpha=0.85)
    _jaw(ax2, JAW_X_Z_TOP, JAW_X_Z_BOT, jaw_x_h, JAW_X_W, label="Mâchoires X",
         color=CW2, alpha=0.85)
    z_fe = np.array([JAW_X_Z_BOT, SAD_MM, PHANTOM_SURFACE_Z + PHANTOM_DEPTH])
    for sgn in (+1, -1):
        r_fe = np.array([sgn * jaw_x_h, sgn * fs_mm / 2.0,
                         sgn * (fs_mm / 2.0) * z_fe[2] / SAD_MM])
        ax2.plot(z_fe, r_fe, color=CFD, ls="--", lw=0.9, alpha=0.7,
                 label="Bord du champ" if sgn == 1 else None)
    ax2.axvline(PHANTOM_SURFACE_Z - 2, color="#22d3ee", ls=":", lw=1.2,
                label=f"PhSp2  z = {PHANTOM_SURFACE_Z - 2:.0f} mm")
    ax2.axvline(SAD_MM, color=CIS, ls="-.", lw=1.0, label=f"SAD  z = {SAD_MM:.0f} mm")
    ax2.scatter([SAD_MM], [0], color=CIS, s=40, zorder=5)
    _rect(ax2, PHANTOM_SURFACE_Z, PHANTOM_SURFACE_Z + PHANTOM_DEPTH,
          0, PHANTOM_XY / 2, label="Fantôme d'eau", color=CWA, alpha=0.30)
    ax2.annotate(f"FS@SAD\n±{fs_mm / 2:.0f} mm",
                 xy=(SAD_MM, fs_mm / 2), xytext=(SAD_MM + 40, fs_mm / 2 + 30),
                 color="#f9fafb", fontsize=7,
                 arrowprops=dict(arrowstyle="->", color="#f9fafb", lw=0.7))
    ax2.set_xlim(250, PHANTOM_SURFACE_Z + PHANTOM_DEPTH + 30)
    ax2.set_ylim(-215, 215)
    ax2.set_xlabel("z (mm) depuis la cible")
    ax2.set_ylabel("r (mm)")
    ax2.set_title(f"Vue d'ensemble — SSD = {SSD_MM:.0f} mm")
    ax2.legend(fontsize=7, loc="upper right", framealpha=0.3,
               labelcolor="#f9fafb", facecolor="#374151", edgecolor="#374151")

    plt.tight_layout()

    if output_dir is None:
        output_dir = pathlib.Path(".")
    out = pathlib.Path(output_dir) / f"geometry_{energy_key}_fs{field_size_cm:.0f}cm.png"
    plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    print(f"  [Géométrie] Schéma → {out}")
    plt.close(fig)


# ═════════════════════════════════════════════════════════════════════════════
#  UTILITAIRE : recherche du fichier dose
# ═════════════════════════════════════════════════════════════════════════════

def _find_dose_file(ph2_dir: pathlib.Path, field_size_cm: float) -> pathlib.Path | None:
    """Recherche le .mhd de dose (suffixe variable selon version Gate)."""
    base = f"dose_fs{field_size_cm:.0f}cm"
    for suffix in ["", "_dose", "-dose"]:
        p = ph2_dir / f"{base}{suffix}.mhd"
        if p.exists():
            return p
    return None


# ═════════════════════════════════════════════════════════════════════════════
#  POINT D'ENTRÉE
# ═════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Analyse MC LINAC : PDD, profils, fit WebLinac, figures",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=(
            "Exemples :\n"
            "  python linac_analysis.py --fs 10\n"
            "  python linac_analysis.py --fs 5 10 20 30 --energy 6\n"
            "  python linac_analysis.py --vis --fs 10 20 --energy 6fff\n"
        ),
    )
    parser.add_argument(
        "--energy", type=str, default="6",
        choices=list(BEAM_PARAMS.keys()),
        help="Énergie nominale (MV) — défaut : 6",
    )
    parser.add_argument(
        "--fs", type=float, nargs="+", default=[10.0],
        metavar="FIELD_CM",
        help="Taille(s) de champ en cm — défaut : 10",
    )
    parser.add_argument(
        "--vis", action="store_true",
        help="Génère le schéma 2D de la géométrie (sans lire les fichiers dose)",
    )
    args = parser.parse_args()

    _, ph2_dir = make_dirs(args.energy)

    # ── Mode visualisation géométrie ──────────────────────────────────────────
    if args.vis:
        print("\n" + "═" * 65)
        print(f"  VISUALISATION GÉOMÉTRIE — {args.energy} MV")
        print("═" * 65)
        for fs_cm in args.fs:
            draw_geometry(args.energy, fs_cm, output_dir=ph2_dir.parent)
        print()
        return

    # ── Analyse des fichiers dose ─────────────────────────────────────────────
    print("\n" + "═" * 65)
    print(f"  ANALYSE — {args.energy} MV  |  FS = {args.fs} cm")
    print("═" * 65)

    all_fitted = []

    for fs_cm in args.fs:
        dose_file = _find_dose_file(ph2_dir, fs_cm)
        if dose_file is None:
            print(f"\n  [AVERTISSEMENT] Aucun fichier dose pour FS={fs_cm:.0f} cm dans {ph2_dir}")
            print( "  Vérifiez que linac_phase2.py a été lancé avec cette taille de champ.")
            continue

        print(f"\n  FS = {fs_cm:.0f}×{fs_cm:.0f} cm — fichier : {dose_file.name}")
        print("  Extraction PDD et profils…")
        mc_data = extract_pdd_profiles(
            dose_mhd_path = str(dose_file),
            field_size_cm = fs_cm,
            ssd_cm        = SSD_MM / cm,
            output_dir    = ph2_dir,
        )

        print("  Fit du modèle analytique…")
        fitted = fit_analytical_params(mc_data, energy_key=args.energy)
        all_fitted.append(fitted)

        print(f"\n  ┌─ Paramètres fittés ({args.energy} MV, FS={fs_cm:.0f} cm) ─────────")
        print(f"  │  dmax  = {fitted['dmax']:.3f} cm")
        print(f"  │  mu    = {fitted['mu']:.5f} cm⁻¹")
        print(f"  │  Ds    = {fitted['Ds']:.4f}")
        print(f"  │  sig0  = {fitted['sig0']:.4f} cm")
        print(f"  │  horn  = {fitted['horn']:.4f}" +
              (f"   sigma_fff = {fitted['sigma_fff']:.3f} cm"
               if "sigma_fff" in fitted else ""))
        print(f"  └───────────────────────────────────────────────────")

        compare_with_analytical(mc_data, fitted, output_dir=ph2_dir)

    if all_fitted:
        fit_path = ph2_dir / f"fitted_params_{args.energy}MV.json"
        with open(fit_path, "w") as f:
            json.dump(all_fitted, f, indent=2)
        print(f"\n  [Résultats] → {fit_path}")
        print("  Ces paramètres peuvent être copiés dans le dict BEAM de index.html.")

    print("\n  Analyse terminée.\n")


if __name__ == "__main__":
    main()
