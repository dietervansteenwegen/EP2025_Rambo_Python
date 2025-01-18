"""Welcome page, first page loaded."""

import logging

import resources.session_store as store
import streamlit as st
from _core.utils.error import ParsingError
from resources.file_loading import SpectrumKind, load_spectrum_file
from resources.page_initialization import initialize_page
from resources.plotting import plot_current_spectrum
from streamlit import file_uploader, plotly_chart

# Initialize the page
initialize_page()
st.title("Accueil")
log = logging.getLogger(__name__)

DESCRIPTION = """X-viz affiche et analyse des spectres énergétiques."""
with st.expander(label="Description de l'application"):
    st.info(DESCRIPTION)

clear_spectrum = st.sidebar.button("Suppression de(s) spectre(s)")
if clear_spectrum:
    store.clean_spectrum()

reset = st.sidebar.button("Remise à zéro complète")
if reset:
    store.clean()

with st.form("Chargement du ou des spectre(s):"):
    sample_file = file_uploader("Échantillon")
    with st.expander(label="Bruit de fond"):
        bkg_file = file_uploader("Bruit de fond", label_visibility="collapsed")
    submit = st.form_submit_button("Valider")

if submit:
    if sample_file is not None:
        try:
            load_spectrum_file(sample_file)
        except ParsingError as err:
            st.error(f"Impossible de lire le spectre de l'échantillon: {err}")
            st.stop()
    if bkg_file is not None:
        try:
            load_spectrum_file(bkg_file, SpectrumKind.background)
        except ParsingError as err:
            st.error(f"Impossible de lire le spectre de bruit de fond: {err}")
            st.stop()

if store.get_current_spectrum() is not None:
    plotly_chart(plot_current_spectrum())
