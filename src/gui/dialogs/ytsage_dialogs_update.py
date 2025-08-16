"""
Update-related dialogs and threads for YTSage application.
Contains dialogs and background threads for checking and performing yt-dlp updates.
"""

import sys
import os
import requests
import subprocess
import time
from packaging import version
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QProgressBar, QMessageBox)
from PySide6.QtCore import Qt, QThread, QTimer, Signal

from ...core.ytsage_yt_dlp import get_yt_dlp_path
from ...core.ytsage_utils import get_ytdlp_version, load_config, save_config
from ...core.ytsage_logging import logger

try:
    import yt_dlp
    YT_DLP_AVAILABLE = True
except ImportError:
    YT_DLP_AVAILABLE = False


class VersionCheckThread(QThread):
    finished = Signal(str, str, str)  # current_version, latest_version, error_message
    
    def run(self):
        current_version = ""
        latest_version = ""
        error_message = ""
        
        try:
            # Get the yt-dlp executable path
            yt_dlp_path = get_yt_dlp_path()
            
            # Get current version with timeout
            try:
                result = subprocess.run([yt_dlp_path, '--version'], 
                                     capture_output=True, 
                                     text=True,
                                     timeout=30,  # 30 second timeout
                                     startupinfo=None if sys.platform != 'win32' else subprocess.STARTUPINFO(dwFlags=subprocess.STARTF_USESHOWWINDOW, wShowWindow=subprocess.SW_HIDE),
                                     creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0)
                if result.returncode == 0:
                    current_version = result.stdout.strip()
                else:  # Try fallback if command failed
                    if YT_DLP_AVAILABLE:
                        current_version = yt_dlp.version.__version__
                    else:
                        error_message = "yt-dlp not available."
                        self.finished.emit(current_version, latest_version, error_message)
                        return
            except subprocess.TimeoutExpired:
                # Try fallback if timeout
                if YT_DLP_AVAILABLE:
                    current_version = yt_dlp.version.__version__
                else:
                    error_message = "yt-dlp version check timed out and package not found."
                    self.finished.emit(current_version, latest_version, error_message)
                    return
            except Exception:
                 # Fallback to importing yt_dlp package directly if subprocess fails
                if YT_DLP_AVAILABLE:
                    current_version = yt_dlp.version.__version__
                else:
                     error_message = "yt-dlp not found or accessible."
                     self.finished.emit(current_version, latest_version, error_message)
                     return

            # Get latest version from PyPI
            response = requests.get("https://pypi.org/pypi/yt-dlp/json", timeout=10)
            response.raise_for_status()
            latest_version = response.json()["info"]["version"]
            
            # Clean up version strings
            current_version = current_version.replace('_', '.')
            latest_version = latest_version.replace('_', '.')

        except requests.RequestException as e:
            error_message = f"Network error checking PyPI: {e}"
        except Exception as e:
            error_message = f"Error checking version: {e}"
            
        self.finished.emit(current_version, latest_version, error_message)


class UpdateThread(QThread):
    update_status = Signal(str)  # For status messages
    update_progress = Signal(int)  # For progress percentage (0-100)
    update_finished = Signal(bool, str)  # success (bool), message/error (str)
    
    def run(self):
        error_message = ""
        success = False
        try:
            self.update_status.emit("🔍 Checking current installation...")
            self.update_progress.emit(10)
            
            # Get the yt-dlp path
            try:
                yt_dlp_path = get_yt_dlp_path()
                self.update_status.emit(f"📍 Found yt-dlp at: {os.path.basename(yt_dlp_path)}")
            except Exception as e:
                self.update_status.emit(f"❌ Error getting yt-dlp path: {e}")
                self.update_finished.emit(False, f"❌ Error getting yt-dlp path: {e}")
                return
            
            # Create startupinfo to hide console on Windows
            startupinfo = None
            if sys.platform == 'win32' and hasattr(subprocess, 'STARTUPINFO'):
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = 0  # SW_HIDE
            
            self.update_progress.emit(20)
            
            # Check if we're using an app-managed binary or system installation
            app_managed_dirs = [
                os.path.join(os.environ.get('LOCALAPPDATA', ''), 'YTSage', 'bin'),
                os.path.expanduser(os.path.join('~', 'Library', 'Application Support', 'YTSage', 'bin')),
                os.path.expanduser(os.path.join('~', '.local', 'share', 'YTSage', 'bin'))
            ]
            
            is_app_managed = any(os.path.dirname(yt_dlp_path) == dir_path for dir_path in app_managed_dirs)
            
            if is_app_managed:
                self.update_status.emit("📦 Updating app-managed yt-dlp binary...")
                success = self._update_binary(yt_dlp_path)
            else:
                self.update_status.emit("🐍 Updating system yt-dlp via pip...")
                success = self._update_via_pip(startupinfo)
            
            if success:
                self.update_progress.emit(100)
                error_message = "✅ yt-dlp has been successfully updated!"
            else:
                error_message = "❌ Failed to update yt-dlp. Please try again or check your internet connection."
                
        except requests.RequestException as e:
            error_message = f"❌ Network error during update: {str(e)}"
            self.update_status.emit(error_message)
            success = False
        except Exception as e:
            error_message = f"❌ Update failed: {str(e)}"
            self.update_status.emit(error_message)
            success = False
            
        self.update_finished.emit(success, error_message)
    
    def _update_binary(self, yt_dlp_path):
        """Update yt-dlp binary directly from GitHub releases."""
        try:
            self.update_status.emit("🌐 Determining download URL...")
            self.update_progress.emit(30)
            
            # Determine the URL based on OS
            if sys.platform == 'win32':
                url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
            elif sys.platform == 'darwin':
                url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp_macos"
            else:
                url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp"
            
            self.update_status.emit("⬇️ Downloading latest yt-dlp binary...")
            self.update_progress.emit(40)
            
            # Download with progress tracking and timeout
            response = requests.get(url, stream=True, timeout=30)
            if response.status_code != 200:
                self.update_status.emit(f"❌ Download failed: HTTP {response.status_code}")
                return False
            
            total_size = int(response.headers.get('content-length', 0))
            temp_file = f"{yt_dlp_path}.new"
            downloaded = 0
            
            self.update_status.emit("💾 Downloading and saving binary...")
            
            with open(temp_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        # Update progress (40-80% for download)
                        if total_size > 0:
                            progress = 40 + int((downloaded / total_size) * 40)
                            self.update_progress.emit(progress)
            
            self.update_status.emit("🔧 Installing updated binary...")
            self.update_progress.emit(85)
            
            # Make executable on Unix systems
            if sys.platform != 'win32':
                os.chmod(temp_file, 0o755)
            
            # Replace the old file with the new one
            try:
                # On Windows, we need to remove the old file first
                if sys.platform == 'win32' and os.path.exists(yt_dlp_path):
                    os.remove(yt_dlp_path)
                
                os.rename(temp_file, yt_dlp_path)
                self.update_status.emit("✅ Binary successfully updated!")
                self.update_progress.emit(95)
                return True
                
            except Exception as e:
                self.update_status.emit(f"❌ Error installing binary: {e}")
                # Clean up temp file if it exists
                if os.path.exists(temp_file):
                    try:
                        os.remove(temp_file)
                    except:
                        pass
                return False
                
        except requests.RequestException as e:
            self.update_status.emit(f"❌ Network error: {e}")
            return False
        except Exception as e:
            self.update_status.emit(f"❌ Binary update failed: {e}")
            return False
    
    def _update_via_pip(self, startupinfo):
        """Update yt-dlp via pip."""
        try:
            import pkg_resources
            
            self.update_status.emit("🔍 Checking current pip installation...")
            self.update_progress.emit(30)
            
            # Get current version
            try:
                current_version = pkg_resources.get_distribution("yt-dlp").version
                self.update_status.emit(f"📋 Current version: {current_version}")
            except pkg_resources.DistributionNotFound:
                self.update_status.emit("⚠️ yt-dlp not found via pip, attempting installation...")
                current_version = "0.0.0"
                
            self.update_progress.emit(40)
            
            # Get the latest version from PyPI
            self.update_status.emit("🌐 Checking for latest version...")
            response = requests.get("https://pypi.org/pypi/yt-dlp/json", timeout=10)
            
            if response.status_code != 200:
                self.update_status.emit("❌ Failed to check for updates")
                return False
                
            data = response.json()
            latest_version = data["info"]["version"]
            self.update_status.emit(f"🆕 Latest version: {latest_version}")
            self.update_progress.emit(50)
            
            # Compare versions
            if version.parse(latest_version) > version.parse(current_version):
                self.update_status.emit(f"⬆️ Updating from {current_version} to {latest_version}...")
                self.update_progress.emit(60)
                
                try:
                    # Run pip update with timeout
                    self.update_status.emit("📦 Running pip install --upgrade...")
                    update_result = subprocess.run(
                        [sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"],
                        capture_output=True,
                        text=True,
                        check=False,
                        timeout=300,  # 5 minute timeout for pip install
                        startupinfo=startupinfo
                    )
                    
                    self.update_progress.emit(85)
                    
                    if update_result.returncode == 0:
                        self.update_status.emit("✅ Pip update completed successfully!")
                        self.update_progress.emit(95)
                        return True
                    else:
                        self.update_status.emit(f"❌ Pip update failed: {update_result.stderr}")
                        return False
                        
                except subprocess.TimeoutExpired:
                    self.update_status.emit("❌ Pip update timed out after 5 minutes")
                    return False
                except Exception as e:
                    self.update_status.emit(f"❌ Error during pip update: {e}")
                    return False
            else:
                self.update_status.emit("✅ yt-dlp is already up to date!")
                self.update_progress.emit(95)
                return True
                
        except Exception as e:
            self.update_status.emit(f"❌ Pip update failed: {e}")
            return False


class YTDLPUpdateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Update yt-dlp")
        self.setMinimumWidth(450)
        self.setMinimumHeight(200)
        self._closing = False  # Flag to track if dialog is closing
        
        layout = QVBoxLayout(self)
        
        # Status label
        self.status_label = QLabel("Checking for updates...")
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
        self.update_btn = QPushButton("Update")
        self.update_btn.clicked.connect(self.perform_update)
        self.update_btn.setEnabled(False)
        
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.close)
        
        button_layout.addWidget(self.update_btn)
        button_layout.addWidget(self.close_btn)
        layout.addLayout(button_layout)
        
        # Style
        self.setStyleSheet("""
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
        """)
        
        # Start version check in background
        self.check_version()
    
    def check_version(self):
        self.status_label.setText("Checking for updates...")
        self.update_btn.setEnabled(False)
        self.version_check_thread = VersionCheckThread()
        self.version_check_thread.finished.connect(self.on_version_check_finished)
        self.version_check_thread.start()

    def on_version_check_finished(self, current_version, latest_version, error_message):
        # Check if dialog is closing to avoid unnecessary updates
        if hasattr(self, '_closing') and self._closing:
            return
            
        if error_message:
            self.status_label.setText(error_message)
            self.update_btn.setEnabled(False)
            return

        if not current_version or not latest_version:
             self.status_label.setText("Could not determine versions.")
             self.update_btn.setEnabled(False)
             return

        try:
            # Compare versions
            current_ver = version.parse(current_version)
            latest_ver = version.parse(latest_version)
            
            if current_ver < latest_ver:
                self.status_label.setText(f"Update available!\nCurrent version: {current_version}\nLatest version: {latest_version}")
                self.update_btn.setEnabled(True)
            else:
                self.status_label.setText(f"yt-dlp is up to date (version {current_version})")
                self.update_btn.setEnabled(False)
        except version.InvalidVersion:
            # If version parsing fails, do a simple string comparison
            if current_version != latest_version:
                self.status_label.setText(f"Update available! (Comparison failed)\nCurrent: {current_version}\nLatest: {latest_version}")
                self.update_btn.setEnabled(True)
            else:
                self.status_label.setText(f"yt-dlp is up to date (version {current_version})")
                self.update_btn.setEnabled(False)
        except Exception as e:
             self.status_label.setText(f"Error comparing versions: {e}")
             self.update_btn.setEnabled(False)

    def perform_update(self):
        # Immediate visual feedback
        self.update_btn.setEnabled(False)
        self.close_btn.setEnabled(False)
        self.update_btn.setText("Updating...")
        self.status_label.setText("🚀 Initializing update process...")
        
        # Show progress bar immediately
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.show()
        
        # Start the update thread
        self._start_update_thread()
    
    def _start_update_thread(self):
        """Start the actual update thread."""
        # Create and start the update thread
        self.update_thread = UpdateThread()
        self.update_thread.update_status.connect(self.on_update_status)
        self.update_thread.update_progress.connect(self.on_update_progress)
        self.update_thread.update_finished.connect(self.on_update_finished)
        self.update_thread.start()

    def on_update_status(self, message):
        """Slot to receive status messages from UpdateThread."""
        if not (hasattr(self, '_closing') and self._closing):
            self.status_label.setText(message)

    def on_update_progress(self, progress):
        """Slot to receive progress updates from UpdateThread."""
        if not (hasattr(self, '_closing') and self._closing):
            self.progress_bar.setValue(progress)

    def on_update_finished(self, success, message):
        """Slot called when the UpdateThread finishes."""
        # Check if dialog is closing to avoid unnecessary updates
        if hasattr(self, '_closing') and self._closing:
            return
            
        self.progress_bar.setValue(100)
        self.status_label.setText(message)
        self.close_btn.setEnabled(True)
        self.update_btn.setText("Update")  # Reset button text
        
        if success:
            # Show success briefly then auto-check version
            QTimer.singleShot(2000, self.check_version)  # Wait 2 seconds then refresh
        else:
            # Re-enable update button on failure after a short delay
            QTimer.singleShot(3000, lambda: self.update_btn.setEnabled(True) if not (hasattr(self, '_closing') and self._closing) else None)

    def closeEvent(self, event):
        """Ensure threads are terminated if the dialog is closed prematurely."""
        # Set a flag to indicate dialog is closing
        self._closing = True
        
        if hasattr(self, 'version_check_thread') and self.version_check_thread.isRunning():
            self.version_check_thread.quit()
            if not self.version_check_thread.wait(3000):  # Wait up to 3 seconds
                self.version_check_thread.terminate()
                
        if hasattr(self, 'update_thread') and self.update_thread.isRunning():
            self.update_thread.quit()
            if not self.update_thread.wait(5000):  # Wait up to 5 seconds for update to finish
                self.update_thread.terminate()
                
        super().closeEvent(event)


class AutoUpdateThread(QThread):
    """Thread for performing automatic background updates without UI feedback."""
    update_finished = Signal(bool, str)  # success (bool), message (str)
    
    def run(self):
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
                current_version = current_version.replace('_', '.')
                latest_version = latest_version.replace('_', '.')
                
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
                        config['last_update_check'] = time.time()
                        save_config(config)
                        self.update_finished.emit(True, f"Successfully updated yt-dlp from {current_version} to {latest_version}")
                    else:
                        logger.warning("AutoUpdateThread: Auto-update failed")
                        self.update_finished.emit(False, "Auto-update failed")
                else:
                    logger.info("AutoUpdateThread: yt-dlp is already up to date")
                    # Still update the timestamp even if no update was needed
                    config = load_config()
                    config['last_update_check'] = time.time()
                    save_config(config)
                    self.update_finished.emit(True, f"yt-dlp is already up to date (version {current_version})")
                    
            except requests.RequestException as e:
                logger.warning(f"AutoUpdateThread: Network error during auto-update check: {e}")
                self.update_finished.emit(False, f"Network error: {e}")
            except Exception as e:
                logger.error(f"AutoUpdateThread: Error during auto-update check: {e}", exc_info=True)
                self.update_finished.emit(False, f"Update check error: {e}")
                
        except Exception as e:
            logger.critical(f"AutoUpdateThread: Critical error in auto-update: {e}", exc_info=True)
            self.update_finished.emit(False, f"Critical error: {e}")
    
    def _perform_update(self):
        """Perform the actual update using similar logic to UpdateThread but without UI feedback."""
        try:
            # Get the yt-dlp path
            yt_dlp_path = get_yt_dlp_path()
            
            # Check if we're using an app-managed binary or system installation
            app_managed_dirs = [
                os.path.join(os.environ.get('LOCALAPPDATA', ''), 'YTSage', 'bin'),
                os.path.expanduser(os.path.join('~', 'Library', 'Application Support', 'YTSage', 'bin')),
                os.path.expanduser(os.path.join('~', '.local', 'share', 'YTSage', 'bin'))
            ]
            
            is_app_managed = any(os.path.dirname(yt_dlp_path) == dir_path for dir_path in app_managed_dirs)
            
            if is_app_managed:
                logger.info("AutoUpdateThread: Updating app-managed yt-dlp binary...")
                return self._update_binary(yt_dlp_path)
            else:
                logger.info("AutoUpdateThread: Updating system yt-dlp via pip...")
                return self._update_via_pip()
                
        except Exception as e:
            logger.error(f"AutoUpdateThread: Error in _perform_update: {e}", exc_info=True)
            return False
    
    def _update_binary(self, yt_dlp_path):
        """Update yt-dlp binary directly from GitHub releases (silent version)."""
        try:
            # Determine the URL based on OS
            if sys.platform == 'win32':
                url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
            elif sys.platform == 'darwin':
                url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp_macos"
            else:
                url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp"
            
            logger.info("AutoUpdateThread: Downloading latest yt-dlp binary...")
            
            # Download without progress tracking (silent)
            response = requests.get(url, stream=True)
            if response.status_code != 200:
                logger.error(f"AutoUpdateThread: Download failed: HTTP {response.status_code}")
                return False
            
            temp_file = f"{yt_dlp_path}.new"
            
            with open(temp_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            logger.info("AutoUpdateThread: Installing updated binary...")
            
            # Make executable on Unix systems
            if sys.platform != 'win32':
                os.chmod(temp_file, 0o755)
            
            # Replace the old file with the new one
            try:
                # On Windows, we need to remove the old file first
                if sys.platform == 'win32' and os.path.exists(yt_dlp_path):
                    os.remove(yt_dlp_path)
                
                os.rename(temp_file, yt_dlp_path)
                logger.info("AutoUpdateThread: Binary successfully updated!")
                return True
                
            except Exception as e:
                logger.error(f"AutoUpdateThread: Error installing binary: {e}")
                # Clean up temp file if it exists
                if os.path.exists(temp_file):
                    try:
                        os.remove(temp_file)
                    except:
                        pass
                return False
                
        except Exception as e:
            logger.error(f"AutoUpdateThread: Binary update failed: {e}", exc_info=True)
            return False
    
    def _update_via_pip(self):
        """Update yt-dlp via pip (silent version)."""
        try:
            import pkg_resources
            
            logger.info("AutoUpdateThread: Checking current pip installation...")
            
            # Get current version
            try:
                current_version = pkg_resources.get_distribution("yt-dlp").version
                logger.info(f"AutoUpdateThread: Current version: {current_version}")
            except pkg_resources.DistributionNotFound:
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
                
                # Create startupinfo to hide console on Windows
                startupinfo = None
                if sys.platform == 'win32' and hasattr(subprocess, 'STARTUPINFO'):
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    startupinfo.wShowWindow = 0  # SW_HIDE
                
                # Run pip update
                logger.info("AutoUpdateThread: Running pip install --upgrade...")
                update_result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"],
                    capture_output=True,
                    text=True,
                    check=False,
                    startupinfo=startupinfo
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
            logger.error(f"AutoUpdateThread: Pip update failed: {e}", exc_info=True)
            return False
