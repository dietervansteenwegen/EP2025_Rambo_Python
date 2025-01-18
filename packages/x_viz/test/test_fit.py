"""Unitary test of the fit module."""

import numpy as np
import pytest

# noinspection PyProtectedMember
from _core.domain.fit import linear_fit
from _core.utils.error import InputError


def test_linear_fit() -> None:
    """Unitary test of the linear_fit function."""
    # Define input data
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([2, 4, 6, 8, 10])

    # Call the function to be tested
    model = linear_fit(x, y)

    # Check the model's coefficients
    assert np.isclose(model.slope, 2.0)
    assert np.isclose(model.origin, 0.0)

    # Test the function with a single value in x
    x_single = np.array([5])
    y_single = np.array([10])
    model_single = linear_fit(x_single, y_single)
    assert np.isclose(model_single.slope, 1.0)
    assert np.isclose(model_single.origin, 5.0)

    # Test case with empty x array
    empty = np.array([])
    z = np.array([1, 2, 3])
    with pytest.raises(InputError, match="Incorrect input for an affine fit: x#0, y#3"):
        linear_fit(empty, z)

    # Test case with empty y array
    with pytest.raises(InputError, match="Incorrect input for an affine fit: x#3, y#0"):
        linear_fit(z, empty)

    # Test case with mismatched sizes
    x_mismatch = np.array([1, 2])
    y_mismatch = np.array([1, 2, 3])
    with pytest.raises(InputError, match="Incorrect input for an affine fit: x#2, y#3"):
        linear_fit(x_mismatch, y_mismatch)
