"""
Update-related dialogs and threads for YTSage application.
Contains dialogs and background threads for checking and performing yt-dlp updates.
"""

import os
import subprocess
import sys
import time
from importlib.metadata import PackageNotFoundError
from pathlib import Path

import requests
from packaging import version
from PySide6.QtCore import Qt, QThread, QTimer, Signal
from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QProgressBar, QPushButton, QVBoxLayout

from src.core.ytsage_utils import get_ytdlp_version, load_config, save_config
from src.core.ytsage_yt_dlp import get_yt_dlp_path
from src.utils.ytsage_constants import OS_NAME, SUBPROCESS_CREATIONFLAGS, YTDLP_APP_BIN_PATH, YTDLP_DOWNLOAD_URL
from src.utils.ytsage_localization import LocalizationManager

# Shorthand for localization
_ = LocalizationManager.get_text
from src.utils.ytsage_localization import _
from src.utils.ytsage_logger import logger

try:
    from importlib.metadata import PackageNotFoundError as ImportlibPackageNotFoundError
    from importlib.metadata import version as importlib_version

    def get_version(package_name: str) -> str:
        return importlib_version(package_name)

    PackageNotFoundError = ImportlibPackageNotFoundError
except ImportError:
    # Fallback for older Python versions
    import pkg_resources

    def get_version(package_name: str) -> str:
        return pkg_resources.get_distribution(package_name).version

    PackageNotFoundError = pkg_resources.DistributionNotFound

try:
    import yt_dlp

    YT_DLP_AVAILABLE = True
except ImportError:
    YT_DLP_AVAILABLE = False


class VersionCheckThread(QThread):
    finished = Signal(str, str, str)  # current_version, latest_version, error_message

    def run(self) -> None:
        current_version = ""
        latest_version = ""
        error_message = ""

        try:
            # Get the yt-dlp executable path
            yt_dlp_path = get_yt_dlp_path()

            # Get current version with timeout
            try:
                result = subprocess.run(
                    [yt_dlp_path, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=30,  # 30 second timeout
                    creationflags=SUBPROCESS_CREATIONFLAGS,
                )
                if result.returncode == 0:
                    current_version = result.stdout.strip()
                else:  # Try fallback if command failed
                    if YT_DLP_AVAILABLE:
                        current_version = yt_dlp.version.__version__  # type: ignore[reportAttributeAccessIssue]
                    else:
                        error_message = "yt-dlp not available."
                        self.finished.emit(current_version, latest_version, error_message)
                    return
            except subprocess.TimeoutExpired:
                # Try fallback if timeout
                if YT_DLP_AVAILABLE:
                    current_version = yt_dlp.version.__version__  # type: ignore[reportAttributeAccessIssue]
                else:
                    error_message = "yt-dlp version check timed out and package not found."
                    self.finished.emit(current_version, latest_version, error_message)
                    return
            except Exception:
                # Fallback to importing yt_dlp package directly if subprocess fails
                if YT_DLP_AVAILABLE:
                    current_version = yt_dlp.version.__version__  # type: ignore[reportAttributeAccessIssue]
                else:
                    error_message = "yt-dlp not found or accessible."
                    self.finished.emit(current_version, latest_version, error_message)
                    return

            # Get latest version from PyPI
            response = requests.get("https://pypi.org/pypi/yt-dlp/json", timeout=10)
            response.raise_for_status()
            latest_version = response.json()["info"]["version"]

            # Clean up version strings
            current_version = current_version.replace("_", ".")
            latest_version = latest_version.replace("_", ".")

        except requests.RequestException as e:
            error_message = f"Network error checking PyPI: {e}"
        except Exception as e:
            error_message = f"Error checking version: {e}"

        self.finished.emit(current_version, latest_version, error_message)


class UpdateThread(QThread):
    update_status = Signal(str)  # For status messages
    update_progress = Signal(int)  # For progress percentage (0-100)
    update_finished = Signal(bool, str)  # success (bool), message/error (str)

    def run(self) -> None:
        error_message = ""
        success = False
        try:
            self.update_status.emit(_('update.checking_current'))
            self.update_progress.emit(10)

            # Get the yt-dlp path
            try:
                yt_dlp_path = get_yt_dlp_path()
                self.update_status.emit(_('update.found_at', path=yt_dlp_path))
            except Exception as e:
                self.update_status.emit(_('update.error_getting_path', error=e))
                self.update_finished.emit(False, f"❌ Error getting yt-dlp path: {e}")
                return

            # Extra logic moved to src\utils\ytsage_constants.py

            self.update_progress.emit(20)

            # Extra logic moved to src\utils\ytsage_constants.py
            # Check if this is an app-managed binary by comparing paths safely
            is_app_managed = False
            try:
                # Only compare if both files exist
                if yt_dlp_path.exists() and YTDLP_APP_BIN_PATH.exists():
                    is_app_managed = yt_dlp_path.samefile(YTDLP_APP_BIN_PATH)
                elif str(yt_dlp_path) == str(YTDLP_APP_BIN_PATH):
                    # If paths are identical as strings, consider it app-managed
                    is_app_managed = True
                else:
                    # If app binary doesn't exist, this is definitely not app-managed
                    is_app_managed = False
            except (OSError, IOError) as e:
                logger.debug(f"Error comparing paths: {e}")
                is_app_managed = False

            if is_app_managed:
                self.update_status.emit(_('update.updating_binary'))
                success = self._update_binary(yt_dlp_path)
            else:
                self.update_status.emit(_('update.updating_pip'))
                success = self._update_via_pip()

            if success:
                self.update_progress.emit(100)
                error_message = "✅ yt-dlp has been successfully updated!"
            else:
                error_message = _('update.update_failed')

        except requests.RequestException as e:
            error_message = f"❌ Network error during update: {e}"
            self.update_status.emit(error_message)
            success = False
        except Exception as e:
            error_message = f"❌ Update failed: {e}"
            self.update_status.emit(error_message)
            success = False

        self.update_finished.emit(success, error_message)

    def _update_binary(self, yt_dlp_path: Path) -> bool:
        """Update yt-dlp binary using its built-in updater (same logic as AutoUpdateThread)."""
        try:
            logger.info("UpdateThread: Checking for yt-dlp updates...")

            result = subprocess.run(
                [yt_dlp_path, "-U"],
                capture_output=True,
                text=True,
                timeout=60,
                creationflags=SUBPROCESS_CREATIONFLAGS,
            )

            if result.returncode == 0:
                # Make executable on Unix systems
                if OS_NAME != "Windows":
                    os.chmod(yt_dlp_path, 0o755)

                logger.info("UpdateThread: yt-dlp update completed successfully.")
                if result.stdout:
                    logger.debug(f"yt-dlp output: {result.stdout.strip()}")
                self.update_status.emit(_('update.binary_updated'))
                self.update_progress.emit(95)
                return True
            else:
                logger.error(f"UpdateThread: yt-dlp update failed. {result.stderr.strip()}")
                self.update_status.emit(_('update.update_failed_stderr', error=result.stderr.strip()))
                return False

        except subprocess.TimeoutExpired:
            logger.error("UpdateThread: yt-dlp update timed out.")
            self.update_status.emit(_('update.update_timeout'))
            return False

        except Exception as e:
            logger.exception(f"UpdateThread: Unexpected error during update: {e}")
            self.update_status.emit(_('update.unexpected_error', error=e))
            return False

    def _update_via_pip(self) -> bool:
        """Update yt-dlp via pip."""
        try:
            self.update_status.emit(_('update.checking_pip'))
            self.update_progress.emit(30)

            # Get current version
            try:
                current_version = get_version("yt-dlp")
                self.update_status.emit(_('update.current_version', version=current_version))
            except PackageNotFoundError:
                self.update_status.emit(_('update.not_found_pip'))
                current_version = "0.0.0"

            self.update_progress.emit(40)

            # Get the latest version from PyPI
            self.update_status.emit(_('update.checking_latest'))
            response = requests.get("https://pypi.org/pypi/yt-dlp/json", timeout=10)

            if response.status_code != 200:
                self.update_status.emit(_('update.failed_check_updates'))
                return False

            data = response.json()
            latest_version = data["info"]["version"]
            self.update_status.emit(_('update.latest_version', version=latest_version))
            self.update_progress.emit(50)

            # Compare versions
            if version.parse(latest_version) > version.parse(current_version):
                self.update_status.emit(_('update.updating_from_to', current=current_version, latest=latest_version))
                self.update_progress.emit(60)

                try:
                    # Run pip update with timeout
                    self.update_status.emit(_('update.running_pip_install'))
                    update_result = subprocess.run(
                        [sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"],
                        capture_output=True,
                        text=True,
                        check=False,
                        timeout=300,  # 5 minute timeout for pip install
                        creationflags=SUBPROCESS_CREATIONFLAGS,
                    )

                    self.update_progress.emit(85)

                    if update_result.returncode == 0:
                        self.update_status.emit(_('update.pip_completed'))
                        self.update_progress.emit(95)
                        return True
                    else:
                        self.update_status.emit(_('update.pip_failed', error=update_result.stderr))
                        return False

                except subprocess.TimeoutExpired:
                    self.update_status.emit(_("update.pip_timeout"))
                    return False
                except Exception as e:
                    self.update_status.emit(f"❌ Error during pip update: {e}")
                    return False
            else:
                self.update_status.emit(_("update.already_up_to_date"))
                self.update_progress.emit(95)
                return True

        except Exception as e:
            self.update_status.emit(f"❌ Pip update failed: {e}")
            return False


class YTDLPUpdateDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle(_('update.title'))
        self.setMinimumWidth(450)
        self.setMinimumHeight(200)
        self._closing = False  # Flag to track if dialog is closing

        layout = QVBoxLayout(self)

        # Status label
        self.status_label = QLabel(_('update.checking'))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setWordWrap(True)
        self.status_label.setMinimumHeight(60)
        layout.addWidget(self.status_label)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.hide()  # Hide initially
        layout.addWidget(self.progress_bar)

        # Buttons
        button_layout = QHBoxLayout()
        self.update_btn = QPushButton(_('buttons.update'))
        self.update_btn.clicked.connect(self.perform_update)
        self.update_btn.setEnabled(False)

        self.close_btn = QPushButton(_('buttons.close'))
        self.close_btn.clicked.connect(self.close)

        button_layout.addWidget(self.update_btn)
        button_layout.addWidget(self.close_btn)
        layout.addLayout(button_layout)

        # Style
        self.setStyleSheet(
            """
            QDialog {
                background-color: #15181b;
            }
            QLabel {
                color: #ffffff;
                font-size: 12px;
                padding: 10px;
            }
            QPushButton {
                padding: 8px 15px;
                background-color: #c90000;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:disabled {
                background-color: #666666;
            }
            QPushButton:hover {
                background-color: #a50000;
            }
            QProgressBar {
                border: 2px solid #1d1e22;
                border-radius: 6px;
                text-align: center;
                color: white;
                background-color: #1d1e22;
                height: 30px;
                font-weight: bold;
                font-size: 12px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #e60000, stop: 0.5 #ff3333, stop: 1 #c90000);
                border-radius: 4px;
                margin: 1px;
            }
        """
        )

        # Start version check in background
        self.check_version()

    def check_version(self) -> None:
        self.status_label.setText(_('update.checking'))
        self.update_btn.setEnabled(False)
        self.version_check_thread = VersionCheckThread()
        self.version_check_thread.finished.connect(self.on_version_check_finished)
        self.version_check_thread.start()

    def on_version_check_finished(self, current_version, latest_version, error_message) -> None:
        # Check if dialog is closing to avoid unnecessary updates
        if hasattr(self, "_closing") and self._closing:
            return

        if error_message:
            self.status_label.setText(error_message)
            self.update_btn.setEnabled(False)
            return

        if not current_version or not latest_version:
            self.status_label.setText(_('update.could_not_determine'))
            self.update_btn.setEnabled(False)
            return

        try:
            # Compare versions
            current_ver = version.parse(current_version)
            latest_ver = version.parse(latest_version)

            if current_ver < latest_ver:
                self.status_label.setText(
                    _('update.update_available', current=current_version, latest=latest_version)
                )
                self.update_btn.setEnabled(True)
            else:
                self.status_label.setText(f"yt-dlp is up to date (version {current_version})")
                self.update_btn.setEnabled(False)
        except version.InvalidVersion:
            # If version parsing fails, do a simple string comparison
            if current_version != latest_version:
                self.status_label.setText(
                    _('update.update_available_failed', current=current_version, latest=latest_version)
                )
                self.update_btn.setEnabled(True)
            else:
                self.status_label.setText(_('update.up_to_date', version=current_version))
                self.update_btn.setEnabled(False)
        except Exception as e:
            self.status_label.setText(_('update.error_comparing', error=e))
            self.update_btn.setEnabled(False)

    def perform_update(self) -> None:
        # Immediate visual feedback
        self.update_btn.setEnabled(False)
        self.close_btn.setEnabled(False)
        self.update_btn.setText(_('update.updating'))
        self.status_label.setText(_('update.initializing'))

        # Show progress bar immediately
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.show()

        # Start the update thread
        self._start_update_thread()

    def _start_update_thread(self) -> None:
        """Start the actual update thread."""
        # Create and start the update thread
        self.update_thread = UpdateThread()
        self.update_thread.update_status.connect(self.on_update_status)
        self.update_thread.update_progress.connect(self.on_update_progress)
        self.update_thread.update_finished.connect(self.on_update_finished)
        self.update_thread.start()

    def on_update_status(self, message) -> None:
        """Slot to receive status messages from UpdateThread."""
        if not (hasattr(self, "_closing") and self._closing):
            self.status_label.setText(message)

    def on_update_progress(self, progress) -> None:
        """Slot to receive progress updates from UpdateThread."""
        if not (hasattr(self, "_closing") and self._closing):
            self.progress_bar.setValue(progress)

    def on_update_finished(self, success, message) -> None:
        """Slot called when the UpdateThread finishes."""
        # Check if dialog is closing to avoid unnecessary updates
        if hasattr(self, "_closing") and self._closing:
            return

        self.progress_bar.setValue(100)
        self.status_label.setText(message)
        self.close_btn.setEnabled(True)
        self.update_btn.setText(_('buttons.update'))  # Reset button text

        if success:
            # Show success briefly then auto-check version
            QTimer.singleShot(2000, self.check_version)  # Wait 2 seconds then refresh
        else:
            # Re-enable update button on failure after a short delay
            QTimer.singleShot(
                3000,
                lambda: (self.update_btn.setEnabled(True) if not (hasattr(self, "_closing") and self._closing) else None),
            )

    def closeEvent(self, event) -> None:
        """Ensure threads are terminated if the dialog is closed prematurely."""
        # Set a flag to indicate dialog is closing
        self._closing = True

        if hasattr(self, "version_check_thread") and self.version_check_thread.isRunning():
            self.version_check_thread.quit()
            if not self.version_check_thread.wait(3000):  # Wait up to 3 seconds
                self.version_check_thread.terminate()

        if hasattr(self, "update_thread") and self.update_thread.isRunning():
            self.update_thread.quit()
            if not self.update_thread.wait(5000):  # Wait up to 5 seconds for update to finish
                self.update_thread.terminate()

        super().closeEvent(event)


class AutoUpdateThread(QThread):
    """Thread for performing automatic background updates without UI feedback."""

    update_finished = Signal(bool, str)  # success (bool), message (str)

    def run(self) -> None:
        """Perform automatic yt-dlp update check and update if needed."""
        try:
            logger.info("AutoUpdateThread: Performing automatic yt-dlp update check...")

            # Get current version
            current_version = get_ytdlp_version()
            if "Error" in current_version:
                logger.warning("AutoUpdateThread: Could not determine current yt-dlp version, skipping auto-update")
                self.update_finished.emit(False, "Could not determine current yt-dlp version")
                return

            # Get latest version from PyPI
            try:
                response = requests.get("https://pypi.org/pypi/yt-dlp/json", timeout=10)
                response.raise_for_status()
                latest_version = response.json()["info"]["version"]

                # Clean up version strings
                current_version = current_version.replace("_", ".")
                latest_version = latest_version.replace("_", ".")

                logger.info(f"AutoUpdateThread: Current yt-dlp version: {current_version}")
                logger.info(f"AutoUpdateThread: Latest yt-dlp version: {latest_version}")

                # Compare versions
                if version.parse(latest_version) > version.parse(current_version):
                    logger.info(f"AutoUpdateThread: Auto-updating yt-dlp from {current_version} to {latest_version}...")

                    # Perform the update
                    success = self._perform_update()

                    if success:
                        logger.info("AutoUpdateThread: Auto-update completed successfully!")
                        # Update the last check timestamp
                        config = load_config()
                        config["last_update_check"] = time.time()
                        save_config(config)
                        self.update_finished.emit(
                            True,
                            f"Successfully updated yt-dlp from {current_version} to {latest_version}",
                        )
                    else:
                        logger.warning("AutoUpdateThread: Auto-update failed")
                        self.update_finished.emit(False, "Auto-update failed")
                else:
                    logger.info("AutoUpdateThread: yt-dlp is already up to date")
                    # Still update the timestamp even if no update was needed
                    config = load_config()
                    config["last_update_check"] = time.time()
                    save_config(config)
                    self.update_finished.emit(
                        True,
                        f"yt-dlp is already up to date (version {current_version})",
                    )

            except requests.RequestException as e:
                logger.warning(f"AutoUpdateThread: Network error during auto-update check: {e}")
                self.update_finished.emit(False, f"Network error: {e}")
            except Exception as e:
                logger.exception(f"AutoUpdateThread: Error during auto-update check: {e}", exc_info=True)
                self.update_finished.emit(False, f"Update check error: {e}")

        except Exception as e:
            logger.critical(f"AutoUpdateThread: Critical error in auto-update: {e}", exc_info=True)
            self.update_finished.emit(False, f"Critical error: {e}")

    def _perform_update(self) -> bool:
        """Perform the actual update using similar logic to UpdateThread but without UI feedback."""
        try:
            # Get the yt-dlp path
            yt_dlp_path = get_yt_dlp_path()

            # Extra logic moved to src\utils\ytsage_constants.py

            # Check if this is an app-managed binary by comparing paths safely
            is_app_managed = False
            try:
                # Only compare if both files exist
                if yt_dlp_path.exists() and YTDLP_APP_BIN_PATH.exists():
                    is_app_managed = yt_dlp_path.samefile(YTDLP_APP_BIN_PATH)
                elif str(yt_dlp_path) == str(YTDLP_APP_BIN_PATH):
                    # If paths are identical as strings, consider it app-managed
                    is_app_managed = True
                else:
                    # If app binary doesn't exist, this is definitely not app-managed
                    is_app_managed = False
            except (OSError, IOError) as e:
                logger.debug(f"AutoUpdateThread: Error comparing paths: {e}")
                is_app_managed = False

            if is_app_managed:
                logger.info("AutoUpdateThread: Updating app-managed yt-dlp binary...")
                return self._update_binary(yt_dlp_path)
            else:
                logger.info("AutoUpdateThread: Updating system yt-dlp via pip...")
                return self._update_via_pip()

        except Exception as e:
            logger.exception(f"AutoUpdateThread: Error in _perform_update: {e}")
            return False

    def _update_binary(self, yt_dlp_path: Path) -> bool:
        """Update yt-dlp binary using its built-in updater."""
        try:
            logger.info("AutoUpdateThread: Checking for yt-dlp updates...")

            result = subprocess.run(
                [yt_dlp_path, "-U"],
                capture_output=True,
                text=True,
                timeout=60,
                creationflags=SUBPROCESS_CREATIONFLAGS,
            )

            if result.returncode == 0:
                # Make executable on Unix systems
                if OS_NAME != "Windows":
                    os.chmod(yt_dlp_path, 0o755)

                logger.info("AutoUpdateThread: yt-dlp update completed successfully.")
                if result.stdout:
                    logger.debug(f"yt-dlp output: {result.stdout.strip()}")
                return True
            else:
                logger.error(f"AutoUpdateThread: yt-dlp update failed. {result.stderr.strip()}")
                return False

        except subprocess.TimeoutExpired:
            logger.error("AutoUpdateThread: yt-dlp update timed out.")
            return False

        except Exception as e:
            logger.exception(f"AutoUpdateThread: Unexpected error during update: {e}")
            return False

    def _update_via_pip(self) -> bool:
        """Update yt-dlp via pip (silent version)."""
        try:
            logger.info("AutoUpdateThread: Checking current pip installation...")

            # Get current version
            try:
                current_version = get_version("yt-dlp")
                logger.info(f"AutoUpdateThread: Current version: {current_version}")
            except PackageNotFoundError:
                logger.warning("AutoUpdateThread: yt-dlp not found via pip, attempting installation...")
                current_version = "0.0.0"

            # Get the latest version from PyPI
            logger.info("AutoUpdateThread: Checking for latest version...")
            response = requests.get("https://pypi.org/pypi/yt-dlp/json", timeout=10)

            if response.status_code != 200:
                logger.error("AutoUpdateThread: Failed to check for updates")
                return False

            data = response.json()
            latest_version = data["info"]["version"]
            logger.info(f"AutoUpdateThread: Latest version: {latest_version}")

            # Compare versions
            if version.parse(latest_version) > version.parse(current_version):
                logger.info(f"AutoUpdateThread: Updating from {current_version} to {latest_version}...")

                # Extra logic moved to src\utils\ytsage_constants.py

                # Run pip update
                logger.info("AutoUpdateThread: Running pip install --upgrade...")
                update_result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"],
                    capture_output=True,
                    text=True,
                    check=False,
                    creationflags=SUBPROCESS_CREATIONFLAGS,
                )

                if update_result.returncode == 0:
                    logger.info("AutoUpdateThread: Pip update completed successfully!")
                    return True
                else:
                    logger.error(f"AutoUpdateThread: Pip update failed: {update_result.stderr}")
                    return False
            else:
                logger.info("AutoUpdateThread: yt-dlp is already up to date!")
                return True

        except Exception as e:
            logger.exception(f"AutoUpdateThread: Pip update failed: {e}")
            return False
