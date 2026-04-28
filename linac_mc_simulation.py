"""
Simulation Monte Carlo LINAC clinique — photons 6 MV (extensible à d'autres énergies)
Moteur : OpenGATE v10 (opengate Python API / Geant4)

Deux phases :
  Phase 1 : Faisceau d'électrons → Cible W → Collimateur primaire → Cône égalisateur
            → Phase space enregistré juste sous le cône égalisateur (~8.4 cm de la source)

  Phase 2 : Lecture du phase space → Chambre moniteur → Mâchoires (jaws) → Air → Fantôme d'eau
            → DoseActor 3D (PDD + profils) pour fitter les paramètres du modèle analytique WebLinac

Géométrie de référence : LINAC Varian TrueBeam 6 MV (cotes approximatives issues de la littérature)
  - SAD (source–isocentre)         : 100 cm
  - Énergie électrons incidents    : 6.0 MeV (Gaussienne σ = 0.20 MeV)
  - Spot source (σ)                : 0.5 mm

Paramètres du modèle analytique (WebLinac / index.html) visés par le fit :
  dmax  : profondeur de dose max (FS=10×10, SSD=100 cm)   → cm
  mu    : coefficient d'atténuation effectif               → cm⁻¹
  Ds    : dose de surface (fraction de Dmax)               → sans unité
  dFS   : variation de dmax par cm de FS                   → cm/cm (faisceaux FF seulement)
  sFS   : variation de Ds par cm de FS                     → sans unité/cm
  sig0  : sigma de pénombre à d=0, FS=10 (cm)
  horn  : coefficient de cornes (FF) — 0 pour FFF
  sigma_fff : demi-largeur Lorentzienne FFF au plan source (cm)

Utilisation :
  python linac_mc_simulation.py --phase 1          # Phase 1 seulement
  python linac_mc_simulation.py --phase 2          # Phase 2 (nécessite le phsp de la phase 1)
  python linac_mc_simulation.py --phase 3          # Phase 1 + Phase 2 + post-traitement + fit
  python linac_mc_simulation.py --phase 3 --energy 10   # 10 MV
  python linac_mc_simulation.py --phase 3 --nthreads 8 --nprimary 5000000

Dépendances :
  pip install opengate itk scipy numpy matplotlib

Auteur : Simulation générée pour WebLinac — Centre Oscar Lambret
"""

import argparse
import json
import pathlib

import numpy as np

# ─────────────────────────────────────────────────────────────────────────────
#  VÉRIFICATION DE L'IMPORT opengate
# ─────────────────────────────────────────────────────────────────────────────
try:
    import opengate as gate
    from opengate.geometry.volumes import unite_volumes  # Gate v10.1+
except ImportError as e:
    raise ImportError(
        "opengate n'est pas installé. Exécutez : pip install opengate\n"
        f"Détail : {e}"
    )

# Unités Geant4 exposées par opengate
mm  = gate.g4_units.mm
cm  = gate.g4_units.cm
m   = gate.g4_units.m
MeV = gate.g4_units.MeV
keV = gate.g4_units.keV
deg = gate.g4_units.deg
Bq  = gate.g4_units.Bq


# ═════════════════════════════════════════════════════════════════════════════
#  PARAMÈTRES GLOBAUX
# ═════════════════════════════════════════════════════════════════════════════

SAD_MM  = 1000.0 * mm   # Distance source–isocentre (100 cm)
SSD_MM  = 1000.0 * mm   # Distance source–surface fantôme (100 cm, isocentre sur surface)

# ── Paramètres faisceau initiaux (6 MV, fittables) ──────────────────────────
# Ces valeurs sont les points de départ ; la MC les ajuste pour les restituer
# aux paramètres analytiques de WebLinac.
BEAM_PARAMS = {
    "4":    {"E_mev": 4.0,  "E_sigma": 0.15, "spot_sigma_mm": 0.45, "FFF": False},
    "6":    {"E_mev": 6.0,  "E_sigma": 0.20, "spot_sigma_mm": 0.50, "FFF": False},
    "6fff": {"E_mev": 6.0,  "E_sigma": 0.20, "spot_sigma_mm": 0.70, "FFF": True},
    "10":   {"E_mev": 10.0, "E_sigma": 0.25, "spot_sigma_mm": 0.55, "FFF": False},
    "10fff":{"E_mev": 10.0, "E_sigma": 0.25, "spot_sigma_mm": 0.75, "FFF": True},
    "15":   {"E_mev": 15.0, "E_sigma": 0.35, "spot_sigma_mm": 0.60, "FFF": False},
    "18":   {"E_mev": 18.0, "E_sigma": 0.40, "spot_sigma_mm": 0.65, "FFF": False},
}

# ── Taille de champ de référence ─────────────────────────────────────────────
FIELD_SIZES_CM = [5.0, 10.0, 20.0, 30.0]   # cm à SAD, pour la dépendance en FS
FIELD_SIZE_REF = 10.0 * cm                  # champ de référence TRS 398

# ─────────────────────────────────────────────────────────────────────────────
#  GÉOMÉTRIE LINAC (cotes approximatives Varian TrueBeam 6 MV)
#  Référentiel : z = 0 à la cible (focal spot), +z vers le patient.
#  Les positions ci-dessous sont en mm depuis la cible.
# ─────────────────────────────────────────────────────────────────────────────

# Cible (Target W/Re)
TARGET_Z_TOP    =  0.0 * mm
TARGET_THICKNESS =  1.0 * mm   # 0.6 mm W + 0.4 mm Cu backing (simplifié en W pur)
TARGET_RADIUS   =  6.0 * mm

# Collimateur primaire (W — cône creux)
PRIM_Z_TOP          =  5.0 * mm
PRIM_Z_BOT          = 50.0 * mm
PRIM_INNER_R_TOP    =  4.5 * mm   # ouverture conique étroite côté source
PRIM_INNER_R_BOT    = 22.0 * mm   # ouverture conique large côté patient
PRIM_OUTER_R        = 80.0 * mm   # rayon externe du collimateur

# Cône égalisateur / Flattening Filter (W — cône plein)
FF_Z_TOP    = 54.0 * mm    # pointe vers la source
FF_Z_BOT    = 80.0 * mm    # base vers le patient
FF_TIP_R    =  0.5 * mm    # rayon de la pointe (quasi-nulle)
FF_BASE_R   = 38.0 * mm    # rayon de la base

# Plan du phase space Phase 1 (juste sous le cône égalisateur)
PHSP1_Z     = 84.0 * mm
PHSP1_R     = 150.0 * mm

# Chambre moniteur (ionisation, air — mylar négligé)
IC_Z_CENTER = 115.0 * mm
IC_THICKNESS =  1.0 * mm
IC_R        = 100.0 * mm

# Mâchoires Y (supérieures, tungstène)
JAW_Y_Z_TOP  = 260.0 * mm
JAW_Y_Z_BOT  = 345.0 * mm
JAW_Y_W      = 100.0 * mm   # largeur d'un bloc mâchoire (axe hors-champ)

# Mâchoires X (inférieures, tungstène)
JAW_X_Z_TOP  = 350.0 * mm
JAW_X_Z_BOT  = 420.0 * mm
JAW_X_W      = 100.0 * mm

# Fantôme d'eau
PHANTOM_SURFACE_Z = SSD_MM              # surface à z = 1000 mm (SSD = 100 cm)
PHANTOM_DEPTH     = 300.0 * mm         # 30 cm de profondeur
PHANTOM_XY        = 400.0 * mm         # 40 × 40 cm (>champ max 30 cm avec divergence)

# Système de coordonnées Gate : origine du monde au centre du monde
# Cible placée à SOURCE_OFFSET en z par rapport au centre du monde
WORLD_Z_SIZE   = 1500.0 * mm
WORLD_XY_SIZE  =  600.0 * mm
SOURCE_OFFSET  = -680.0 * mm   # translation de la cible → z_gate = SOURCE_OFFSET + z_abs


def to_gate_z(z_abs_mm):
    """Convertit une position absolue (depuis la cible, mm) en z Gate (depuis le centre du monde)."""
    return SOURCE_OFFSET + z_abs_mm


def phsp1_gate_z():
    return to_gate_z(PHSP1_Z)


def phantom_center_gate():
    zc = to_gate_z(PHANTOM_SURFACE_Z + PHANTOM_DEPTH / 2)
    return [0.0, 0.0, zc]


def jaw_half_opening(z_center_abs_mm, field_size_mm):
    """Demi-ouverture d'une mâchoire pour obtenir FS à SAD."""
    return (field_size_mm / 2.0) * (z_center_abs_mm / SAD_MM)


# ─────────────────────────────────────────────────────────────────────────────
#  RÉPERTOIRES DE SORTIE
# ─────────────────────────────────────────────────────────────────────────────

def make_dirs(energy_key: str):
    base    = pathlib.Path("output_mc") / f"e{energy_key}"
    ph1_dir = base / "phase1"
    ph2_dir = base / "phase2"
    ph1_dir.mkdir(parents=True, exist_ok=True)
    ph2_dir.mkdir(parents=True, exist_ok=True)
    return ph1_dir, ph2_dir


# ═════════════════════════════════════════════════════════════════════════════
#  PHASE 1 : Source → Cible → Collimateur primaire → Cône égalisateur
#            → Phase space enregistré juste sous le cône égalisateur
# ═════════════════════════════════════════════════════════════════════════════

def build_phase1(energy_key: str = "6",
                 n_primary: int = 2_000_000,
                 n_threads: int = 4,
                 ph1_dir: pathlib.Path = None) -> gate.Simulation:
    """
    Construit et configure la simulation de Phase 1.

    La source d'électrons est dirigée sur la cible W. Les interactions
    (bremsstrahlung, diffusions multiples) produisent le faisceau de photons.
    Le phase space capture toutes les particules juste sous le cône égalisateur.

    Paramètres fittables de cette phase :
      - E_mev / E_sigma : énergie et étalement en énergie des électrons primaires
      - spot_sigma_mm   : taille du spot à la cible (influence la pénombre)
    """
    bp = BEAM_PARAMS[energy_key]

    sim = gate.Simulation()
    sim.random_seed        = "auto"
    sim.number_of_threads  = n_threads
    sim.visu               = False

    # ── Physique ──────────────────────────────────────────────────────────────
    # option4 : physique EM très précise (recommandée pour dosimétrie médicale)
    sim.physics_manager.physics_list_name = "G4EmStandardPhysics_option4"
    sim.physics_manager.enable_decay      = False
    sim.physics_manager.global_production_cuts.gamma    = 0.1 * mm
    sim.physics_manager.global_production_cuts.electron = 0.1 * mm
    sim.physics_manager.global_production_cuts.positron = 0.1 * mm
    sim.physics_manager.global_production_cuts.proton   = 10  * mm

    # ── Monde : vide (G4_Galactic) pour ne pas perturber les particules ───────
    world          = sim.world
    world.size     = [WORLD_XY_SIZE, WORLD_XY_SIZE, WORLD_Z_SIZE]
    world.material = "G4_Galactic"

    # ── Cible : tungstène (W) ─────────────────────────────────────────────────
    # Lieu de production du rayonnement de freinage (bremsstrahlung)
    target               = sim.add_volume("Tubs", "target")
    target.rmin          = 0.0
    target.rmax          = TARGET_RADIUS
    target.dz            = TARGET_THICKNESS / 2.0
    target.translation   = [0.0, 0.0, to_gate_z(TARGET_Z_TOP + TARGET_THICKNESS / 2.0)]
    target.material      = "G4_W"

    # ── Collimateur primaire : W creux conique ────────────────────────────────
    # Bloc en W traversé par un cône d'ouverture croissante vers le patient.
    # Modélisé en Gate comme un Cons (tronc de cône) creux.
    prim_z_ctr = (PRIM_Z_TOP + PRIM_Z_BOT) / 2.0
    prim_dz    = (PRIM_Z_BOT - PRIM_Z_TOP) / 2.0
    prim               = sim.add_volume("Cons", "primary_collimator")
    # Face côté source (z_local = -dz) : ouverture étroite
    prim.rmin1         = PRIM_INNER_R_TOP
    prim.rmax1         = PRIM_OUTER_R
    # Face côté patient (z_local = +dz) : ouverture large
    prim.rmin2         = PRIM_INNER_R_BOT
    prim.rmax2         = PRIM_OUTER_R
    prim.dz            = prim_dz
    prim.translation   = [0.0, 0.0, to_gate_z(prim_z_ctr)]
    prim.material      = "G4_W"

    # ── Cône égalisateur (Flattening Filter) : W ─────────────────────────────
    # Cone plein dont la pointe est orientée vers la source.
    # Attenue davantage le centre du faisceau pour obtenir un profil plat (FF).
    # Sans cône égalisateur (FFF) : remplacé par un disque fin ou supprimé.
    ff_z_ctr = (FF_Z_TOP + FF_Z_BOT) / 2.0
    ff_dz    = (FF_Z_BOT - FF_Z_TOP) / 2.0

    if not bp["FFF"]:
        ff             = sim.add_volume("Cons", "flattening_filter")
        # Face côté source (-dz) : pointe très étroite
        ff.rmin1       = 0.0
        ff.rmax1       = FF_TIP_R
        # Face côté patient (+dz) : base large
        ff.rmin2       = 0.0
        ff.rmax2       = FF_BASE_R
        ff.dz          = ff_dz
        ff.translation = [0.0, 0.0, to_gate_z(ff_z_ctr)]
        ff.material    = "G4_W"
    # Pour FFF : pas de cône égalisateur → aucun volume ajouté

    # ── Plan de phase space Phase 1 (quasi-transparent) ──────────────────────
    phsp1_vol               = sim.add_volume("Tubs", "phsp1_plane")
    phsp1_vol.rmin          = 0.0
    phsp1_vol.rmax          = PHSP1_R
    phsp1_vol.dz            = 0.01 * mm     # épaisseur quasi-nulle (plan virtuel)
    phsp1_vol.translation   = [0.0, 0.0, phsp1_gate_z()]
    phsp1_vol.material      = "G4_Galactic"

    phsp1_act                  = sim.add_actor("PhaseSpaceActor", "phsp1_actor")
    phsp1_act.attached_to      = phsp1_vol.name
    phsp1_act.output_filename  = str(ph1_dir / "phsp_post_ff.root")
    phsp1_act.attributes       = [
        "KineticEnergy",   # énergie cinétique (MeV)
        "Weight",          # poids statistique
        "PrePosition",     # position d'entrée (x, y, z)
        "PreDirection",    # direction unitaire (ux, uy, uz)
        "PDGCode",         # code PDG de la particule
        "ParticleName",    # nom de la particule
    ]
    phsp1_act.steps_to_store   = "entering"   # enregistrement à l'entrée du plan

    # ── Source : faisceau d'électrons ─────────────────────────────────────────
    src                       = sim.add_source("GenericSource", "electron_beam")
    src.particle              = "e-"
    src.n                     = n_primary

    # Énergie : distribution gaussienne autour de l'énergie nominale
    src.energy.type           = "gauss"
    src.energy.mono           = bp["E_mev"] * MeV
    src.energy.sigma_gauss    = bp["E_sigma"] * MeV

    # Position : disque gaussien sur la cible (plan XY)
    src.position.type         = "disc"
    src.position.radius       = 3.0 * bp["spot_sigma_mm"] * mm   # rayon = 3σ
    src.position.sigma_x      = bp["spot_sigma_mm"] * mm
    src.position.sigma_y      = bp["spot_sigma_mm"] * mm
    src.position.translation  = [0.0, 0.0, to_gate_z(TARGET_Z_TOP)]

    # Direction : axe faisceau +z (direction vers le patient)
    src.direction.type        = "momentum"
    src.direction.momentum    = [0.0, 0.0, 1.0]

    # ── Statistiques de la simulation ─────────────────────────────────────────
    stats                  = sim.add_actor("SimulationStatisticsActor", "stats_ph1")
    stats.output_filename  = str(ph1_dir / "stats_phase1.txt")

    return sim


# ═════════════════════════════════════════════════════════════════════════════
#  PHASE 2 : Phase space → Chambre moniteur → Mâchoires → Fantôme d'eau
#            → DoseActor 3D (PDD + profils transversaux)
# ═════════════════════════════════════════════════════════════════════════════

def build_phase2(energy_key: str = "6",
                 field_size_cm: float = 10.0,
                 n_threads: int = 4,
                 ph1_dir: pathlib.Path = None,
                 ph2_dir: pathlib.Path = None) -> gate.Simulation:
    """
    Construit et configure la simulation de Phase 2.

    Lit le phase space produit en Phase 1, le transporte à travers les mâchoires
    (jaws) et calcule la distribution de dose 3D dans le fantôme d'eau.

    Le DoseActor produit un volume de dose 3D (fichier .mhd) depuis lequel
    on extrait :
      - le PDD (rendement en profondeur sur l'axe central)
      - les profils transversaux à plusieurs profondeurs

    Paramètres fittables de cette phase :
      - dmax, mu, Ds, dFS, sFS (PDD analytique)
      - sig0, horn, sigma_fff   (profil analytique)
    """
    phsp_file = str(ph1_dir / "phsp_post_ff.root")
    fs_mm     = field_size_cm * cm

    sim = gate.Simulation()
    sim.random_seed        = "auto"
    sim.number_of_threads  = n_threads
    sim.visu               = False

    # ── Physique ──────────────────────────────────────────────────────────────
    sim.physics_manager.physics_list_name = "G4EmStandardPhysics_option4"
    sim.physics_manager.enable_decay      = False
    sim.physics_manager.global_production_cuts.gamma    = 0.1 * mm
    sim.physics_manager.global_production_cuts.electron = 0.1 * mm
    sim.physics_manager.global_production_cuts.positron = 0.1 * mm

    # ── Monde : air ───────────────────────────────────────────────────────────
    world          = sim.world
    world.size     = [WORLD_XY_SIZE, WORLD_XY_SIZE, WORLD_Z_SIZE]
    world.material = "G4_AIR"

    # ── Chambre moniteur (ions, air) ──────────────────────────────────────────
    ic               = sim.add_volume("Tubs", "monitor_chamber")
    ic.rmin          = 0.0
    ic.rmax          = IC_R
    ic.dz            = IC_THICKNESS / 2.0
    ic.translation   = [0.0, 0.0, to_gate_z(IC_Z_CENTER)]
    ic.material      = "G4_AIR"

    # ── Mâchoires Y (supérieures) ─────────────────────────────────────────────
    # Deux blocs W dont les faces internes définissent la demi-ouverture du champ.
    jaw_y_z_ctr  = (JAW_Y_Z_TOP + JAW_Y_Z_BOT) / 2.0
    jaw_y_dz     =  JAW_Y_Z_BOT - JAW_Y_Z_TOP
    jaw_y_half   = jaw_half_opening(jaw_y_z_ctr, fs_mm)   # demi-ouverture en mm

    jaw_y_pos              = sim.add_volume("Box", "jaw_y_pos")
    jaw_y_pos.size         = [2 * WORLD_XY_SIZE / 2,   JAW_Y_W, jaw_y_dz]
    jaw_y_pos.translation  = [0.0,  jaw_y_half + JAW_Y_W / 2.0, to_gate_z(jaw_y_z_ctr)]
    jaw_y_pos.material     = "G4_W"

    jaw_y_neg              = sim.add_volume("Box", "jaw_y_neg")
    jaw_y_neg.size         = [2 * WORLD_XY_SIZE / 2,   JAW_Y_W, jaw_y_dz]
    jaw_y_neg.translation  = [0.0, -(jaw_y_half + JAW_Y_W / 2.0), to_gate_z(jaw_y_z_ctr)]
    jaw_y_neg.material     = "G4_W"

    # ── Mâchoires X (inférieures) ─────────────────────────────────────────────
    jaw_x_z_ctr  = (JAW_X_Z_TOP + JAW_X_Z_BOT) / 2.0
    jaw_x_dz     =  JAW_X_Z_BOT - JAW_X_Z_TOP
    jaw_x_half   = jaw_half_opening(jaw_x_z_ctr, fs_mm)

    jaw_x_pos              = sim.add_volume("Box", "jaw_x_pos")
    jaw_x_pos.size         = [JAW_X_W,   2 * WORLD_XY_SIZE / 2, jaw_x_dz]
    jaw_x_pos.translation  = [ jaw_x_half + JAW_X_W / 2.0, 0.0, to_gate_z(jaw_x_z_ctr)]
    jaw_x_pos.material     = "G4_W"

    jaw_x_neg              = sim.add_volume("Box", "jaw_x_neg")
    jaw_x_neg.size         = [JAW_X_W,   2 * WORLD_XY_SIZE / 2, jaw_x_dz]
    jaw_x_neg.translation  = [-(jaw_x_half + JAW_X_W / 2.0), 0.0, to_gate_z(jaw_x_z_ctr)]
    jaw_x_neg.material     = "G4_W"

    # ── Fantôme d'eau ─────────────────────────────────────────────────────────
    phantom               = sim.add_volume("Box", "water_phantom")
    phantom.size          = [PHANTOM_XY, PHANTOM_XY, PHANTOM_DEPTH]
    phantom.translation   = phantom_center_gate()
    phantom.material      = "G4_WATER"

    # ── DoseActor 3D dans le fantôme ──────────────────────────────────────────
    # Résolution : 2 × 2 × 2 mm → grille 200 × 200 × 150 voxels
    # Augmenter la résolution (ex. 1 mm) pour des profils plus précis (× 8 mémoire)
    dose_actor                  = sim.add_actor("DoseActor", "dose_3d")
    dose_actor.attached_to      = phantom.name
    dose_actor.output_filename  = str(ph2_dir / f"dose_fs{field_size_cm:.0f}cm.mhd")
    dose_actor.size             = [200, 200, 150]   # nx, ny, nz
    dose_actor.spacing          = [2.0 * mm, 2.0 * mm, 2.0 * mm]
    dose_actor.hit_type         = "random"   # position aléatoire dans le voxel
    dose_actor.dose             = True
    dose_actor.dose_uncertainty = True       # calcule l'incertitude statistique

    # ── Source : lecture du phase space Phase 1 ───────────────────────────────
    # Toutes les particules (photons, électrons, positrons) sont relues.
    src                   = sim.add_source("PhaseSpaceSource", "phsp_source")
    src.phsp_file         = phsp_file
    src.batch_size        = 10_000
    src.n                 = 0              # 0 = lire tout le fichier phase space
    src.generate_until_next_primary = True # reproduit le poids statistique correct
    # Les positions/directions sont celles stockées dans le phase space (aucun offset)
    src.position.translation = [0.0, 0.0, 0.0]

    # ── Phase space optionnel juste avant le fantôme ──────────────────────────
    preph_z   = to_gate_z(PHANTOM_SURFACE_Z - 2.0 * mm)
    preph_vol               = sim.add_volume("Box", "phsp2_plane")
    preph_vol.size          = [PHANTOM_XY + 40 * mm,
                                PHANTOM_XY + 40 * mm,
                                0.2 * mm]
    preph_vol.translation   = [0.0, 0.0, preph_z]
    preph_vol.material      = "G4_AIR"

    phsp2_act                 = sim.add_actor("PhaseSpaceActor", "phsp2_actor")
    phsp2_act.attached_to     = preph_vol.name
    phsp2_act.output_filename = str(ph2_dir / f"phsp_pre_phantom_fs{field_size_cm:.0f}cm.root")
    phsp2_act.attributes      = ["KineticEnergy", "Weight",
                                  "PrePosition", "PreDirection", "PDGCode"]
    phsp2_act.steps_to_store  = "entering"

    # ── Statistiques ──────────────────────────────────────────────────────────
    stats                  = sim.add_actor("SimulationStatisticsActor", "stats_ph2")
    stats.output_filename  = str(ph2_dir / f"stats_phase2_fs{field_size_cm:.0f}cm.txt")

    return sim


# ═════════════════════════════════════════════════════════════════════════════
#  POST-TRAITEMENT : extraction PDD et profils depuis le DoseActor
# ═════════════════════════════════════════════════════════════════════════════

def extract_pdd_profiles(dose_mhd_path: str,
                         field_size_cm: float,
                         ssd_cm: float = 100.0,
                         output_dir: pathlib.Path = None) -> dict:
    """
    Lit le volume de dose 3D (fichier .mhd produit par DoseActor) et extrait :
      - PDD (rendement en profondeur) sur l'axe central, normalisé à Dmax
      - Profils transversaux (X et Y) à plusieurs profondeurs

    Retourne un dict JSON-compatible prêt à être comparé au modèle analytique.
    """
    try:
        import itk
    except ImportError:
        raise ImportError("itk est requis pour lire les fichiers .mhd. "
                          "Installez-le avec : pip install itk")

    dose_img  = itk.imread(dose_mhd_path)
    dose_arr  = itk.array_view_from_image(dose_img)   # shape (nz, ny, nx), ordre ITK
    spacing   = dose_img.GetSpacing()   # (sx, sy, sz) mm
    origin    = dose_img.GetOrigin()    # (ox, oy, oz) mm — coin inférieur-gauche-avant

    nz, ny, nx = dose_arr.shape
    cx, cy      = nx // 2, ny // 2     # indices du voxel axial central

    # ── PDD : dose sur l'axe central ─────────────────────────────────────────
    pdd_raw    = dose_arr[:, cy, cx].astype(float)
    pdd_max    = pdd_raw.max()
    pdd_norm   = (pdd_raw / pdd_max * 100.0) if pdd_max > 0 else pdd_raw.copy()

    # Profondeurs en cm depuis la surface du fantôme
    depths_cm  = [(origin[2] + k * spacing[2]) / 10.0 for k in range(nz)]

    # Indice du dmax
    dmax_idx  = int(np.argmax(pdd_raw))
    dmax_cm   = depths_cm[dmax_idx]

    # ── Profils transversaux ──────────────────────────────────────────────────
    # Profondeurs cibles : dmax, 5 cm, 10 cm, 20 cm
    depth_targets_cm = [dmax_cm, 5.0, 10.0, 20.0]
    profiles = {}

    for d_cm in depth_targets_cm:
        iz = int(round(d_cm * 10.0 / spacing[2]))
        if not (0 <= iz < nz):
            continue
        prof_x_raw = dose_arr[iz, cy, :].astype(float)
        prof_y_raw = dose_arr[iz, :, cx].astype(float)

        # Positions en cm depuis le centre du fantôme
        x_pos = [(origin[0] + j * spacing[0]) / 10.0 for j in range(nx)]
        y_pos = [(origin[1] + j * spacing[1]) / 10.0 for j in range(ny)]

        # Normalisation : 100 % sur l'axe
        p0x = prof_x_raw[cx] if prof_x_raw[cx] > 0 else prof_x_raw.max()
        p0y = prof_y_raw[cy] if prof_y_raw[cy] > 0 else prof_y_raw.max()
        profiles[f"{d_cm:.1f}cm"] = {
            "x_cm":      x_pos,
            "profile_x": (prof_x_raw / p0x).tolist() if p0x > 0 else prof_x_raw.tolist(),
            "y_cm":      y_pos,
            "profile_y": (prof_y_raw / p0y).tolist() if p0y > 0 else prof_y_raw.tolist(),
        }

    result = {
        "field_size_cm":  field_size_cm,
        "ssd_cm":         ssd_cm,
        "pdd": {
            "depths_cm":        depths_cm,
            "dose_percent":     pdd_norm.tolist(),
            "dmax_cm":          dmax_cm,
        },
        "profiles": profiles,
    }

    if output_dir is not None:
        out_path = output_dir / f"pdd_profiles_fs{field_size_cm:.0f}cm.json"
        with open(out_path, "w") as f:
            json.dump(result, f, indent=2)
        print(f"  [PDD/Profils] → {out_path}")

    return result


# ═════════════════════════════════════════════════════════════════════════════
#  FIT DES PARAMÈTRES DU MODÈLE ANALYTIQUE (WebLinac / index.html)
# ═════════════════════════════════════════════════════════════════════════════

def fit_analytical_params(mc_results: dict, energy_key: str = "6") -> dict:
    """
    Ajuste les paramètres du modèle analytique WebLinac à partir des données MC.

    Modèle PDD (d >= dmax) :
      PDD(d) = 100 × [(SSD + dmax)/(SSD + d)]² × exp(-mu × (d - dmax)) × scatter(d)
      avec scatter(d) = 1 + 1.5e-3 × (FS - 10) × (d - dmax)

    Modèle profil (faisceau FF) :
      P(x) = 0.5 × [erf((a-x)/M) + erf((a+x)/M)] × (1 + horn × r²)
      avec M = √2 × (sig0 + 0.012×d + 0.004×(FS-10)), r = |x|/a
    """
    try:
        from scipy.optimize import curve_fit
    except ImportError:
        raise ImportError("scipy est requis pour le fit. pip install scipy")

    ssd_cm = mc_results.get("ssd_cm", 100.0)
    sad_cm = 100.0
    fs_cm  = mc_results["field_size_cm"]

    pdd_data    = mc_results["pdd"]
    depths_arr  = np.array(pdd_data["depths_cm"])
    dose_arr    = np.array(pdd_data["dose_percent"])

    dmax_mc     = pdd_data["dmax_cm"]

    # Dose de surface (interpolation à d = 0)
    if depths_arr[0] < 0.3:
        ds_mc = dose_arr[0] / 100.0
    else:
        ds_mc = np.interp(0.0, depths_arr, dose_arr) / 100.0

    # ── Fit du PDD exponentiel (d >= dmax) ───────────────────────────────────
    mask  = depths_arr >= dmax_mc
    d_fit = depths_arr[mask]
    p_fit = dose_arr[mask]

    def pdd_model(d, mu):
        scatter = 1.0 + 1.5e-3 * (fs_cm - 10.0) * (d - dmax_mc)
        isl     = ((ssd_cm + dmax_mc) / (ssd_cm + d)) ** 2
        return 100.0 * isl * np.exp(-mu * (d - dmax_mc)) * scatter

    try:
        popt_pdd, _ = curve_fit(pdd_model, d_fit, p_fit,
                                 p0=[0.033], bounds=([0.01], [0.10]))
        mu_fit = float(popt_pdd[0])
    except Exception:
        mu_fit = 0.033   # valeur par défaut 6 MV si le fit échoue

    # ── Fit du profil (pénombre) ──────────────────────────────────────────────
    # Utilise le profil à dmax (profil le plus caractéristique de la source + FF)
    prof_key  = f"{dmax_mc:.1f}cm"
    if prof_key not in mc_results["profiles"]:
        # Choisir le profil disponible le plus proche
        keys      = list(mc_results["profiles"].keys())
        depths_k  = [float(k.replace("cm","")) for k in keys]
        idx_best  = int(np.argmin(np.abs(np.array(depths_k) - dmax_mc)))
        prof_key  = keys[idx_best]

    prof_data = mc_results["profiles"][prof_key]
    x_arr     = np.array(prof_data["x_cm"])
    px_arr    = np.array(prof_data["profile_x"])
    d_prof    = float(prof_key.replace("cm",""))

    # Demi-largeur de champ à la profondeur d_prof par divergence
    a_cm = (fs_cm / 2.0) * (ssd_cm + d_prof) / sad_cm

    from scipy.special import erf as scipy_erf

    def profile_model_ff(x, sig0, horn):
        sig = sig0 + 0.012 * d_prof + 0.004 * (fs_cm - 10.0)
        M   = np.sqrt(2.0) * sig
        pen = 0.5 * (scipy_erf((a_cm - x) / M) + scipy_erf((a_cm + x) / M))
        r   = np.abs(x) / a_cm if a_cm > 0 else np.zeros_like(x)
        horns = np.where(r < 1.0, 1.0 + horn * r**2, 1.0)
        return pen * horns + 0.018 * (1.0 - pen)

    def profile_model_fff(x, sig0, sigma_fff):
        sig   = sig0 + 0.012 * d_prof + 0.004 * (fs_cm - 10.0)
        M     = np.sqrt(2.0) * sig
        pen   = 0.5 * (scipy_erf((a_cm - x) / M) + scipy_erf((a_cm + x) / M))
        x_src = np.abs(x) * sad_cm / (ssd_cm + d_prof)
        lor   = 1.0 / (1.0 + (x_src / sigma_fff)**2)
        return pen * lor + 0.018 * (1.0 - pen)

    is_fff = BEAM_PARAMS[energy_key]["FFF"]

    try:
        if is_fff:
            popt_p, _ = curve_fit(profile_model_fff, x_arr, px_arr,
                                   p0=[0.36, 13.0],
                                   bounds=([0.10, 2.0], [1.0, 30.0]))
            sig0_fit, sigma_fff_fit = float(popt_p[0]), float(popt_p[1])
            horn_fit = 0.0
        else:
            popt_p, _ = curve_fit(profile_model_ff, x_arr, px_arr,
                                   p0=[0.35, 0.05],
                                   bounds=([0.05, 0.0], [1.0, 0.5]))
            sig0_fit, horn_fit = float(popt_p[0]), float(popt_p[1])
            sigma_fff_fit = None
    except Exception:
        sig0_fit      = 0.35
        horn_fit      = 0.05
        sigma_fff_fit = 13.0 if is_fff else None

    # ── Compilation des paramètres fittés ─────────────────────────────────────
    fitted = {
        "energy":     energy_key,
        "field_size": fs_cm,
        "dmax":       round(dmax_mc, 3),
        "mu":         round(mu_fit,  5),
        "Ds":         round(ds_mc,   4),
        "sig0":       round(sig0_fit, 4),
        "horn":       round(horn_fit, 4),
    }
    if sigma_fff_fit is not None:
        fitted["sigma_fff"] = round(sigma_fff_fit, 3)

    return fitted


# ═════════════════════════════════════════════════════════════════════════════
#  UTILITAIRE : comparaison MC vs modèle analytique WebLinac
# ═════════════════════════════════════════════════════════════════════════════

def compare_with_analytical(mc_results: dict, fitted_params: dict,
                              output_dir: pathlib.Path = None):
    """
    Compare visuellement les courbes MC aux courbes analytiques WebLinac
    et sauvegarde les figures.
    """
    try:
        import matplotlib.pyplot as plt
        from scipy.special import erf as scipy_erf
    except ImportError:
        print("  [Comparaison] matplotlib ou scipy absent — graphiques non générés.")
        return

    p    = fitted_params
    fs   = p["field_size"]
    ssd  = mc_results.get("ssd_cm", 100.0)
    sad  = 100.0
    dmax = p["dmax"]
    mu   = p["mu"]
    Ds   = p["Ds"]
    sig0 = p["sig0"]
    horn = p["horn"]
    s_fff = p.get("sigma_fff", None)
    is_fff = BEAM_PARAMS.get(p["energy"], {}).get("FFF", False)

    def analytical_pdd(d):
        if d <= 0:
            return Ds * 100.0
        if d < dmax:
            t = d / dmax
            return 100.0 * (Ds + (1.0 - Ds) * (3*t*t - 2*t*t*t))
        scatter = 1.0 + 1.5e-3 * (fs - 10.0) * (d - dmax)
        isl     = ((ssd + dmax) / (ssd + d)) ** 2
        return 100.0 * isl * np.exp(-mu * (d - dmax)) * scatter

    def analytical_profile(x, d_cm):
        a   = (fs / 2.0) * (ssd + d_cm) / sad
        sig = sig0 + 0.012 * d_cm + 0.004 * (fs - 10.0)
        M   = np.sqrt(2.0) * sig
        pen = 0.5 * (scipy_erf((a - x) / M) + scipy_erf((a + x) / M))
        if is_fff and s_fff:
            x_src  = np.abs(x) * sad / (ssd + d_cm)
            horns  = 1.0 / (1.0 + (x_src / s_fff) ** 2)
        else:
            r      = np.abs(x) / a if a > 0 else np.zeros_like(x)
            horns  = np.where(r < 1.0, 1.0 + horn * r**2, 1.0)
        return pen * horns + 0.018 * (1.0 - pen)

    # ── Figure PDD ────────────────────────────────────────────────────────────
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f"MC vs Modèle analytique — {p['energy']} MV — FS = {fs:.0f}×{fs:.0f} cm")

    ax_pdd = axes[0]
    depths_mc   = np.array(mc_results["pdd"]["depths_cm"])
    dose_mc     = np.array(mc_results["pdd"]["dose_percent"])
    depths_anal = np.linspace(0.0, 30.0, 300)
    dose_anal   = np.array([analytical_pdd(d) for d in depths_anal])

    ax_pdd.plot(depths_mc,   dose_mc,   "o-", ms=3, label="Monte Carlo", color="#38bdf8")
    ax_pdd.plot(depths_anal, dose_anal, "--",       label="Analytique",  color="#fb923c")
    ax_pdd.axvline(dmax, ls=":", color="yellow", lw=1, label=f"dmax={dmax:.2f} cm")
    ax_pdd.set_xlabel("Profondeur (cm)")
    ax_pdd.set_ylabel("PDD (%)")
    ax_pdd.set_title("Rendement en profondeur")
    ax_pdd.legend(fontsize=9)
    ax_pdd.grid(True, alpha=0.3)

    # ── Figure profils ────────────────────────────────────────────────────────
    ax_prof = axes[1]
    colors_prof = ["#38bdf8", "#4ade80", "#fb923c", "#e879f9"]

    for idx, (key, prof) in enumerate(mc_results["profiles"].items()):
        col   = colors_prof[idx % len(colors_prof)]
        d_cm  = float(key.replace("cm", ""))
        x_mc  = np.array(prof["x_cm"])
        px_mc = np.array(prof["profile_x"])
        x_an  = np.linspace(-20.0, 20.0, 400)
        p_an  = analytical_profile(x_an, d_cm)

        ax_prof.plot(x_mc,  px_mc, "o",  ms=2, color=col, alpha=0.7)
        ax_prof.plot(x_an,  p_an,  "--", color=col, label=f"d = {d_cm:.1f} cm")

    ax_prof.set_xlabel("Position latérale (cm)")
    ax_prof.set_ylabel("Dose normalisée")
    ax_prof.set_title("Profils transversaux (MC : points, Analytique : tirets)")
    ax_prof.legend(fontsize=9)
    ax_prof.grid(True, alpha=0.3)

    plt.tight_layout()

    if output_dir:
        fig_path = output_dir / f"comparison_{p['energy']}_fs{fs:.0f}cm.png"
        plt.savefig(fig_path, dpi=150, bbox_inches="tight")
        print(f"  [Comparaison] Figure → {fig_path}")
    plt.close(fig)


# ═════════════════════════════════════════════════════════════════════════════
#  POINT D'ENTRÉE PRINCIPAL
# ═════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Simulation MC LINAC clinique (OpenGATE v10) — photons",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=(
            "Exemples :\n"
            "  python linac_mc_simulation.py --phase 1\n"
            "  python linac_mc_simulation.py --phase 2 --fs 10 --energy 6\n"
            "  python linac_mc_simulation.py --phase 3 --nthreads 8 --nprimary 5000000\n"
        ),
    )
    parser.add_argument(
        "--phase", type=int, choices=[1, 2, 3], default=3,
        help=(
            "1 : Phase 1 seulement (source → cône égalisateur)\n"
            "2 : Phase 2 seulement (cône égalisateur → fantôme d'eau)\n"
            "3 : Phase 1 + Phase 2 + post-traitement + fit (défaut)"
        ),
    )
    parser.add_argument(
        "--energy", type=str, default="6",
        choices=list(BEAM_PARAMS.keys()),
        help="Énergie nominale du faisceau (MV), défaut : 6",
    )
    parser.add_argument(
        "--fs", type=float, nargs="+", default=[10.0],
        metavar="FIELD_CM",
        help="Taille(s) de champ en cm à SAD (défaut : 10). "
             "Ex : --fs 5 10 20",
    )
    parser.add_argument(
        "--nthreads", type=int, default=4,
        help="Nombre de threads OpenMP Geant4 (défaut : 4)",
    )
    parser.add_argument(
        "--nprimary", type=int, default=2_000_000,
        help="Nombre de particules primaires Phase 1 (défaut : 2 000 000)",
    )
    args = parser.parse_args()

    ph1_dir, ph2_dir = make_dirs(args.energy)
    all_fitted = []

    # ─────────────────────────────────────────────────────────────────────────
    #  PHASE 1
    # ─────────────────────────────────────────────────────────────────────────
    if args.phase in (1, 3):
        print("\n" + "═" * 65)
        print(f"  PHASE 1 — Énergie : {args.energy} MV  |  N = {args.nprimary:,}")
        print("  Source e⁻ → Cible W → Collimateur primaire → Cône égalisateur")
        print("═" * 65)

        sim1 = build_phase1(
            energy_key = args.energy,
            n_primary  = args.nprimary,
            n_threads  = args.nthreads,
            ph1_dir    = ph1_dir,
        )
        sim1.run()
        phsp_file = ph1_dir / "phsp_post_ff.root"
        print(f"\n  Phase 1 terminée. Phase space → {phsp_file}")

    # ─────────────────────────────────────────────────────────────────────────
    #  PHASE 2 + POST-TRAITEMENT (pour chaque taille de champ)
    # ─────────────────────────────────────────────────────────────────────────
    if args.phase in (2, 3):
        for fs_cm in args.fs:
            print("\n" + "═" * 65)
            print(f"  PHASE 2 — FS = {fs_cm:.0f}×{fs_cm:.0f} cm  |  SSD = 100 cm")
            print("  Cône égalisateur → Mâchoires → Fantôme d'eau")
            print("═" * 65)

            sim2 = build_phase2(
                energy_key    = args.energy,
                field_size_cm = fs_cm,
                n_threads     = args.nthreads,
                ph1_dir       = ph1_dir,
                ph2_dir       = ph2_dir,
            )
            sim2.run()

            dose_file = ph2_dir / f"dose_fs{fs_cm:.0f}cm.mhd"
            print(f"\n  Phase 2 terminée. Dose 3D → {dose_file}")

            # ── Post-traitement ───────────────────────────────────────────────
            if args.phase == 3 and dose_file.exists():
                print("\n  [Post-traitement] Extraction PDD et profils…")
                mc_data = extract_pdd_profiles(
                    dose_mhd_path = str(dose_file),
                    field_size_cm = fs_cm,
                    ssd_cm        = SSD_MM / cm,
                    output_dir    = ph2_dir,
                )

                print("  [Fit] Ajustement des paramètres du modèle analytique…")
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

    # ── Sauvegarde globale des paramètres fittés ──────────────────────────────
    if all_fitted:
        fit_path = ph2_dir / f"fitted_params_{args.energy}MV.json"
        with open(fit_path, "w") as f:
            json.dump(all_fitted, f, indent=2)
        print(f"\n  [Résultats] Paramètres fittés → {fit_path}")
        print("\n  Ces paramètres peuvent être copiés directement dans le")
        print("  dictionnaire BEAM de index.html pour calibrer le modèle analytique.")

    print("\n  Simulation terminée.\n")


if __name__ == "__main__":
    main()