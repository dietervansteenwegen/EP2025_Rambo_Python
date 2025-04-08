"""Python tasks."""


# noinspection PyUnresolvedReferences

DOIT_CONFIG = {"default_tasks": ["pycheck"]}


def task_fmt() -> dict:
    """Format the code."""
    return {
        "actions": [
            "pre-commit run pretty-format-json --all-files",
            "pre-commit run pymarkdown --all-files",
        ],
        "task_dep": ["pyfmt"],
    }


def task_pyfmt() -> dict:
    """Format the code."""
    return {"actions": ["uv run ruff format ."]}


def task_lint() -> dict:
    """Lint the code."""
    return {"actions": ["uv run ruff check ."]}


def task_type() -> dict:
    """Check the types."""
    return {"actions": ["uv run mypy ."]}


def task_pycheck() -> dict:
    """Run all the Python quality tools."""
    return {
        "actions": None,
        "verbosity": 1,
        "task_dep": ["pyfmt", "lint", "type"],
    }


def task_precom(file: str = "") -> dict:
    """Run all the pre-commit checks."""
    cmd = "pre-commit run"
    cmd += f" --files {file}" if file else " --all-files"
    return {"actions": [cmd]}


def task_test() -> dict:
    """Run the tests."""
    return {
        "actions": ["uv run pytest"],
        "verbosity": 1,
    }


def task_lab() -> dict:
    """Run Jupyter lab."""
    return {"actions": ["uv run jupyter lab"]}


def task_app() -> dict:
    """Launch the app."""
    return {"actions": ["cd packages/x_viz && uv run streamlit run src/Accueil.py"]}


def task_lint_dockerfile() -> dict:
    """Lint the Dockerfile."""
    return {"actions": ["docker run --rm -i docker.io/hadolint/hadolint < Dockerfile"]}
