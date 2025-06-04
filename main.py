import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from ytsage_gui_main import YTSageApp  # Import the main application class from ytsage_gui_main
from ytsage_utils import update_yt_dlp  # Import the update function

def show_error_dialog(message):
    error_dialog = QMessageBox()
    error_dialog.setIcon(QMessageBox.Icon.Critical)
    error_dialog.setText("Application Error")
    error_dialog.setInformativeText(message)
    error_dialog.setWindowTitle("Error")
    error_dialog.exec()

def main():
    try:
        # Try to update yt-dlp before starting the app
        try:
            update_yt_dlp()
        except Exception as e:
            print(f"Warning: Could not update yt-dlp: {e}")
            # Continue with application startup even if the update fails
        
        app = QApplication(sys.argv)
        window = YTSageApp() # Instantiate the main application class
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        show_error_dialog(f"Critical error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()