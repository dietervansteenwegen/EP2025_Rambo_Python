"""Contain functions to compute the calibration coefficients."""

import numpy as np
from _core.domain.fit import FitResult, linear_fit
from spectrum.spectrum import SpectrumKind

import resources.session_store as store


def compute_calibration(peaks: np.ndarray, energy: list) -> FitResult:
    """Compute the calibration coefficients from the peaks and their energy."""
    return linear_fit(peaks, np.array(energy))


def set_and_save_energy_scale(slope: float, origin: float = 0.0) -> None:
    """Set the energy scale in the spectra and save it in the store."""
    store.put("slope", slope)
    store.put("origin", origin)
    for kind in SpectrumKind:
        if spectrum := store.get(kind.name):
            spectrum.set_energy_scale(slope, origin)
