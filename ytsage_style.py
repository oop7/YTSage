MAIN_STYLE = """
QMainWindow {
    background-color: #2b2b2b;
}
QWidget {
    background-color: #2b2b2b;
    color: #ffffff;
    font-size: 12px;
}
QLineEdit {
    padding: 8px;
    border: 2px solid #3d3d3d;
    border-radius: 4px;
    background-color: #363636;
    color: #ffffff;
    selection-background-color: #ff0000;
    selection-color: #ffffff;
}
QPushButton {
    padding: 8px 15px;
    background-color: #ff0000;  /* YouTube red */
    border: none;
    border-radius: 4px;
    color: white;
    font-weight: bold;
    min-height: 20px;
}
QPushButton:hover {
    background-color: #cc0000;  /* Darker red on hover */
}
QPushButton:pressed {
    background-color: #990000;  /* Even darker red when pressed */
}
QPushButton:disabled {
    background-color: #666666;  /* Gray when disabled */
    color: #999999;
}
QTableWidget {
    border: 2px solid #3d3d3d;
    border-radius: 4px;
    background-color: #363636;
    gridline-color: #3d3d3d;
    selection-background-color: #ff0000;
    selection-color: #ffffff;
}
QHeaderView::section {
    background-color: #2b2b2b;
    padding: 5px;
    border: 1px solid #3d3d3d;
    color: #ffffff;
    font-weight: bold;
}
QScrollBar:vertical {
    border: none;
    background-color: #2b2b2b;
    width: 12px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background-color: #666666;
    min-height: 20px;
    border-radius: 6px;
}
QScrollBar::handle:vertical:hover {
    background-color: #ff0000;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
QProgressBar {
    border: 2px solid #3d3d3d;
    border-radius: 4px;
    text-align: center;
    color: white;
    background-color: #363636;
}
QProgressBar::chunk {
    background-color: #ff0000;
    border-radius: 2px;
}
QComboBox {
    padding: 5px;
    border: 2px solid #3d3d3d;
    border-radius: 4px;
    background-color: #363636;
    color: #ffffff;
    min-height: 20px;
}
QComboBox::drop-down {
    border: none;
    width: 20px;
}
QComboBox::down-arrow {
    image: url(down_arrow.png);
    width: 12px;
    height: 12px;
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
    background: #2b2b2b;
}
QCheckBox::indicator:checked {
    border: 2px solid #ff0000;
    background: #ff0000;
}
QLabel {
    color: #ffffff;
}
QTextEdit, QPlainTextEdit {
    background-color: #363636;
    color: #ffffff;
    border: 2px solid #3d3d3d;
    border-radius: 4px;
    selection-background-color: #ff0000;
    selection-color: #ffffff;
}
QMessageBox {
    background-color: #2b2b2b;
}
QMessageBox QLabel {
    color: #ffffff;
}
QMessageBox QPushButton {
    min-width: 80px;
}
""" 