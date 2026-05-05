"""
Phase 2 : Phase space → Chambre moniteur → Mâchoires → Fantôme d'eau → Dose 3D

Prérequis : linac_phase1.py doit avoir été exécuté avec la même énergie.
Produit   : output_mc/e{energy}/phase2/dose_fs{N}cm.mhd

Utilisation (un champ à la fois — lancer plusieurs fois pour plusieurs champs) :
  python linac_phase2.py --fs 10
  python linac_phase2.py --fs 20 --energy 6 --nthreads 8

Pour enchaîner plusieurs tailles de champ depuis un shell :
  for fs in 5 10 20 30; do python linac_phase2.py --fs $fs; done

Dépendances : pip install opengate
"""

import argparse
import pathlib

import opengate as gate

from linac_config import (
    PHSP1_R, mm, cm,
    BEAM_PARAMS,
    IC_Z_CENTER, IC_THICKNESS, IC_R,
    JAW_Y_Z_TOP, JAW_Y_Z_BOT, JAW_Y_W,
    JAW_X_Z_TOP, JAW_X_Z_BOT, JAW_X_W,
    PHANTOM_SURFACE_Z, PHANTOM_DEPTH, PHANTOM_XY,
    WORLD_Z_SIZE, WORLD_XY_SIZE,
    to_gate_z, phantom_center_gate, jaw_half_opening, make_dirs, phsp1_gate_z,
)


def _estimate_n(field_size_mm: float,
                voxel_spacing_mm: float = 2.0,
                sigma_pct: float = 2.0,
                safety: float = 2.0) -> int:
    """
    Nombre de particules Phase 2 pour ~sigma_pct% d'incertitude à Dmax.

    Modèle géométrique (faisceau plat FF) :
      fraction du faisceau sur le voxel central : f = (dx/FS)²
      comptages nécessaires : N_voxel = (100/sigma)²
      N_total = safety × N_voxel / f
    """
    n_voxel = (100.0 / sigma_pct) ** 2
    n_geom  = n_voxel * (field_size_mm / voxel_spacing_mm) ** 2
    return max(int(safety * n_geom), 1_000_000)


def build_phase2(energy_key: str = "6",
                 field_size_cm: float = 10.0,
                 n_primary: int = 10_000_000,
                 n_threads: int = 4,
                 ph1_dir: pathlib.Path = None,
                 ph2_dir: pathlib.Path = None) -> gate.Simulation:
    """
    Construit la simulation Phase 2.

    Lit le phase space de Phase 1, le transporte à travers les mâchoires et
    calcule la dose 3D dans le fantôme d'eau (DoseActor → fichier .mhd).
    """
    phsp_file = str(ph1_dir / "phsp_post_ff.root")
    fs_mm     = field_size_cm * cm

    sim = gate.Simulation()
    sim.random_seed       = "auto"
    sim.number_of_threads = n_threads
    sim.visu              = False

    sim.physics_manager.physics_list_name = "G4EmStandardPhysics_option4"
    sim.physics_manager.enable_decay      = False
    sim.physics_manager.global_production_cuts.gamma    = 0.1 * mm
    sim.physics_manager.global_production_cuts.electron = 0.1 * mm
    sim.physics_manager.global_production_cuts.positron = 0.1 * mm

    world          = sim.world
    world.size     = [WORLD_XY_SIZE, WORLD_XY_SIZE, WORLD_Z_SIZE]
    world.material = "G4_AIR"

    # ── Chambre moniteur (air) ────────────────────────────────────────────────
    ic             = sim.add_volume("Tubs", "monitor_chamber")
    ic.rmin        = 0.0
    ic.rmax        = IC_R
    ic.dz          = IC_THICKNESS / 2.0
    ic.translation = [0.0, 0.0, to_gate_z(IC_Z_CENTER)]
    ic.material    = "G4_AIR"

    # ── Mâchoires Y (supérieures) ─────────────────────────────────────────────
    jaw_y_z_ctr = (JAW_Y_Z_TOP + JAW_Y_Z_BOT) / 2.0
    jaw_y_dz    =  JAW_Y_Z_BOT - JAW_Y_Z_TOP
    jaw_y_half  = jaw_half_opening(jaw_y_z_ctr, fs_mm)
    jaw_y_w     = WORLD_XY_SIZE / 2.0 - jaw_y_half   # de l'ouverture jusqu'au bord du monde

    jaw_y_pos             = sim.add_volume("Box", "jaw_y_pos")
    jaw_y_pos.size        = [WORLD_XY_SIZE, jaw_y_w, jaw_y_dz]
    jaw_y_pos.translation = [0.0,  jaw_y_half + jaw_y_w / 2.0, to_gate_z(jaw_y_z_ctr)]
    jaw_y_pos.material    = "G4_W"

    jaw_y_neg             = sim.add_volume("Box", "jaw_y_neg")
    jaw_y_neg.size        = [WORLD_XY_SIZE, jaw_y_w, jaw_y_dz]
    jaw_y_neg.translation = [0.0, -(jaw_y_half + jaw_y_w / 2.0), to_gate_z(jaw_y_z_ctr)]
    jaw_y_neg.material    = "G4_W"

    # ── Mâchoires X (inférieures) ─────────────────────────────────────────────
    jaw_x_z_ctr = (JAW_X_Z_TOP + JAW_X_Z_BOT) / 2.0
    jaw_x_dz    =  JAW_X_Z_BOT - JAW_X_Z_TOP
    jaw_x_half  = jaw_half_opening(jaw_x_z_ctr, fs_mm)
    jaw_x_w     = WORLD_XY_SIZE / 2.0 - jaw_x_half   # de l'ouverture jusqu'au bord du monde

    jaw_x_pos             = sim.add_volume("Box", "jaw_x_pos")
    jaw_x_pos.size        = [jaw_x_w, WORLD_XY_SIZE, jaw_x_dz]
    jaw_x_pos.translation = [ jaw_x_half + jaw_x_w / 2.0, 0.0, to_gate_z(jaw_x_z_ctr)]
    jaw_x_pos.material    = "G4_W"

    jaw_x_neg             = sim.add_volume("Box", "jaw_x_neg")
    jaw_x_neg.size        = [jaw_x_w, WORLD_XY_SIZE, jaw_x_dz]
    jaw_x_neg.translation = [-(jaw_x_half + jaw_x_w / 2.0), 0.0, to_gate_z(jaw_x_z_ctr)]
    jaw_x_neg.material    = "G4_W"

    # ── Fantôme d'eau ─────────────────────────────────────────────────────────
    phantom             = sim.add_volume("Box", "water_phantom")
    phantom.size        = [PHANTOM_XY, PHANTOM_XY, PHANTOM_DEPTH]
    phantom.translation = phantom_center_gate()
    phantom.material    = "G4_WATER"

    # ── DoseActor 3D (résolution 2×2×2 mm) ───────────────────────────────────
    dose_act                 = sim.add_actor("DoseActor", "dose_3d")
    dose_act.attached_to     = phantom.name
    dose_act.size            = [200, 200, 150]
    dose_act.spacing         = [2.0 * mm, 2.0 * mm, 2.0 * mm]
    dose_act.hit_type        = "random"
    dose_act.dose.active             = True
    dose_act.dose_uncertainty.active = True
    dose_act.dose.output_filename = str(ph2_dir / f"dose_fs{field_size_cm:.0f}cm.mhd")
    dose_act.dose_uncertainty.output_filename = str(ph2_dir / f"UncDose_fs{field_size_cm:.0f}cm.mhd")
    dose_act.edep.output_filename = str(ph2_dir / f"edep_fs{field_size_cm:.0f}cm.mhd")
    """
    dose_act.uncertainty_goal       = 0.02  
    dose_act.uncertainty_first_check_after_n_events = n_primary // 10
    dose_act.uncertainty_voxel_edep_threshold = 0.8
    """
    # ── Source : phase space Phase 1 ──────────────────────────────────────────

    
    phsp_vol             = sim.add_volume("Tubs", "phsp1_plane")
    phsp_vol.rmin        = 0.0
    phsp_vol.rmax        = PHSP1_R
    phsp_vol.dz          = 0.01 * mm
    phsp_vol.translation = [0.0, 0.0, phsp1_gate_z()]
    phsp_vol.material    = "G4_Galactic"

    src                      = sim.add_source("PhaseSpaceSource", "phsp_source")
    src.phsp_file            = phsp_file
    src.batch_size           = 10_000
    src.n                    = n_primary
    src.attached_to         = phsp_vol.name


    # ── Statistiques ──────────────────────────────────────────────────────────
    stats                 = sim.add_actor("SimulationStatisticsActor", "stats_ph2")
    stats.output_filename = str(ph2_dir / f"stats_phase2_fs{field_size_cm:.0f}cm.txt")

    return sim


def main():
    parser = argparse.ArgumentParser(
        description="Phase 2 MC LINAC : phase space → fantôme d'eau → dose 3D",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=(
            "Exemples :\n"
            "  python linac_phase2.py --fs 10\n"
            "  python linac_phase2.py --fs 20 --energy 6 --nthreads 8\n"
            "\n"
            "Prérequis : linac_phase1.py doit avoir été lancé avec la même énergie.\n"
            "Pour plusieurs tailles de champ, lancer le script plusieurs fois :\n"
            "  for fs in 5 10 20 30; do python linac_phase2.py --fs $fs; done\n"
        ),
    )
    parser.add_argument(
        "--energy", type=str, default="6",
        choices=list(BEAM_PARAMS.keys()),
        help="Énergie nominale (MV) — défaut : 6",
    )
    parser.add_argument(
        "--fs", type=float, required=True,
        metavar="FIELD_CM",
        help="Taille de champ en cm à SAD (un seul champ par exécution)",
    )
    parser.add_argument(
        "--nthreads", type=int, default=4,
        help="Threads OpenMP Geant4 — défaut : 4",
    )
    parser.add_argument(
        "--nprimary", type=int, default=10000000,
        help=(
            "Nombre de particules à simuler"
        ),
    )
    args = parser.parse_args()

    ph1_dir, ph2_dir = make_dirs(args.energy)

    phsp = ph1_dir / "phsp_post_ff.root"
    if not phsp.exists():
        print(f"\n  ERREUR : phase space introuvable : {phsp}")
        print("  Lancez d'abord : python linac_phase1.py --energy", args.energy)
        raise SystemExit(1)

    print("\n" + "═" * 65)
    print(f"  PHASE 2 — {args.energy} MV  |  FS = {args.fs:.0f}×{args.fs:.0f} cm  |  threads = {args.nthreads}")
    print("  Phase space → Chambre moniteur → Mâchoires → Fantôme d'eau")
    print("═" * 65)

    sim = build_phase2(
        energy_key    = args.energy,
        field_size_cm = args.fs,
        n_primary     = args.nprimary,
        n_threads     = args.nthreads,
        ph1_dir       = ph1_dir,
        ph2_dir       = ph2_dir,
    )
    sim.progress_bar = True
    sim.run()

    print(f"\n  Phase 2 terminée.")
    print(f"  Dose 3D → {ph2_dir / f'dose_fs{args.fs:.0f}cm.mhd'}\n")


if __name__ == "__main__":
    main()
