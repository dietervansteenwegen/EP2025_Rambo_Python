"""Contain the function creating figures to plot in the pages."""

from _core.utils.error import SpectrumError
from plotly.graph_objs import Figure
from spectrum.spectrum import SpectrumKind

import resources.session_store as store


def plot_current_spectrum() -> Figure:
    """Plot the spectrum."""
    sample = store.get(SpectrumKind.sample.name)
    if sample is None:
        raise SpectrumError("Aucun spectre chargé")
    fig = sample.plot()
    if (bkg := store.get(SpectrumKind.background.name)) is not None:
        fig.add_scatter(x=bkg.data.index, y=bkg.data, name=bkg.data.name)
    return fig


def plot_spectrum_with_peaks() -> Figure:
    """Plot the spectrum with the peaks highlighted."""
    spectrum = store.get_current_spectrum()
    if spectrum is None:
        raise SpectrumError("Aucun spectre chargé")
    peaks = spectrum.find_peaks()
    fig = spectrum.plot()
    fig.add_scatter(
        x=[spectrum.data.index[p] for p in peaks],
        y=[spectrum.data.iloc[p] for p in peaks],
        mode="markers",
        marker={"symbol": "x", "size": 10, "color": "black"},
        name="pics",
    )
    return fig
