import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from src.gui.ytsage_gui_main import YTSageApp  # Import the main application class from ytsage_gui_main
from src.core.ytsage_yt_dlp import check_ytdlp_binary, setup_ytdlp, get_ytdlp_executable_path  # Import the new yt-dlp setup functions
from src.core.ytsage_logging import logger

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
        expected_path = get_ytdlp_executable_path()
        if not check_ytdlp_binary():
            # No app-specific binary found, show setup dialog regardless of Python package
            logger.warning("No yt-dlp binary found, starting setup process")
            yt_dlp_path = setup_ytdlp()
            if yt_dlp_path == "yt-dlp":  # If user canceled or something went wrong
                logger.warning("yt-dlp not configured properly")
        
        window = YTSageApp() # Instantiate the main application class
        window.show()
        logger.info("Application window shown, entering main loop")
        sys.exit(app.exec())
    except Exception as e:
        logger.critical(f"Critical application error: {str(e)}", exc_info=True)
        show_error_dialog(f"Critical error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()