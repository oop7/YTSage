import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from ytsage_gui_main import YTSageApp  # Import the main application class from ytsage_gui_main

def show_error_dialog(message):
    error_dialog = QMessageBox()
    error_dialog.setIcon(QMessageBox.Icon.Critical)
    error_dialog.setText("Application Error")
    error_dialog.setInformativeText(message)
    error_dialog.setWindowTitle("Error")
    error_dialog.exec()

def main():
    try:
        app = QApplication(sys.argv)
        window = YTSageApp() # Instantiate the main application class
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        show_error_dialog(f"Critical error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()