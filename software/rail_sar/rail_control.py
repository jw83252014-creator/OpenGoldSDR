#!/usr/bin/env python3
"""OpenGoldSDR — rail control + capture sync (skeleton).

Drives the NEMA17 stepper along the rail in precise increments and, at each stop, triggers an IQ
capture from the SDR/FMCW frontend. Output is a stack of (position, IQ profile) pairs that feed
backprojection.py. The whole measurement depends on KNOWING the position exactly, so: home against
the end-stop first, then count steps; log the step count with every capture.

Hardware-agnostic by design — fill in `step_motor()` and `capture_iq()` for your parts
(e.g. RPi.GPIO / gpiozero for the stepper; SoapySDR / pyrtlsdr / hackrf for the radio).
"""
from __future__ import annotations
import json, time
from dataclasses import dataclass, asdict
from pathlib import Path
import numpy as np


@dataclass
class ScanConfig:
    rail_length_m: float = 1.5
    n_positions: int = 64          # steps across the rail = synthetic aperture samples
    settle_s: float = 0.25         # let vibration die before capturing (position must be still)
    out_dir: str = "~/OpenGoldSDR-data/scans"


def home_to_endstop() -> None:
    """Back the carriage into the end-stop = position datum / SAR phase reference. TODO: wire switch."""
    # while not endstop_pressed(): step_motor(-1)
    pass


def step_motor(steps: int) -> None:
    """Move the carriage `steps` microsteps (sign = direction). TODO: GPIO to the stepper driver."""
    pass


def capture_iq(n_samples: int = 4096) -> np.ndarray:
    """Grab one complex IQ range profile from the SDR/FMCW frontend. TODO: SoapySDR/hackrf/rtlsdr."""
    return np.zeros(n_samples, dtype=np.complex64)  # placeholder


def run_scan(cfg: ScanConfig = ScanConfig()) -> Path:
    out = Path(cfg.out_dir).expanduser()
    out.mkdir(parents=True, exist_ok=True)
    home_to_endstop()
    dx = cfg.rail_length_m / (cfg.n_positions - 1)
    steps_per_pos = 200  # TODO: derive from belt pitch / lead-screw + microstepping
    rail_x, profiles = [], []
    for i in range(cfg.n_positions):
        if i:
            step_motor(steps_per_pos)
        time.sleep(cfg.settle_s)
        rail_x.append(i * dx)
        profiles.append(capture_iq())
    stamp = int(time.time())
    np.savez(out / f"scan-{stamp}.npz",
             rail_x=np.array(rail_x), profiles=np.array(profiles))
    (out / f"scan-{stamp}.json").write_text(json.dumps(asdict(cfg), indent=2))
    print(f"saved {cfg.n_positions} captures -> {out}/scan-{stamp}.npz  (feed to backprojection.py)")
    return out / f"scan-{stamp}.npz"


if __name__ == "__main__":
    run_scan()
