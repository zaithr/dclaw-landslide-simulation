"""
Resample a raster (e.g., DEM) to a coarser resolution

Input:
- GeoTIFF raster

Output:
- Resampled GeoTIFF
"""

import rasterio
from rasterio.enums import Resampling
import argparse
import os


# -----------------------------
# ARGUMENTS
# -----------------------------
parser = argparse.ArgumentParser(description="Resample raster to coarser resolution")
parser.add_argument("--input", required=True, help="Input raster (GeoTIFF)")
parser.add_argument("--output", default="resampled.tif", help="Output raster")
parser.add_argument("--scale", type=int, default=4, help="Downsampling factor (e.g., 4 = 4x coarser)")
parser.add_argument("--method", default="average", choices=["average", "nearest"], help="Resampling method")

args = parser.parse_args()


# -----------------------------
# SELECT RESAMPLING METHOD
# -----------------------------
resampling_method = {
    "average": Resampling.average,
    "nearest": Resampling.nearest
}[args.method]


# -----------------------------
# RESAMPLE
# -----------------------------
with rasterio.open(args.input) as src:
    data = src.read(
        out_shape=(
            src.count,
            int(src.height / args.scale),
            int(src.width / args.scale)
        ),
        resampling=resampling_method
    )

    transform = src.transform * src.transform.scale(
        (src.width / data.shape[-1]),
        (src.height / data.shape[-2])
    )

    meta = src.meta.copy()
    meta.update({
        "height": data.shape[1],
        "width": data.shape[2],
        "transform": transform
    })

    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    with rasterio.open(args.output, "w", **meta) as dst:
        dst.write(data)


print("✅ Resampling complete")
print(f"Method: {args.method}")
print(f"Scale factor: {args.scale}")