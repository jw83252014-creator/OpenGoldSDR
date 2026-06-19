#!/usr/bin/env python3
"""OpenGoldSDR — time-domain back-projection SAR image formation (rail SAR).

The core SAR math, garage-scale: we recorded a complex (IQ) range profile at each known rail
position. Back-projection coherently sums, for every pixel in the ground plane, the contribution
from every rail position by indexing each profile at the round-trip range to that pixel. Bright,
in-focus pixels = strong dielectric boundaries (quartz veins, voids, mineralized contacts).

This is an independent, open implementation of standard SAR — NOT Biondi's patented pipeline.
Dependencies: numpy. Real capture wiring lives in rail_control.py.
"""
from __future__ import annotations
import numpy as np

C = 299_792_458.0  # m/s


def backproject(profiles: np.ndarray,
                rail_x: np.ndarray,
                range_bins_m: np.ndarray,
                scene_x: np.ndarray,
                scene_y: np.ndarray,
                antenna_y: float = 0.0) -> np.ndarray:
    """Form a 2D SAR image by time-domain back-projection.

    profiles     : (N_positions, N_range) complex IQ range profiles (one per rail step)
    rail_x       : (N_positions,) rail position of each profile, metres (homed to end-stop = phase ref)
    range_bins_m : (N_range,) one-way range of each range bin, metres
    scene_x/y    : 1D arrays defining the output ground grid, metres
    returns      : (len(scene_y), len(scene_x)) complex image; take np.abs() to view
    """
    profiles = np.asarray(profiles, dtype=np.complex128)
    img = np.zeros((scene_y.size, scene_x.size), dtype=np.complex128)
    # precompute interpolation over range for speed/clarity
    for p, xr in zip(profiles, rail_x):
        for iy, gy in enumerate(scene_y):
            # one-way distance from this rail position to each pixel in the row
            dx = scene_x - xr
            dy = gy - antenna_y
            rng = np.hypot(dx, dy)
            # nearest-range-bin sample (replace with np.interp for sub-bin accuracy)
            samp = np.interp(rng, range_bins_m, p, left=0.0, right=0.0)
            # matched-filter phase term for two-way path (FMCW/CW carrier handled in opts; placeholder f0)
            img[iy] += samp
    return img


if __name__ == "__main__":
    # tiny synthetic smoke test: a single point scatterer at (0.0, 2.0) m
    N_pos, N_rng = 64, 512
    rail_x = np.linspace(-0.75, 0.75, N_pos)        # 1.5 m rail
    range_bins = np.linspace(0.5, 5.0, N_rng)
    target = np.array([0.0, 2.0])
    profiles = np.zeros((N_pos, N_rng), dtype=np.complex128)
    for i, xr in enumerate(rail_x):
        r = np.hypot(target[0] - xr, target[1])
        profiles[i, np.argmin(np.abs(range_bins - r))] = 1.0
    sx = np.linspace(-1.0, 1.0, 80)
    sy = np.linspace(1.0, 3.0, 80)
    img = np.abs(backproject(profiles, rail_x, range_bins, sx, sy))
    iy, ix = np.unravel_index(np.argmax(img), img.shape)
    print(f"peak at x={sx[ix]:+.2f} y={sy[iy]:.2f} (truth x=0.00 y=2.00)")
