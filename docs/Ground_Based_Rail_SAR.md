# Ground-Based Rail SAR — hardware design

Origin: research thread on Filippo Biondi's satellite radio-tomography (the "scan under the
pyramids" method, commercialized as HarmonicSAR). The satellite version is out of reach, but the
**math is identical at garage scale** — move a radar along a precise track to synthesize a large
aperture (Synthetic Aperture Radar). This is the OpenGoldSDR ground analog.

> What it actually finds: not gold flakes. It maps **structural/dielectric boundaries** where gold
> hides in the Georgia Gold Belt — quartz veins (very different dielectric constant vs. red clay /
> saprolite), mineralized contacts, wet faults, old workings, voids. Anomaly detection, not a metal detector.

## The rail = the aperture
A still antenna sees a tiny patch. A radar **stepped along a rail** records phase+amplitude at many
positions; back-projection combines them into one synthetic antenna as long as the rail. Longer rail +
finer steps = sharper cross-range resolution. The rail must move in **repeatable, precisely-known
increments** — position accuracy is the whole game, so a stepper + lead screw/belt + homing switch.

Lineage to copy, not reinvent: **Dr. Gregory L. Charvat's MIT Coffee Can Radar** (MIT OpenCourseWare,
6.S099) — laptop-based FMCW radar that already does range, Doppler, and SAR. We swap the cantenna for
an SDR/FMCW frontend and put it on a motorized rail.

## Tier 1 — "Garage-built" Rail SAR ($250–$700) — START HERE
| Subsystem | Part | $ |
|---|---|---|
| RF frontend | FMCW radar module **or** clean upconverter + SDR (HackRF / RTL-SDR v4) | 150–300 |
| Linear rail | Aluminum extrusion (2020/2040) + NEMA17 stepper + GT2 belt or lead screw + end-stop | 100–200 |
| Antennas | DIY copper horn / waveguide "cans" or cheap PCB patch | 20–50 |
| Control/log | Raspberry Pi or existing laptop logging IQ vs. rail position | 0–100 |

Frequency reality: skip 2.4/5 GHz Wi-Fi (dies in centimeters of damp soil). Use FMCW in a band that
penetrates, and treat moisture as the #1 confounder.

## Tier 2 — Direct-sampling SDR / VLF EM array ($1,200–$2,500) — goes DEEPER, no rail
For bedrock-scale anomalies instead of shallow high-res. VLF induction (≈10 kHz) walked on a grid:
high-dynamic-range SDR (LimeSDR/BladeRF/RTL-SDR v4 + LNA), power amp + filters, shielded loop coils,
and an **RTK GPS (u-blox ZED-F9P, cm-accurate)** to tag every reading. This is the traditional
geophysics path (VLF-EM) done with SDR.

## Designing the rail — text-to-CAD path
We design the rail/gantry parametrically so dimensions are editable and export clean for CNC/3D-print:
- **Zoo "Zookeeper" (zoo.dev)** — conversational/text-to-CAD that emits *real* parametric geometry and
  exports STEP/DXF (CNC-ready). Best for "a 1.5 m antenna carriage rail with NEMA17 mount, 6 bolt holes."
- **OpenSCAD** — fully scriptable; our starter model is `hardware/rail_sar/rail_gantry.scad`.
- **build123d / CadQuery** — parametric CAD *in Python*, so the rail model lives next to the signal code
  (`Text-to-CadQuery` exists if we want LLM-generated CadQuery).

See also `SAR_Algorithms_and_Data.md` for the data + Python processing side.
