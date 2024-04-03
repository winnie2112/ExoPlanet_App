"""Gui app entry point."""

import sys
from pathlib import Path

import numpy as np
import numpy.typing as npt
from PySide6.QtCore import Property, QObject, QSize, QUrl, Signal, Slot
from PySide6.QtGui import QGuiApplication, QIcon, QImage
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickImageProvider

from backend.exoplanet_backend import ExoPlanetBakend, SelectionData
from resources.build_util import get_constant, resource_path
from resources.constants import VERSION_ID

CURRENT_DIRECTORY = Path(__file__).resolve().parent


def to_q_image(exo_image: npt.NDArray[np.uint8]) -> QImage:
    """Convert np.array image to QImage."""
    if exo_image.ndim == 3:
        image_format = QImage.Format.Format_BGR888

    q_image = QImage(
        exo_image.data, exo_image.shape[1], exo_image.shape[0], image_format
    )
    return q_image


class ImageProvider(QQuickImageProvider):
    """Signals for changing the displayed image."""

    def __init__(self) -> None:
        """Initialize class."""
        super(ImageProvider, self).__init__(  #  pylint: disable= [super-with-arguments]
            QQuickImageProvider.Image,  # type: ignore
        )
        self._image = None

    # pylint: disable=unused-argument
    def requestImage(self, id: str, size: QSize, requestedSize: QSize) -> QImage:
        """Update the to-be-displayed image."""
        return self._image  # type: ignore

    def set_image(self, image: QImage) -> None:
        """Setter."""
        self._image = image.copy()  # type: ignore


class PlanetParamaters(QObject):
    """Display parameters of planet from Python backend on QML interface."""

    params_log_changed = Signal(str)

    def __init__(self, parent: QObject | None = None) -> None:
        """Initialize class."""
        super().__init__(parent)
        self._params_log = ""

    @Slot(str)
    def set_params_log(self, log: str) -> None:
        """Set params_log."""
        self._params_log = log
        self.params_log_changed.emit(log)

    @Property(  # type: ignore
        str, fset=set_params_log, notify=params_log_changed  # type: ignore
    )
    def params_log(self) -> str:
        """Get params_log."""
        return self._params_log

    @Slot(dict)
    def params_entry(self, user_data: SelectionData):
        """Have backend display planet parameters."""
        params_entry = ExoPlanetBakend().params_entry(user_data)
        self.params_log_changed.emit(params_entry)


class PlanetImage(QObject):
    """Display images from Python backend on QML interface."""

    planet_image_changed = Signal()
    update_planet_image = Signal()

    def __init__(self, parent: QObject | None = None) -> None:
        """Initialize class."""
        super().__init__(parent)
        self._planet_image: QImage = QImage()

    def set_planet_image(self, image: QImage) -> None:
        """Set planet_image."""
        self._planet_image = image
        self.planet_image_changed.emit()

    @Property(  # type: ignore
        QImage, notify=planet_image_changed, fset=set_planet_image, constant=False  # type: ignore
    )
    def get_planet_image(self) -> QImage:
        """Get planet_image."""
        return self._planet_image

    @Slot(dict)
    def display_planets(self, user_data: SelectionData) -> None:
        """Have backend display planet images."""
        exo_planet = ExoPlanetBakend().display_planets(user_data)
        qexo_planet = to_q_image(exo_planet)
        self.set_planet_image(qexo_planet)


class DiscoveryLog(QObject):
    """Display discovery messages from Python backend on QML interface."""

    discovery_log_changed = Signal(str)

    def __init__(self, parent: QObject | None = None) -> None:
        """Initialize class."""
        super().__init__(parent)
        self._discovery_log = ""

    @Slot(str)
    def set_discovery_log(self, log: str) -> None:
        """Set discovery_log."""
        self._discovery_log = log
        self.discovery_log_changed.emit(log)

    @Property(  # type: ignore
        str, fset=set_discovery_log, notify=discovery_log_changed  # type: ignore
    )
    def discovery_log(self) -> str:
        """Get discovery_log."""
        return self._discovery_log

    @Slot(dict)
    def log_entry(self, user_data: SelectionData):
        """Have backend display planet discovery log."""
        discovery_entry = ExoPlanetBakend().log_entry(user_data)
        self.discovery_log_changed.emit(discovery_entry)


class ExoPlanetApp(QGuiApplication):
    """Bridge for creating exoplanet app."""

    def __init__(self) -> None:
        """Initialize exoplanet app."""
        super().__init__()
        name = "Exoplanet App"
        version = get_constant(VERSION_ID, fallback="0.0.0")
        self.setApplicationDisplayName(name + " " + version)
        self.setWindowIcon(QIcon("resources_ui_app/exoplanet.ico"))
        self.setWindowIcon(QIcon(str(resource_path() / "exoplanet.ico")))

        self.params_log = PlanetParamaters()
        self.planet_image = PlanetImage()
        self.provider = ImageProvider()
        self.discovery_log = DiscoveryLog()

        self.engine = QQmlApplicationEngine()
        self.engine.rootContext().setContextProperty("planetparams", self.params_log)
        self.engine.rootContext().setContextProperty("theplanet", self.planet_image)
        self.engine.addImageProvider("provider", self.provider)
        self.engine.rootContext().setContextProperty("mydiscovery", self.discovery_log)
        self.engine.load(QUrl.fromLocalFile(str(CURRENT_DIRECTORY / "main.qml")))

        self.planet_image.planet_image_changed.connect(self.display_planet_image)

    def display_planet_image(self) -> None:
        """Display planet upon selection."""
        exo_planet = self.planet_image.get_planet_image
        self.provider.set_image(exo_planet)
        self.planet_image.update_planet_image.emit()


def main() -> None:
    """App entry point."""
    app = ExoPlanetApp()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
