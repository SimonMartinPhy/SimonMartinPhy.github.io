"""
Constantes de géométrie et paramètres faisceau partagés.

Importé par linac_phase1.py, linac_phase2.py et linac_analysis.py.
Aucune dépendance à opengate — utilisable sans installation Geant4.

Système d'unités Geant4 : base mm / MeV (mm = 1, MeV = 1).
"""
import pathlib

# ── Unités (système interne Geant4) ──────────────────────────────────────────
mm  = 1.0
cm  = 10.0
m   = 1000.0
MeV = 1.0
keV = 1e-3

# ── Paramètres faisceau ───────────────────────────────────────────────────────
BEAM_PARAMS = {
    "4":     {"E_mev":  4.0, "E_sigma": 0.0, "spot_sigma_mm": 0.0, "FFF": False},
    "6":     {"E_mev":  6.0, "E_sigma": 0.0, "spot_sigma_mm": 0.0, "FFF": False},
    "6fff":  {"E_mev":  6.0, "E_sigma": 0.0, "spot_sigma_mm": 0.0, "FFF": True},
    "10":    {"E_mev": 10.0, "E_sigma": 0.0, "spot_sigma_mm": 0.0, "FFF": False},
    "10fff": {"E_mev": 10.0, "E_sigma": 0.0, "spot_sigma_mm": 0.0, "FFF": True},
    "15":    {"E_mev": 15.0, "E_sigma": 0.0, "spot_sigma_mm": 0.0, "FFF": False},
    "18":    {"E_mev": 18.0, "E_sigma": 0.0, "spot_sigma_mm": 0.0, "FFF": False},
}

FIELD_SIZES_CM = [5.0, 10.0, 20.0, 30.0]
FIELD_SIZE_REF = 10.0 * cm

# ── Distances principales ─────────────────────────────────────────────────────
SAD_MM = 1000.0 * mm    # source–isocentre
SSD_MM = 1000.0 * mm    # source–surface fantôme

# ── Cible W ───────────────────────────────────────────────────────────────────
TARGET_Z_TOP     =  0.0 * mm
TARGET_THICKNESS =  1.0 * mm
TARGET_RADIUS    =  6.0 * mm

# ── Collimateur primaire (W creux conique) ────────────────────────────────────
PRIM_Z_TOP       =  5.0 * mm
PRIM_Z_BOT       = 50.0 * mm
PRIM_INNER_R_TOP =  4.5 * mm
PRIM_INNER_R_BOT = 22.0 * mm
PRIM_OUTER_R     = 80.0 * mm

# ── Cône égalisateur FF (W plein) ─────────────────────────────────────────────
FF_Z_TOP  = 54.0 * mm
FF_Z_BOT  = 80.0 * mm
FF_TIP_R  =  0.5 * mm
FF_BASE_R = 38.0 * mm

# ── Plan de phase space Phase 1 ───────────────────────────────────────────────
PHSP1_Z = 84.0 * mm
PHSP1_R = 150.0 * mm

# ── Chambre moniteur (air) ────────────────────────────────────────────────────
IC_Z_CENTER  = 115.0 * mm
IC_THICKNESS =   1.0 * mm
IC_R         = 100.0 * mm

# ── Mâchoires Y (supérieures, W) ─────────────────────────────────────────────
JAW_Y_Z_TOP = 260.0 * mm
JAW_Y_Z_BOT = 345.0 * mm
JAW_Y_W     = 100.0 * mm

# ── Mâchoires X (inférieures, W) ─────────────────────────────────────────────
JAW_X_Z_TOP = 350.0 * mm
JAW_X_Z_BOT = 420.0 * mm
JAW_X_W     = 100.0 * mm

# ── Fantôme d'eau ─────────────────────────────────────────────────────────────
PHANTOM_SURFACE_Z = SSD_MM
PHANTOM_DEPTH     = 300.0 * mm
PHANTOM_XY        = 400.0 * mm

# ── Monde Gate ────────────────────────────────────────────────────────────────
WORLD_Z_SIZE  = 1500.0 * mm
WORLD_XY_SIZE =  600.0 * mm
SOURCE_OFFSET = -680.0 * mm    # z_gate = SOURCE_OFFSET + z_abs


# ── Helpers géométriques ──────────────────────────────────────────────────────

def to_gate_z(z_abs_mm: float) -> float:
    """Coordonnée z Gate depuis la position absolue (cible = z = 0)."""
    return SOURCE_OFFSET + z_abs_mm


def phsp1_gate_z() -> float:
    return to_gate_z(PHSP1_Z)


def phantom_center_gate() -> list:
    return [0.0, 0.0, to_gate_z(PHANTOM_SURFACE_Z + PHANTOM_DEPTH / 2)]


def jaw_half_opening(z_center_abs_mm: float, field_size_mm: float) -> float:
    """Demi-ouverture de mâchoire pour obtenir field_size_mm à SAD."""
    return (field_size_mm / 2.0) * (z_center_abs_mm / SAD_MM)


def make_dirs(energy_key: str):
    """Crée et retourne (ph1_dir, ph2_dir) pour une énergie donnée."""
    base    = pathlib.Path("output_mc") / f"e{energy_key}"
    ph1_dir = base / "phase1"
    ph2_dir = base / "phase2"
    ph1_dir.mkdir(parents=True, exist_ok=True)
    ph2_dir.mkdir(parents=True, exist_ok=True)
    return ph1_dir, ph2_dir
