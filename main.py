import sys

from PySide6.QtWidgets import QApplication, QMessageBox

from src.utils.ytsage_logger import logger
from src.core.ytsage_yt_dlp import check_ytdlp_binary, setup_ytdlp  # Import the new yt-dlp setup functions
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
