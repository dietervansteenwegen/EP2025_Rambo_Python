"""Contain functions to fit data with a model."""

from dataclasses import dataclass
from typing import cast

import numpy as np

from _core.utils.error import InputError


@dataclass
class FitResult:
    """Result of a linear fit."""

    slope: float
    origin: float


def linear_fit(x: np.ndarray, y: np.ndarray) -> FitResult:
    """Find a and b which minimize the distance of y` = a * x + b to y."""
    size_x = len(x)
    size_y = len(y)
    if size_x == 0 or size_y == 0 or size_x != size_y:
        raise InputError(f"Incorrect input for an affine fit: x#{size_x}, y#{size_y}")

    b, a = np.polynomial.polynomial.Polynomial.fit(x, y, 1, domain=[])
    return FitResult(cast(float, a), cast(float, b))
