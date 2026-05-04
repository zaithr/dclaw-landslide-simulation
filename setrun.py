
#!/usr/bin/env python3
"""
🚀 D-CLAW setrun.py (OSO-TUNED: slow, high-friction, short runout)
"""

from clawpack.clawutil import data  # type: ignore
from setinput import x0, x2, y0, y2, dx, nx, ny

# =======================================================
# EQUATION SETUP
# =======================================================
i_eta = 8
i_hm  = 4
num_eqn = 7


def setrun(claw_pkg="dclaw"):
    assert claw_pkg.lower() == "dclaw"

    rundata = data.ClawRunData(claw_pkg, 2)
    clawdata = rundata.clawdata

    # =======================================================
    # DOMAIN
    # =======================================================
    clawdata.num_dim = 2
    clawdata.num_cells[0] = nx
    clawdata.num_cells[1] = ny
    clawdata.lower[0] = x0
    clawdata.upper[0] = x2
    clawdata.lower[1] = y0
    clawdata.upper[1] = y2

    # =======================================================
    # TIME
    # =======================================================
    clawdata.num_eqn = num_eqn
    clawdata.num_aux = 10

    clawdata.t0 = 0.0
    clawdata.tfinal = 120.0

    clawdata.output_style = 1
    clawdata.num_output_times = 12
    clawdata.output_format = "ascii"

    # =======================================================
    # NUMERICS (SLOWED DOWN)
    # =======================================================
    clawdata.dt_variable = True
    clawdata.dt_initial = 5e-5     # slower evolution
    clawdata.cfl_desired = 0.35
    clawdata.cfl_max = 0.5
    clawdata.steps_max = 250000

    clawdata.order = 2
    clawdata.dimensional_split = "unsplit"
    clawdata.transverse_waves = 2
    clawdata.num_waves = 5
    clawdata.limiter = [4] * 5
    clawdata.use_fwaves = True

    clawdata.num_ghost = 2

    clawdata.bc_lower[0] = "extrap"
    clawdata.bc_upper[0] = "extrap"
    clawdata.bc_lower[1] = "extrap"
    clawdata.bc_upper[1] = "extrap"

    # =======================================================
    # AMR (kept simple for stability)
    # =======================================================
    amr = rundata.amrdata
    amr.amr_levels_max = 1
    amr.refinement_ratios_x = [1]
    amr.refinement_ratios_y = [1]
    amr.refinement_ratios_t = [1]
    amr.aux_type = ['center'] * 10

    # =======================================================
    # PHYSICS (OSO / VISCOUS STYLE)
    # =======================================================
    geo = rundata.geo_data
    geo.gravity = 32.174
    geo.friction_forcing = True
    geo.manning_coefficient = 0.02   # ↑ resistance
    geo.dry_tolerance = 5e-4

    dclaw = rundata.dclaw_data

    dclaw.rho_f = 1000.0
    dclaw.rho_s = 2700.0

    # Dense, sluggish material
    dclaw.m0 = 0.70
    dclaw.mref = 0.68
    dclaw.m_crit = 0.70

    # Strong internal friction → short runout
    dclaw.mu = 0.4
    dclaw.phi = 34.0

    # Reduce fluidization → more "lava-like"
    dclaw.alpha_c = 0.002

    dclaw.src2method = 2
    dclaw.alphamethod = 1

    # =======================================================
    # INPUT FILES
    # =======================================================
    rundata.topo_data.topofiles = [
        [3, 1, 1, 0, 1e10, 'surface_topo.tt3']
    ]

    rundata.qinitdclaw_data.qinitfiles = [
        [3, i_eta, 'eta_init.tt3'],
        [3, i_hm, 'thickness.tt3']
    ]

    rundata.auxinitdclaw_data.auxinitfiles = []

    # =======================================================
    # FGOUT (focused near source)
    # =======================================================
    from clawpack.geoclaw import fgout_tools  # type: ignore

    fgout = fgout_tools.FGoutGrid()
    fgout.fgno = 1
    fgout.point_style = 2
    fgout.output_format = "ascii"

    fgout.nx = 120
    fgout.ny = 120

    fgout.x1 = x0 + 150 * dx
    fgout.y1 = y0 + 150 * dx
    fgout.x2 = fgout.x1 + fgout.nx * dx
    fgout.y2 = fgout.y1 + fgout.ny * dx

    fgout.tstart = 0.0
    fgout.tend = clawdata.tfinal
    fgout.nout = 25

    rundata.fgout_data.fgout_grids.append(fgout)

    return rundata


if __name__ == "__main__":
    rundata = setrun()
    rundata.write()
