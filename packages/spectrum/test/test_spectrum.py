"""Unitary test of the spectrum module."""

from math import isclose

import numpy as np
from pandas import Timedelta
from path import Path
from spectrum.spectrum import Spectrum, analyze_sample

CO60_PEAKS_ENERGY = (1173.2, 1332.5)


def test_spectrum() -> None:
    """Unitary test of the Spectrum class."""
    spectrum = Spectrum(np.array([1, 2, 3, 4, 5]), 10.0)
    assert spectrum.live_time == Timedelta(seconds=10.0)
    assert repr(spectrum).startswith("Spectrum")
    assert str(spectrum).startswith("Spectrum")
    assert spectrum.data.tolist() == [0.1, 0.2, 0.3, 0.4, 0.5]

    repo_dir = Path(__file__).parent.parent.parent.parent
    data_path = repo_dir / "data"
    sample_path = data_path / "co60.csv"
    bkg_path = data_path / "bkg.csv"

    sample = Spectrum.from_file(sample_path)
    bkg = Spectrum.from_file(bkg_path)
    diff = sample - bkg
    assert len(sample.data) == 16384

    peaks = diff.find_peaks()
    assert len(peaks) == 2
    peaks2 = diff.find_peaks()
    assert len(peaks2) == 2

    diff.set_energy_scale(1.0)
    diff.set_energy_scale(0.18741176, -1.8717647058820148)
    assert isclose(diff.data.index[peaks[0]], CO60_PEAKS_ENERGY[0], abs_tol=0.01)
    assert diff.plot().layout.xaxis.title.text == "E [keV]"

    diff.reset_energy_scale()
    assert diff.data.index[peaks[0]] == peaks[0]
    assert diff.plot().layout.xaxis.title.text == "bins []"

    fig = analyze_sample(sample_path, bkg_path)
    assert all(fig.data[-1]["x"] == peaks)
