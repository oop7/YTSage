"""
Settings-related dialogs for YTSage application.
Contains dialogs for configuring download settings and auto-update preferences.
"""

import os
import requests
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QGroupBox, QCheckBox,
                             QRadioButton, QComboBox, QDialogButtonBox,
                             QButtonGroup, QMessageBox, QFileDialog)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon
from ...core.ytsage_logging import logger

from ...core.ytsage_utils import (get_auto_update_settings, update_auto_update_settings,
                         check_and_update_ytdlp_auto, get_ytdlp_version)


class DownloadSettingsDialog(QDialog):
    def __init__(self, current_path, current_limit, current_unit_index, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Download Settings")
        self.setMinimumWidth(450)
        self.setMinimumHeight(400)
        self.current_path = current_path
        self.current_limit = current_limit if current_limit is not None else ""
        self.current_unit_index = current_unit_index

        # Apply main app styling
        self.setStyleSheet("""
            QDialog {
                background-color: #15181b;
                color: #ffffff;
            }
            QWidget {
                background-color: #15181b;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
            QGroupBox {
                color: #ffffff;
                border: 2px solid #1b2021;
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
                background-color: #15181b;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #ffffff;
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
            QComboBox {
                padding: 5px;
                border: 2px solid #1b2021;
                border-radius: 4px;
                background-color: #1b2021;
                color: #ffffff;
                min-height: 20px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #1b2021;
                border-radius: 4px;
                background-color: #15181b;
                color: #ffffff;
                selection-background-color: #c90000;
                selection-color: #ffffff;
            }
        """)

        layout = QVBoxLayout(self)

        # --- Download Path Section ---
        path_group_box = QGroupBox("Download Path")
        path_layout = QVBoxLayout()

        self.path_display = QLabel(self.current_path)
        self.path_display.setWordWrap(True)
        self.path_display.setStyleSheet("QLabel { color: #ffffff; padding: 5px; border: 1px solid #1b2021; border-radius: 4px; background-color: #1b2021; }")
        path_layout.addWidget(self.path_display)

        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(self.browse_new_path)
        path_layout.addWidget(browse_button)

        path_group_box.setLayout(path_layout)
        layout.addWidget(path_group_box)

        # --- Speed Limit Section ---
        speed_group_box = QGroupBox("Speed Limit")
        speed_layout = QHBoxLayout()

        self.speed_limit_input = QLineEdit(str(self.current_limit))
        self.speed_limit_input.setPlaceholderText("None")
        speed_layout.addWidget(self.speed_limit_input)

        self.speed_limit_unit = QComboBox()
        self.speed_limit_unit.addItems(["KB/s", "MB/s"])
        self.speed_limit_unit.setCurrentIndex(self.current_unit_index)
        speed_layout.addWidget(self.speed_limit_unit)

        speed_group_box.setLayout(speed_layout)
        layout.addWidget(speed_group_box)

        # --- Auto-Update yt-dlp Section ---
        auto_update_group_box = QGroupBox("Auto-Update yt-dlp")
        auto_update_layout = QVBoxLayout()

        # Load current auto-update settings
        auto_settings = get_auto_update_settings()

        # Enable/Disable auto-update checkbox
        self.auto_update_enabled = QCheckBox("Enable automatic yt-dlp updates")
        self.auto_update_enabled.setChecked(auto_settings['enabled'])
        auto_update_layout.addWidget(self.auto_update_enabled)

        # Frequency options
        frequency_label = QLabel("Update frequency:")
        frequency_label.setStyleSheet("color: #ffffff; margin-top: 10px;")
        auto_update_layout.addWidget(frequency_label)

        self.startup_radio = QRadioButton("Check on every startup (minimum 1 hour between checks)")
        self.daily_radio = QRadioButton("Check daily")
        self.weekly_radio = QRadioButton("Check weekly")

        # Set current selection based on saved settings
        current_frequency = auto_settings['frequency']
        if current_frequency == 'startup':
            self.startup_radio.setChecked(True)
        elif current_frequency == 'daily':
            self.daily_radio.setChecked(True)
        else:  # weekly
            self.weekly_radio.setChecked(True)

        auto_update_layout.addWidget(self.startup_radio)
        auto_update_layout.addWidget(self.daily_radio)
        auto_update_layout.addWidget(self.weekly_radio)

        # Test update button
        test_update_layout = QHBoxLayout()
        test_update_button = QPushButton("Check for Updates Now")
        test_update_button.clicked.connect(self.test_update_check)
        test_update_layout.addWidget(test_update_button)
        test_update_layout.addStretch()
        auto_update_layout.addLayout(test_update_layout)

        auto_update_group_box.setLayout(auto_update_layout)
        layout.addWidget(auto_update_group_box)

        # Dialog buttons (OK/Cancel)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def browse_new_path(self):
        new_path = QFileDialog.getExistingDirectory(self, "Select Download Directory", self.current_path)
        if new_path:
            self.current_path = new_path
            self.path_display.setText(self.current_path)

    def get_selected_path(self):
        """Returns the confirmed path after the dialog is accepted."""
        return self.current_path

    def get_selected_speed_limit(self):
        """Returns the entered speed limit value (as string or None)."""
        limit_str = self.speed_limit_input.text().strip()
        if not limit_str:
            return None
        try:
            float(limit_str)  # Check if convertible to float
            return limit_str
        except ValueError:
            logger.info("Invalid speed limit input in dialog")
            return None

    def get_selected_unit_index(self):
        """Returns the index of the selected speed limit unit."""
        return self.speed_limit_unit.currentIndex()

    def _create_styled_message_box(self, icon, title, text):
        """Create a styled QMessageBox that matches the app theme."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setWindowIcon(self.windowIcon())
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #15181b;
                color: #ffffff;
            }
            QMessageBox QLabel {
                color: #ffffff;
            }
            QMessageBox QPushButton {
                padding: 8px 15px;
                background-color: #c90000;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #a50000;
            }
            QMessageBox QPushButton:pressed {
                background-color: #800000;
            }
        """)
        return msg_box

    def test_update_check(self):
        """Test the update check functionality."""
        try:
            # Get current version
            current_version = get_ytdlp_version()
            if "Error" in current_version:
                msg_box = self._create_styled_message_box(
                    QMessageBox.Warning,
                    "Update Check",
                    "Could not determine current yt-dlp version."
                )
                msg_box.exec()
                return
            
            # Get latest version from PyPI
            response = requests.get("https://pypi.org/pypi/yt-dlp/json", timeout=10)
            response.raise_for_status()
            latest_version = response.json()["info"]["version"]
            
            # Clean up version strings
            current_version = current_version.replace('_', '.')
            latest_version = latest_version.replace('_', '.')
            
            from packaging import version as version_parser
            if version_parser.parse(latest_version) > version_parser.parse(current_version):
                msg_box = self._create_styled_message_box(
                    QMessageBox.Information,
                    "Update Check",
                    f"Update available!\n\nCurrent: {current_version}\nLatest: {latest_version}\n\nUse the 'Update yt-dlp' button in the main window to update."
                )
                msg_box.exec()
            else:
                msg_box = self._create_styled_message_box(
                    QMessageBox.Information,
                    "Update Check",
                    f"yt-dlp is up to date!\n\nCurrent version: {current_version}"
                )
                msg_box.exec()
        except Exception as e:
            msg_box = self._create_styled_message_box(
                QMessageBox.Warning,
                "Update Check",
                f"Error checking for updates: {str(e)}"
            )
            msg_box.exec()

    def get_auto_update_settings(self):
        """Returns the auto-update settings from the dialog."""
        enabled = self.auto_update_enabled.isChecked()
        
        if self.startup_radio.isChecked():
            frequency = 'startup'
        elif self.daily_radio.isChecked():
            frequency = 'daily'
        else:  # weekly_radio is checked
            frequency = 'weekly'
            
        return enabled, frequency

    def accept(self):
        """Override accept to save auto-update settings."""
        try:
            # Save auto-update settings
            enabled, frequency = self.get_auto_update_settings()
            
            if update_auto_update_settings(enabled, frequency):
                QMessageBox.information(self, "Settings Saved",
                                      "Auto-update settings have been saved successfully!")
            else:
                QMessageBox.warning(self, "Error",
                                  "Failed to save auto-update settings.")
        except Exception as e:
            QMessageBox.critical(self, "Error",
                               f"Error saving auto-update settings: {str(e)}")
        
        # Call the parent accept method to close the dialog
        super().accept()


class AutoUpdateSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Auto-Update Settings")
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)
        
        # Set the window icon to match the main app
        if parent:
            self.setWindowIcon(parent.windowIcon())
        
        self.init_ui()
        self.load_current_settings()
        self.apply_styling()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("<h2>🔄 Auto-Update Settings</h2>")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel("Configure automatic updates for yt-dlp to ensure you always have the latest features and bug fixes.")
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setStyleSheet("color: #cccccc; margin: 10px; font-size: 11px;")
        layout.addWidget(desc_label)
        
        # Enable/Disable auto-update
        self.enable_checkbox = QCheckBox("Enable automatic yt-dlp updates")
        self.enable_checkbox.setChecked(True)  # Default enabled
        self.enable_checkbox.toggled.connect(self.on_enable_toggled)
        layout.addWidget(self.enable_checkbox)
        
        # Frequency options
        frequency_group = QGroupBox("Update Frequency")
        frequency_layout = QVBoxLayout()
        
        self.frequency_group = QButtonGroup(self)
        
        self.startup_radio = QRadioButton("Check on every startup (minimum 1 hour between checks)")
        self.daily_radio = QRadioButton("Check daily")
        self.weekly_radio = QRadioButton("Check weekly")
        
        self.daily_radio.setChecked(True)  # Default to daily
        
        self.frequency_group.addButton(self.startup_radio, 0)
        self.frequency_group.addButton(self.daily_radio, 1)
        self.frequency_group.addButton(self.weekly_radio, 2)
        
        frequency_layout.addWidget(self.startup_radio)
        frequency_layout.addWidget(self.daily_radio)
        frequency_layout.addWidget(self.weekly_radio)
        frequency_group.setLayout(frequency_layout)
        
        layout.addWidget(frequency_group)
        
        # Current status
        status_group = QGroupBox("Current Status")
        status_layout = QVBoxLayout()
        
        self.current_version_label = QLabel("Current yt-dlp version: Checking...")
        self.last_check_label = QLabel("Last update check: Never")
        self.next_check_label = QLabel("Next check: Based on settings")
        
        status_layout.addWidget(self.current_version_label)
        status_layout.addWidget(self.last_check_label)
        status_layout.addWidget(self.next_check_label)
        status_group.setLayout(status_layout)
        
        layout.addWidget(status_group)
        
        # Manual check button
        self.manual_check_btn = QPushButton("🔍 Check for Updates Now")
        self.manual_check_btn.clicked.connect(self.manual_check)
        layout.addWidget(self.manual_check_btn)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("Save Settings")
        self.save_btn.clicked.connect(self.save_settings)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        
    def apply_styling(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #15181b;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
            QGroupBox {
                color: #ffffff;
                border: 2px solid #1b2021;
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
                background-color: #15181b;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #ffffff;
            }
            QCheckBox, QRadioButton {
                color: #ffffff;
                spacing: 5px;
                margin: 5px;
            }
            QCheckBox::indicator, QRadioButton::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;
            }
            QCheckBox::indicator:unchecked, QRadioButton::indicator:unchecked {
                border: 2px solid #666666;
                background: #15181b;
            }
            QCheckBox::indicator:checked, QRadioButton::indicator:checked {
                border: 2px solid #c90000;
                background: #c90000;
            }
            QPushButton {
                padding: 8px 15px;
                background-color: #c90000;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
                margin: 5px;
                min-width: 100px;
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
        """)
        
    def load_current_settings(self):
        """Load current auto-update settings from config."""
        try:
            import time
            from datetime import datetime
            
            settings = get_auto_update_settings()
            
            # Set checkbox
            self.enable_checkbox.setChecked(settings['enabled'])
            
            # Set frequency
            frequency = settings['frequency']
            if frequency == 'startup':
                self.startup_radio.setChecked(True)
            elif frequency == 'weekly':
                self.weekly_radio.setChecked(True)
            else:  # daily
                self.daily_radio.setChecked(True)

            # Update status labels
            current_version = get_ytdlp_version()
            self.current_version_label.setText(f"Current yt-dlp version: {current_version}")
            
            last_check = settings['last_check']
            if last_check > 0:
                last_check_time = datetime.fromtimestamp(last_check).strftime("%Y-%m-%d %H:%M:%S")
                self.last_check_label.setText(f"Last update check: {last_check_time}")
            else:
                self.last_check_label.setText("Last update check: Never")
            
            # Calculate next check time
            self.update_next_check_label()
            
            # Update UI state
            self.on_enable_toggled(settings['enabled'])
            
        except Exception as e:
            logger.error(f"Error loading auto-update settings: {e}")
            
    def update_next_check_label(self):
        """Update the next check label based on current settings."""
        try:
            if not self.enable_checkbox.isChecked():
                self.next_check_label.setText("Next check: Disabled")
                return
                
            import time
            from datetime import datetime, timedelta
            
            settings = get_auto_update_settings()
            last_check = settings['last_check']
            frequency = self.get_selected_frequency()
            
            if last_check == 0:
                self.next_check_label.setText("Next check: On next startup")
                return
            
            next_check_time = last_check
            if frequency == 'startup':
                next_check_time += 3600  # 1 hour
            elif frequency == 'daily':
                next_check_time += 86400  # 24 hours  
            elif frequency == 'weekly':
                next_check_time += 604800  # 7 days
                
            current_time = time.time()
            if next_check_time <= current_time:
                self.next_check_label.setText("Next check: Now (overdue)")
            else:
                next_check_datetime = datetime.fromtimestamp(next_check_time)
                self.next_check_label.setText(f"Next check: {next_check_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
                
        except Exception as e:
            self.next_check_label.setText("Next check: Error calculating")
            logger.error(f"Error calculating next check time: {e}")
    
    def on_enable_toggled(self, enabled):
        """Handle enable/disable checkbox toggle."""
        # Enable/disable frequency options
        for i in range(self.frequency_group.buttons().__len__()):
            self.frequency_group.button(i).setEnabled(enabled)
            
        self.update_next_check_label()
        
    def get_selected_frequency(self):
        """Get the selected frequency setting."""
        if self.startup_radio.isChecked():
            return 'startup'
        elif self.weekly_radio.isChecked():
            return 'weekly'
        else:
            return 'daily'
    
    def manual_check(self):
        """Perform a manual update check."""
        self.manual_check_btn.setEnabled(False)
        self.manual_check_btn.setText("🔄 Checking...")
        
        # Force an immediate update check
        def check_in_thread():
            try:
                result = check_and_update_ytdlp_auto()
                
                # Update UI in main thread
                from PySide6.QtCore import QTimer
                QTimer.singleShot(0, lambda: self.manual_check_finished(result))
            except Exception as e:
                logger.error(f"Error during manual check: {e}")
                QTimer.singleShot(0, lambda: self.manual_check_finished(False))
        
        # Run in separate thread to avoid blocking UI
        import threading
        threading.Thread(target=check_in_thread, daemon=True).start()
        
    def _create_styled_message_box(self, icon, title, text):
        """Create a styled QMessageBox that matches the app theme."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setWindowIcon(self.windowIcon())
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #15181b;
                color: #ffffff;
            }
            QMessageBox QLabel {
                color: #ffffff;
            }
            QMessageBox QPushButton {
                padding: 8px 15px;
                background-color: #c90000;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #a50000;
            }
            QMessageBox QPushButton:pressed {
                background-color: #800000;
            }
        """)
        return msg_box
        
    def manual_check_finished(self, success):
        """Handle completion of manual update check."""
        self.manual_check_btn.setEnabled(True)
        self.manual_check_btn.setText("🔍 Check for Updates Now")
        
        if success:
            msg_box = self._create_styled_message_box(
                QMessageBox.Information, 
                "Update Check",
                "✅ Update check completed successfully!\nCheck the console for details."
            )
            msg_box.exec()
        else:
            msg_box = self._create_styled_message_box(
                QMessageBox.Warning,
                "Update Check", 
                "❌ Update check failed.\nCheck the console for error details."
            )
            msg_box.exec()
        
        # Refresh the current settings display
        self.load_current_settings()
        
    def save_settings(self):
        """Save the auto-update settings."""
        try:
            enabled = self.enable_checkbox.isChecked()
            frequency = self.get_selected_frequency()
            
            if update_auto_update_settings(enabled, frequency):
                msg_box = self._create_styled_message_box(
                    QMessageBox.Information,
                    "Settings Saved",
                    "✅ Auto-update settings have been saved successfully!"
                )
                msg_box.exec()
                self.accept()
            else:
                msg_box = self._create_styled_message_box(
                    QMessageBox.Warning,
                    "Error",
                    "❌ Failed to save auto-update settings.\nPlease try again."
                )
                msg_box.exec()
        except Exception as e:
            logger.error(f"Error saving auto-update settings: {e}")
            msg_box = self._create_styled_message_box(
                QMessageBox.Critical,
                "Error",
                f"❌ Error saving settings: {str(e)}"
            )
            msg_box.exec()
