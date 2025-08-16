import os
import sys
import platform
import shutil
import subprocess
import requests
from pathlib import Path
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPushButton, 
                             QProgressBar, QRadioButton, QHBoxLayout, 
                             QMessageBox, QFileDialog, QWidget)
from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtGui import QIcon
from .ytsage_logging import logger

# Define binary URLs
YTDLP_URLS = {
    "windows": "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe",
    "macos": "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp_macos",
    "linux": "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp"
}

# Define installation paths
def get_ytdlp_install_dir():
    """Get the OS-specific yt-dlp installation directory"""
    if sys.platform == 'win32':
        # Windows: %LOCALAPPDATA%\YTSage\bin\
        return os.path.join(os.environ.get('LOCALAPPDATA'), 'YTSage', 'bin')
    elif sys.platform == 'darwin':
        # macOS: ~/Library/Application Support/YTSage/bin/
        return os.path.expanduser(os.path.join('~', 'Library', 'Application Support', 'YTSage', 'bin'))
    else:
        # Linux: ~/.local/share/YTSage/bin/
        return os.path.expanduser(os.path.join('~', '.local', 'share', 'YTSage', 'bin'))

def get_ytdlp_executable_path():
    """Get the full path to the yt-dlp executable based on OS"""
    install_dir = get_ytdlp_install_dir()
    if sys.platform == 'win32':
        return os.path.join(install_dir, 'yt-dlp.exe')
    else:
        return os.path.join(install_dir, 'yt-dlp')

def get_os_type():
    """Detect the operating system"""
    if sys.platform == 'win32':
        return "windows"
    elif sys.platform == 'darwin':
        return "macos"
    else:
        return "linux"

def ensure_install_dir_exists():
    """Make sure the installation directory exists"""
    install_dir = get_ytdlp_install_dir()
    os.makedirs(install_dir, exist_ok=True)
    return install_dir

class DownloadYtdlpThread(QThread):
    progress_signal = Signal(int)
    finished_signal = Signal(bool, str)
    
    def __init__(self, os_type):
        super().__init__()
        self.os_type = os_type
        
    def run(self):
        try:
            url = YTDLP_URLS[self.os_type]
            install_dir = ensure_install_dir_exists()
            
            if self.os_type == "windows":
                exe_path = os.path.join(install_dir, "yt-dlp.exe")
            else:
                exe_path = os.path.join(install_dir, "yt-dlp")
                
            # Download with progress reporting
            response = requests.get(url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 Kibibyte
            
            if total_size == 0:
                self.progress_signal.emit(100)
            
            with open(exe_path, 'wb') as f:
                downloaded = 0
                for data in response.iter_content(block_size):
                    f.write(data)
                    downloaded += len(data)
                    if total_size > 0:
                        progress = int(downloaded / total_size * 100)
                        self.progress_signal.emit(progress)
            
            # Make executable on macOS and Linux
            if self.os_type != "windows":
                os.chmod(exe_path, 0o755)
                
            self.finished_signal.emit(True, exe_path)
            
        except Exception as e:
            self.finished_signal.emit(False, str(e))

class YtdlpSetupDialog(QDialog):
    setup_complete = Signal(str)  # Signal emitting the path to yt-dlp
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.os_type = get_os_type()
        self.setWindowTitle("yt-dlp Setup Required")
        self.setMinimumWidth(520)
        self.setMinimumHeight(350)
        self.resize(520, 380)
        
        # Set the window icon to match the main app
        if parent and parent.windowIcon():
            self.setWindowIcon(parent.windowIcon())
        else:
            # Try to load the icon directly if parent not available
            # Navigate from src/core/ to project root, then to assets/Icon/
            current_dir = os.path.dirname(os.path.abspath(__file__))  # core/
            src_dir = os.path.dirname(current_dir)                    # src/
            project_root = os.path.dirname(src_dir)                   # project root
            icon_path = os.path.join(project_root, 'assets', 'Icon', 'icon.png')
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))
        
        self.init_ui()
        
        # Apply dark theme styling to match app
        self.setStyleSheet("""
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
            QRadioButton {
                color: #ffffff;
                spacing: 10px;
                padding: 8px;
                font-size: 13px;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;
            }
            QRadioButton::indicator:unchecked {
                border: 2px solid #666666;
                background: #1d1e22;
            }
            QRadioButton::indicator:checked {
                border: 2px solid #c90000;
                background: #c90000;
            }
        """)
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)
        
        # Header title
        title_label = QLabel("yt-dlp Setup Required")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff; padding: 5px 0;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Information label with improved styling
        if self.os_type == "windows":
            os_name = "Windows"
        elif self.os_type == "macos":
            os_name = "macOS"
        else:
            os_name = "Linux"
            
        info_label = QLabel(f"YTSage requires yt-dlp to download videos.<br><br>"
                           f"yt-dlp was not found in the app's local directory. "
                           f"YTSage needs to set up yt-dlp for your {os_name} system.<br><br>"
                           f"Please choose an option below:")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setWordWrap(True)
        info_label.setStyleSheet("font-size: 13px; color: #cccccc; padding: 5px; line-height: 1.4;")
        layout.addWidget(info_label)
        
        # Radio buttons with minimal spacing
        option_widget = QWidget()
        option_layout = QVBoxLayout(option_widget)
        option_layout.setSpacing(8)
        option_layout.setContentsMargins(0, 0, 0, 0)
        
        self.auto_radio = QRadioButton("Download automatically (Recommended)")
        self.auto_radio.setChecked(True)
        self.manual_radio = QRadioButton("Select path manually")
        
        option_layout.addWidget(self.auto_radio)
        option_layout.addWidget(self.manual_radio)
        layout.addWidget(option_widget)
        
        # Progress bar with proper sizing
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setFixedHeight(20)  # Fixed height for consistency
        self.progress_bar.setStyleSheet("""
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
        """)
        layout.addWidget(self.progress_bar)
        
        # Status label with better spacing
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 12px; color: #cccccc; padding: 8px 0;")
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)
        
        # Add stretch to push buttons to bottom
        layout.addStretch()
        
        # Button layout with improved spacing
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.setContentsMargins(0, 10, 0, 0)  # Add top margin for buttons
        
        self.setup_button = QPushButton("Setup yt-dlp")
        self.setup_button.clicked.connect(self.setup_ytdlp)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.setup_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def setup_ytdlp(self):
        if self.auto_radio.isChecked():
            self.download_ytdlp()
        else:
            self.select_ytdlp_path()
    
    def download_ytdlp(self):
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("Downloading yt-dlp...")
        self.setup_button.setEnabled(False)
        self.cancel_button.setEnabled(False)
        
        self.download_thread = DownloadYtdlpThread(self.os_type)
        self.download_thread.progress_signal.connect(self.update_progress)
        self.download_thread.finished_signal.connect(self.download_finished)
        self.download_thread.start()
    
    def update_progress(self, value):
        self.progress_bar.setValue(value)
    
    def download_finished(self, success, result):
        self.setup_button.setEnabled(True)
        self.cancel_button.setEnabled(True)
        
        if success:
            self.status_label.setText("yt-dlp was successfully installed!")
            self.setup_complete.emit(result)
            self.accept()
        else:
            self.status_label.setText(f"Error: {result}")
            error_dialog = QMessageBox(self)
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setWindowTitle("Download Failed")
            error_dialog.setText(f"Failed to download yt-dlp: {result}")
            # Set the window icon to match the main dialog
            error_dialog.setWindowIcon(self.windowIcon())
            error_dialog.setStyleSheet("""
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
            """)
            error_dialog.exec()
    
    def select_ytdlp_path(self):
        if self.os_type == "windows":
            file_filter = "Executable Files (*.exe)"
        else:
            file_filter = "All Files (*)"
            
        # Apply style to QFileDialog
        file_dialog = QFileDialog(self)
        file_dialog.setStyleSheet("""
            QFileDialog {
                background-color: #15181b;
                color: #ffffff;
            }
            QLabel, QCheckBox, QListView, QTreeView, QComboBox, QLineEdit {
                color: #ffffff;
                background-color: #1b2021;
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
        """)
        
        file_path, _ = file_dialog.getOpenFileName(
            self, "Select yt-dlp executable", "", file_filter
        )
        
        if file_path:
            logger.debug(f"User selected file: {file_path}")
            # Verify the selected file
            try:
                # Set up startupinfo to hide console window on Windows
                startupinfo = None
                if sys.platform == 'win32' and hasattr(subprocess, 'STARTUPINFO'):
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    startupinfo.wShowWindow = 0  # SW_HIDE
                
                # Try to run yt-dlp --version
                logger.debug(f"Verifying file with --version command")
                result = subprocess.run(
                    [file_path, "--version"], 
                    capture_output=True, 
                    text=True,
                    check=False,
                    startupinfo=startupinfo
                )
                logger.debug(f"Version check result: {result.returncode}, Output: {result.stdout.strip()}")
                
                if result.returncode == 0:
                    # File is valid, copy it to our app's bin directory
                    try:
                        # Ensure the bin directory exists
                        install_dir = ensure_install_dir_exists()
                        logger.debug(f"Install directory: {install_dir}")
                        
                        # Determine the target filename based on OS
                        if self.os_type == "windows":
                            target_path = os.path.join(install_dir, "yt-dlp.exe")
                        else:
                            target_path = os.path.join(install_dir, "yt-dlp")
                        logger.debug(f"Target path: {target_path}")
                        
                        # Copy the file
                        shutil.copy2(file_path, target_path)
                        logger.debug(f"File copied successfully")
                        
                        # Set executable permissions on Unix systems
                        if self.os_type != "windows":
                            os.chmod(target_path, 0o755)
                            logger.debug(f"Permissions set on Unix system")
                        
                        # Return the path of the copied file
                        self.status_label.setText(f"yt-dlp successfully copied to {target_path}")
                        logger.debug(f"Emitting setup_complete signal with path: {target_path}")
                        self.setup_complete.emit(target_path)
                        self.accept()
                    except Exception as copy_error:
                        logger.debug(f"Error copying file: {str(copy_error)}")
                        error_dialog = QMessageBox(self)
                        error_dialog.setIcon(QMessageBox.Critical)
                        error_dialog.setWindowTitle("Setup Error")
                        error_dialog.setText(f"Error copying yt-dlp to app directory: {str(copy_error)}")
                        error_dialog.setStyleSheet("""
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
                        """)
                        error_dialog.exec()
                else:
                    logger.debug(f"File verification failed with return code: {result.returncode}")
                    error_dialog = QMessageBox(self)
                    error_dialog.setIcon(QMessageBox.Warning)
                    error_dialog.setWindowTitle("Invalid Executable")
                    error_dialog.setText("The selected file does not appear to be a valid yt-dlp executable.")
                    error_dialog.setStyleSheet("""
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
                    """)
                    error_dialog.exec()
            except Exception as e:
                logger.debug(f"Exception during verification: {str(e)}")
                error_dialog = QMessageBox(self)
                error_dialog.setIcon(QMessageBox.Critical)
                error_dialog.setWindowTitle("Error")
                error_dialog.setText(f"Error verifying yt-dlp executable: {str(e)}")
                error_dialog.setStyleSheet("""
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
                """)
                error_dialog.exec()

def check_ytdlp_binary():
    """
    Check if yt-dlp binary exists in the expected location.
    Returns:
        str or None: Path to yt-dlp binary if found, None otherwise
    """
    exe_path = get_ytdlp_executable_path()
    if os.path.exists(exe_path):
        # Make sure it's executable on Unix systems
        if sys.platform != 'win32' and not os.access(exe_path, os.X_OK):
            try:
                os.chmod(exe_path, 0o755)
                logger.info(f"Fixed permissions on yt-dlp at {exe_path}")
            except Exception as e:
                logger.warning(f"Could not set executable permissions on {exe_path}: {e}")
                return None
        return exe_path
    
    # If not found in app directory, check if yt-dlp is available in PATH
    try:
        # Use subprocess to check if yt-dlp is available
        if sys.platform == 'win32':
            # On Windows, use 'where' command and hide console window
            startupinfo = None
            if hasattr(subprocess, 'STARTUPINFO'):
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = 0  # SW_HIDE
            
            result = subprocess.run(
                ['where', 'yt-dlp'], 
                capture_output=True, 
                text=True, 
                check=False,
                startupinfo=startupinfo
            )
            if result.returncode == 0 and result.stdout.strip():
                yt_dlp_path = result.stdout.strip().split('\n')[0]
                logger.info(f"Found yt-dlp in PATH: {yt_dlp_path}")
                return yt_dlp_path
        else:
            # On Unix systems, use 'which' command
            result = subprocess.run(['which', 'yt-dlp'], capture_output=True, text=True, check=False)
            if result.returncode == 0 and result.stdout.strip():
                yt_dlp_path = result.stdout.strip()
                logger.info(f"Found yt-dlp in PATH: {yt_dlp_path}")
                return yt_dlp_path
    except Exception as e:
        logger.error(f"Error checking for yt-dlp in PATH: {e}")
    
    # We're only interested in our app-specific installation or system PATH
    return None

def check_ytdlp_installed():
    """
    Check if yt-dlp is installed and accessible.
    Returns:
        bool: True if yt-dlp is found and working, False otherwise
    """
    try:
        ytdlp_path = check_ytdlp_binary()
        if ytdlp_path:
            # Try to run yt-dlp --version to verify it's working
            try:
                # Create startupinfo to hide console on Windows
                startupinfo = None
                if sys.platform == 'win32' and hasattr(subprocess, 'STARTUPINFO'):
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    startupinfo.wShowWindow = 0  # SW_HIDE
                
                result = subprocess.run(
                    [ytdlp_path, '--version'],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    startupinfo=startupinfo
                )
                return result.returncode == 0
            except Exception:
                return False
        return False
    except Exception:
        return False

def get_yt_dlp_path():
    """
    Get the yt-dlp path, either from the app's bin directory or system PATH.
    This replaces the function in ytsage_utils.py.
    Returns:
        str: Path to yt-dlp binary
    """
    # First check if we have yt-dlp in our app's bin directory or system PATH
    ytdlp_path = check_ytdlp_binary()
    if ytdlp_path:
        logger.info(f"Using yt-dlp from: {ytdlp_path}")
        return ytdlp_path
    
    # If not found anywhere, fall back to the command name as a last resort
    logger.info("yt-dlp not found in app directory or PATH, falling back to command name")
    return "yt-dlp"

def setup_ytdlp(parent_widget=None):
    """
    Show the yt-dlp setup dialog and handle the result.
    Returns:
        str: Path to yt-dlp binary
    """
    logger.debug("Starting yt-dlp setup dialog")
    dialog = YtdlpSetupDialog(parent_widget)
    
    # Store the setup result from the signal
    setup_result = {"path": None}
    
    def on_setup_complete(path):
        logger.debug(f"Received setup_complete signal with path: {path}")
        setup_result["path"] = path
    
    # Connect to the setup_complete signal
    dialog.setup_complete.connect(on_setup_complete)
    
    # Show the dialog
    result = dialog.exec()
    logger.debug(f"Dialog result: {result} (Accepted={QDialog.Accepted})")
    
    if result == QDialog.Accepted:
        # First check if we received a path from the signal
        if setup_result["path"] and os.path.exists(setup_result["path"]):
            logger.debug(f"Using path from signal: {setup_result['path']}")
            return setup_result["path"]
            
        # Get the expected path for verification as fallback
        expected_path = get_ytdlp_executable_path()
        logger.debug(f"Expected yt-dlp path: {expected_path}")
        
        # Verify the path exists after dialog is accepted
        if os.path.exists(expected_path):
            logger.debug(f"yt-dlp successfully found at expected path: {expected_path}")
            return expected_path
        else:
            logger.debug(f"Expected path does not exist, trying alternate detection")
            # Try to use the get_yt_dlp_path function to find yt-dlp elsewhere
            yt_dlp_path = get_yt_dlp_path()
            logger.debug(f"Alternate detection result: {yt_dlp_path}")
            if yt_dlp_path != "yt-dlp" and os.path.exists(yt_dlp_path):
                logger.debug(f"yt-dlp found at alternate location: {yt_dlp_path}")
                return yt_dlp_path
            
            # Something went wrong, show an error message
            logger.debug(f"Setup failed, showing error dialog")
            if parent_widget:
                error_dialog = QMessageBox(parent_widget)
                error_dialog.setIcon(QMessageBox.Warning)
                error_dialog.setWindowTitle("Setup Failed")
                error_dialog.setText("Failed to set up yt-dlp. Some features may not work correctly.")
                # Set the window icon to match the parent
                error_dialog.setWindowIcon(parent_widget.windowIcon())
                error_dialog.setStyleSheet("""
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
                """)
                error_dialog.exec()
            logger.warning(f"yt-dlp setup failed, path does not exist: {expected_path}")
    else:
        logger.debug("User cancelled the setup dialog")
    
    # User cancelled or setup failed, return the fallback command
    logger.debug("Returning fallback command 'yt-dlp'")
    return "yt-dlp" 