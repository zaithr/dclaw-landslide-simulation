#!/usr/bin/env python3
"""
setplot.py - PRO D-Claw plotting (grayscale hillshade + clean flow overlay)
"""

import numpy as np
import matplotlib as mpl
from setinput import x0, x2, y0, y2

# ======================================================
# GLOBAL STYLE (publication quality)
# ======================================================
mpl.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times"],
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "axes.linewidth": 0.8,
    "xtick.direction": "in",
    "ytick.direction": "in",

    # 🔥 HIGH RES OUTPUT (FIXED)
    "savefig.dpi": 300,
    "savefig.bbox": "tight"
})

# Domain limits
xlimits = [x0, x2]
ylimits = [y0, y2]


def format_k(x, pos):
    val = x / 1000
    if val.is_integer():
        return f"{int(val)}k"
    return f"{val:.1f}k"


def setplot(plotdata=None):
    import clawpack.dclaw.plot as dplot

    if plotdata is None:
        from clawpack.visclaw.data import ClawPlotData
        plotdata = ClawPlotData()

    plotdata.clearfigures()
    plotdata.format = "binary"

    # ======================================================
    # HILLSHADE FUNCTION
    # ======================================================
    def hillshade(Z):
        dy, dx = np.gradient(Z)

        slope = np.pi / 2.0 - np.arctan(np.sqrt(dx * dx + dy * dy))
        aspect = np.arctan2(-dx, dy)

        azimuth = np.pi / 3.5
        altitude = np.pi / 4.5

        shaded = (
            np.sin(altitude) * np.sin(slope)
            + np.cos(altitude) * np.cos(slope) * np.cos(azimuth - aspect)
        )

        shaded = (shaded - shaded.min()) / (shaded.max() - shaded.min())
        shaded = shaded ** 1.6

        return shaded

    # ======================================================
    # FIGURE SETUP
    # ======================================================
    plotfigure = plotdata.new_plotfigure(name="Flow + Terrain", figno=0)
    plotfigure.kwargs = {"figsize": (9, 7)}

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.scaled = True
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits

    plotaxes.title = "D-Claw Simulated Debris Flow"
    plotaxes.xlabel = "Easting (m)"
    plotaxes.ylabel = "Northing (m)"

    # ======================================================
    # BACKGROUND: HILLSHADE
    # ======================================================
    def topo_hillshade(current_data):
        topo = dplot.topo(current_data)
        return hillshade(topo)

    bg = plotaxes.new_plotitem(plot_type="2d_imshow")
    bg.plot_var = topo_hillshade
    bg.imshow_cmap = "Greys"
    bg.imshow_alpha = 1.0
    bg.add_colorbar = False
    bg.kwargs = {"interpolation": "bilinear"}

    # ======================================================
    # FLOW DEPTH OVERLAY
    # ======================================================
    def masked_depth(current_data):
        h = dplot.depth(current_data)
        return np.ma.masked_where(h < 0.1, h)

    flow = plotaxes.new_plotitem(plot_type="2d_imshow")
    flow.plot_var = masked_depth
    flow.imshow_cmap = "magma"
    flow.imshow_alpha = 0.85
    flow.add_colorbar = True
    flow.colorbar_label = "Flow Depth (ft)"
    flow.kwargs = {"interpolation": "bilinear"}

    # ======================================================
    # CONTOURS (SUBTLE)
    # ======================================================
    contour = plotaxes.new_plotitem(plot_type="2d_contour")
    contour.plot_var = dplot.topo
    contour.contour_levels = 12
    contour.amr_contour_colors = ['k']
    contour.kwargs = {"linewidths": 0.25, "alpha": 0.3}

    # ======================================================
    # OUTPUT SETTINGS
    # ======================================================
    plotdata.printfigs = True
    plotdata.print_format = "png"

    plotdata.print_framenos = 'all'
    plotdata.print_fignos = 'all'

    plotdata.html = True
    plotdata.parallel = True

    return plotdata