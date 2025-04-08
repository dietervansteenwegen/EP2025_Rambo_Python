"""Handle the application initialization, even in case of reload."""

import base64
import logging
import logging.config

import streamlit as st
from path import Path
from ruamel.yaml import YAML

APP_NAME = "X-Viz"
MAIN_COLOR = "#FF0000"
SECONDARY_COLOR = "white"

_STYLE = """
    section[data-testid="stSidebar"] > div {{
         background-color: {main_color};
    }}
    ul[data-testid="stSidebarNavItems"] * {{
         color: {secondary_color};
    }}
    div[data-testid="stSidebarUserContent"] div[data-testid="stRadio"] * {{
         color: {secondary_color};
    }}
    div[data-testid="stSidebarUserContent"] div[data-testid="stWidgetLabel"] * {{
         color: {secondary_color};
    }}
    div[data-testid="stSidebarUserContent"] label[data-testid="stWidgetLabel"] * {{
         color: {secondary_color};
    }}
    [data-testid="stSidebarNav"]::before {{
        content: "{app_name}";
        margin-left: 30px;
        font-size: 30px;
        position: relative;
        color: {secondary_color};
    }}
"""

_LOGO = """
    [data-testid="stSidebar"] {{
        background-image: {img};
        background-repeat: no-repeat;
        padding-top: 200px;
        background-position: top 0px center;
        background-size: auto 200px;
        background-color: {secondary_color};
    }}
"""


@st.cache_data()
def _get_base64_of_file(file: str) -> str:
    """Return the base 64 encoding of the given file."""
    data = Path(file).read_bytes()
    return base64.b64encode(data).decode()


def initialize_page() -> None:
    """Ensure the application is initialized and initialize the page (title, CSS)."""
    st.set_page_config(page_title=APP_NAME, layout="wide")

    if "is_initialized" not in st.session_state:
        _initialize_app()

    st.markdown(f"<style>{st.session_state.style}</style>", unsafe_allow_html=True)


def _initialize_app() -> None:
    """Initialize the application."""
    src_dir = Path(__file__).parent.parent
    repo_dir = src_dir.parent.parent.parent

    with open(repo_dir / "log_config.yaml") as file:
        yaml = YAML()
        log_config = yaml.load(file)
        # Use absolute path in log config to avoid initialization error in tests
        for pars in log_config["handlers"].values():
            if "filename" in pars:
                pars["filename"] = repo_dir.joinpath(pars["filename"]).absolute()
        logging.config.dictConfig(log_config)
    log = logging.getLogger(__name__)
    log.debug("Logger initialized")

    logo_img = _get_base64_of_file(src_dir / "static" / "photoelectric.png")
    logo_css = _LOGO.format(
        img=f'url("data:image/png;base64,{logo_img}")', secondary_color=SECONDARY_COLOR
    )
    style_css = _STYLE.format(
        app_name=APP_NAME, main_color=MAIN_COLOR, secondary_color=SECONDARY_COLOR
    )
    st.session_state.style = style_css + logo_css

    st.session_state.store = {}

    log.info("Session state variables initialized")
    st.session_state.is_initialized = True
