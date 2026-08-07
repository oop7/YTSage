import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QMessageBox

from .utils.ytsage_logger import logger
from .gui.ytsage_gui_main import YTSageApp  # Import the main application class from ytsage_gui_main


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

        window = YTSageApp()  # Instantiate the main application class
        if len(sys.argv) > 1:
            initial_url = sys.argv[1].strip()
            if initial_url:
                window.url_input.setText(initial_url)
        window.show()
        if len(sys.argv) > 1 and sys.argv[1].strip():
            QTimer.singleShot(0, window.analyze_url)
        logger.info("Application window shown, entering main loop")
        sys.exit(app.exec())
    except Exception as e:
        logger.critical(f"Critical application error: {e}", exc_info=True)
        show_error_dialog(f"Critical error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
