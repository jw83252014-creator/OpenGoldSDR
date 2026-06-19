# OpenGoldSDR — Concrete, Runnable Experiment Design (2026)

Status: research design, not field-proven. Everything below is a falsifiable experiment
with a defined input, method, expected output, and a "kill condition" (what result would
prove the approach doesn't work). Built only on open tools and public data; no use of
Biondi's patented pipeline (see `docs/SAR_Algorithms_and_Data.md`).

Three experiments, each independently runnable:

1. **EXP-1 — "Already mined?"** Detect whether a parcel was previously worked
   (disturbed ground / subsidence / old workings) from free satellite + LiDAR data. **No
   land access required** — pure desk study.
2. **EXP-2 — "How deep?"** On land you have permission to enter, estimate the depth of a
   subsurface anomaly with a ground-based rail/FMCW radar plus back-projection + a simple
   dielectric inversion — bounded by realistic frequency/depth physics.
3. **EXP-3 — "Where to look + what to buy."** A Tier-1 rail SAR bill of materials with
   example products/prices, and a target-prioritization workflow over USGS MRDS historic-mine
   data for the Georgia Gold Belt (Augusta / Clarks Hill / Columbia County).

A standing constraint runs through all three: **legal/land access** (Section 5). You cannot
lawfully prospect, dig, or even enter most of this ground without permission or a valid claim.

---

## 0. What is physically detectable (sets the ceiling for every experiment)

- Consumer Wi-Fi (2.4/5 GHz) dies in centimeters of damp soil — not usable for depth. This is
  already the project's stated position and the literature agrees: penetration falls as
  frequency rises and as conductivity/moisture rise.
- GPR depth vs. frequency, order-of-magnitude (use as design bounds, not promises):
  - **10–100 MHz:** up to ~30 m in optimal (dry, low-conductivity) ground; coarse resolution.
  - **100–500 MHz:** ~5–10 m typical; balanced.
  - **500 MHz–2.5 GHz:** ~1–5 m; high resolution, small features.
  - Clean dry sand ~18 m; **dense wet clay ~6 m** at typical frequencies.
  ([multiVIEW](https://www.multiview.ca/news-and-media/2024/09/24/understanding-ground-penetrating-radar-frequencies-depth-accuracy-and-soil-impact/),
   [EPA GPR](https://www.epa.gov/environmental-geophysics/ground-penetrating-radar-gpr))
- **Georgia red clay / saprolite is the worst case**: high clay content = high conductivity =
  high attenuation. Plan for the low end (a few meters), not the textbook 30 m. Moisture both
  helps (raises dielectric contrast) and hurts (raises attenuation) — it is the #1 confounder.
  ([Nature 2026 — max penetration depth vs. soil EM properties](https://www.nature.com/articles/s41598-026-36996-z))

Implication: EXP-1 (satellite) detects *surface/near-surface disturbance signatures*, not
buried gold. EXP-2 (ground radar) realistically images *a few meters* of structural/dielectric
boundaries in clay. Both are anomaly mapping, consistent with the README framing.

---

## 1. EXP-1 — Detect previously extracted ground (no land access needed)

**Hypothesis:** Parcels that were historically worked (pits, adits, trenches, placer cuts,
spoil/tailings, subsidence over old stopes) carry persistent geometric and radar-coherence
signatures distinguishable from undisturbed Piedmont forest/farm.

Two independent signal channels, then fuse.

### 1A. Sentinel-1 InSAR coherence loss / change

InSAR **coherence** is a 0.0–1.0 measure of phase stability between two SAR passes; stable
ground (rock, structures) stays high, while disturbed/vegetating/eroding ground decorrelates.
Open-pit and active mining are routinely monitored this way; coherence loss is an accepted
ground-disturbance indicator.
([Open-pit coherence monitoring](https://www.researchgate.net/publication/356060728_Monitoring_Mining_Activities_Using_Sentinel-1A_InSAR_Coherence_in_Open-Pit_Coal_Mines),
 [coherence time-series for change/early warning](https://pmc.ncbi.nlm.nih.gov/articles/PMC8536966/))

Caveat to respect up front: C-band coherence is *low over vegetation generally*, so forested
Georgia decorrelates fast — this is why we use a **time-series and seasonal stack**, not a
single pair, and why we treat coherence as one vote, not proof.

**Inputs (all free):**
- Sentinel-1 IW SLC pairs over the target tile (Augusta / Clarks Hill / Columbia County) from
  the **Alaska Satellite Facility (ASF)**. Pairs must match orbit direction, polarization
  (VV), and geometry.
- Optional: ESA global seasonal coherence/backscatter dataset as a baseline reference.
  ([global seasonal coherence dataset](https://pmc.ncbi.nlm.nih.gov/articles/PMC8917198/))

**Method (runnable today):**
1. Generate InSAR products with a **coherence GeoTIFF** via **ASF HyP3** — three ways: the
   Vertex web portal, the `hyp3_sdk` Python SDK, or the HyP3 REST API. Standard product
   includes amplitude, **coherence**, unwrapped phase, displacement, water mask.
   ([ASF HyP3 InSAR product guide](https://hyp3-docs.asf.alaska.edu/guides/insar_product_guide/))
2. Build a **coherence time-series stack** (many pairs across seasons/years). Compute, per
   pixel: mean coherence, coherence variance, and slow trend.
3. **Subsidence channel:** request displacement/LOS products from the same HyP3 jobs; look for
   small persistent subsidence bowls (sag over collapsed old workings). Note Sentinel-1
   resolution is ~5×20 m — it will not resolve a single hand-dug pit, only field-scale
   features. ([resolution caveat](https://farmonaut.com/mining/sentinel-1-more-top-satellites-for-insar-mining-2025))
4. Process in the open Python stack already named in the repo: **ESA SNAP / GMTSAR** for
   interferometry, **MintPy** for time-series, **Sarsen / xarray-sentinel** for ingest.
   (`docs/SAR_Algorithms_and_Data.md`)

**Expected output:** a per-parcel raster of "disturbance likelihood" = anomalous coherence
behavior + any persistent subsidence, relative to the surrounding undisturbed baseline.

**Kill condition:** if coherence over known historic-mine polygons (from EXP-3 MRDS data) is
statistically indistinguishable from random undisturbed control polygons across the stack,
the satellite-coherence channel is not informative at this site/resolution — drop it and lean
on LiDAR (1B).

### 1B. USGS 3DEP LiDAR microtopography (the high-resolution channel)

3DEP now covers ~99% of the nation at high resolution and is explicitly used to sharpen
geologic mapping and reveal engineered/disturbed features; LiDAR strips vegetation to expose
ground.
([3DEP](https://www.usgs.gov/3d-elevation-program/what-3dep),
 [3DEP hazards/resources role](https://www.congress.gov/crs-product/IF13079))

**Inputs (free):** 3DEP point cloud / DEM tiles over the target area (The National Map / USGS
LiDAR Explorer).

**Method:**
1. Build a **bare-earth DEM** (ground-classified returns only — removes tree canopy).
2. Derive microtopography layers: **slope, hillshade (multi-azimuth), local relief / Topographic
   Position Index, and a high-pass "residual" surface** that isolates meter-scale bumps and
   hollows from regional slope.
3. Flag candidate signatures: linear/clustered **pits and shafts** (small circular depressions),
   **trenches/costean cuts** (linear depressions following a vein strike), **adit benches**,
   **spoil/tailings mounds** (positive relief), and **placer cuts/benches** along creeks.
   These are exactly the feature classes USGS digitizes in its historic-mine work (USMIN).
   ([USMIN mineral deposit DB](https://www.usgs.gov/centers/gggsc/science/usmin-mineral-deposit-database))
4. (Optional ML) train a small classifier on labeled known-mine microtopography vs. control —
   but start with hand-thresholded morphological filters; they're auditable.

**Expected output:** vector points/polygons of candidate workings with a confidence score,
overlaid on the bare-earth hillshade. This is the *unrecorded-pit finder* described in the
repo's data-fusion section.

**Kill condition:** if bare-earth residuals at known MRDS mine coordinates show no
distinguishable microrelief above DEM noise (i.e., features are below 3DEP vertical accuracy),
LiDAR microtopography is not viable at the available tile quality — note the tile's QL (quality
level) and seek higher-density acquisition.

### 1C. Fusion / decision rule

A parcel is scored "likely already worked" when **≥2 independent channels agree**:
(coherence anomaly) AND/OR (LiDAR microtopography feature) AND/OR (MRDS/USMIN historic record
within buffer). Require independence so one noisy channel can't trigger a flag alone.
Repeatability rule from the repo applies: strict grid, baseline noise, re-verify.

---

## 2. EXP-2 — Estimate the DEPTH of an anomaly (requires land access)

Goal: on a parcel you may lawfully enter (Section 5), collect ground radar over a known anomaly
and return a **depth estimate with explicit uncertainty**, honest about physics limits.

### 2A. Physics budget (do this BEFORE buying anything)

Two-way depth from radar travel time:  **d = (v · t) / 2**, with wave speed
**v = c / √εr** in a medium of relative permittivity εr.

- Georgia red clay/saprolite, moist: εr roughly 10–30 → v ≈ 0.055–0.095 m/ns. So a target
  echo at 100 ns two-way time implies ~2.7–4.7 m depth — the εr uncertainty alone is a ~±1 m
  band, which is why **calibration (2D) matters**.
- **Realistic max depth in this clay: a few meters**, not tens. Choose center frequency for the
  depth/resolution trade you actually need (100–500 MHz band = ~5–10 m ceiling in good ground,
  less in clay). ([multiVIEW](https://www.multiview.ca/news-and-media/2024/09/24/understanding-ground-penetrating-radar-frequencies-depth-accuracy-and-soil-impact/),
  [Nature 2026](https://www.nature.com/articles/s41598-026-36996-z))

If the physics budget says the target is deeper than the attenuation limit for your frequency,
**stop** — no processing recovers a signal that never came back. This is the honest gate.

### 2B. Acquisition — rail SAR / FMCW

Use the project's Tier-1 rail (`docs/Ground_Based_Rail_SAR.md`, `hardware/rail_sar/`):
- Step an FMCW radar along the precision rail; log IQ vs. **exactly known** rail position
  (stepper + lead screw + homing switch). Position accuracy is the whole game.
- Lineage: **Charvat MIT Coffee Can / IAP radar** — a ~$360 laptop FMCW radar already doing
  range/Doppler/SAR; we motorize it on the rail.
  ([Charvat MIT IAP radar](https://www.semanticscholar.org/paper/The-MIT-IAP-radar-course:-Build-a-small-radar-of-Charvat-Fenn/9c13bca0d8f3e0d51f5fd9c97bd55df42f5c6d5c),
   [Hackaday $360 SAR](https://hackaday.com/2012/12/18/build-a-360-synthetic-aperture-radar-with-mits-opencourseware/))
- Collect a 2D survey line (or grid) over the anomaly; constant rail speed, fixed step size,
  record a baseline over known-undisturbed ground for subtraction.

### 2C. Processing — back-projection then inversion

1. **Image formation:** classic **time-domain back-projection** from IQ + rail position →
   2D range/cross-range reflectivity image (the repo's `software/rail_sar/backprojection.py`).
   Modern deep-learning self-focusing back-projection exists if needed for speed/resolution,
   but start with the textbook version (auditable).
   ([self-focusing back-projection GPR](https://pmc.ncbi.nlm.nih.gov/articles/PMC11820573/))
2. **Velocity / εr calibration:** fit hyperbola(s) from a point reflector, or use a buried
   known target / common-midpoint pass, to estimate in-situ v (hence εr). This converts time
   to depth and shrinks the εr band.
3. **Depth + uncertainty:** report depth as a range from the εr spread, not a single number.
4. **(Stretch) full-waveform / joint inversion:** frequency-domain FWI recovers permittivity vs.
   depth; joint gravity+GPR inversion better localizes cavities (old stopes/voids). Treat as
   v2, not the first deliverable.
   ([GJI full-waveform inversion](https://academic.oup.com/gji/article/232/1/504/6670780),
    [joint gravity+GPR cavity inversion (patent)](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9977124))

**Expected output:** annotated back-projection image with a boxed anomaly and
"estimated depth = X m (±Y m), εr assumed 10–30, frequency f, soil = moist clay" — plus the
baseline-subtracted version.

**Kill condition:** if the baseline-undisturbed pass produces the *same* "anomaly," the feature
is an artifact (rail wobble, clutter, surface object), not subsurface — discard. If no coherent
return appears above noise within the physics-budget depth, declare "below detection limit for
this rig in this soil."

---

## 3. EXP-3 — Parts list (Tier-1 BOM) + "best places to look"

### 3A. Tier-1 Rail SAR — Bill of Materials (example products / prices, USD, 2026)

Aligned with `docs/Ground_Based_Rail_SAR.md` Tier-1 ($250–$700 target). Prices are
representative; verify at purchase.

| Subsystem | Example product | ~Price | Notes |
|---|---|---|---|
| RF frontend (option A, cheapest) | **Charvat MIT Coffee-Can FMCW** build (VCO + mixer + breadboard + cantennas) | ~$360 kit-equivalent | Proven SAR-capable; the reference design ([Hackaday](https://hackaday.com/2012/12/18/build-a-360-synthetic-aperture-radar-with-mits-opencourseware/)) |
| RF frontend (option B, modern) | **TI AWR1843BOOST** mmWave FMCW eval board (76–81 GHz) + **DCA1000EVM** raw-data capture | board ~$300–400; DCA1000 ~$600 | Easy IQ capture over Ethernet; **note: 77 GHz penetrates almost nothing — good for method dev / above-ground SAR validation, not soil depth** ([TI AWR1843BOOST](https://www.ti.com/tool/AWR1843BOOST)) |
| RF frontend (option C, SDR) | **HackRF One** or **RTL-SDR v4** + clean FMCW upconverter/VCO | $150–320 | Flexible band choice; pick a band that penetrates, not Wi-Fi |
| Linear rail | 2020/2040 aluminum extrusion + **NEMA17 stepper** + GT2 belt or lead screw + end-stop/homing switch | $100–200 | Position repeatability is the whole game |
| Antennas | DIY copper horn / waveguide "cans" or cheap PCB patch | $20–50 | Lower freq = bigger antenna |
| Control / logging | Raspberry Pi 5 (or existing laptop) logging IQ vs. rail position | $0–100 | Sync capture to stepper steps |
| Positioning (optional, for georef + Tier-2) | **u-blox ZED-F9P RTK GPS** (cm-accurate) | ~$200 | Needed to tag readings / future VLF grid |
| **Tier-1 total** | | **~$300–$700** | matches repo target |

Reality check on frequency: a true **subsurface-depth** result wants a **low-frequency GPR
band (100–500 MHz)**. Commercial low-freq GPR (GSSI/Sensors&Software 200 MHz, pulseEKKO,
Zond) runs **~$9k–$12k+** — out of Tier-1 scope; that's why Tier-1 targets shallow high-res
method development and the project's anomaly-mapping framing rather than deep imaging.
([Sensors&Software pulseEKKO low-freq](https://www.sensoft.ca/products/pulseekkopro/pulseekko-low-frequency/),
 [GSSI 200 MHz antenna](https://www.allied-associates.com/solutions/gssi-200mhz-antenna/),
 [commercial GPR pricing context](https://www.aliexpress.com/s/wiki-ssr/article/ground-penetrating-radar-equipment-price))

### 3B. "Best places to look" — MRDS-driven target prioritization

**Data source:** USGS **Mineral Resources Data System (MRDS)** — names, coordinates, commodity,
status, production, geologic notes for historic mines worldwide.
([MRDS](https://mrdata.usgs.gov/mrds/))

**Programmatic access (runnable):**
- Bulk download as **CSV** (44-field "flattened", or comprehensive) or **Shapefile**.
- OGC web services for filtered/spatial queries: **WMS** `https://mrdata.usgs.gov/services/mrds`
  and **WFS 1.1.0** `https://mrdata.usgs.gov/services/wfs/mrds` (filter by bbox; post-filter by
  commodity = Au / gold and by state = Georgia).
  ([MRDS access page](https://mrdata.usgs.gov/mrds/))
- Pair with **USMIN** (digitized historic mine features) for the LiDAR cross-check in EXP-1.
  ([USMIN](https://www.usgs.gov/centers/gggsc/science/usmin-mineral-deposit-database))

**Geology context for the target area (Augusta / Clarks Hill / Columbia County):**
- The **Georgia Gold Belt** runs from eastern Alabama to NE Georgia; most gold sits in the
  **Carolina Slate Belt** (a.k.a. Georgia Gold Belt locally). The Augusta/Columbia County
  district is on the **Carolina Slate Belt** side, distinct from the Dahlonega/Carroll County
  belts up in the northern Piedmont.
  ([Georgia Gold Belt](https://en.wikipedia.org/wiki/Georgia_Gold_Belt),
   [Carolina Slate Belt gold deposits, incl. GA](https://pubs.usgs.gov/publication/70220356))
- Concrete local anchor: the **McDuffie Gold Mine, Columbia County** (just north of Augusta).
  ([Apalache Research — Augusta-area gold](https://apalacheresearch.com/2023/11/22/thars-gold-in-them-thar-hills/))

**Prioritization workflow (the deliverable):**
1. Pull MRDS gold occurrences within a bbox around Augusta / Clarks Hill / Columbia County.
2. Score each candidate by: distance to a mapped **lithologic contact / fault** (gold loves
   contacts and structure), past **production/status**, density of nearby occurrences, and
   proximity to **creeks/benches** (placer concentration).
3. Cross-reference with EXP-1 outputs: a candidate gets promoted when an MRDS/USMIN record OR a
   LiDAR microtopography feature OR a coherence anomaly co-locate.
4. **Filter by land access (Section 5) before anything physical** — rank only parcels you can
   lawfully reach to the top of the field list.

**Expected output:** a ranked, georeferenced shortlist (CSV + map) of "test-worthy" parcels,
each with geology rationale, EXP-1 evidence, and an access status flag.

---

## 4. End-to-end pipeline (how the three experiments chain)

```
USGS MRDS / USMIN  ─┐
USGS 3DEP LiDAR  ───┼─►  EXP-1 desk study  ─►  ranked candidate parcels (CSV + map)
Sentinel-1 (ASF) ──┘         (no access)              │
                                                      ▼
                                        Section 5 legal/access filter
                                                      │
                                                      ▼
                                   EXP-3 BOM build (Tier-1 rail SAR)
                                                      │
                                                      ▼
                              EXP-2 field survey + back-projection + depth
                                   (only on permitted/claimed land)
```

---

## 5. Legal / land-access reality (gates EXP-2 and any field step)

This is not optional and it bounds the whole project. Summary for Georgia:

- **Private land:** you must get the **property owner's permission first — ideally in writing**
  — to pan, detect, or survey. Entering claimed/patented/private land without permission is
  **criminal trespass**: a misdemeanor, up to 12 months jail and/or up to $1,000 fine.
  ([Georgia prospecting regs](https://ourpastimes.com/georgia-goldprospecting-regulations-6144661.html),
   [gold panning law](https://legalclarity.org/gold-panning-regulations-and-compliance-in-georgia/),
   [metal detecting in GA](https://www.silverrecyclers.com/blog/metal-detecting-in-georgia.aspx))
- **Existing claims:** anyone wishing to examine/mine must first check whether land is private,
  already **claimed**, or under **patent**; records are verified at the **county courthouse**.
  ([Georgia prospecting regs](https://ourpastimes.com/georgia-goldprospecting-regulations-6144661.html))
- **State recreational mining exemption:** no state surface-mining permit for *hobbyist hand
  panning* of rocks/minerals incl. gold; stay **within the stream channel, no bank disturbance**;
  **suction dredging not allowed** in national forests / not recommended in private streams;
  some trout streams close seasonally. Permission still strongly recommended.
  ([Georgia EPD recreational mining exemption](https://epd.georgia.gov/recreational-mining-exemption))
- **Federal forest (e.g., Chattahoochee-Oconee NF):** panning allowed without hand/power
  *digging* tools and without interfering with existing mineral rights; metal-detecting policy
  varies by forest — check the specific unit.
  ([Georgia prospecting regs](https://ourpastimes.com/georgia-goldprospecting-regulations-6144661.html),
   [USFS metal detecting policy example](https://www.fs.usda.gov/r08/gwj/safety-ethics/metal-detecting-policy))
- **Antiquities / artifacts:** disturbing archaeological resources on state land is separately
  prohibited — relevant since old workings can be historic sites.
  ([GA DNR artifact collecting FAQ](https://gastateparks.org/Archaeology/ArtifactCollecting/FAQ))

**Operational rule for OpenGoldSDR:** EXP-1 (desk study on free data) is unrestricted. EXP-2
(any on-the-ground radar/dig) requires a documented permission or valid claim per parcel, plus
a courthouse claim check, before a single field session. Bake the access flag into the EXP-3
shortlist so unreachable parcels never reach the field list.

---

## 6. Honest limitations (so reviewers can attack the right things)

- C-band Sentinel-1 decorrelates over Georgia forest; coherence is one weak vote, not proof,
  and 5×20 m resolution can't see a single hand-dug pit.
- Tier-1 hardware at penetrating-but-affordable frequencies is method-development grade; deep,
  high-confidence depth imaging needs commercial low-freq GPR ($9k+).
- Clay/moisture is the dominant confounder for both depth (attenuation) and εr (depth
  calibration). Always collect an undisturbed baseline and subtract.
- None of this directly detects gold. It detects **disturbance and structural/dielectric
  anomalies** that, fused with historic-mine data, tell a prospector where to *test next*.

---

## 7. Sources

- [multiVIEW — GPR frequency/depth/soil](https://www.multiview.ca/news-and-media/2024/09/24/understanding-ground-penetrating-radar-frequencies-depth-accuracy-and-soil-impact/)
- [Nature 2026 — max GPR penetration depth vs. soil EM properties](https://www.nature.com/articles/s41598-026-36996-z)
- [EPA — Ground Penetrating Radar](https://www.epa.gov/environmental-geophysics/ground-penetrating-radar-gpr)
- [GJI — full-waveform inversion of GPR](https://academic.oup.com/gji/article/232/1/504/6670780)
- [Deep-learning self-focusing back-projection GPR (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11820573/)
- [Joint gravity+GPR cavity inversion (USPTO)](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9977124)
- [ASF HyP3 — InSAR product guide (coherence)](https://hyp3-docs.asf.alaska.edu/guides/insar_product_guide/)
- [Sentinel-1A InSAR coherence — open-pit mining monitoring](https://www.researchgate.net/publication/356060728_Monitoring_Mining_Activities_Using_Sentinel-1A_InSAR_Coherence_in_Open-Pit_Coal_Mines)
- [Coherence time-series for landslide/change detection (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8536966/)
- [Global seasonal Sentinel-1 coherence dataset (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8917198/)
- [Sentinel-1 resolution / mining context](https://farmonaut.com/mining/sentinel-1-more-top-satellites-for-insar-mining-2025)
- [USGS 3DEP — What is 3DEP](https://www.usgs.gov/3d-elevation-program/what-3dep)
- [CRS — 3DEP role in mapping hazards/resources](https://www.congress.gov/crs-product/IF13079)
- [USGS USMIN mineral deposit database](https://www.usgs.gov/centers/gggsc/science/usmin-mineral-deposit-database)
- [USGS MRDS portal](https://mrdata.usgs.gov/mrds/)
- [Charvat MIT IAP radar paper](https://www.semanticscholar.org/paper/The-MIT-IAP-radar-course:-Build-a-small-radar-of-Charvat-Fenn/9c13bca0d8f3e0d51f5fd9c97bd55df42f5c6d5c)
- [Hackaday — $360 SAR from MIT OCW](https://hackaday.com/2012/12/18/build-a-360-synthetic-aperture-radar-with-mits-opencourseware/)
- [TI AWR1843BOOST eval board](https://www.ti.com/tool/AWR1843BOOST)
- [Sensors & Software pulseEKKO low-frequency GPR](https://www.sensoft.ca/products/pulseekkopro/pulseekko-low-frequency/)
- [GSSI 200 MHz antenna](https://www.allied-associates.com/solutions/gssi-200mhz-antenna/)
- [Commercial GPR pricing context](https://www.aliexpress.com/s/wiki-ssr/article/ground-penetrating-radar-equipment-price)
- [Georgia Gold Belt (Wikipedia)](https://en.wikipedia.org/wiki/Georgia_Gold_Belt)
- [USGS — Carolina Slate Belt gold deposits (incl. GA)](https://pubs.usgs.gov/publication/70220356)
- [Apalache Research — Augusta-area gold / McDuffie Mine](https://apalacheresearch.com/2023/11/22/thars-gold-in-them-thar-hills/)
- [Georgia gold-prospecting regulations](https://ourpastimes.com/georgia-goldprospecting-regulations-6144661.html)
- [Gold panning laws in Georgia (LegalClarity)](https://legalclarity.org/gold-panning-regulations-and-compliance-in-georgia/)
- [Metal detecting in Georgia](https://www.silverrecyclers.com/blog/metal-detecting-in-georgia.aspx)
- [Georgia EPD — recreational mining exemption](https://epd.georgia.gov/recreational-mining-exemption)
- [USFS — metal detecting policy (example unit)](https://www.fs.usda.gov/r08/gwj/safety-ethics/metal-detecting-policy)
- [GA DNR — artifact collecting FAQ](https://gastateparks.org/Archaeology/ArtifactCollecting/FAQ)
