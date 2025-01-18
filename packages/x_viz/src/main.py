"""Run the app from a single script."""

import sys

from path import Path
from streamlit import runtime
from streamlit.web import cli as stcli


def main() -> int:
    """Launch the app."""
    if runtime.exists():
        return stcli.main()
    start_page = Path(__file__).parent / "Accueil.py"
    sys.argv = ["streamlit", "run", start_page]
    return stcli.main()


if __name__ == "__main__":
    sys.exit(main())
