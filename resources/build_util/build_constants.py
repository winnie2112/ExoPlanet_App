"""Generate and retrieve build time constants for use in executables."""

import sys
from pathlib import Path

import toml

from resources.constants import VERSION_ID


def generate_constants(out_file_path: str, out_file_name: str = "_constants.py") -> str:
    """Generate build time constants for use in executables."""
    project_toml = toml.load("pyproject.toml")
    tool_poetry = project_toml["tool"]["poetry"]
    build_constants = {
        "name": tool_poetry["name"],
        VERSION_ID: tool_poetry[VERSION_ID],
    }
    path = Path(out_file_path)
    constants_path = (path / out_file_name).resolve()

    if path.exists():
        with open(constants_path, "w", encoding="ascii") as file:
            toml.dump(build_constants, file)
        return str(constants_path)
    return ""


def resource_path() -> Path:
    """Get absolute path to resource, works for dev and for PyInstaller."""
    return Path(getattr(sys, "_MEIPASS", str(Path(__file__).resolve().parent)))


def get_constant(key: str, fallback: str, file_name: str = "_constants.py") -> str:
    """Return a constant."""
    constants_file_path = resource_path() / file_name
    if constants_file_path.exists():
        constants = toml.load(constants_file_path)
        if key in constants:
            return str(constants[key])
    return fallback
