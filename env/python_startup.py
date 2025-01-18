"""Python script executed at each launch of the interpreter."""

# standard library import
from __future__ import annotations

import json
import random
import re
import string
import sys
from collections import *
from itertools import *
from pprint import pprint
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence


if sys.version_info >= (3, 11):
    NOFLAG = re.NOFLAG
else:
    NOFLAG = 0


def grep(pattern: str, sequence: Sequence[str], keep_case: bool = False) -> list[str]:
    """Return the sequence elements containing the pattern."""
    if keep_case:
        return [el for el in sequence if pattern in el]
    pattern = pattern.lower()
    return [el for el in sequence if pattern in el.lower()]


def rgrep(regex: str, sequence: Sequence[str], flag=NOFLAG) -> list[str]:
    """Return the sequence elements matching the regex."""
    return [el for el in sequence if re.search(regex, el, flag)]


#
# weak random sequence generator, can be used for a weak test password
def generate_weak_random_sequence(size: int = 16, alpha_only: bool = False):
    """Generate a password of given size, by default containing special characters."""
    letters = string.ascii_letters if alpha_only else string.printable[:-6]
    return "".join(letters[random.randint(0, len(letters) - 1)] for _ in range(size))


#
# non standard library import
try:
    from path import Path

    HAS_PATH = True
    wd = Path.cwd()
except ImportError:
    print("path.py is not available in this (virtual ?) environment")
    HAS_PATH = False

try:
    import ruamel.yaml as yaml
except ImportError:
    print("ruamel.yaml is not available in this (virtual ?) environment")

try:
    import pendulum
    from pendulum import Date, DateTime, Duration, Interval, Time

    tz = "Europe/Paris"
    now = pendulum.now()
    today = Date.today()
except ImportError:
    print("pendulum is not available in this (virtual ?) environment")

try:
    import numpy
    import numpy as np
except ImportError:
    print("numpy is not available in this (virtual ?) environment")

try:
    import pandas
    import pandas as pd
    from pandas import DataFrame, DatetimeIndex, Index, Series, Timestamp

    di = pd.date_range(
        start=Timestamp(2018, 9, 9, 9),
        end=Timestamp(2018, 9, 9, 10),
        freq="10min",
        tz="Europe/Paris",
    )
    df = DataFrame(
        dict(
            bool=np.random.randint(2, size=len(di), dtype=bool),
            int=np.arange(0, -len(di), -1),
            float=np.random.rand(len(di)) * 10.0,
            string=[random.choice(string.ascii_letters) * 5 for i in range(len(di))],
        ),
        index=di,
    )
except ImportError:
    print("pandas is not available in this (virtual ?) environment")

try:
    import plotly
    import plotly.graph_objects as pg
    from plotly.subplots import make_subplots

    if "pandas" in sys.modules:
        import plotly.express as px

        try:
            pandas.options.plotting.backend = "plotly"
        except Exception:
            print("Your pandas version does not support plotly as backend")

    def plot(data_ax1: DataFrame, data_ax2: DataFrame | None = None) -> None:
        """Plot simply a DataFrame, and optionaly a second one on a second axis."""
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        x = data_ax1.index
        for col in data_ax1:
            fig.add_trace(pg.Scatter(x=x, y=data_ax1[col], name=col), secondary_y=False)
        if data_ax2 is None or data_ax2.empty:
            fig.show()
            return
        x = data_ax2.index
        for col in data_ax2:
            fig.add_trace(pg.Scatter(x=x, y=data_ax2[col], name=col), secondary_y=True)
        fig.show()

    def html_plot_to_image(path: str, img_format: str = "svg") -> pg.Figure:
        """Save a plotly figure written as HTML in the given image format."""
        with open(path) as istream:
            html = istream.read()
        call_arg_str = re.findall(r"Plotly\.newPlot\((.*)\)", html[-(2**17) :])
        if not call_arg_str:
            call_arg_str = re.findall(r"Plotly\.newPlot\((.*)\)", html)
        call_args = json.loads(f"[{call_arg_str[0]}]")
        plotly_json = {"data": call_args[1], "layout": call_args[2]}
        fig = plotly.io.from_json(json.dumps(plotly_json))
        fig.write_image(".".join((path.removesuffix(".html"), img_format)))
        return fig

except ImportError:
    print("plotly is not available in this (virtual ?) environment")
