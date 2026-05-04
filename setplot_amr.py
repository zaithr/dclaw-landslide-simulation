#!/usr/bin/env python3
"""
Clean plotting for D-Claw (safe + useful)
"""

import matplotlib as mpl
from setinput import x0, x2, y0, y2

xlimits = [x0, x2]
ylimits = [y0, y2]


def setplot(plotdata=None):
    import clawpack.dclaw.plot as dplot

    if plotdata is None:
        from clawpack.visclaw.data import ClawPlotData
        plotdata = ClawPlotData()

    plotdata.clearfigures()
    plotdata.format = "binary"

    # =========================
    # DEPTH
    # =========================
    plotfigure = plotdata.new_plotfigure(name="Depth", figno=0)
    plotaxes = plotfigure.new_plotaxes()

    plotaxes.title = "Flow Depth"
    plotaxes.scaled = True
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits

    plotitem = plotaxes.new_plotitem(plot_type="2d_imshow")
    plotitem.plot_var = dplot.depth
    plotitem.add_colorbar = True
    plotitem.colorbar_label = "Depth (ft)"
    plotitem.imshow_cmap = "Purples"
    plotitem.imshow_norm = mpl.colors.Normalize(vmin=0, vmax=None)

    # =========================
    # VELOCITY (optional but useful)
    # =========================
    plotfigure = plotdata.new_plotfigure(name="Velocity", figno=1)
    plotaxes = plotfigure.new_plotaxes()

    plotaxes.title = "Velocity"
    plotaxes.scaled = True
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits

    plotitem = plotaxes.new_plotitem(plot_type="2d_imshow")
    plotitem.plot_var = dplot.velocity_magnitude
    plotitem.add_colorbar = True
    plotitem.colorbar_label = "Velocity (ft/s)"
    plotitem.imshow_cmap = "Greens"
    plotitem.imshow_norm = mpl.colors.Normalize(vmin=0, vmax=10)

    # =========================
    # OUTPUT
    # =========================
    plotdata.printfigs = True
    plotdata.print_format = "png"
    plotdata.html = True
    plotdata.parallel = True

    return plotdata