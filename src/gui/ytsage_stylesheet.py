
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
