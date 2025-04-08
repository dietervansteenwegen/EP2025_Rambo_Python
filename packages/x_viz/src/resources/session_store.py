"""Manage the session state, which persists data across page changes."""

import logging
from typing import Any

import streamlit as st
from spectrum.spectrum import Spectrum, SpectrumKind

log = logging.getLogger(__name__)


def put(key: str, val: Any) -> None:  # noqa: ANN401
    """Set a value in the session state store."""
    st.session_state.store[key] = val


def get(key: str, default_value: Any = None) -> Any:  # noqa: ANN401
    """Get a value from the session state store."""
    return st.session_state.store.get(key, default_value)


def clean() -> None:
    """Clean the session state store."""
    log.info("Reset")
    st.session_state.store.clear()


def clean_spectrum() -> None:
    """Clean the spectrum from the store."""
    log.info("Clear spectrum")
    for kind in SpectrumKind:
        st.session_state.store.pop(kind.name, None)


def get_current_spectrum() -> Spectrum | None:
    """Return the sample spectrum, minus the background if loaded."""
    diff = st.session_state.store.get(SpectrumKind.diff.name)
    if diff is not None:
        return diff

    sample = st.session_state.store.get(SpectrumKind.sample.name)
    bkg = st.session_state.store.get(SpectrumKind.background.name)
    if sample is not None and bkg is not None:
        diff = sample - bkg
        st.session_state.store[SpectrumKind.diff.name] = diff
        return diff
    return sample
