MAIN_STYLE = """
QMainWindow {
    background-color: #15181b;
}
QWidget {
    background-color: #15181b;
    color: #ffffff;
    font-size: 12px;
}
QLineEdit {
    padding: 8px;
    border: 2px solid #1b2021;
    border-radius: 4px;
    background-color: #1b2021;
    color: #ffffff;
    selection-background-color: #c90000;
    selection-color: #ffffff;
}
QPushButton {
    padding: 8px 15px;
    background-color: #c90000;
    border: none;
    border-radius: 4px;
    color: white;
    font-weight: bold;
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
QTableWidget {
    border: 2px solid #1b2021;
    border-radius: 4px;
    background-color: #1b2021;
    gridline-color: #1b2021;
    selection-background-color: #c90000;
    selection-color: #ffffff;
}
QHeaderView::section {
    background-color: #15181b;
    padding: 5px;
    border: 1px solid #1b2021;
    color: #ffffff;
    font-weight: bold;
}
QScrollBar:vertical {
    border: none;
    background-color: #15181b;
    width: 12px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background-color: #666666;
    min-height: 20px;
    border-radius: 6px;
}
QScrollBar::handle:vertical:hover {
    background-color: #c90000;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
QProgressBar {
    border: 2px solid #1b2021;
    border-radius: 4px;
    text-align: center;
    color: white;
    background-color: #1b2021;
}
QProgressBar::chunk {
    background-color: #c90000;
    border-radius: 2px;
}
QComboBox {
    padding: 8px;
    border: 2px solid #1b2021;
    border-radius: 4px;
    background-color: #1b2021;
    color: #ffffff;
    min-height: 20px;
}
QComboBox:hover {
    border: 2px solid #c90000;
}
QComboBox:focus {
    border: 2px solid #c90000;
}
QComboBox::drop-down {
    border: none;
    width: 30px;
    background-color: #1b2021;
    border-radius: 0 4px 4px 0;
}
QComboBox::drop-down:hover {
    background-color: #c90000;
}
QComboBox::down-arrow {
    width: 0;
    height: 0;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 8px solid #ffffff;
    margin: auto;
}
QComboBox QAbstractItemView {
    border: 2px solid #1b2021;
    border-radius: 4px;
    background-color: #1b2021;
    color: #ffffff;
    selection-background-color: #c90000;
    selection-color: #ffffff;
    outline: none;
}
QComboBox QAbstractItemView::item {
    height: 30px;
    padding: 5px;
    border: none;
    background-color: #1b2021;
    color: #ffffff;
}
QComboBox QAbstractItemView::item:hover {
    background-color: #c90000;
    color: #ffffff;
}
QComboBox QAbstractItemView::item:selected {
    background-color: #c90000;
    color: #ffffff;
}
QCheckBox {
    spacing: 5px;
    color: #ffffff;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 9px;
}
QCheckBox::indicator:unchecked {
    border: 2px solid #666666;
    background: #15181b;
}
QCheckBox::indicator:checked {
    border: 2px solid #c90000;
    background: #c90000;
}
QRadioButton {
    spacing: 5px;
    color: #ffffff;
}
QRadioButton::indicator {
    width: 18px;
    height: 18px;
    border-radius: 9px;
}
QRadioButton::indicator:unchecked {
    border: 2px solid #666666;
    background: #15181b;
}
QRadioButton::indicator:checked {
    border: 2px solid #c90000;
    background: #c90000;
}
QLabel {
    color: #ffffff;
}
QGroupBox {
    color: #ffffff;
    border: 2px solid #1b2021;
    border-radius: 4px;
    margin-top: 1ex;
    padding-top: 10px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px 0 5px;
    color: #c90000;
    font-weight: bold;
}
QTextEdit, QPlainTextEdit {
    background-color: #1b2021;
    color: #ffffff;
    border: 2px solid #1b2021;
    border-radius: 4px;
    selection-background-color: #c90000;
    selection-color: #ffffff;
}
QMessageBox {
    background-color: #15181b;
}
QMessageBox QLabel {
    color: #ffffff;
}
QMessageBox QPushButton {
    min-width: 80px;
}
"""
