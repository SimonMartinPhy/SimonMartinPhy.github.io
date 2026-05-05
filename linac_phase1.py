"""
Phase 1 : Faisceau d'électrons → Cible W → Collimateur primaire → Cône égalisateur
          → Phase space enregistré à z = 84 mm (juste sous le FF)

Produit : output_mc/e{energy}/phase1/phsp_post_ff.root

Utilisation :
  python linac_phase1.py
  python linac_phase1.py --energy 10 --nthreads 8 --nprimary 5000000
  python linac_phase1.py --energy 6fff

Dépendances : pip install opengate
"""

import argparse
import pathlib

import opengate as gate
from opengate.utility import g4_units
from linac_config import (
    mm, MeV,
    BEAM_PARAMS,
    TARGET_Z_TOP, TARGET_THICKNESS, TARGET_RADIUS,
    PRIM_Z_TOP, PRIM_Z_BOT, PRIM_INNER_R_TOP, PRIM_INNER_R_BOT, PRIM_OUTER_R,
    FF_Z_TOP, FF_Z_BOT, FF_TIP_R, FF_BASE_R,
    PHSP1_R,
    WORLD_Z_SIZE, WORLD_XY_SIZE,
    to_gate_z, phsp1_gate_z, make_dirs,
)
deg = g4_units.deg

def build_phase1(energy_key: str = "6",
                 n_primary: int = 2_000_000,
                 n_threads: int = 4,
                 ph1_dir: pathlib.Path = None) -> gate.Simulation:
    """
    Construit la simulation Phase 1.

    Source e⁻ gaussienne → Cible W (bremsstrahlung) → Collimateur primaire →
    Cône égalisateur (FF) → Phase space capturé à z = 84 mm.
    """
    bp = BEAM_PARAMS[energy_key]

    sim = gate.Simulation()
    sim.random_seed       = "auto"
    sim.number_of_threads = n_threads
    sim.visu              = False

    sim.physics_manager.physics_list_name = "G4EmStandardPhysics_option4"
    sim.physics_manager.enable_decay      = False
    sim.physics_manager.global_production_cuts.gamma    = 0.1 * mm
    sim.physics_manager.global_production_cuts.electron = 0.1 * mm
    sim.physics_manager.global_production_cuts.positron = 0.1 * mm
    sim.physics_manager.global_production_cuts.proton   = 10  * mm

    world          = sim.world
    world.size     = [WORLD_XY_SIZE, WORLD_XY_SIZE, WORLD_Z_SIZE]
    world.material = "G4_Galactic"

    # ── Cible W (cylindre plein) ──────────────────────────────────────────────
    target             = sim.add_volume("Tubs", "target")
    target.rmin        = 0.0
    target.rmax        = TARGET_RADIUS
    target.dz          = TARGET_THICKNESS / 2.0
    target.translation = [0.0, 0.0, to_gate_z(TARGET_Z_TOP + TARGET_THICKNESS / 2.0)]
    target.material    = "G4_W"
    target.color = [0.8, 1.0, 0.0, 0.8]  # rouge

    # ── Collimateur primaire (cône creux W) ───────────────────────────────────
    prim_z_ctr = (PRIM_Z_TOP + PRIM_Z_BOT) / 2.0
    prim_dz    = (PRIM_Z_BOT - PRIM_Z_TOP) / 2.0
    prim               = sim.add_volume("Cons", "primary_collimator")
    prim.rmin1         = PRIM_INNER_R_TOP
    prim.rmax1         = PRIM_OUTER_R
    prim.rmin2         = PRIM_INNER_R_BOT
    prim.rmax2         = PRIM_OUTER_R
    prim.dz            = prim_dz
    prim.sphi           = 0.0
    prim.dphi           = 360.0 * deg
    prim.translation   = [0.0, 0.0, to_gate_z(prim_z_ctr)]
    prim.material      = "G4_W"
    prim.color = [0.8, 0.0, 1.0, 0.8]  # vert

    # ── Collimateur primaire kill actor ───────────────────────────────────
    kill_prim                 = sim.add_actor("KillActor", "kill_prim")
    kill_prim.attached_to     = prim.name

    # ── Plan au dessus de la source  + kill actor ───────────────────────────────────
    plane_above_src             = sim.add_volume("Box", "plane_above_src")
    plane_above_src.size        = [WORLD_XY_SIZE, WORLD_XY_SIZE, 0.01 * mm]
    plane_above_src.translation = [0.0, 0.0, to_gate_z(TARGET_Z_TOP - 10.0 * mm)]

    kill_abv_src                = sim.add_actor("KillActor", "kill_abv_src")
    kill_abv_src.attached_to    = plane_above_src.name


    # ── Cône égalisateur (FF seulement — absent en FFF) ───────────────────────
    if not bp["FFF"]:
        ff_z_ctr = (FF_Z_TOP + FF_Z_BOT) / 2.0
        ff_dz    = (FF_Z_BOT - FF_Z_TOP) / 2.0
        ff             = sim.add_volume("Cons", "flattening_filter")
        ff.rmin1       = 0.0
        ff.rmax1       = FF_TIP_R
        ff.rmin2       = 0.0
        ff.rmax2       = FF_BASE_R
        ff.dz          = ff_dz
        ff.sphi         = 0.0
        ff.dphi         = 360.0 * deg
        ff.translation = [0.0, 0.0, to_gate_z(ff_z_ctr)]
        ff.material    = "G4_W"
        ff.color = [0.8, 0.0, 0.0, 0.8]  # bleu
    # ── Plan de phase space (plan virtuel quasi-transparent) ──────────────────
    phsp_vol             = sim.add_volume("Tubs", "phsp1_plane")
    phsp_vol.rmin        = 0.0
    phsp_vol.rmax        = PHSP1_R
    phsp_vol.dz          = 0.01 * mm
    phsp_vol.translation = [0.0, 0.0, phsp1_gate_z()]
    phsp_vol.material    = "G4_Galactic"

    phsp_act                 = sim.add_actor("PhaseSpaceActor", "phsp1_actor")
    phsp_act.attached_to     = phsp_vol.name
    phsp_act.output_filename = str(ph1_dir / "phsp_post_ff.root")
    phsp_act.attributes      = [
        "KineticEnergy", "Weight",
        "PrePositionLocal", "PreDirectionLocal",
        "PDGCode", "ParticleName",
    ]
    phsp_act.steps_to_store = "entering"

    # ── Source : faisceau d'électrons ─────────────────────────────────────────
    src                    = sim.add_source("GenericSource", "electron_beam")
    src.particle           = "e-"
    src.n                  = n_primary
    src.energy.type        = "gauss"
    src.energy.mono        = bp["E_mev"] * MeV
    src.energy.sigma_gauss = bp["E_sigma"] * MeV
    src.position.type      = "disc"
    src.position.radius    = 3.0 * bp["spot_sigma_mm"] * mm
    src.position.sigma_x   = bp["spot_sigma_mm"] * mm
    src.position.sigma_y   = bp["spot_sigma_mm"] * mm
    src.position.translation = [0.0, 0.0, to_gate_z(TARGET_Z_TOP- 5.0 * mm)]
    src.direction.type     = "momentum"
    src.direction.momentum = [0.0, 0.0, 1.0]

    # ── Statistiques ──────────────────────────────────────────────────────────
    stats                 = sim.add_actor("SimulationStatisticsActor", "stats_ph1")
    stats.output_filename = str(ph1_dir / "stats_phase1.txt")

    return sim


def main():
    parser = argparse.ArgumentParser(
        description="Phase 1 MC LINAC : source e⁻ → phase space sous le cône égalisateur",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=(
            "Exemples :\n"
            "  python linac_phase1.py\n"
            "  python linac_phase1.py --energy 10 --nthreads 8 --nprimary 5000000\n"
            "  python linac_phase1.py --energy 6fff\n"
        ),
    )
    parser.add_argument(
        "--energy", type=str, default="6",
        choices=list(BEAM_PARAMS.keys()),
        help="Énergie nominale (MV) — défaut : 6",
    )
    parser.add_argument(
        "--nthreads", type=int, default=4,
        help="Threads OpenMP Geant4 — défaut : 4",
    )
    parser.add_argument(
        "--nprimary", type=int, default=2_000_000,
        help="Nombre d'électrons primaires — défaut : 2 000 000",
    )
    args = parser.parse_args()

    ph1_dir, _ = make_dirs(args.energy)

    print("\n" + "═" * 65)
    print(f"  PHASE 1 — {args.energy} MV  |  N = {args.nprimary:,}  |  threads = {args.nthreads}")
    print("  Source e⁻ → Cible W → Collimateur → Cône égalisateur → PhSp")
    print("═" * 65)

    sim = build_phase1(
        energy_key = args.energy,
        n_primary  = args.nprimary,
        n_threads  = args.nthreads,
        ph1_dir    = ph1_dir,
    )
    sim.progress_bar = True
    sim.run()

    print(f"\n  Phase 1 terminée.")
    print(f"  Phase space → {ph1_dir / 'phsp_post_ff.root'}\n")


if __name__ == "__main__":
    main()
