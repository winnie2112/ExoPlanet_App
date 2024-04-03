"""Backend for exoplanet app."""

from pathlib import Path
from typing import TypedDict

import cv2
import numpy as np
import numpy.typing as npt

TOI_700d = Path(r"resources\pictures\toi-700d.png")
TOI_700d_Log = Path(r"resources\entry_logs\toi-700d.txt")
TOI_700d_Params = Path(r"resources\parameters\toi-700d.txt")

ROSS_128b = Path(r"resources\pictures\ross-128b.png")
ROSS_128b_Log = Path(r"resources\entry_logs\ross-128b.txt")
ROSS_128b_Params = Path(r"resources\parameters\ross-128b.txt")

TRAPPIST_1e = Path(r"resources\pictures\trappist-1e.png")
TRAPPIST_1e_Log = Path(r"resources\entry_logs\trappist-1e.txt")
TRAPPIST_1e_Params = Path(r"resources\parameters\trappist-1e.txt")

KEPLER_62e = Path(r"resources\pictures\kepler-62e.png")
KEPLER_62e_Log = Path(r"resources\entry_logs\kepler-62e.txt")
KEPLER_62e_Params = Path(r"resources\parameters\kepler-62e.txt")


class SelectionData(TypedDict):
    """Allow the user to select planet."""

    planet: str


def read_image(img_path: Path) -> npt.NDArray[np.uint8]:
    """Read png image."""
    return cv2.imread(str(img_path), cv2.IMREAD_UNCHANGED)


def read_log(discovery_path: Path) -> str:
    """Read text."""
    file = open(discovery_path, "r")
    return file.read()


class ExoPlanetBakend:
    """Backend to display information."""

    def __init__(self) -> None:
        """Initialize the backend."""

    def params_entry(self, user_data: SelectionData) -> str:
        """Planet parameters."""
        if user_data["planet"] == "TOI-700 d":
            params_log = read_log(TOI_700d_Params)
        if user_data["planet"] == "ROSS-128 b":
            params_log = read_log(ROSS_128b_Params)
        if user_data["planet"] == "TRAPPIST-1 e":
            params_log = read_log(TRAPPIST_1e_Params)
        if user_data["planet"] == "KEPLER-62 e":
            params_log = read_log(KEPLER_62e_Params)
        return params_log

    def display_planets(self, user_data: SelectionData) -> npt.NDArray[np.uint8]:
        """Display the planet (hypothetical) images."""
        if user_data["planet"] == "TOI-700 d":
            image = read_image(TOI_700d)
        if user_data["planet"] == "ROSS-128 b":
            image = read_image(ROSS_128b)
        if user_data["planet"] == "TRAPPIST-1 e":
            image = read_image(TRAPPIST_1e)
        if user_data["planet"] == "KEPLER-62 e":
            image = read_image(KEPLER_62e)
        return np.array(image)

    def log_entry(self, user_data: SelectionData) -> str:
        """Discovery note of each planet."""
        if user_data["planet"] == "TOI-700 d":
            discovery_entry = read_log(TOI_700d_Log)
        if user_data["planet"] == "ROSS-128 b":
            discovery_entry = read_log(ROSS_128b_Log)
        if user_data["planet"] == "TRAPPIST-1 e":
            discovery_entry = read_log(TRAPPIST_1e_Log)
        if user_data["planet"] == "KEPLER-62 e":
            discovery_entry = read_log(KEPLER_62e_Log)
        return discovery_entry
