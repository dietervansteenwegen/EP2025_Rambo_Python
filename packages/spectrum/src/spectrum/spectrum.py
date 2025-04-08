"""Contains the Spectrum class representing an energy spectrum."""

import logging
from enum import Enum, auto, unique
from io import BytesIO
from typing import Self

import pandas as pd
from numpy import ndarray
from pandas import DataFrame, Series, Timedelta, read_csv
from path import Path
from plotly.graph_objs import Figure
from scipy.signal import find_peaks

pd.options.plotting.backend = "plotly"
log = logging.getLogger(__name__)


@unique
class SpectrumKind(Enum):
    """Identify what kind of spectrum is analysed."""

    sample = auto()
    background = auto()
    diff = auto()


class Spectrum:
    """An energy spectrum."""

    def __init__(self, data: ndarray | Series, live_time: float = 1.0):
        """Initialize self."""
        self._data: Series
        if isinstance(data, Series):
            self._data = data / live_time
        else:
            self._data = Series(data) / live_time
        self._live_time: Timedelta = Timedelta(seconds=live_time)
        self._slope: float | None = None
        self._origin: float = 0.0
        self._peaks: ndarray | None = None

    def __repr__(self) -> str:
        """Return repr(self)."""
        return (
            f"{self.__class__.__name__}({self._data},"
            f" {self._live_time.total_seconds()})"
        )

    def __str__(self) -> str:
        """Return str(self)."""
        return (
            f"{self.__class__.__name__}:\n"
            f"Live time: {self._live_time}\n"
            f"Energy scale: {self._slope} keV/bin x val + {self._origin}\n"
            f"{self._data}"
        )

    @property
    def data(self) -> Series:
        """Return the internal data."""
        return self._data

    @property
    def live_time(self) -> Timedelta:
        """Return the live time in seconds."""
        return self._live_time

    @classmethod
    def from_file(cls, file: Path | BytesIO) -> Self:
        """Initialize the spectrum from a file."""
        log.info(f"Creating a Spectrum from: {file.name}")

        # Load the data, only 1 column
        spectrum: Series = read_csv(file).iloc[:, 0]

        # Recover the live time from the column name : "name @ [live_time]s"
        live_time = float(str(spectrum.name).split("@")[1].strip("s"))

        return cls(spectrum, live_time)

    def __sub__(self, other: Self) -> "Spectrum":
        """Subtract other from self, keeping self index."""
        spectrum = Spectrum(self.data.to_numpy() - other.data.to_numpy())
        spectrum._slope = self._slope
        spectrum._origin = self._origin
        return spectrum

    def find_peaks(self, prominence_factor: float = 0.1) -> ndarray:
        """Find the peaks of the spectrum."""
        if self._peaks is not None:
            return self._peaks
        # noinspection PyTypeChecker
        prominence = self._data.max() * prominence_factor
        self._peaks = find_peaks(self._data.to_numpy(), prominence=prominence)[0]
        return self._peaks

    def reset_energy_scale(self) -> None:
        """Reset the energy scale, showing the spectrum in bins."""
        self._data = self._data.reset_index(drop=True)
        self._slope = None
        self._origin = 0.0

    def set_energy_scale(self, slope_in_kev: float, origin: float = 0.0) -> None:
        """Set the spectrum energy scale."""
        if self._slope is not None:
            self.reset_energy_scale()
        self._slope = slope_in_kev
        self._origin = origin
        self._data.index = self._origin + self._slope * self._data.index

    def plot(self) -> Figure:
        """Plot the spectrum."""
        fig: Figure = self._data.plot()
        fig.update_xaxes(title_text="E [keV]" if self._slope else "bins []")
        fig.update_yaxes(title_text="Hit rate [/s]")
        return fig


def analyze_sample(sample_path: Path, bkg_path: Path) -> Figure:
    """Load a sample and a background spectrum, subtract them and find peaks."""
    bkg = Spectrum.from_file(bkg_path)
    sample = Spectrum.from_file(sample_path)
    diff: Spectrum = sample - bkg
    peaks = diff.find_peaks()
    analysis = DataFrame({"bkg": bkg.data, "sample": sample.data, "diff": diff.data})
    fig = analysis.plot()
    fig.add_scatter(
        x=diff.data.index[peaks],
        y=diff.data.iloc[peaks],
        mode="markers",
        marker={"symbol": "x", "size": 10, "color": "black"},
    )
    return fig
