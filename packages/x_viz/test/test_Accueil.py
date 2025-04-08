"""
Contain the tests of the Accueil page.

As of January 2025, AppTest is missing a lot of interface (e.g.: no file_uploader)
so the test also use mocks.
"""

from unittest.mock import MagicMock, patch

import pytest
import streamlit as st
from path import Path
from resources.plotting import SpectrumError, plot_current_spectrum
from streamlit.testing.v1 import AppTest


def test_app_initialization() -> None:
    """Integration test of the main page."""
    # Initialize the app test
    at = AppTest.from_file("../src/Accueil.py")
    st.session_state = at.session_state  # type: ignore[assignment]

    # Run the app
    at.run()

    # Check if the title is correctly displayed
    assert at.title[0].value == "Accueil"

    # Check if the description is correctly displayed
    assert at.info[0].value == "X-viz affiche et analyse des spectres énergétiques."
    assert not at.expander[0].proto.expanded
    assert at.expander[0].info[0].value == (
        "X-viz affiche et analyse des spectres énergétiques."
    )

    # Simulate validation of an empty form, so no current spectrum
    at.button[0].click()
    at.run()
    with pytest.raises(SpectrumError, match="Aucun spectre chargé"):
        plot_current_spectrum()


@patch("streamlit.plotly_chart")
@patch("streamlit.file_uploader")
def test_file_uploading(
    mock_file_uploader: MagicMock, mock_plotly_chart: MagicMock, data_dir: Path
) -> None:
    """Integration test of the main page."""
    # Initialize the file_uploader mock
    sample_path = data_dir / "co60.csv"
    bkg_path = data_dir / "bkg.csv"

    def return_spectrum_path(*args: object, **kwargs: object) -> Path:  # noqa: ARG001
        """Return a spectrum path for the mock of file_uploader."""
        if args[0] == "Échantillon":
            return sample_path
        return bkg_path

    mock_file_uploader.side_effect = return_spectrum_path

    # Initialize the app test
    at = AppTest.from_file("../src/Accueil.py")
    st.session_state = at.session_state  # type: ignore[assignment]

    # Run the app
    at.run()

    # Test the file uploading
    at.button[0].click()
    at.run()
    mock_plotly_chart.assert_called_once()

    # Test other buttons resetting the application
    at.button[1].click()
    at.button[2].click()
    at.run()
    mock_plotly_chart.assert_called_once()

    # Test error in file uploading
    mock_file_uploader.side_effect = None
    mock_file_uploader.return_value = Path(__file__)  # will trigger an exception
    at.button[0].click()
    at.run()
    mock_plotly_chart.assert_called_once()
