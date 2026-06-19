# Rail SAR — shopping list + portable "v2" design

Goal: genius-simple, **cheap**, and **transportable** — backpack-portable, battery-powered, assembles
in the field. Builds on `Ground_Based_Rail_SAR.md`; informed by the competitive-landscape finding that
the closest real kin is **Jean-Michel Friedt's SDR-GB-SAR / `sentinel1_pbr`** (passive radar using a
free illuminator) — which points at the cheapest path of all.

## v2 design moves (cheap + portable)
1. **Segmented/folding rail.** Instead of one rigid 1.5 m extrusion, use **3× 0.5 m 2020 segments** that
   bolt together with corner brackets → assembles to 1.5 m, breaks down into a backpack. (Or a
   telescoping aluminum/carbon track.) Aperture length is preserved; transport size shrinks 3×.
2. **3D-print the moving parts.** Carriage, antenna post, stepper bracket, end-stop mount all print from
   our `rail_gantry.scad` → near-zero cost, easy to replace in the field.
3. **One SDR, no separate transmitter (passive option).** Following Friedt: use an ambient/known
   illuminator (broadcast tower, Sentinel-1 passes, or a cheap CW beacon) so you carry only a HackRF/
   RTL-SDR v4 + RPi. Lighter, cheaper, lower power than active FMCW. Keep active FMCW as the "deeper" mode.
4. **Battery + tripod.** USB-C power bank runs RPi + SDR + stepper driver; rail clamps to a camera tripod
   or lays on the ground on feet. Fully cordless field rig.
5. **Phone as the screen.** RPi headless; drive/monitor from the phone over the agent bridge (we already
   have a phone lane). No laptop in the field.

## Shopping list — Tier-1 portable build (~$300–$550)
| Part | Example | ~$ |
|---|---|---|
| SDR receiver | RTL-SDR v4 (Blog) **or** HackRF One (for Tx/FMCW) | 40 / 150 |
| Low-noise amp / upconverter | LNA + Ham-It-Up style upconverter (for VLF/HF) | 40 |
| Rail | 3× 0.5 m 2020 aluminum extrusion + corner brackets + GT2 belt + pulley | 60 |
| Motion | NEMA17 stepper + A4988/DRV8825 driver + end-stop microswitch | 30 |
| Compute | Raspberry Pi 4/5 + SD card | 60–90 |
| Antennas | DIY copper horn / waveguide cans **or** PCB log-periodic | 20–40 |
| Power | USB-C power bank (PD) + buck converters | 35 |
| Position | (optional, recommended) u-blox **RTK GPS** for cm-accurate field tags | 0–200 |
| Mounting | camera tripod + 3D-printed clamps/carriage | 25 |

Budget core (RTL-SDR path): ~$300. Deeper/active (HackRF + RTK): ~$550–750.

## Frequency reality (keeps us honest)
Penetration vs. resolution is the core tradeoff: high microwave = sharp but dies in damp soil; VLF/HF =
deeper but coarse. Carry two modes — VLF/HF EM for depth, the rail SAR for shallow high-res structure —
and **map dielectric/structural boundaries that host gold, not gold itself** (per the paper's framing).

## Iterate further (open ideas)
- Carbon-fiber telescoping rail for max portability.
- Add an IMU/encoder on the carriage so position is logged even on an imperfect rail.
- A "corner reflector" calibration target (per experiment E0) to prove the rig before field use.
- Kit-ify it: a documented BOM + printed-parts pack = the "sell-the-plan" product.
