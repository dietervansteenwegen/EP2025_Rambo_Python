"""Contain functions to load data from file in the application."""

import logging

from _core.utils.error import ParsingError
from spectrum.spectrum import Spectrum, SpectrumKind
from streamlit.runtime.uploaded_file_manager import UploadedFile

import resources.session_store as store

log = logging.getLogger(__name__)


def load_spectrum_file(
    path: UploadedFile, kind: SpectrumKind = SpectrumKind.sample
) -> None:
    """Load a spectrum from a file. Returns an error message if necessary."""
    try:
        spectrum = Spectrum.from_file(path)
    except Exception as err:
        log.exception(f"Unexpected error parsing {path}")
        raise ParsingError(
            f"Erreur de lecture du spectre dans {path.name}: {err}"
        ) from err

    store.put(kind.name, spectrum)
