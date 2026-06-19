# Competitive Landscape: SDR / GB-SAR / Low-Cost EM for Gold & Mineral Prospecting

*Compiled June 2026. Scope: who is actually doing software-defined-radio (SDR), ground-based SAR (GB-SAR), and low-cost electromagnetic (EM) sensing aimed at gold / mineral prospecting; the academic & DIY GB-SAR lineage; and an honest assessment of how novel vs. established each piece is — especially the "satellite SAR radio-tomography for shallow gold anomalies" idea.*

## TL;DR / Honest novelty verdict

| Piece | How new is it? | Notes |
|---|---|---|
| Satellite SAR for **structural / lineament mapping** to *target* gold | **Established (~30 yrs)** | Standard exploration practice. Maps faults/shear zones that *host* gold; does not "see" the gold. |
| **Commercial GB-SAR** hardware | **Mature, but for deformation** | IDS GeoRadar, GroundProbe, MetaSensing — all for slope/landslide monitoring, *not* prospecting. |
| **DIY / academic SDR GB-SAR** | **Established as a hobby/research toy** | MIT Coffee-Can (2011), Charvat rail SAR, Friedt's SDR-GB-SAR. None aimed at minerals. |
| **VLF-EM / GPR low-cost EM** for ore | **Old & established (since 1960s–70s)** | Cheap, proven for conductive sulphides & shallow structure. Not a radar/SDR novelty. |
| **AI + remote-sensing mineral targeting** | **Hot but crowded (2018→)** | KoBold, Earth AI, VerAI, etc. Mostly multi-data ML, *not* SAR-tomography of gold. |
| **Biondi-style "SAR Doppler Tomography" of deep subsurface** | **Fringe / contested** | Not accepted by the mainstream radar community; physically dubious at depth. |
| **Satellite-SAR radio-tomography applied to *shallow gold anomaly* mapping specifically** | **Genuinely under-explored / arguably novel** — *but* for physics reasons that may also explain why nobody does it | See "Novelty assessment" below. |

The honest bottom line: each *component* is established, but the specific combination you'd be chasing — **low-cost SDR/SAR radio-tomography to map shallow gold anomalies** — is not a populated commercial space. That is partly an opportunity and partly a warning sign (the physics of EM penetration into moist/conductive ground is brutal).

---

## 1. Companies

### 1a. Filippo Biondi / "HarmonicSAR" (SAR Doppler Tomography)
- **Who:** Filippo Biondi, PhD (electronic/electrical eng., University of Strathclyde, Glasgow), Italian aerospace/remote-sensing engineer. Background includes satellite-SAR monitoring of dams/bridges (vibration detection from space).
- **Claim:** Proprietary "HarmonicSAR" software reframes SAR returns as **phononic / vibration** information ("SAR Doppler Tomography"), claiming to image internal structure tens-to-hundreds of metres deep — most famously ~700 m below the Giza plateau (the Khafre / "underground city" claim, March 2025).
- **Peer-review status:** A 2022 paper on SAR Doppler Tomography of the Great Pyramid was published in MDPI *Remote Sensing* (peer-reviewed, but MDPI's rigor is itself debated). The **2025 "underground city" claims were released via a YouTube press conference, not a paper** — heavily criticized for that.
- **Mainstream reaction:** Skeptical to dismissive. Snopes: *"no credible evidence."* ESA and even Biondi reportedly agree SAR's direct underground capacity is limited and that deep claims require heavy **modelling/interpretation** (i.e., not a direct measurement). Egyptologists called it artistic interpretation of data.
- **Relevance to gold:** **No published Biondi work on gold/mineral detection found.** The technique is archaeology-flavored. Treat HarmonicSAR as an *inspiration* / cautionary example, not a validated mineral tool.
- Sources:
  - arXiv 2208.00811 (Giza paper): https://arxiv.org/abs/2208.00811 ; MDPI version: https://www.mdpi.com/2072-4292/14/20/5231
  - Google Scholar: https://scholar.google.com/citations?user=GVyeIgIAAAAJ&hl=it
  - Snopes fact-check: https://www.snopes.com/fact-check/pyramids-of-giza-new-discovery-structures/
  - Critical appraisal: https://grahamhancock.com/pilicyd1/

### 1b. Commercial GB-SAR hardware vendors (deformation, NOT prospecting)
These are the real, mature GB-SAR companies — but their product is **millimetric deformation monitoring** (slope stability, landslides, dams), *not* mineral detection. Worth knowing because they define what "real" GB-SAR hardware costs and does.
- **IDS GeoRadar** (part of Hexagon) — ArcSAR / ArcSAR Neo (2026: claims true-3D GB-SAR for 360° mine-slope monitoring). Also sells GPR and InSAR services. https://idsgeoradar.com/ ; ArcSAR Neo: https://hexagon.com/company/newsroom/press-releases/2026/ids-georadar-launches-arcsar-neo-to-strengthen-slope-risk-management-and-mine-safety
- **GroundProbe** (Orica subsidiary) — Slope Stability Radar (SSR) line: SSR-Agilis, SSR-Omni, SSR-SARx, SSR-FX, SSR-XT; real + synthetic aperture; >4.5 km range. https://www.groundprobe.com/radars/
- **MetaSensing** — GB-SAR / airborne SAR hardware. (Listed among InSAR-market players.)
- Satellite InSAR service players (for completeness): TRE ALTAMIRA, Gamma Remote Sensing, CGG, Fugro, SatSense, SkyGeo, 3vGeomatics, Airbus DS, Planetek Italia.

> Key point: **no GB-SAR vendor markets a "detect gold" product.** Their radar measures *surface movement*, not buried mineralization.

### 1c. VLF-EM / GPR / low-cost EM vendors
The genuinely *low-cost, proven* EM-for-ore tools — old technology, still sold:
- **GEM Systems** (Canada) — one of the few surviving portable **VLF-EM** + resistivity-mapping vendors. https://www.gemsys.ca/very-low-frequency-electromagnetics/
- **Abitibi Geophysics, Radar Solutions International, Geo-App, cqtopgeo (Chongqing Gold)** — survey firms / equipment suppliers offering VLF, EM terrain conductivity, GPR, magnetometry. https://radar-solutions.com/our-methods.html ; https://www.geo-app.com/techniques/
- VLF-EM physics: passive, uses 15–40.8 kHz military submarine-comms transmitters as the source; a single operator with a backpack covers kilometres/day. Established for **massive sulphides** and conductive structure since the 1960s–70s; weaker for *disseminated* ores (and gold is often disseminated / non-conductive). US EPA primer: https://www.epa.gov/environmental-geophysics/very-low-frequency-electromagnetic-vlf

### 1d. "AI + remote sensing / SAR" mineral-exploration startups
Crowded and well-funded, but note: **almost all use AI over *multi-source* geodata, not SAR radio-tomography of the ore itself.**
- **KoBold Metals** (Berkeley, founded 2018; Gates/Bezos/a16z backed; raised ~$527M Series C, Jan 2025). Platforms "TerraShed" (data fusion) + "Machine Prospector" (target ranking). Focus = battery metals (Cu, Li, Ni, Co), e.g. Mingomba copper, Zambia. https://carboncredits.com/ai-powered-mineral-exploration-billionaires-backed-kobold-metals-raised-491-million/ ; https://spectrum.ieee.org/ai-mining
- **Farmonaut** — markets "satellite analytics" mineral detection (claims >90% accuracy, "64 g/t" gold case studies). Heavy marketing, light on disclosed SAR method; treat claims with skepticism. https://farmonaut.com/mining/sar-satellite-mineral-exploration-5-breakthroughs-for-2025
- **XRTech Group** — AI + satellite imagery monitoring for mineral exploration. https://xrtechgroup.com/ai-powered-satellite-imagery-for-gold/
- Others in the broader space frequently cited: **Earth AI, VerAI, GoldSpot Discoveries, ALS GoldSpot** (AI targeting from geophysics/drilling/satellite).

> None of these is "low-cost SDR radar." They are software/data plays on *existing* satellite + legacy geophysics.

---

## 2. Academic & DIY GB-SAR projects (the real low-cost lineage)

This is where the "low-cost SDR SAR" idea actually lives — as research/hobby, **not aimed at minerals**:

- **MIT Lincoln Laboratory "Coffee-Can Radar" — Gregory L. Charvat et al. (IAP 2011).** FMCW radar from coffee cans + breadboard + Mini-Circuits parts, digitized via the laptop audio port; does Doppler, range, and crude **rail-SAR** imaging. ~$360–$400 BOM. The canonical entry point. Course (free): https://ocw.mit.edu/courses/res-ll-003-build-a-small-radar-system-capable-of-sensing-range-doppler-and-synthetic-aperture-radar-imaging-january-iap-2011/ ; Charvat: https://sites.google.com/view/glcharvat/radar/mit-coffee-can-radar ; Hackaday writeups: https://hackaday.com/2012/12/18/build-a-360-synthetic-aperture-radar-with-mits-opencourseware/
- **Gregory Charvat — rail SAR / phased-array radar.** Author of *Small and Short-Range Radar Systems*; built numerous rail-SAR imagers. https://sites.google.com/view/glcharvat/imaging/synthetic-aperture-radar-sar
- **Jean-Michel Friedt (FEMTO-ST / Univ. Franche-Comté, France)** — the most relevant modern academic for *cheap SDR SAR*:
  - **SDR-GB-SAR**: WiFi dongle (Alfa AWUS036ACS, 5.8 GHz) as a pseudo-random RF source + Ettus B210 dual-channel SDR receiver + horn antennas + motorized linear rail + Raspberry Pi 4 running GNU Radio on Buildroot. Full system ~€6,700 (antennas dominate). Aimed at **landslide/displacement monitoring**. https://github.com/jmfriedt/SDR-GB-SAR ; FOSDEM 2024 talk: https://archive.fosdem.org/2024/schedule/event/fosdem-2024-2050-covert-ground-based-synthetic-aperture-radar-using-a-wifi-emitter-and-sdr-receiver/
  - **passive_radar** (RTL-SDR DVB-T) and **sentinel1_pbr** (passive bistatic radar *using Sentinel-1 as the illuminator*) — directly relevant if you want to piggy-back on satellite SAR illumination cheaply. https://github.com/jmfriedt/passive_radar ; https://github.com/jmfriedt/sentinel1_pbr
- **HackRF-based GPR** — Military University of Technology, Poland: low-cost **ground-penetrating radar** prototype on a HackRF SDR. https://www.hackster.io/news/polish-researchers-tap-the-open-source-hackrf-sdr-for-low-cost-ground-penetrating-radar-prototype-e951898c3fb0
- **Drone-based DIY SAR** (FPGA + ADC + 6 GHz antennas on an FPV drone). https://www.rtl-sdr.com/creating-a-drone-based-synthetic-aperture-radar/
- **openSAR (Earth Big Data LLC)** — SAR *processing* tools/docs (software, not hardware). https://github.com/EarthBigData/openSAR
- Rail-SAR / GB-SAR academic methodology papers (deformation): https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6308647/ ; arc-array GB-SAR imaging: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5751644/

> The DIY/academic SDR-SAR scene is real and active, but it is overwhelmingly about **deformation monitoring or education**. Applying it to **gold/mineral anomaly mapping is an empty niche** in this community.

---

## 3. Is "satellite SAR radio-tomography for shallow gold-anomaly mapping" novel or established?

**Split the question into the established part and the novel part — honestly.**

### Established (decades old)
- **SAR for structural / lineament / alteration mapping to *target* gold is standard.** Faults, shear zones, fracture density correlate with hydrothermal gold systems; SAR sees these through cloud/vegetation, day-night. L-band ALOS/PALSAR and C-band Sentinel-1 are routine. Gold occurrences correlate with medium-to-high lineament density. This is well-published and operational. Examples:
  - Ketté goldfield, Cameroon: https://www.sciencedirect.com/science/article/abs/pii/S1464343X21002879
  - Satellite-based structural geology mapping for exploration: https://www.tandfonline.com/doi/full/10.1080/10106049.2025.2541930
  - Lineament mapping overview: https://farmonaut.com/mining/satellite-lineament-mapping-minerals-2025-breakthroughs
- **SAR *tomography* (TomoSAR) is an established 3-D technique** — but for **vegetation/forest biomass** (P-band, ESA BIOMASS mission since ~2007), giving ~20 m vertical resolution. Penetration into *ground* is the hard limit: P-band penetrates only ~**60 cm in very dry quartz-rich soil**, far less when moist. https://www.nature.com/articles/s41598-023-33311-y ; https://www.mdpi.com/2072-4292/13/8/1485

### The hard physics (why "see the gold" is mostly marketing)
- SAR microwave penetration into ground is governed by **skin depth**: longer wavelength → deeper, but **moisture and conductivity crush it**. L-band ≈ a few cm of topsoil; P-band ≈ tens of cm; metres only in *extremely* dry sand (Sahara). Solid rock penetration is *limited*. So **SAR does not directly image buried gold**; at best it images near-surface structure/roughness/moisture proxies. (See penetration-depth refs: https://earthenable.wordpress.com/2016/11/16/using-synthetic-aperture-radar-sar-imagery-to-look-beneath-dry-soil-surfaces/ , https://intechopen.com/books/soil-moisture/soil-moisture-retrieval-from-microwave-remote-sensing-observations )
- Claims of "lab-validated >90% mineral detection / 64 g/t from satellite" (Farmonaut-style) should be treated **skeptically** — they conflate anomaly *correlation* with direct detection.

### Genuinely novel / under-explored
- **Using *satellite-SAR-illuminated* passive-bistatic radio-tomography, processed cheaply on SDR, specifically tuned to *shallow gold anomalies*** is **not a populated space.** Friedt's `sentinel1_pbr` shows the *plumbing* (free satellite illuminator + cheap SDR receiver) exists, but nobody appears to have aimed it at mineral/gold anomaly mapping.
- **Biondi's "Doppler/phononic" reframing** is the only thing resembling deep-subsurface SAR tomography in public discourse, and it is contested and not mineral-focused.
- So: the **architecture you're contemplating is arguably novel**, but its novelty exists in part *because the EM physics makes shallow-gold detection from SAR genuinely hard*. The honest framing for any OpenGoldSDR pitch: you are not competing with an established product — you are entering an **empty niche whose emptiness is partly physics-driven**. Differentiator candidates that are defensible: (a) **anomaly/structural targeting** (proven) rather than "detecting gold"; (b) fusing cheap SDR **VLF-EM/GPR-style EM** (which *does* respond to conductivity/sulphide proxies) with SAR structural maps; (c) low cost + open hardware as the moat, since incumbents (IDS, GroundProbe) are expensive and aimed elsewhere.

---

## 4. Practical takeaways for OpenGoldSDR positioning

1. **Don't claim to "detect gold" with radar** — claim to *map structure/conductivity anomalies that host gold*. That keeps you on the right side of physics and of the established literature.
2. **Closest real competitors are not gold-radar companies** — they are (a) GB-SAR deformation vendors (wrong application, expensive), (b) legacy VLF-EM/GPR survey gear (right physics, old, low-margin), and (c) AI-targeting startups (software over existing data, well-funded).
3. **Closest technical kin is Jean-Michel Friedt's SDR-GB-SAR / sentinel1_pbr** — study it; it is the de-facto open reference design for cheap SDR SAR, including using Sentinel-1 as a free illuminator.
4. **HarmonicSAR is a cautionary tale**, not a competitor: bold deep-subsurface SAR-tomography claims, weak peer-review/mainstream acceptance. Differentiate by being verifiable and shallow-focused.
5. **The white-space is real**: low-cost, open SDR EM/SAR fusion for *shallow gold anomaly targeting* is genuinely unoccupied — but de-risk early with the EM physics (skin depth, moisture, disseminated vs. conductive ore).

---

## Sources
- Filippo Biondi / HarmonicSAR (Giza): https://arxiv.org/abs/2208.00811 , https://www.mdpi.com/2072-4292/14/20/5231 , https://scholar.google.com/citations?user=GVyeIgIAAAAJ&hl=it
- Biondi criticism: https://www.snopes.com/fact-check/pyramids-of-giza-new-discovery-structures/ , https://grahamhancock.com/pilicyd1/
- Commercial GB-SAR: https://idsgeoradar.com/ , https://hexagon.com/company/newsroom/press-releases/2026/ids-georadar-launches-arcsar-neo-to-strengthen-slope-risk-management-and-mine-safety , https://www.groundprobe.com/radars/
- VLF-EM / GPR / EM survey: https://www.gemsys.ca/very-low-frequency-electromagnetics/ , https://www.epa.gov/environmental-geophysics/very-low-frequency-electromagnetic-vlf , https://radar-solutions.com/our-methods.html , https://www.geo-app.com/techniques/
- AI mineral startups: https://carboncredits.com/ai-powered-mineral-exploration-billionaires-backed-kobold-metals-raised-491-million/ , https://spectrum.ieee.org/ai-mining , https://farmonaut.com/mining/sar-satellite-mineral-exploration-5-breakthroughs-for-2025 , https://xrtechgroup.com/ai-powered-satellite-imagery-for-gold/
- MIT Coffee-Can / Charvat: https://ocw.mit.edu/courses/res-ll-003-build-a-small-radar-system-capable-of-sensing-range-doppler-and-synthetic-aperture-radar-imaging-january-iap-2011/ , https://sites.google.com/view/glcharvat/radar/mit-coffee-can-radar , https://hackaday.com/2012/12/18/build-a-360-synthetic-aperture-radar-with-mits-opencourseware/
- Friedt SDR-GB-SAR / passive radar: https://github.com/jmfriedt/SDR-GB-SAR , https://github.com/jmfriedt/passive_radar , https://github.com/jmfriedt/sentinel1_pbr , https://archive.fosdem.org/2024/schedule/event/fosdem-2024-2050-covert-ground-based-synthetic-aperture-radar-using-a-wifi-emitter-and-sdr-receiver/
- HackRF GPR: https://www.hackster.io/news/polish-researchers-tap-the-open-source-hackrf-sdr-for-low-cost-ground-penetrating-radar-prototype-e951898c3fb0
- Drone SAR / openSAR: https://www.rtl-sdr.com/creating-a-drone-based-synthetic-aperture-radar/ , https://github.com/EarthBigData/openSAR
- SAR structural/lineament gold mapping: https://www.sciencedirect.com/science/article/abs/pii/S1464343X21002879 , https://www.tandfonline.com/doi/full/10.1080/10106049.2025.2541930
- TomoSAR / penetration physics: https://www.nature.com/articles/s41598-023-33311-y , https://www.mdpi.com/2072-4292/13/8/1485 , https://earthenable.wordpress.com/2016/11/16/using-synthetic-aperture-radar-sar-imagery-to-look-beneath-dry-soil-surfaces/
