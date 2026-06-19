# SAR data, algorithms & open-source stack

Two ways to apply Synthetic Aperture Radar to OpenGoldSDR: (A) download existing **satellite** SAR
over the Georgia Gold Belt and process it, and (B) form images from our own **ground-based rail SAR**
(`Ground_Based_Rail_SAR.md`). Both share the same math.

## Patent / clean-room note
Biondi's "Tomographic Doppler Imaging" pipeline is patent-pending (WIPO submission **12077659**). A
patent protects **his specific code & commercial use — not the underlying physics/math.** Writing an
independent algorithm from open building blocks for **private research/personal use** is fine. We keep
OpenGoldSDR transparent and built only on open tools, never on his code.

## A) Free satellite SAR datasets
- **Alaska Satellite Facility (ASF) / Sentinel-1** (NASA + ESA) — the holy grail of free SAR. Download
  raw **Single Look Complex (SLC)** scenes globally, incl. historical passes over our target areas.
- **Capella Space** and **Umbra** Open Data Programs (GitHub/AWS, Creative Commons) — high-res (down to
  ~25 cm) spotlight SAR for free. (Biondi explicitly used Capella + Italy's COSMO-SkyMed.)

## B) Open-source processing stack (Python-first)
- **ESA SNAP (Sentinel Application Platform)** + **GMTSAR** — full InSAR processing toolchains.
- **MintPy** (Miami InSAR Time-series in Python) — time-series of radar phase; tweak its filters to
  isolate micro-vibration / coherence change rather than tectonic motion.
- **Xarray-Sentinel** + **Sarsen** — ingest Copernicus Sentinel-1 products straight into Python arrays
  and terrain-correct them.
- **RadarCODE/awesome-sar** (GitHub) — curated master list of SAR simulators, image-formation toolkits,
  and noise-correction scripts to dissect.

## The algorithm — three pillars to replicate (independently)
1. **Phase autofocus (measure micro-vibration):** still ground returns a uniform phase; natural sub-Hz
   surface motion injects phase errors. Implement **Phase Gradient Autofocus (PGA)** or **Entropy-Based
   Autofocus (EBA)** in Python to recover those.
2. **Coherence over time (ground elasticity):** stack multiple passes of the same coordinate; a
   **time-series cross-correlation** flags where surface radar coherence drops/spikes vs. baseline
   terrain — voids, dense quartz, loose alluvium behave differently.
3. **Wave-structure inversion (2D → 3D depth):** the hard step. Assume a soil baseline density (Georgia
   red clay vs. Piedmont saprolite) and solve the **inverse problem** for the depth that would produce
   the observed phase-shift pattern.

For our own rail data the front end is simpler classic SAR **back-projection** — see
`software/rail_sar/backprojection.py` (image formation from IQ + rail position) and
`software/rail_sar/rail_control.py` (stepper stepping + capture sync).

## Data fusion layer (the real near-term value)
Cross-reference radar anomalies with public geology so anomalies become predictive:
- **USGS MRDS** (Mineral Resources Data System) — exact coords of historical mines (Augusta / Clarks
  Hill / Piedmont–Slate Belt transitions).
- **USGS 3DEP LiDAR** — strip vegetation digitally to reveal unrecorded pits, hand-dug trenches, and
  creek benches where gold concentrates.
- Local agents ingest SDR/IQ logs + GPS + USGS shapefiles and flag where an RF-attenuation anomaly lands
  on a known geologic contact. Repeatability rule: strict grid, constant speed, baseline noise, re-verify.
