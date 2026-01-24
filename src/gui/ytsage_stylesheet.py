
class StyleSheet:
    MAIN = """
            QMainWindow {
                background-color: #15181b;
            }
            QWidget {
                background-color: #15181b;
                color: #ffffff;
            }
            QLineEdit {
                padding: 5px 15px;
                border: 2px solid #2a2d2e;
                border-radius: 6px;
                background-color: #1b2021;
                color: #ffffff;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #ff6b6b;
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
            QPushButton:pressed {
                background-color: #800000;
            }
            QPushButton:disabled {
                background-color: #3d3d3d;
                color: #888888;
            }
            QTableWidget {
                border: 2px solid #1b2021;
                border-radius: 4px;
                background-color: #1b2021;
                gridline-color: #1b2021;
            }
            QHeaderView::section {
                background-color: #15181b;
                padding: 5px;
                border: 1px solid #1b2021;
                color: #ffffff;
            }
            QProgressBar {
                border: 2px solid #1b2021;
                border-radius: 4px;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #c90000;
                border-radius: 2px;
            }
            QLabel {
                color: #ffffff;
            }
            /* Style for filter buttons */
            QPushButton.filter-btn {
                background-color: #1b2021;
                padding: 5px 10px;
                margin: 0 5px;
            }
            QPushButton.filter-btn:checked {
                background-color: #c90000;
            }
            QPushButton.filter-btn:hover {
                background-color: #444444;
            }
            QPushButton.filter-btn:checked:hover {
                background-color: #a50000;
            }
            /* Modern Scrollbar Styling */
            QScrollBar:vertical {
                border: none;
                background: #15181b;
                width: 14px;
                margin: 15px 0 15px 0;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical {
                background: #404040;
                min-height: 30px;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical:hover {
                background: #505050;
            }
            QScrollBar::sub-line:vertical {
                border: none;
                background: #15181b;
                height: 15px;
                border-top-left-radius: 7px;
                border-top-right-radius: 7px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
            QScrollBar::add-line:vertical {
                border: none;
                background: #15181b;
                height: 15px;
                border-bottom-left-radius: 7px;
                border-bottom-right-radius: 7px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:vertical:hover,
            QScrollBar::add-line:vertical:hover {
                background: #404040;
            }
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                background: none;
                width: 0;
                height: 0;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
    """

    PASTE_BUTTON = """
            QPushButton {
                padding: 9px 20px;
                background-color: #1b2021;
                border: 2px solid #2a2d2e;
                border-radius: 5px;
                color: #ffffff;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #252829;
                border-color: #3a3d3e;
            }
            QPushButton:pressed {
                background-color: #1a1d1e;
            }
    """

    ANALYZE_BUTTON = """
            QPushButton {
                padding: 9px 20px;
                background-color: #c90000;
                border: none;
                border-radius: 5px;
                color: white;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #a50000;
            }
            QPushButton:pressed {
                background-color: #800000;
            }
            QPushButton:disabled {
                background-color: #3d3d3d;
                color: #888888;
            }
    """

    PLAYLIST_BUTTON = """
            QPushButton {
                padding: 6px 12px; 
                background-color: #1d1e22;
                border: 1px solid #c90000;
                border-radius: 4px;
                color: white;
                font-weight: normal;
                text-align: left;
                padding-left: 10px;
            }
            QPushButton:hover { 
                background-color: #2a2d36;
                border-color: #a50000;
            }
    """

    FORMAT_TOGGLE_BUTTON = """
            QPushButton {
                padding: 8px 15px;
                background-color: #1d1e22;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:checked {
                background-color: #c90000;
            }
            QPushButton:hover {
                background-color: #2a2d36;
            }
            QPushButton:checked:hover {
                background-color: #a50000;
            }
    """

    CHECKBOX = """
            QCheckBox {
                color: #ffffff;
                padding: 5px;
                margin-left: 20px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #666666;
                background: #1d1e22;
                border-radius: 9px;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #c90000;
                background: #c90000;
                border-radius: 9px;
            }
             QCheckBox:disabled { color: #888888; }
             QCheckBox::indicator:disabled { border-color: #555555; background: #444444; }
    """

    PROGRESS_BAR = """
            QProgressBar {
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                text-align: center;
                color: white;
                background-color: #363636;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #ff0000;
                border-radius: 2px;
            }
    """

    STATUS_LABEL = """
            QLabel {
                color: #cccccc;
                font-size: 12px;
                padding: 5px;
            }
    """

    OPEN_FOLDER_BUTTON = """
            QPushButton {
                background-color: #2a2d2e;
                color: #cccccc;
                border: 1px solid #404040;
                border-radius: 5px;
                font-size: 16px;
                padding: 2px;
            }
            QPushButton:hover {
                background-color: #3a3d3e;
                border: 1px solid #505050;
            }
            QPushButton:pressed {
                background-color: #1a1d1e;
            }
    """

    UPDATE_DIALOG_MESSAGE = """
            QLabel {
                background-color: #1d1e22;
                border: 1px solid #3d3d3d;
                border-radius: 6px;
                padding: 15px;
                margin: 5px 0;
            }
    """

    UPDATE_DIALOG_CHANGELOG = """
            QTextEdit {
                background-color: #1d1e22;
                border: 2px solid #3d3d3d;
                border-radius: 6px;
                color: #ffffff;
                padding: 10px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 12px;
                line-height: 1.4;
            }
            QScrollBar:vertical {
                border: none;
                background: #1d1e22;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #404040;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background: #505050;
            }
    """

    UPDATE_DIALOG_DOWNLOAD_BTN = """
            QPushButton {
                padding: 10px 20px;
                background-color: #c90000;
                border: none;
                border-radius: 6px;
                color: white;
                font-weight: bold;
                font-size: 13px;
                min-width: 140px;
            }
            QPushButton:hover {
                background-color: #a50000;
            }
            QPushButton:pressed {
                background-color: #800000;
            }
    """

    UPDATE_DIALOG_REMIND_BTN = """
            QPushButton {
                padding: 10px 20px;
                background-color: #3d3d3d;
                border: 1px solid #555555;
                border-radius: 6px;
                color: white;
                font-weight: bold;
                font-size: 13px;
                min-width: 140px;
            }
            QPushButton:hover {
                background-color: #4d4d4d;
                border-color: #666666;
            }
            QPushButton:pressed {
                background-color: #2d2d2d;
            }
    """

    UPDATE_DIALOG_MAIN = """
            QDialog {
                background-color: #15181b;
                border: 1px solid #3d3d3d;
                border-radius: 8px;
            }
            QLabel {
                color: #ffffff;
                font-size: 12px;
            }
    """

    TIME_RANGE_BTN_ACTIVE = """
            QPushButton {
                padding: 8px 15px;
                background-color: #c90000;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
                border: 2px solid white;
            }
            QPushButton:hover {
                background-color: #a50000;
            }
    """

    FILE_EXISTS_DIALOG = """
            QMessageBox {
                background-color: #2b2b2b;
            }
            QLabel {
                color: #ffffff;
            }
            QPushButton {
                padding: 8px 15px;
                background-color: #ff0000;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #cc0000;
            }
    """

    SETUP_SUCCESS_DIALOG = """
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

