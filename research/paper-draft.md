# Low-Cost Synthetic Aperture Radar for Subsurface Anomaly Mapping in Gold-Bearing Terrain: A Garage-Scale Rail-SAR and Open-Data Fusion Approach

**Draft — OpenGoldSDR research note. Version 0.1, 2026-06-18.**

> Status: working draft for community review. This is anomaly-mapping research, **not** a gold detector. Every quantitative claim below is sourced; speculative steps are flagged as such.

---

## Abstract

We propose and motivate a low-cost, open-source synthetic aperture radar (SAR) instrument and processing pipeline for mapping subsurface dielectric and structural anomalies in historically gold-bearing terrain, using the Georgia Gold Belt as the initial study area. The system follows the well-established ground-based SAR (GB-SAR) paradigm — a radar front end stepped along a precisely controlled linear rail to synthesize a large aperture — built from commodity software-defined radio (SDR) / FMCW hardware in the spirit of the MIT "Coffee Can Radar" [1]. Image formation uses time-domain back-projection [2], and a three-pillar analysis layer adapts established techniques (phase-gradient / minimum-entropy autofocus [3,4], interferometric coherence time-series [5,6], and an under-determined wave-structure inversion) to flag boundaries where the dielectric contrast between quartz veins (relative permittivity ε_r ≈ 4.5) and moist clay/saprolite (ε_r ≈ 5–10 dry, rising sharply when wet, vs. ε_r ≈ 80 for water) [7,8] is detectable. Detected anomalies are fused with public geology — USGS Mineral Resources Data System (MRDS) mine coordinates and 3DEP LiDAR microtopography [9,10] — so that radar features can be ranked against known mineralized contacts. We are explicit that the method maps *anomalies correlated with the geologic settings gold associates with*, not gold itself, and we discuss the dominant confounder (soil moisture) [7], honest limitations of the inversion step, and land-access / ethics constraints. The contribution is an independent, open implementation built only on open tools and public physics, distinct from any patented commercial pipeline.

---

## 1. Introduction and motivation

Gold in the southern Appalachian Piedmont is overwhelmingly *structurally controlled*: it occurs in hydrothermal gold-bearing quartz veins and sulfide bodies hosted in metavolcanic and metasedimentary rock. The Dahlonega belt of northern Georgia alone produced on the order of 500,000 ounces (~14,000 kg) of gold between 1838 and 1941, with the Consolidated mine sitting on one of the world's largest gold-bearing quartz veins [11]. The adjacent Carolina Slate Belt — ~600 mi (970 km) of weakly-to-moderately metamorphosed Avalonian rock from Georgia to Virginia — is regarded by the USGS as a frontier still thought to host significant undiscovered gold and silver [12,13]. The operative geologic rule is blunt: *where the quartz was, the gold was; where the gold was, placers formed downstream* [11].

This structural control is the opening for remote sensing. A consumer radio cannot detect a gold flake through soil — but the *host structures* (quartz veins, mineralized contacts, voids, old workings, wet faults) differ in dielectric and geometric properties from the surrounding red clay and saprolite, and dielectric contrast is exactly what radar responds to [7,8]. The research question of OpenGoldSDR is therefore not "can radio find gold?" but "can a cheap, repeatable, GPS-tagged radar survey, fused with public geology, narrow down *where to physically test next*?"

The inspiration is satellite SAR Doppler tomography — the line of work (Biondi et al.) claiming subsurface structure beneath the Great Pyramid from spaceborne SAR vibration analysis [14]. Those claims are contested and the spaceborne instrument is out of reach; **we deliberately do not rely on their specific results or code.** What transfers is only the textbook physics: synthesizing a long aperture by moving a radar along a known path. That physics is identical at garage scale and is the basis of decades of conventional GB-SAR deformation monitoring [2,15]. Our aim is a transparent, falsifiable, open instrument that domain experts can tear apart.

---

## 2. Related work

**Low-cost coherent radar.** The MIT Lincoln Laboratory / Charvat "Coffee Can Radar" (MIT OpenCourseWare RES.LL-003) demonstrates a laptop-based FMCW radar measuring range, Doppler, and SAR images from commodity parts, and is the canonical entry point for hobbyist coherent radar [1]. We adopt its FMCW + IQ-logging architecture and replace the cantenna/manual scan with an SDR/FMCW front end on a motorized rail.

**Ground-based SAR (GB-SAR).** Stepping two horn antennas along a linear rail to synthesize an aperture is the conventional GB-SAR method, widely used for deformation monitoring of dams, slopes, bridges and buildings, with image formation typically via the back-projection (BP) algorithm operating on corner-reflector scenes [2,15,16]. Arc and array variants exist with frequency-domain / wavenumber imaging [2,16], but linear-rail BP is the simplest faithful baseline and what we target first.

**SAR autofocus.** Phase errors from imperfect motion knowledge are corrected by autofocus. Phase Gradient Autofocus (PGA) — Wahl, Eichel, Ghiglia, Jakowatz (1994) — is the standard model-free estimator for spotlight SAR phase error [3]. Minimum-entropy / image-sharpness autofocus, including hybrids with PGA, is the other major family, using image entropy as the focus-quality objective [4]. We treat motion-induced phase error on our rail as the same problem.

**InSAR coherence and time-series.** Repeat-pass interferometric coherence drops where the scene changes between passes; this is exploited for change detection, and temporal coherence underpins time-series tools such as MintPy (small-baseline stacks → line-of-sight displacement) and the ASF HyP3 InSAR products built on Sentinel-1 SLC data [5,6,17]. We repurpose coherence not for tectonic motion but for *baseline-vs-anomaly* discrimination of ground response.

**GPR / dielectric petrophysics.** GPR work establishes that subsurface dielectric permittivity is dominated by water content and mineral composition, with strong frequency dependence and the well-known trade between penetration depth and resolution [7,8,18]. This grounds both our frequency choice and our headline confounder (moisture).

**Public geospatial data.** USGS MRDS provides downloadable (incl. shapefile) mine/deposit locations and commodity records [9], and USGS 3DEP delivers LiDAR-derived bare-earth microtopography [10]; both are standard exploration inputs we fuse with radar.

---

## 3. Method

### 3.1 Instrument: rail = aperture

A stationary antenna images a tiny patch; a coherent radar **stepped along a precise rail** records phase and amplitude at many positions, which back-projection combines into one synthetic antenna as long as the rail [2]. Cross-range resolution improves with rail length and step density, so **position accuracy is the dominant engineering requirement** — hence a stepper + lead-screw/belt + homing end-stop for repeatable, known increments.

*Tier-1 (garage, ~$250–700):* FMCW radar module **or** clean upconverter + SDR (HackRF / RTL-SDR v4); 2020/2040 aluminum extrusion + NEMA17 stepper + GT2 belt or lead screw + end-stop; DIY copper-horn/waveguide or PCB-patch antennas; Raspberry Pi or laptop logging IQ vs. rail position.

*Tier-2 (no rail, deeper, ~$1,200–2,500):* VLF-EM induction (~10 kHz) on a walked grid with a high-dynamic-range SDR (LimeSDR/BladeRF) + LNA, power amp/filters, shielded loop coils, and cm-accurate RTK GPS (u-blox ZED-F9P) to tag every reading — the classic geophysics path done with SDR.

**Frequency reality.** Wi-Fi bands (2.4/5 GHz) attenuate within centimeters of damp soil. We choose an FMCW band balancing penetration against resolution per GPR petrophysics, and treat soil moisture as confounder #1 [7,8,18].

### 3.2 Image formation: back-projection

For our own rail data the front end is classic time-domain SAR back-projection: for each pixel in a ground grid, coherently sum the range-compressed return from every rail position with the phase term corresponding to that position-to-pixel two-way delay [2]. BP is chosen over frequency-domain methods because it natively handles a known-but-irregular sampling track and a near-field geometry — the realistic case on a short, imperfect garage rail. Reference skeletons live in `software/rail_sar/backprojection.py` (image formation) and `software/rail_sar/rail_control.py` (stepper stepping + capture sync).

### 3.3 The three-pillar analysis (independent re-implementation)

We re-implement, from open building blocks, three analyses inspired by the satellite-tomography literature — built only on public physics, never on any patented pipeline:

1. **Phase autofocus (micro-motion / motion-error recovery).** Still ground returns near-uniform phase; rail-position error and natural sub-Hz surface motion inject phase errors that blur the image. We implement PGA [3] and/or entropy-based autofocus [4] in Python to estimate and remove them. *Defensible:* these are standard, model-free SAR phase-error correctors.

2. **Coherence over repeat passes (ground response).** Stack multiple passes of the same coordinates and compute interferometric/temporal coherence; map where coherence drops or spikes relative to baseline terrain, following established InSAR coherence-change practice [5,6]. Different materials (dense quartz, voids, loose alluvium) and moisture states change scene stability differently. *Defensible:* repurposing a validated coherence metric, with the caveat that vegetation and weather are powerful confounders [5].

3. **Wave-structure inversion (2D → depth).** The hard, honest step: assume a soil baseline permittivity (Georgia red clay vs. Piedmont saprolite) and solve the inverse problem for the depth/geometry that would produce the observed phase pattern. *Caveat (explicit):* this inverse problem is **under-determined and non-unique** — many subsurface configurations and moisture profiles fit one phase pattern. We treat its output as a hypothesis-ranking heuristic, not a measurement, and require independent corroboration (pillar 2, geology fusion, or ground truth).

### 3.4 Data-fusion layer (the near-term value)

Radar anomalies only become useful when cross-referenced with public geology. We overlay anomalies on:
- **USGS MRDS** — coordinates/commodity of historical mines (Augusta / Clarks Hill / Piedmont–Slate Belt transitions) [9];
- **USGS 3DEP LiDAR** — bare-earth microtopography to digitally strip vegetation and reveal unrecorded pits, hand-dug trenches, and creek benches where placer gold concentrates [10,11].

An anomaly that lands on a known mineralized contact or an unrecorded working is promoted; an isolated anomaly with no geologic support is deprioritized. For comparison/validation we can also process free satellite SAR over the belt — Sentinel-1 SLC via ASF, plus Capella / Umbra open-data spotlight scenes — with the open Python stack (ESA SNAP, GMTSAR, MintPy, Xarray-Sentinel/Sarsen) [6,17].

---

## 4. Proposed experiments

We propose a staged, falsification-first program. Each stage has a pass/fail criterion so the method can be killed early if it fails.

- **E0 — Controlled point-target (instrument truth).** Image a single corner reflector on bare ground at known range/cross-range. *Pass:* BP places it within one resolution cell and PGA improves entropy. This validates geometry and autofocus before any geology claim [2,3].
- **E1 — Buried dielectric phantom.** Bury a known high-contrast target (e.g., a quartz block / metal plate / air void) at measured depth in local red clay; image dry and after wetting. *Pass:* the target is detectable when dry, and the wet-vs-dry comparison quantifies the moisture confounder [7,8].
- **E2 — Repeat-pass coherence baseline.** Survey an undisturbed reference plot across multiple days/weather. *Pass:* characterize natural coherence variability so a real "anomaly" must exceed this baseline [5,6].
- **E3 — Known-mine blind test.** Survey transects across a *documented* MRDS quartz-vein contact without telling the operator where it is; check whether radar/coherence anomalies co-locate with the mapped vein [9,11]. *Pass:* anomalies align with the contact above chance.
- **E4 — Satellite cross-check.** Process Sentinel-1/Capella over the same coordinates and test whether spaceborne coherence/amplitude anomalies correlate with ground-rail anomalies [6,17].
- **E5 — Prospective ranking + ground truth.** Produce a ranked anomaly list over a permitted parcel, then physically test (pan/dig/XRF) the top vs. bottom of the list. *Pass:* top-ranked sites show mineralization indicators more often than bottom-ranked.

Repeatability protocol throughout: strict grid, constant speed, recorded baseline noise, RTK/GPS tags, and re-verification of every anomaly.

---

## 5. Limitations and honest caveats

- **This is anomaly mapping, not gold detection.** No step in the pipeline detects gold. At best we map dielectric/structural anomalies statistically associated with the *settings* gold occurs in. Treat all output as "where to look," not "what is there."
- **Moisture dominates everything.** Soil water content is the largest driver of dielectric permittivity and of GPR/coherence response [7,8]. A wet quartz vein and a damp clay lens can look alike; dry-vs-wet differencing (E1) is mandatory, not optional.
- **The inversion is non-unique.** §3.3 pillar 3 is an ill-posed inverse problem; its depth estimates are hypotheses, not measurements, and must never be reported as confirmed structure.
- **Penetration vs. resolution trade.** Bands that resolve fine structure penetrate poorly in damp soil; bands that penetrate resolve coarsely [18]. A garage rail SAR is inherently shallow/high-res or deep/low-res, not both.
- **Confounders are everywhere.** Vegetation, metal trash, buried infrastructure, fences, and weather all produce anomalies [5]. Most anomalies will be uninteresting; the geology-fusion layer exists to suppress false positives.
- **Satellite-tomography claims are contested.** The Giza-subsurface SAR results that inspired this line of work are disputed by Egyptologists and radar specialists [14]; we borrow only standard physics, not their conclusions, and present nothing here as validated by them.
- **Garage hardware is noisy.** Rail position error, clock drift, antenna coupling, and low transmit power all degrade coherent imaging; E0/E2 exist precisely to bound these.

---

## 6. Ethics, legality, and land-access

- **Permission first.** Surveying or digging requires landowner permission on private land and the correct permits on public land. Many promising parcels in the Georgia Gold Belt are private, state, or federal; **do not survey or sample without written authorization.** Recreational panning is often restricted to designated areas and has its own rules — check current state/federal regulations before any fieldwork.
- **No exaggerated claims.** OpenGoldSDR will not market this as a gold detector or as investment/mining advice. Public communication must preserve the "anomaly mapping, not detection" framing of the project README.
- **Clean-room / IP hygiene.** The pipeline is built only on open tools and publicly documented physics. We do not use, copy, or reverse-engineer any patented commercial code; an independent implementation of public physics for private research is the explicit design constraint. Before accepting outside code, the project must select an open-source license.
- **Cultural / archaeological care.** If a survey suggests buried human-made features (old workings, structures, graves), treat it as a stop-and-consult trigger, not a dig target — historical mine works and burials carry legal and ethical protections.
- **Data honesty.** Publish baselines, noise floors, negative results, and confounder analyses alongside any positive anomaly, so the community can falsify rather than just admire results.

---

## References

[1] MIT OpenCourseWare, *Build a Small Radar System Capable of Sensing Range, Doppler, and Synthetic Aperture Radar Imaging* (RES.LL-003, G. L. Charvat et al., IAP 2011). https://ocw.mit.edu/courses/res-ll-003-build-a-small-radar-system-capable-of-sensing-range-doppler-and-synthetic-aperture-radar-imaging-january-iap-2011/ ; project page: https://sites.google.com/view/glcharvat/radar/mit-coffee-can-radar

[2] Frequency / back-projection imaging for ground-based SAR — *Frequency Domain Panoramic Imaging Algorithm for Ground-Based ArcSAR*, Sensors (PMC7764108). https://pmc.ncbi.nlm.nih.gov/articles/PMC7764108/

[3] D. E. Wahl, P. H. Eichel, D. C. Ghiglia, C. V. Jakowatz, "Phase gradient autofocus — a robust tool for high-resolution SAR phase correction," *IEEE Trans. Aerospace and Electronic Systems*, 30(3):827–835, 1994. https://ui.adsabs.harvard.edu/abs/1994ITAES..30..827W

[4] Azouz et al., "Improved phase gradient autofocus algorithm based on segments of variable lengths and minimum-entropy phase correction," *IET Radar, Sonar & Navigation*, 2015. https://ietresearch.onlinelibrary.wiley.com/doi/full/10.1049/iet-rsn.2014.0201

[5] *Sentinel-1 interferometric coherence* (temporal decorrelation as a change/vegetation index), Remote Sensing of Environment. https://www.sciencedirect.com/science/article/pii/S0034425722003169

[6] MintPy / ASF HyP3 Sentinel-1 InSAR — InSAR Product Guide. https://hyp3-docs.asf.alaska.edu/guides/insar_product_guide/

[7] *Application of ground penetrating radar methods in soil studies: A review*, Geoderma. https://www.sciencedirect.com/science/article/abs/pii/S0016706118303823

[8] J. M. Martinez & ... *Modeling Dielectric-constant Values of Geologic Materials*, Kansas Geological Survey. https://www.kgs.ku.edu/Current/2001/martinez/martinez.pdf (quartz ε_r ≈ 4.5, water ≈ 80; see also Engineering ToolBox relative permittivity table https://www.engineeringtoolbox.com/relative-permittivity-d_1660.html )

[9] USGS Mineral Resources Data System (MRDS), Mineral Resources Online Spatial Data (downloadable incl. shapefile). https://mrdata.usgs.gov/mrds/

[10] USGS Mineral Resources Program — Data & Tools (3DEP / spatial data portal). https://www.usgs.gov/programs/mineral-resources-program/data ; https://mrdata.usgs.gov/

[11] Georgia Gold Belt / Dahlonega gold belt (Consolidated mine; ~500,000 oz 1838–1941; quartz-vein control). https://en.wikipedia.org/wiki/Georgia_Gold_Belt ; Earth@Home, *Mineral resources of the Blue Ridge and Piedmont* https://earthathome.org/hoe/se/minerals-brp/

[12] *Carolina slate belt gold deposits in Virginia, North Carolina, South Carolina, and Georgia*, USGS. https://pubs.usgs.gov/publication/70220356

[13] USGS, *Geochemical reconnaissance, Carroll County gold belt and southwestern part of the Dahlonega gold belt* (host-rock lithology). https://pubs.usgs.gov/mf/2213/report.pdf

[14] F. Biondi & C. Malanga, "Synthetic Aperture Radar Doppler Tomography Reveals Details of Undiscovered High-Resolution Internal Structure of the Great Pyramid of Giza," *Remote Sensing* (MDPI), 2022; arXiv:2208.00811. https://arxiv.org/abs/2208.00811 (claims contested; cited for the physics lineage only)

[15] *Structural displacement monitoring using ground-based synthetic aperture radar*, Int. J. Applied Earth Observation. https://www.sciencedirect.com/science/article/pii/S1569843222003326

[16] *Investigation of Wavenumber Domain Imaging Algorithm for Ground-Based Arc Array SAR*, Sensors (PMC5751644). https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5751644/

[17] *Offline-Online Change Detection for Sentinel-1 InSAR Time Series*, Remote Sensing (MDPI). https://www.mdpi.com/2072-4292/13/9/1656/htm

[18] *Ground-Penetrating Radar (GPR): Principles, Applications* (penetration vs. resolution; frequency dependence). https://geologyscience.com/geology-branches/geophysics/ground-penetrating-radar-gpr/

---

*Method approach: this draft follows the Google DeepMind "Science Skills" working style — ground every step in primary sources, never fabricate IDs/results, report negatives honestly, and keep citations as terminal, verifiable URLs (https://github.com/google-deepmind/science-skills). Internal grounding: `docs/Ground_Based_Rail_SAR.md`, `docs/SAR_Algorithms_and_Data.md`, `README.md`.*
