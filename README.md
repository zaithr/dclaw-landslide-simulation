# D-Claw Landslide Simulation Pipeline

![Python](https://img.shields.io/badge/Python-3.x-blue)
![GIS](https://img.shields.io/badge/GIS-Raster-green)
![Model](https://img.shields.io/badge/Model-D--Claw-orange)

A complete geospatial pipeline for simulating landslide and debris-flow dynamics using **D-Claw**, from DEM preprocessing to TT3 input generation and flow visualization.

---

## 🧠 Overview

This project builds an end-to-end workflow combining **GIS processing + numerical modeling**.

The pipeline covers:

- DEM resampling  
- Source area rasterization  
- Thickness generation  
- Surface elevation (η) computation  
- Conversion to D-Claw TT3 format  
- Numerical simulation  
- Visualization of flow depth and velocity  


## 📊 Input Data (Not Included)

This repository does **not include raw datasets**.

### Required inputs:
- DEM (GeoTIFF)
- Source area polygon (Shapefile)

### Requirements:
- Same CRS  
- Same resolution  
- Same spatial extent  

---

## ⚙️ Workflow

### Step 1: Resample DEM

```bash
python scripts/resample_raster.py \
  --input data/dem.tif \
  --output data/dem_resampled.tif \
  --scale 8 \
  --method average
 
Step 2: Generate Thickness Raster
python scripts/make_thickness.py \
  --dem data/dem_resampled.tif \
  --mask data/source.shp \
  --output data/thickness.tif \
  --thickness 18

Step 3: Generate η and TT3 Inputs
python scripts/make_eta_and_tt3.py \
  --dem data/dem_resampled.tif \
  --thickness data/thickness.tif \
  --outdir dclaw/

##Outputs:

surface_topo.tt3
thickness.tt3
eta_init.tt3
Step 4: Run D-Claw
make .data
make .output
make .plots
🔬 Model Description

D-Claw is a depth-averaged two-phase flow model designed for:

debris flows
landslide runout
granular-fluid mixtures

This implementation focuses on:

terrain-controlled flow
high-friction (slow) regimes
viscous / lava-like behavior
⚙️ Key Parameters (setrun.py)

Important parameters controlling behavior:

mu → basal friction
phi → internal friction
m0, mref → solid fraction
dt_initial → numerical stability

These influence:

mobility
runout distance
flow coherence
⚠️ Limitations
Simulates post-failure flow only
Does NOT model:
slope failure initiation
pore pressure evolution
entrainment or erosion
material heterogeneity

👉 Results are qualitative unless calibrated with real data.

📈 Outputs
Flow depth maps
Velocity fields
Terrain + flow overlays (hillshade)
Time-series simulation frames

## 🧪 Example Results

![image alt](https://github.com/zaithr/dclaw-landslide-simulation/blob/4de5d94360b38a3b3dcca471b3d7d811c9e3bacd/dclaw_4k_very_slow.gif)


🛠️ Requirements

Install dependencies:
pip install -r requirements.txt
requirements.txt
rasterio
numpy
fiona
shapely
scipy
matplotlib


🚀 Getting Started
Prepare DEM and shapefile
Run preprocessing scripts
Generate TT3 inputs
Run D-Claw simulation
Visualize results

📌 Future Improvements
Calibration using real landslide data
Integration with rainfall datasets
Coupling with slope stability models
Automated pipeline execution


👤 Author
Zaithr
