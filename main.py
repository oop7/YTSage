import sys
import os

# Early detection and handling of windowed mode to prevent console window flicker
def setup_windowed_mode():
    """
    Setup windowed mode handling to prevent console window flickering.
    This must be called as early as possible in the application startup.
    """
    if getattr(sys, 'frozen', False):
        # Running as compiled executable (PyInstaller)
        if sys.stdout is None or sys.stderr is None:
            # Windowed mode - completely suppress console output
            import io
            null_stream = io.StringIO()
            if sys.stdout is None:
                sys.stdout = null_stream
            if sys.stderr is None:
                sys.stderr = null_stream
        else:
            # Console mode but compiled - redirect to null to prevent window flicker
            if os.name == 'nt':  # Windows
                try:
                    import io
                    # Create a null output stream
                    null_stream = io.StringIO()
                    # Only redirect if we detect this might cause console window issues
                    # Check if we're not already in a console
                    try:
                        # Try to get console window handle - if this fails, we're likely windowed
                        import ctypes
                        kernel32 = ctypes.windll.kernel32
                        console_window = kernel32.GetConsoleWindow()
                        if console_window == 0:
                            # No console window exists, redirect to prevent one from appearing
                            sys.stdout = null_stream
                            sys.stderr = null_stream
                    except:
                        # If console detection fails, err on the side of caution
                        sys.stdout = null_stream
                        sys.stderr = null_stream
                except:
                    # If all else fails, continue normally
                    pass

# Call windowed mode setup immediately
setup_windowed_mode()

from PySide6.QtWidgets import QApplication, QMessageBox

from src.core.ytsage_logging import logger
from src.core.ytsage_yt_dlp import (  # Import the new yt-dlp setup functions
    check_ytdlp_binary,
    setup_ytdlp,
)
from src.gui.ytsage_gui_main import YTSageApp  # Import the main application class from ytsage_gui_main


def show_error_dialog(message):
    error_dialog = QMessageBox()
    error_dialog.setIcon(QMessageBox.Icon.Critical)
    error_dialog.setText("Application Error")
    error_dialog.setInformativeText(message)
    error_dialog.setWindowTitle("Error")
    error_dialog.exec()


def main():
    try:
        logger.info("Starting YTSage application")
        app = QApplication(sys.argv)

        # Get the expected binary path and check if it exists
        if not check_ytdlp_binary():
            # No app-specific binary found, show setup dialog regardless of Python package
            logger.warning("No yt-dlp binary found, starting setup process")
            yt_dlp_path = setup_ytdlp()
            if yt_dlp_path == "yt-dlp":  # If user canceled or something went wrong
                logger.warning("yt-dlp not configured properly")

        window = YTSageApp()  # Instantiate the main application class
        window.show()
        logger.info("Application window shown, entering main loop")
        sys.exit(app.exec())
    except Exception as e:
        logger.critical(f"Critical application error: {e}", exc_info=True)
        show_error_dialog(f"Critical error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
