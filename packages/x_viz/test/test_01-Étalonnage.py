"""
Contain the tests of the 01-Étalonnage page.

As of January 2025, AppTest is missing a lot of interface (e.g.: no file_uploader)
so the test also use mocks.
"""

from math import isclose

import streamlit as st
from path import Path
from spectrum.spectrum import Spectrum
from streamlit.testing.v1 import AppTest


# noinspection PyPep8Naming
def test_Etalonnage_page(data_dir: Path) -> None:
    """Integration test of the Etalonnage page."""
    # Initialize the app test
    at = AppTest.from_file("../src/pages/01-Étalonnage.py")
    st.session_state = at.session_state  # type: ignore[assignment]

    # Run the app
    at.run()

    # Check if the page stopped early
    assert at.error[0].value == "Il est nécessaire de charger un spectre d'abord"

    # Set a spectrum and re-run the page
    at.session_state.store["sample"] = Spectrum.from_file(data_dir / "co60.csv")
    at.run()

    at.number_input[2].set_value(1173.2)
    at.number_input[3].set_value(1332.5)
    at.button[1].click()
    at.run()

    assert isclose(at.session_state.store["slope"], 0.19, abs_tol=0.01)
    assert isclose(at.session_state.store["origin"], -1.87, abs_tol=0.01)
