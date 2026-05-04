"""
Generate thickness raster for D-Claw simulation

Inputs:
- DEM (GeoTIFF)
- Source area polygon (Shapefile)

Output:
- Thickness raster aligned to DEM grid
"""

import rasterio
from rasterio.features import rasterize
import fiona
from shapely.geometry import shape, mapping
import numpy as np
import argparse
import matplotlib.pyplot as plt


# -----------------------------
# ARGUMENTS
# -----------------------------
parser = argparse.ArgumentParser(description="Generate thickness raster from source mask")
parser.add_argument("--dem", required=True, help="Path to DEM (GeoTIFF)")
parser.add_argument("--mask", required=True, help="Path to source polygon (Shapefile)")
parser.add_argument("--output", default="thickness.tif", help="Output thickness raster")
parser.add_argument("--thickness", type=float, default=18.0, help="Thickness value (same unit as DEM)")

args = parser.parse_args()


# -----------------------------
# STEP 1: READ DEM
# -----------------------------
with rasterio.open(args.dem) as dem:
    meta = dem.meta.copy()
    transform = dem.transform
    width = dem.width
    height = dem.height


# -----------------------------
# STEP 2: READ SHAPEFILE
# -----------------------------
geoms = []
with fiona.open(args.mask, "r") as shp:
    for feature in shp:
        geom = shape(feature["geometry"])
        if not geom.is_valid:
            geom = geom.buffer(0)
        geoms.append(mapping(geom))


# -----------------------------
# STEP 3: CREATE MASK
# -----------------------------
mask = rasterize(
    [(g, 1) for g in geoms],
    out_shape=(height, width),
    transform=transform,
    fill=0,
    all_touched=False,
    dtype="uint8"
)


# -----------------------------
# STEP 4: BUILD THICKNESS
# -----------------------------
thickness = np.zeros((height, width), dtype="float32")
thickness[mask == 1] = args.thickness

# enforce strict zero outside
thickness[mask == 0] = 0.0


# -----------------------------
# STEP 5: SAVE OUTPUT
# -----------------------------
meta.update({
    "dtype": "float32",
    "count": 1,
    "nodata": 0.0
})

with rasterio.open(args.output, "w", **meta) as dst:
    dst.write(thickness, 1)


# -----------------------------
# DEBUG
# -----------------------------
print("✅ Thickness raster created")
print("Unique values:", np.unique(thickness))
print("Non-zero cells:", np.sum(thickness > 0))


# -----------------------------
# PLOT (optional)
# -----------------------------
plt.figure(figsize=(8, 6))
plt.imshow(thickness, origin="upper")
plt.colorbar(label="Thickness")
plt.title("Thickness Raster")
plt.show()