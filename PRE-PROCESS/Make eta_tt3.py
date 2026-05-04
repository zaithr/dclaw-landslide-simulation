# make_eta_and_tt3.py

"""
Generate eta (surface) raster and convert inputs to TT3 format for D-Claw

Inputs:
- DEM (GeoTIFF)
- Thickness raster (GeoTIFF)

Outputs:
- eta.tif
- surface_topo.tt3
- thickness.tt3
- eta_init.tt3
"""

import rasterio
import numpy as np
import argparse
import os
import matplotlib.pyplot as plt


# -----------------------------
# ARGUMENTS
# -----------------------------
parser = argparse.ArgumentParser(description="Prepare D-Claw inputs (eta + TT3)")
parser.add_argument("--dem", required=True, help="Path to DEM (GeoTIFF)")
parser.add_argument("--thickness", required=True, help="Path to thickness raster")
parser.add_argument("--outdir", default="outputs", help="Output directory")

args = parser.parse_args()

os.makedirs(args.outdir, exist_ok=True)


# -----------------------------
# TT3 CONVERSION FUNCTION
# -----------------------------
def tif_to_tt3(input_tif, output_tt3):
    with rasterio.open(input_tif) as src:
        data = src.read(1)
        transform = src.transform

        nrows, ncols = data.shape
        xll = transform[2]
        yll = transform[5] + nrows * transform[4]
        dx = transform[0]
        nodata = -9999

        with open(output_tt3, "w") as f:
            f.write(f"{ncols}\n")
            f.write(f"{nrows}\n")
            f.write(f"{xll}\n")
            f.write(f"{yll}\n")
            f.write(f"{dx}\n")
            f.write(f"{nodata}\n")

            for row in data:
                f.write(" ".join(map(str, row)) + "\n")


# -----------------------------
# READ INPUTS
# -----------------------------
with rasterio.open(args.dem) as topo_src:
    topo = topo_src.read(1)
    meta = topo_src.meta.copy()

with rasterio.open(args.thickness) as thk_src:
    thickness = thk_src.read(1)


# -----------------------------
# BUILD ETA
# -----------------------------
eta = topo + thickness

# enforce strict equality outside source
eta[thickness == 0] = topo[thickness == 0]


# -----------------------------
# SAVE ETA
# -----------------------------
eta_path = os.path.join(args.outdir, "eta.tif")

meta.update(dtype="float32", count=1, nodata=0.0)

with rasterio.open(eta_path, "w", **meta) as dst:
    dst.write(eta.astype("float32"), 1)


# -----------------------------
# DEBUG CHECK
# -----------------------------
diff = eta - topo

print("Max diff:", diff.max())
print("Min diff:", diff.min())
print("Cells > 0:", np.sum(diff > 0))


# -----------------------------
# CONVERT TO TT3
# -----------------------------
tif_to_tt3(args.dem, os.path.join(args.outdir, "surface_topo.tt3"))
tif_to_tt3(args.thickness, os.path.join(args.outdir, "thickness.tt3"))
tif_to_tt3(eta_path, os.path.join(args.outdir, "eta_init.tt3"))


# -----------------------------
# PLOT
# -----------------------------
plt.figure(figsize=(14, 10))

plt.subplot(2, 2, 1)
plt.imshow(topo, cmap="terrain", origin="upper")
plt.title("Topography")

plt.subplot(2, 2, 2)
plt.imshow(thickness, origin="upper")
plt.title("Thickness")

plt.subplot(2, 2, 3)
plt.imshow(eta, cmap="terrain", origin="upper")
plt.title("Eta")

plt.subplot(2, 2, 4)
plt.imshow(diff, origin="upper")
plt.title("Eta - Topo")

plt.tight_layout()
plt.show()