#!/usr/bin/env python3
"""OpenGoldSDR — Sentinel-1 SAR fetch + first anomaly map over the Georgia Gold Belt.

What it does:
  1. Searches the Alaska Satellite Facility (ASF) archive for free Sentinel-1 scenes over an AOI
     (default: Augusta / Clarks Hill / Little River, GA).
  2. Downloads two scenes (needs a free NASA Earthdata login).
  3. Builds a first-pass *amplitude change / anomaly map* (log-ratio of two passes). Areas that change
     little over time but differ sharply from their surroundings (e.g. quartz boundaries, bedrock
     contacts) stand out; transient changes (moisture, vegetation) get flagged as noise to ignore.

This is a starting point, NOT InSAR. For phase/coherence + the 3-pillar algorithm (autofocus,
coherence time-series, wave-structure inversion) graduate to MintPy / SNAP / GMTSAR — see
docs/SAR_Algorithms_and_Data.md.

Setup:
  pip install asf_search numpy rasterio
  # free Earthdata login: https://urs.earthdata.nasa.gov/  then:
  export EARTHDATA_USER=...  EARTHDATA_PASS=...

Usage:
  python3 sentinel1_georgia.py --search           # list available scenes (no download)
  python3 sentinel1_georgia.py --download 2        # download newest 2 scenes
  python3 sentinel1_georgia.py --anomaly a.tif b.tif   # change map from two GRD geotiffs
"""
from __future__ import annotations
import argparse, os, sys
from pathlib import Path

# Georgia Gold Belt AOI — Augusta / Clarks Hill / Little River (WKT bbox, lon/lat)
AOI_WKT = "POLYGON((-82.45 33.40, -82.05 33.40, -82.05 33.75, -82.45 33.75, -82.45 33.40))"
OUT = Path("~/OpenGoldSDR-data/sentinel1").expanduser()


def search(max_results: int = 20):
    import asf_search as asf
    results = asf.search(
        platform=asf.PLATFORM.SENTINEL1,
        processingLevel=[asf.PRODUCT_TYPE.GRD_HD],   # GRD for amplitude; use SLC for InSAR/phase
        beamMode=asf.BEAMMODE.IW,
        intersectsWith=AOI_WKT,
        maxResults=max_results,
    )
    for r in results:
        p = r.properties
        print(f"{p['sceneName']}  {p['startTime'][:10]}  {p.get('flightDirection','')}  {p['polarization']}")
    print(f"\n{len(results)} scenes over the Georgia Gold Belt AOI")
    return results


def download(n: int):
    import asf_search as asf
    user, pw = os.environ.get("EARTHDATA_USER"), os.environ.get("EARTHDATA_PASS")
    if not (user and pw):
        sys.exit("set EARTHDATA_USER / EARTHDATA_PASS (free at urs.earthdata.nasa.gov)")
    OUT.mkdir(parents=True, exist_ok=True)
    session = asf.ASFSession().auth_with_creds(user, pw)
    results = search(max_results=n)
    results.download(path=str(OUT), session=session)
    print(f"downloaded {n} scene(s) -> {OUT}")


def anomaly(a_tif: str, b_tif: str, out_png: str = "anomaly_map.png"):
    """Log-ratio change/anomaly map between two co-registered amplitude GeoTIFFs."""
    import numpy as np, rasterio
    with rasterio.open(a_tif) as A, rasterio.open(b_tif) as B:
        a = A.read(1).astype("float32"); b = B.read(1).astype("float32")
    eps = 1e-3
    ratio = np.log10((a + eps) / (b + eps))            # change between passes
    # spatial anomaly: how far each pixel deviates from its local neighborhood baseline
    from numpy.lib.stride_tricks import sliding_window_view as swv
    k = 15
    pad = np.pad(ratio, k // 2, mode="reflect")
    local = swv(pad, (k, k)).mean(axis=(-1, -2))
    anom = ratio - local
    z = (anom - np.nanmean(anom)) / (np.nanstd(anom) + eps)
    try:
        import matplotlib.pyplot as plt
        plt.imsave(out_png, np.clip(z, -3, 3), cmap="magma")
        print(f"anomaly map -> {out_png} (bright = strong, stable spatial anomaly)")
    except ImportError:
        np.save(out_png.replace(".png", ".npy"), z)
        print(f"matplotlib missing; saved array -> {out_png.replace('.png','.npy')}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--search", action="store_true")
    ap.add_argument("--download", type=int, metavar="N")
    ap.add_argument("--anomaly", nargs=2, metavar=("A.tif", "B.tif"))
    args = ap.parse_args()
    if args.search: search()
    elif args.download: download(args.download)
    elif args.anomaly: anomaly(*args.anomaly)
    else: ap.print_help()
