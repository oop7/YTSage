import os
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path
from typing import Optional

import requests
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
)

from src.utils.ytsage_logger import logger
from src.utils.ytsage_localization import _
from src.utils.ytsage_constants import (
    APP_BIN_DIR,
    ICON_PATH,
    OS_FULL_NAME,
    OS_NAME,
    SUBPROCESS_CREATIONFLAGS,
    DENO_APP_BIN_PATH,
    DENO_DOWNLOAD_URL,
    DENO_SHA256_URL,
)
from src.core.ytsage_ffmpeg import get_file_sha256


def verify_deno_sha256(file_path: Path, sha256_url: str) -> bool:
    """
    Verify Deno file SHA256 hash against official checksums.
    
    Args:
        file_path: Path to the downloaded Deno zip file
        sha256_url: URL to download the SHA256 checksum file
        
    Returns:
        bool: True if verification successful, False otherwise
    """
    try:
        # Download the SHA256 checksum file
        logger.info(f"Downloading SHA256 checksum from: {sha256_url}")
        response = requests.get(sha256_url, timeout=10)
        response.raise_for_status()
        checksum_content = response.text
        
        # Parse the checksum file - format is:
        # Algorithm : SHA256
        # Hash      : <HASH>
        # Path      : <PATH>
        expected_hash = None
        for line in checksum_content.strip().split("\n"):
            if line.startswith("Hash"):
                # Extract hash from "Hash      : <HASH>" format
                parts = line.split(":", 1)
                if len(parts) == 2:
                    expected_hash = parts[1].strip()
                    break
        
        if not expected_hash:
            logger.error("Could not find SHA256 hash in checksum file")
            return False
        
        # Calculate actual hash of downloaded file
        logger.info("Calculating SHA256 hash of downloaded file...")
        actual_hash = get_file_sha256(file_path)
        
        # Compare hashes (case-insensitive)
        if actual_hash.lower() == expected_hash.lower():
            logger.info("✓ SHA256 verification successful!")
            logger.info(f"  Expected: {expected_hash}")
            logger.info(f"  Actual:   {actual_hash}")
            return True
        else:
            logger.error("✗ SHA256 verification failed!")
            logger.error(f"  Expected: {expected_hash}")
            logger.error(f"  Actual:   {actual_hash}")
            return False
            
    except requests.RequestException as e:
        logger.error(f"Failed to download SHA256 checksum: {e}")
        return False
    except Exception as e:
        logger.exception(f"Error during SHA256 verification: {e}")
        return False


class DownloadDenoThread(QThread):
    progress_signal = Signal(int)
    status_signal = Signal(str)
    finished_signal = Signal(bool, str)

    def __init__(self):
        super().__init__()

    def run(self) -> None:
        temp_zip_path = None
        try:
            # Create temporary file for zip download
            temp_zip_fd, temp_zip_path = tempfile.mkstemp(suffix=".zip")
            os.close(temp_zip_fd)  # Close the file descriptor
            
            # Download with progress reporting
            logger.info(f"Downloading Deno from: {DENO_DOWNLOAD_URL}")
            self.status_signal.emit(_("deno.downloading"))
            
            response = requests.get(DENO_DOWNLOAD_URL, stream=True)
            response.raise_for_status()
            total_size = int(response.headers.get("content-length", 0))
            block_size = 8192  # 8KB blocks

            if total_size == 0:
                self.progress_signal.emit(100)

            with open(temp_zip_path, "wb") as f:
                downloaded = 0
                for data in response.iter_content(block_size):
                    f.write(data)
                    downloaded += len(data)
                    if total_size > 0:
                        progress = int(downloaded / total_size * 100)
                        self.progress_signal.emit(progress)

            logger.info("Download complete, verifying SHA256 hash...")
            self.status_signal.emit(_("deno.verifying"))
            
            # Verify SHA256 hash
            if not verify_deno_sha256(Path(temp_zip_path), DENO_SHA256_URL):
                # Hash verification failed - delete the downloaded file
                logger.error("SHA256 verification failed! Removing downloaded file.")
                if Path(temp_zip_path).exists():
                    Path(temp_zip_path).unlink()
                self.finished_signal.emit(
                    False, 
                    _("deno.verification_failed")
                )
                return

            # Extract deno executable from zip
            logger.info("Extracting Deno executable...")
            self.status_signal.emit(_("deno.extracting"))
            
            with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
                # Deno zip contains just the executable at root
                executable_name = "deno.exe" if OS_NAME == "Windows" else "deno"
                
                # Find the executable in the zip
                if executable_name not in zip_ref.namelist():
                    logger.error(f"Executable '{executable_name}' not found in zip file")
                    self.finished_signal.emit(False, f"Executable '{executable_name}' not found in zip")
                    return
                
                # Extract to app bin directory
                zip_ref.extract(executable_name, APP_BIN_DIR)
            
            # Verify the extracted file exists
            exe_path = DENO_APP_BIN_PATH
            if not exe_path.exists():
                logger.error(f"Extraction failed: {exe_path} does not exist")
                self.finished_signal.emit(False, "Extraction failed")
                return

            # Make executable on macOS and Linux
            if OS_NAME != "Windows":
                os.chmod(exe_path, 0o755)
                logger.info("Set executable permissions on Unix system")

            # Clean up the temporary zip file
            if temp_zip_path and Path(temp_zip_path).exists():
                Path(temp_zip_path).unlink()
                logger.info("Cleaned up temporary zip file")

            logger.info("Deno downloaded, verified, and extracted successfully!")
            self.finished_signal.emit(True, str(exe_path))

        except Exception as e:
            logger.exception(f"Error downloading/extracting Deno: {e}")
            # Clean up temporary zip file on error
            if temp_zip_path and Path(temp_zip_path).exists():
                try:
                    Path(temp_zip_path).unlink()
                except Exception:
                    pass
            self.finished_signal.emit(False, str(e))


class DenoSetupDialog(QDialog):
    setup_complete = Signal(str)  # Signal emitting the path to Deno

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(_("deno.setup_required"))
        self.setMinimumWidth(520)
        self.setMinimumHeight(300)
        self.resize(520, 320)

        # Set the window icon to match the main app
        if parent and parent.windowIcon():
            self.setWindowIcon(parent.windowIcon())
        else:
            icon_path = ICON_PATH
            if Path.exists(icon_path):
                self.setWindowIcon(QIcon(str(icon_path)))

        self.init_ui()

        # Apply dark theme styling to match app
        self.setStyleSheet(
            """
            QDialog {
                background-color: #15181b;
                color: #ffffff;
            }
            QLabel {
                color: #cccccc;
                line-height: 1.4;
            }
            QPushButton {
                padding: 10px 20px;
                background-color: #c90000;
                border: none;
                border-radius: 6px;
                color: white;
                font-weight: bold;
                font-size: 13px;
                min-width: 120px;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #a50000;
            }
            QPushButton:pressed {
                background-color: #800000;
            }
            QPushButton:disabled {
                background-color: #666666;
                color: #999999;
            }
            QProgressBar {
                border: 2px solid #1d1e22;
                border-radius: 6px;
                text-align: center;
                color: white;
                background-color: #1d1e22;
                height: 25px;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #e60000, stop: 0.5 #ff3333, stop: 1 #c90000);
                border-radius: 4px;
                margin: 1px;
            }
        """
        )

    def init_ui(self) -> None:
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)

        # Header title
        title_label = QLabel(_("deno.setup_required"))
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff; padding: 5px 0;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Information label with improved styling
        info_label = QLabel(
            _("deno.setup_description", os_name=OS_FULL_NAME)
        )
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setWordWrap(True)
        info_label.setStyleSheet("font-size: 13px; color: #cccccc; padding: 5px; line-height: 1.4;")
        layout.addWidget(info_label)

        # Progress bar with proper sizing
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setFixedHeight(20)
        self.progress_bar.setStyleSheet(
            """
            QProgressBar {
                border: 1px solid #3d3d3d;
                border-radius: 8px;
                background-color: #1d1e22;
                text-align: center;
                color: #ffffff;
                font-size: 12px;
                font-weight: bold;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #c90000;
                border-radius: 6px;
                margin: 1px;
            }
        """
        )
        layout.addWidget(self.progress_bar)

        # Status label with better spacing
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-size: 12px; color: #cccccc; padding: 8px 0;")
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        # Add stretch to push buttons to bottom
        layout.addStretch()

        # Button layout with improved spacing
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.setContentsMargins(0, 10, 0, 0)

        self.setup_button = QPushButton(_("deno.setup_button"))
        self.setup_button.clicked.connect(self.download_deno)

        self.cancel_button = QPushButton(_("buttons.cancel"))
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.setup_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def download_deno(self) -> None:
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText(_("deno.downloading"))
        self.setup_button.setEnabled(False)
        self.cancel_button.setEnabled(False)

        self.download_thread = DownloadDenoThread()
        self.download_thread.progress_signal.connect(self.update_progress)
        self.download_thread.status_signal.connect(self.update_status)
        self.download_thread.finished_signal.connect(self.download_finished)
        self.download_thread.start()

    def update_progress(self, value) -> None:
        self.progress_bar.setValue(value)

    def update_status(self, status: str) -> None:
        self.status_label.setText(status)

    def download_finished(self, success, result) -> None:
        self.setup_button.setEnabled(True)
        self.cancel_button.setEnabled(True)

        if success:
            self.status_label.setText(_("deno.success"))
            self.setup_complete.emit(result)
            self.accept()
        else:
            self.status_label.setText(f"{_('deno.download_error', error=result)}")
            error_dialog = QMessageBox(self)
            error_dialog.setIcon(QMessageBox.Icon.Critical)
            error_dialog.setWindowTitle(_("deno.download_failed"))
            error_dialog.setText(_("deno.download_error", error=result))
            error_dialog.setWindowIcon(self.windowIcon())
            error_dialog.setStyleSheet(
                """
                QMessageBox {
                    background-color: #15181b;
                    color: #ffffff;
                }
                QLabel {
                    color: #ffffff;
                }
                QPushButton {
                    padding: 8px 15px;
                    background-color: #c90000;
                    border: none;
                    border-radius: 4px;
                    color: white;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #a50000;
                }
            """
            )
            error_dialog.exec()


def check_deno_binary() -> Optional[Path]:
    """
    Check if Deno binary exists in the app's bin directory ONLY.
    We only use our managed binary, not system PATH.
    
    Returns:
        Path or None: Path to Deno binary if found in app bin, None otherwise
    """
    exe_path = DENO_APP_BIN_PATH
    if exe_path.exists():
        # Make sure it's executable on Unix systems
        if OS_NAME != "Windows" and not os.access(exe_path, os.X_OK):
            try:
                os.chmod(exe_path, 0o755)
                logger.info(f"Fixed permissions on Deno at {exe_path}")
            except Exception as e:
                logger.exception(f"Could not set executable permissions on {exe_path}: {e}")
        logger.info(f"Found Deno in app bin directory: {exe_path}")
        return exe_path

    # Binary not found in app directory - return None to trigger setup
    logger.warning(f"Deno binary not found in app bin directory: {exe_path}")
    return None


def check_deno_installed() -> bool:
    """
    Check if Deno is installed and accessible.
    
    Returns:
        bool: True if Deno is found and working, False otherwise
    """
    try:
        deno_path = check_deno_binary()
        if deno_path:
            # Try to run deno --version to verify it's working
            try:
                result = subprocess.run(
                    [str(deno_path), "--version"], 
                    capture_output=True, 
                    text=True, 
                    timeout=5, 
                    creationflags=SUBPROCESS_CREATIONFLAGS
                )
                return result.returncode == 0
            except Exception:
                return False
        return False
    except Exception:
        return False


def get_deno_path() -> Path:
    """
    Get the Deno path from the app's bin directory.
    
    Returns:
        Path or str: Path to Deno binary, or "deno" as fallback command
    """
    deno_path = check_deno_binary()
    if deno_path:
        logger.info(f"Using Deno from: {deno_path}")
        return deno_path

    # If not found, fall back to the command name as a last resort
    logger.info("Deno not found in app directory, falling back to command name")
    return "deno"  # type: ignore[return-value]


def setup_deno(parent_widget=None):
    """
    Show the Deno setup dialog and handle the result.
    
    Returns:
        str: Path to Deno binary
    """
    logger.debug("Starting Deno setup dialog")
    dialog = DenoSetupDialog(parent_widget)

    # Store the setup result from the signal
    setup_result = {"path": None}

    def on_setup_complete(path) -> None:
        logger.debug(f"Received setup_complete signal with path: {path}")
        setup_result["path"] = path

    # Connect to the setup_complete signal
    dialog.setup_complete.connect(on_setup_complete)

    # Show the dialog
    result = dialog.exec()
    logger.debug(f"Dialog result: {result} (Accepted={QDialog.DialogCode.Accepted})")

    if result == QDialog.DialogCode.Accepted:
        # First check if we received a path from the signal
        if setup_result["path"]:
            path_obj = Path(setup_result["path"]) if isinstance(setup_result["path"], str) else setup_result["path"]
            if path_obj.exists():
                logger.debug(f"Using path from signal: {setup_result['path']}")
                return str(setup_result["path"])

        # Get the expected path for verification as fallback
        expected_path = DENO_APP_BIN_PATH
        logger.debug(f"Expected Deno path: {expected_path}")

        # Verify the path exists after dialog is accepted
        if expected_path.exists():
            logger.debug(f"Deno successfully found at expected path: {expected_path}")
            return str(expected_path)
        else:
            logger.debug(f"Expected path does not exist, trying alternate detection")
            # Try to use the get_deno_path function to find Deno elsewhere
            deno_path = get_deno_path()
            logger.debug(f"Alternate detection result: {deno_path}")
            if deno_path != "deno":
                path_obj = Path(deno_path) if isinstance(deno_path, str) else deno_path
                if path_obj.exists():
                    logger.debug(f"Deno found at alternate location: {deno_path}")
                    return str(deno_path)

            # Something went wrong, show an error message
            logger.debug(f"Setup failed, showing error dialog")
            if parent_widget:
                error_dialog = QMessageBox(parent_widget)
                error_dialog.setIcon(QMessageBox.Icon.Warning)
                error_dialog.setWindowTitle(_("deno.setup_error"))
                error_dialog.setText(_("deno.setup_failed"))
                error_dialog.setWindowIcon(parent_widget.windowIcon())
                error_dialog.setStyleSheet(
                    """
                    QMessageBox {
                        background-color: #15181b;
                        color: #ffffff;
                    }
                    QLabel {
                        color: #ffffff;
                    }
                    QPushButton {
                        padding: 8px 15px;
                        background-color: #c90000;
                        border: none;
                        border-radius: 4px;
                        color: white;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #a50000;
                    }
                """
                )
                error_dialog.exec()
            logger.warning(f"Deno setup failed, path does not exist: {expected_path}")
    else:
        logger.debug("User cancelled the setup dialog")

    # User cancelled or setup failed, return the fallback command
    logger.debug("Returning fallback command 'deno'")
    return "deno"
