#!/usr/bin/env python3
"""
setinput.py (ROBUST TT3 VERSION - FIXED)

✔ Handles both correct and broken TT3 headers
✔ Safe parsing
✔ Builds domain aligned with GeoClaw grid
✔ Avoids edge overlap issues
"""

import os

# =======================================================
# FILE PATHS
# =======================================================

TOPO_TT3 = "surface_topo.tt3"
THICKNESS_TT3 = "thickness.tt3"

# Small buffer to avoid boundary overlap
eps = 1e-6


# =======================================================
# READ TT3 HEADER (ROBUST)
# =======================================================

def read_tt3_header(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ File not found: {path}")

    with open(path, "r") as f:
        lines = [f.readline().strip() for _ in range(6)]

    try:
        # --- Handle case: "ncols nrows" on same line ---
        first_line = lines[0].split()
        if len(first_line) == 2:
            ncols = int(first_line[0])
            nrows = int(first_line[1])
            xll   = float(lines[1])
            yll   = float(lines[2])
            dx    = float(lines[3])
            nodata = float(lines[4])
        else:
            # Normal correct format
            ncols = int(lines[0])
            nrows = int(lines[1])
            xll   = float(lines[2])
            yll   = float(lines[3])
            dx    = float(lines[4])
            nodata = float(lines[5])

    except Exception as e:
        raise ValueError(f"❌ Invalid TT3 header in {path}: {e}")

    # ===================================================
    # DOMAIN (GeoClaw-safe)
    # ===================================================

    # Lower-left (slightly inside)
    x0 = xll + eps
    y0 = yll + eps

    # Upper-right (slightly inside)
    x2 = xll + (ncols - 1) * dx - eps
    y2 = yll + (nrows - 1) * dx - eps

    return x0, x2, y0, y2, dx, ncols, nrows


# =======================================================
# DOMAIN FROM TOPO
# =======================================================

x0, x2, y0, y2, dx, nx, ny = read_tt3_header(TOPO_TT3)

print("\n===== DOMAIN FROM TT3 =====")
print(f"Grid size : {nx} x {ny}")
print(f"Cellsize  : {dx}")
print(f"X range   : {x0:.3f} → {x2:.3f}")
print(f"Y range   : {y0:.3f} → {y2:.3f}")
print("===========================\n")


# =======================================================
# OPTIONAL SOURCE REGION (CENTER BOX)
# =======================================================

xc = 0.5 * (x0 + x2)
yc = 0.5 * (y0 + y2)

span = 0.2 * (x2 - x0)

xl1 = xc - span / 2
xl2 = xc + span / 2
yl1 = yc - span / 2
yl2 = yc + span / 2


# =======================================================
# ROTATION FLAG (KEEP FALSE)
# =======================================================

rotate = False


# =======================================================
# DEBUG
# =======================================================

if __name__ == "__main__":
    print("✅ TT3 input loaded successfully.")