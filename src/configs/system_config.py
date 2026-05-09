import tomllib
import platform

from pathlib import Path


# =========================
# Root
# =========================

ROOT_DIR = Path(__file__).resolve().parents[2]


# =========================
# pyproject.toml
# =========================

PYPROJECT_PATH = ROOT_DIR / "pyproject.toml"


with open(PYPROJECT_PATH, "rb") as file:
    pyproject = tomllib.load(file)


PROJECT = pyproject["project"]


# =========================
# Project Metadata
# =========================

PROJECT_NAME = PROJECT["name"]

VERSION = PROJECT["version"]

DESCRIPTION = PROJECT.get(
    "description",
    ""
)


# Nome amigável
NAME = PROJECT_NAME.replace(
    "-",
    " "
).title()


# =========================
# Runtime Paths
# =========================

CURRENT_PATH = Path.cwd()

HOME_PATH = Path.home()


try:

    relative = CURRENT_PATH.relative_to(
        HOME_PATH
    )

    CURRENT_PATH_TILDE = (
        Path("~") / relative
    )

except ValueError:

    CURRENT_PATH_TILDE = CURRENT_PATH


# =========================
# Platform
# =========================

SYSTEM = platform.system()

IS_WINDOWS = SYSTEM == "Windows"

IS_LINUX = SYSTEM == "Linux"

IS_MAC = SYSTEM == "Darwin"