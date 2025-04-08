"""Peak analysis of a spectrum."""

import logging

import resources.session_store as store
import streamlit as st
from resources.calibration import compute_calibration, set_and_save_energy_scale
from resources.file_loading import SpectrumKind
from resources.page_initialization import initialize_page
from resources.plotting import plot_spectrum_with_peaks

# Initialize the page
initialize_page()
st.title("Étalonnage")
log = logging.getLogger(__name__)

slope = store.get("slope", 0.0)
origin = store.get("origin", 0.0)
st.sidebar.markdown(f"- **Origine: {origin:.3f}**\n- **Pente: {slope:.3f}**")

# Check a spectrum has been loaded
spectrum = store.get(SpectrumKind.sample.name)
if spectrum is None:
    st.error("Il est nécessaire de charger un spectre d'abord")
    st.stop()

# Manual coefficient
st.markdown("# Coefficients manuels")
with st.form("Coefficients"):
    slope = st.number_input("Énergie par bin en keV", value=slope)
    origin = st.number_input("Énergie à l'origine en keV", value=origin)
    submit_manual = st.form_submit_button("Appliquer")

if submit_manual:
    set_and_save_energy_scale(slope, origin)

# Peak research and fit
st.markdown("# Recherche de pics et ajustement de l'énergie")

peaks = spectrum.find_peaks()
st.plotly_chart(plot_spectrum_with_peaks())

with st.form("Énergie des pics"):
    energy = [0.0] * len(peaks)
    for i, peak in enumerate(peaks):
        bin_col, e_col = st.columns(2)
        with bin_col:
            st.markdown(f"- Pic à {peak} : énergie en keV =")
        with e_col:
            energy[i] = st.number_input(
                "", value=0.0, key=f"energy {i}", label_visibility="collapsed"
            )

    submit_peaks = st.form_submit_button("Calculer l'étalonnage")

if submit_peaks:
    if len(peaks):
        result = compute_calibration(peaks, energy)
        set_and_save_energy_scale(result.slope, result.origin)
    else:
        st.warning("Aucun pic trouvé, impossible de calculer l'étalonnage")
