"""Shared geometry handling for resizable dialogs."""

from PySide6.QtCore import QByteArray
from PySide6.QtWidgets import QApplication, QDialog

from ...utils.ytsage_config_manager import ConfigManager
from ...utils.ytsage_logger import logger


def restore_dialog_geometry(dialog: QDialog, config_key: str, default_size: tuple[int, int] | None = None) -> None:
    """Restore a dialog's saved geometry and keep it inside the work area."""
    if default_size is not None:
        dialog.resize(*default_size)

    screen = dialog.screen() or QApplication.primaryScreen()
    if screen is None:
        return

    available_height = screen.availableGeometry().height()
    maximum_height = max(dialog.minimumHeight(), available_height - 40)
    dialog.setMaximumHeight(maximum_height)

    saved_geometry = ConfigManager.get(config_key)
    if saved_geometry:
        try:
            dialog.restoreGeometry(QByteArray.fromBase64(saved_geometry.encode("ascii")))
        except (AttributeError, TypeError, UnicodeError, ValueError):
            logger.warning(f"Failed to restore dialog geometry for '{config_key}'")
    elif default_size is None:
        dialog.adjustSize()

    if dialog.height() > maximum_height:
        dialog.resize(dialog.width(), maximum_height)


def save_dialog_geometry(dialog: QDialog, config_key: str) -> None:
    """Persist a dialog's current geometry."""
    try:
        geometry = dialog.saveGeometry().toBase64().data().decode("ascii")
        ConfigManager.set(config_key, geometry)
    except (AttributeError, UnicodeDecodeError, OSError):
        logger.exception(f"Failed to save dialog geometry for '{config_key}'")
