"""
Settings-related dialogs for YTSage application.
Contains dialogs for configuring download settings.
"""

import threading
import time
from datetime import datetime

import requests
from packaging import version as version_parser
from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)

from ..ytsage_smooth_tab_widget import SmoothTabWidget
from ...utils.ytsage_logger import logger
from ...utils.ytsage_localization import _
from ...utils.ytsage_config_manager import ConfigManager
from ...utils.ytsage_constants import APP_LOG_DIR


class DownloadSettingsDialog(QDialog):
    def __init__(self, current_path, current_limit, current_unit_index, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle(_("settings.title"))
        self.setMinimumWidth(550)
        self.setMinimumHeight(400)
        self.current_path = current_path
        self.current_limit = current_limit if current_limit is not None else ""
        self.current_unit_index = current_unit_index

        # Apply main app styling
        self.setStyleSheet(
            """
            QDialog {
                background-color: #15181b;
            }
            QFrame#tabContent { 
                border: 1px solid #3d3d3d;
                background-color: #15181b;
            }
            QTabBar::tab {
                background-color: #1d1e22;
                color: #ffffff;
                padding: 8px 12px;
                border: 1px solid #3d3d3d;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #c90000;
            }
            QTabBar::tab:hover:!selected {
                background-color: #2a2d36;
            }
            QWidget {
                background-color: #15181b;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
            QGroupBox {
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                margin-top: 1.5ex;
                color: #ffffff;
                padding: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
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
                background: #1d1e22;
                border-radius: 9px;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #c90000;
                background: #c90000;
                border-radius: 9px;
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
                background: #1d1e22;
                border-radius: 9px;
            }
            QRadioButton::indicator:checked {
                border: 2px solid #c90000;
                background: #c90000;
                border-radius: 9px;
            }
            QComboBox {
                padding: 8px;
                border: 2px solid #1b2021;
                border-radius: 4px;
                background-color: #1b2021;
                color: #ffffff;
                min-width: 150px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                border: none;
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                background-color: #1d1e22;
                color: #ffffff;
                border: 1px solid #3d3d3d;
                selection-background-color: #c90000;
            }
        """
        )

        layout = QVBoxLayout(self)

        # Create tab widget
        self.tab_widget = SmoothTabWidget()
        layout.addWidget(self.tab_widget)

        # === General Tab ===
        general_tab = QWidget()
        general_layout = QVBoxLayout(general_tab)

        # --- Download Path Section ---
        path_group_box = QGroupBox(_("settings.download_path"))
        path_layout = QVBoxLayout()

        self.path_display = QLabel(str(self.current_path))
        self.path_display.setWordWrap(True)
        self.path_display.setStyleSheet(
            "QLabel { color: #ffffff; padding: 5px; border: 1px solid #1b2021; border-radius: 4px; background-color: #1b2021; }"
        )
        path_layout.addWidget(self.path_display)

                
        browse_button = QPushButton(_("settings.browse"))
        browse_button.clicked.connect(self.browse_new_path)
        path_layout.addWidget(browse_button)

        path_group_box.setLayout(path_layout)
        general_layout.addWidget(path_group_box)

        # --- Speed Limit Section ---
        speed_group_box = QGroupBox(_("settings.speed_limit"))
        speed_layout = QHBoxLayout()

        self.speed_limit_input = QLineEdit(str(self.current_limit))
        self.speed_limit_input.setPlaceholderText(_("settings.speed_limit_placeholder"))
        speed_layout.addWidget(self.speed_limit_input)

        self.speed_limit_unit = QComboBox()
        self.speed_limit_unit.addItems(["KB/s", "MB/s"])
        self.speed_limit_unit.setCurrentIndex(self.current_unit_index)
        speed_layout.addWidget(self.speed_limit_unit)

        speed_group_box.setLayout(speed_layout)
        general_layout.addWidget(speed_group_box)

        # --- Connections Section ---
        connections_group_box = QGroupBox(_("settings.concurrent_fragments", default="Concurrent Connections"))
        connections_layout = QVBoxLayout()

        self.connections_enabled = ConfigManager.get("concurrent_fragments") or 1

        connections_spin_layout = QHBoxLayout()
        self.connections_input = QComboBox()
        self.connections_input.addItems([str(i) for i in range(1, 21)])
        self.connections_input.setCurrentText(str(self.connections_enabled))
        connections_spin_layout.addWidget(self.connections_input)
        connections_spin_layout.addStretch()
        connections_layout.addLayout(connections_spin_layout)

        connections_help_label = QLabel(_("settings.concurrent_fragments_help", default="Number of connections per download. Higher values bypass throttling but may cause temporary blocks if set too high. Default: 1."))
        connections_help_label.setWordWrap(True)
        connections_help_label.setStyleSheet("color: #cccccc; margin: 5px; font-size: 11px;")
        connections_layout.addWidget(connections_help_label)

        connections_group_box.setLayout(connections_layout)
        general_layout.addWidget(connections_group_box)

        # --- Generic Mode Section ---
        generic_mode_group_box = QGroupBox(_("settings.generic_mode"))
        generic_mode_layout = QVBoxLayout()

        self.generic_mode_enabled = ConfigManager.get("generic_mode") or False

        self.generic_mode_checkbox = QCheckBox(_("settings.enable_generic_mode"))
        self.generic_mode_checkbox.setChecked(self.generic_mode_enabled)
        generic_mode_layout.addWidget(self.generic_mode_checkbox)

        generic_mode_help_label = QLabel(_("settings.generic_mode_help"))
        generic_mode_help_label.setWordWrap(True)
        generic_mode_help_label.setStyleSheet("color: #cccccc; margin: 5px; font-size: 11px;")
        generic_mode_layout.addWidget(generic_mode_help_label)

        generic_mode_group_box.setLayout(generic_mode_layout)
        general_layout.addWidget(generic_mode_group_box)
        general_layout.addStretch()

        # === Format Tab ===
        format_tab = QWidget()
        format_layout = QVBoxLayout(format_tab)

        # --- Output Format Settings Section ---
        output_format_group_box = QGroupBox(_("settings.output_format_settings"))
        output_format_layout = QVBoxLayout()

        # Load current format settings from ConfigManager
        self.force_format_enabled = ConfigManager.get("force_output_format") or False
        self.preferred_format_value = ConfigManager.get("preferred_output_format") or "mp4"

        # Enable/Disable force output format checkbox
        self.force_format_checkbox = QCheckBox(_("settings.force_output_format"))
        self.force_format_checkbox.setChecked(self.force_format_enabled)
        output_format_layout.addWidget(self.force_format_checkbox)

        # Format selection layout
        format_select_layout = QHBoxLayout()
        format_label = QLabel(_("settings.preferred_format"))
        format_label.setStyleSheet("color: #ffffff; margin-top: 5px;")
        format_select_layout.addWidget(format_label)

        self.format_combo = QComboBox()
        self.format_combo.addItems([
            _("settings.format_mp4"),
            _("settings.format_webm"),
            _("settings.format_mkv")
        ])
        # Set current selection based on saved format
        format_index_map = {"mp4": 0, "webm": 1, "mkv": 2}
        self.format_combo.setCurrentIndex(format_index_map.get(self.preferred_format_value, 0))
        format_select_layout.addWidget(self.format_combo)
        format_select_layout.addStretch()
        output_format_layout.addLayout(format_select_layout)

        # Help text
        help_label = QLabel(_("settings.force_format_help"))
        help_label.setWordWrap(True)
        help_label.setStyleSheet("color: #cccccc; margin: 5px; font-size: 11px;")
        output_format_layout.addWidget(help_label)

        output_format_group_box.setLayout(output_format_layout)
        format_layout.addWidget(output_format_group_box)

        # --- Audio Format Settings Section (for audio-only downloads) ---
        audio_format_group_box = QGroupBox(_("settings.audio_format_settings"))
        audio_format_layout = QVBoxLayout()

        # Load current audio format settings from ConfigManager
        self.force_audio_format_enabled = ConfigManager.get("force_audio_format") or False
        self.preferred_audio_format_value = ConfigManager.get("preferred_audio_format") or "best"
        self.audio_normalization_enabled = ConfigManager.get("audio_normalization") or False

        # Enable/Disable force audio format checkbox
        self.force_audio_format_checkbox = QCheckBox(_("settings.force_audio_format"))
        self.force_audio_format_checkbox.setChecked(self.force_audio_format_enabled)
        audio_format_layout.addWidget(self.force_audio_format_checkbox)

        # Enable/Disable audio normalization checkbox
        self.audio_normalization_checkbox = QCheckBox(_("settings.audio_normalization", default="Audio Normalization"))
        self.audio_normalization_checkbox.setChecked(self.audio_normalization_enabled)
        audio_format_layout.addWidget(self.audio_normalization_checkbox)

        # Audio normalization help text
        audio_norm_help_label = QLabel(_("settings.audio_normalization_help", default="When enabled, audio will be normalized using EBU R128 standard."))
        audio_norm_help_label.setWordWrap(True)
        audio_norm_help_label.setStyleSheet("color: #cccccc; margin: 5px; font-size: 11px;")
        audio_format_layout.addWidget(audio_norm_help_label)

        # Audio format selection layout
        audio_format_select_layout = QHBoxLayout()
        audio_format_label = QLabel(_("settings.preferred_audio_format"))
        audio_format_label.setStyleSheet("color: #ffffff; margin-top: 5px;")
        audio_format_select_layout.addWidget(audio_format_label)

        self.audio_format_combo = QComboBox()
        self.audio_format_combo.addItems([
            _("settings.audio_format_best"),
            _("settings.audio_format_aac"),
            _("settings.audio_format_mp3"),
            _("settings.audio_format_flac"),
            _("settings.audio_format_wav"),
            _("settings.audio_format_opus"),
            _("settings.audio_format_m4a"),
            _("settings.audio_format_vorbis")
        ])
        # Set current selection based on saved format
        audio_format_index_map = {"best": 0, "aac": 1, "mp3": 2, "flac": 3, "wav": 4, "opus": 5, "m4a": 6, "vorbis": 7}
        self.audio_format_combo.setCurrentIndex(audio_format_index_map.get(self.preferred_audio_format_value, 0))
        audio_format_select_layout.addWidget(self.audio_format_combo)
        audio_format_select_layout.addStretch()
        audio_format_layout.addLayout(audio_format_select_layout)

        # Help text for audio format
        audio_help_label = QLabel(_("settings.force_audio_format_help"))
        audio_help_label.setWordWrap(True)
        audio_help_label.setStyleSheet("color: #cccccc; margin: 5px; font-size: 11px;")
        audio_format_layout.addWidget(audio_help_label)

        # Connect signals
        self.audio_normalization_checkbox.stateChanged.connect(self._on_audio_normalization_toggled)
        self.force_audio_format_checkbox.stateChanged.connect(self._on_force_audio_format_toggled)

        audio_format_group_box.setLayout(audio_format_layout)
        format_layout.addWidget(audio_format_group_box)

        # --- Default Quality and Subtitles Section ---
        defaults_group_box = QGroupBox(_("settings.defaults_settings", default="Default Selection Settings"))
        defaults_layout = QVBoxLayout()
        
        # Default Video Quality
        vid_qual_layout = QHBoxLayout()
        vid_qual_label = QLabel(_("settings.default_video_quality", default="Default Video Resolution (Height):"))
        vid_qual_label.setStyleSheet("color: #ffffff; margin-top: 5px;")
        self.default_vid_qual_input = QLineEdit(str(ConfigManager.get("default_video_quality") or ""))
        self.default_vid_qual_input.setPlaceholderText("e.g. 1080 or 720")
        vid_qual_layout.addWidget(vid_qual_label)
        vid_qual_layout.addWidget(self.default_vid_qual_input)
        defaults_layout.addLayout(vid_qual_layout)

        # Default Subtitles
        sub_layout = QHBoxLayout()
        sub_label = QLabel(_("settings.default_subtitle_language", default="Default Subtitle Language(s):"))
        sub_label.setStyleSheet("color: #ffffff; margin-top: 5px;")
        self.default_sub_input = QLineEdit(ConfigManager.get("default_subtitle_language") or "")
        self.default_sub_input.setPlaceholderText("e.g. en, es")
        sub_layout.addWidget(sub_label)
        sub_layout.addWidget(self.default_sub_input)
        defaults_layout.addLayout(sub_layout)

        defaults_help = QLabel(_("settings.defaults_help", default="Set your preferred video height and subtitle languages (comma-separated). They will be auto-selected if available."))
        defaults_help.setWordWrap(True)
        defaults_help.setStyleSheet("color: #cccccc; margin: 5px; font-size: 11px;")
        defaults_layout.addWidget(defaults_help)

        defaults_group_box.setLayout(defaults_layout)
        format_layout.addWidget(defaults_group_box)

        format_layout.addStretch()

        # === File Tab ===
        file_tab = QWidget()
        file_layout = QVBoxLayout(file_tab)

        # --- Filename Format Section ---
        filename_format_group_box = QGroupBox(_("settings.filename_format"))
        filename_layout = QVBoxLayout()
        
        # Load current filename format from ConfigManager
        self.filename_format_value = ConfigManager.get("filename_format") or "%(title)s_%(resolution)s_[%(id)s].%(ext)s"
        
        # Input and Reset Button Layout
        filename_input_layout = QHBoxLayout()

        self.filename_format_input = QLineEdit(self.filename_format_value)
        self.filename_format_input.setPlaceholderText("%(title)s_%(resolution)s_[%(id)s].%(ext)s")
        filename_input_layout.addWidget(self.filename_format_input)
        
        self.reset_format_button = QPushButton(_("buttons.reset"))
        self.reset_format_button.setFixedWidth(70)
        self.reset_format_button.clicked.connect(lambda: self.filename_format_input.setText("%(title)s_%(resolution)s_[%(id)s].%(ext)s"))
        filename_input_layout.addWidget(self.reset_format_button)

        filename_layout.addLayout(filename_input_layout)
        
        filename_help_label = QLabel(_("settings.filename_format_help"))
        filename_help_label.setWordWrap(True)
        filename_help_label.setStyleSheet("color: #cccccc; margin: 5px; font-size: 11px;")
        filename_layout.addWidget(filename_help_label)
        
        filename_format_group_box.setLayout(filename_layout)
        file_layout.addWidget(filename_format_group_box)
        file_layout.addStretch()

        # Add tabs to tab widget
        self.tab_widget.addTab(general_tab, _("settings.tab_general", default="General"))
        self.tab_widget.addTab(format_tab, _("settings.tab_format", default="Format"))
        self.tab_widget.addTab(file_tab, _("settings.tab_file", default="File"))

        # Dialog buttons (OK/Cancel)
        button_box = QDialogButtonBox()
        ok_button = button_box.addButton(_("buttons.ok"), QDialogButtonBox.ButtonRole.AcceptRole)
        cancel_button = button_box.addButton(_("buttons.cancel"), QDialogButtonBox.ButtonRole.RejectRole)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        # Style the buttons to look identical to Custom Options dialog
        for btn in [ok_button, cancel_button]:
            btn.setMinimumHeight(35)
            btn.setMinimumWidth(80)
            btn.setStyleSheet(
                """
                QPushButton {
                    padding: 8px 20px;
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
            )

        layout.addWidget(button_box)

    def _on_audio_normalization_toggled(self, state: int) -> None:
        """Handle logic when audio normalization is toggled."""
        if state == Qt.CheckState.Checked.value:
            # Normalization requires re-encoding, so we must force an audio format
            self.force_audio_format_checkbox.setChecked(True)
            
            # If 'Best (No conversion)' is selected, change it to MP3 to ensure re-encoding
            if self.audio_format_combo.currentIndex() == 0:
                self.audio_format_combo.setCurrentIndex(2)  # Index 2 is typically MP3

    def _on_force_audio_format_toggled(self, state: int) -> None:
        """Handle logic when force audio format is toggled."""
        if state == Qt.CheckState.Unchecked.value:
            # If re-encoding is disabled, normalization cannot happen
            self.audio_normalization_checkbox.setChecked(False)

    def browse_new_path(self) -> None:
        new_path = QFileDialog.getExistingDirectory(self, _("dialogs.select_folder"), str(self.current_path))
        if new_path:
            self.current_path = new_path
            self.path_display.setText(self.current_path)

    def get_selected_path(self) -> str:
        """Returns the confirmed path after the dialog is accepted."""
        return self.current_path

    def get_selected_speed_limit(self) -> str | None:
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

    def get_selected_unit_index(self) -> int:
        """Returns the index of the selected speed limit unit."""
        return self.speed_limit_unit.currentIndex()

    def get_force_format_enabled(self) -> bool:
        """Returns whether force output format is enabled."""
        return self.force_format_checkbox.isChecked()

    def get_generic_mode_enabled(self) -> bool:
        """Returns whether generic mode is enabled."""
        return self.generic_mode_checkbox.isChecked()

    def get_concurrent_fragments(self) -> int:
        """Returns the number of concurrent fragments."""
        try:
            return int(self.connections_input.currentText())
        except ValueError:
            return 1

    def get_preferred_format(self) -> str:
        """Returns the selected preferred format (lowercase)."""
        format_map = {0: "mp4", 1: "webm", 2: "mkv"}
        return format_map.get(self.format_combo.currentIndex(), "mp4")

    def get_force_audio_format_enabled(self) -> bool:
        """Returns whether force audio format is enabled."""
        return self.force_audio_format_checkbox.isChecked()

    def get_preferred_audio_format(self) -> str:
        """Returns the selected preferred audio format (lowercase)."""
        audio_format_map = {0: "best", 1: "aac", 2: "mp3", 3: "flac", 4: "wav", 5: "opus", 6: "m4a", 7: "vorbis"}
        return audio_format_map.get(self.audio_format_combo.currentIndex(), "best")

    def get_audio_normalization_enabled(self) -> bool:
        """Returns whether audio normalization is enabled."""
        return self.audio_normalization_checkbox.isChecked()

    def get_filename_format(self) -> str:
        """Returns the filename format string."""
        return self.filename_format_input.text().strip()

    def _create_styled_message_box(self, icon, title, text) -> QMessageBox:
        """Create a styled QMessageBox that matches the app theme."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setWindowIcon(self.windowIcon())
        msg_box.setStyleSheet(
            """
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
        """
        )
        return msg_box

    def accept(self) -> None:
        """Override accept to save format settings."""
        try:
            ConfigManager.set("generic_mode", self.get_generic_mode_enabled())
            ConfigManager.set("concurrent_fragments", self.get_concurrent_fragments())

            # Save output format settings
            force_format = self.get_force_format_enabled()
            preferred_format = self.get_preferred_format()
            ConfigManager.set("force_output_format", force_format)
            ConfigManager.set("preferred_output_format", preferred_format)

            # Save audio format settings
            force_audio_format = self.get_force_audio_format_enabled()
            preferred_audio_format = self.get_preferred_audio_format()
            audio_normalization = self.get_audio_normalization_enabled()
            ConfigManager.set("force_audio_format", force_audio_format)
            ConfigManager.set("preferred_audio_format", preferred_audio_format)
            ConfigManager.set("audio_normalization", audio_normalization)

            # Save defaults
            default_vid = self.default_vid_qual_input.text().strip()
            ConfigManager.set("default_video_quality", default_vid if default_vid else None)
            default_sub = self.default_sub_input.text().strip()
            ConfigManager.set("default_subtitle_language", default_sub if default_sub else None)

            # Save filename format
            filename_format = self.get_filename_format()
            if filename_format:
                ConfigManager.set("filename_format", filename_format)

            QMessageBox.information(
                self,
                _("settings.settings_saved_title"),
                _("settings.settings_saved_message"),
            )
        except Exception as e:
            QMessageBox.critical(self, _("settings.error_title"), _("settings.error_saving_settings", error=str(e)))

        # Call the parent accept method to close the dialog
        super().accept()


class AutoUpdateSettingsDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle(_("settings.auto_update_title"))
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)

        # Set the window icon to match the main app
        if parent:
            self.setWindowIcon(parent.windowIcon())

        self.init_ui()
        self.load_current_settings()
        self.apply_styling()

    def init_ui(self) -> None:
        layout = QVBoxLayout(self)

        # Title
        title_label = QLabel(f"<h2>{_("settings.auto_update_header")}</h2>")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Description
        desc_label = QLabel(_("settings.auto_update_description"))
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setStyleSheet("color: #cccccc; margin: 10px; font-size: 11px;")
        layout.addWidget(desc_label)

        # Enable/Disable auto-update
        self.enable_checkbox = QCheckBox(_("settings.enable_auto_updates"))
        self.enable_checkbox.setChecked(True)  # Default enabled
        self.enable_checkbox.toggled.connect(self.on_enable_toggled)
        layout.addWidget(self.enable_checkbox)

        # Frequency options
        frequency_group = QGroupBox(_("settings.update_frequency_group"))
        frequency_layout = QVBoxLayout()

        self.frequency_group = QButtonGroup(self)

        self.startup_radio = QRadioButton(_("settings.check_startup"))
        self.daily_radio = QRadioButton(_("settings.check_daily"))
        self.weekly_radio = QRadioButton(_("settings.check_weekly"))

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
        status_group = QGroupBox(_("settings.current_status"))
        status_layout = QVBoxLayout()

        self.current_version_label = QLabel(_("settings.current_version_label"))
        self.last_check_label = QLabel(_("settings.last_check_label"))
        self.next_check_label = QLabel(_("settings.next_check_label"))

        status_layout.addWidget(self.current_version_label)
        status_layout.addWidget(self.last_check_label)
        status_layout.addWidget(self.next_check_label)
        status_group.setLayout(status_layout)

        layout.addWidget(status_group)

        # Manual check button
        self.manual_check_btn = QPushButton(_("settings.manual_check_button"))
        self.manual_check_btn.clicked.connect(self.manual_check)
        layout.addWidget(self.manual_check_btn)

        # Buttons
        button_layout = QHBoxLayout()

        self.save_btn = QPushButton(_("settings.save_settings"))
        self.save_btn.clicked.connect(self.save_settings)

        self.cancel_btn = QPushButton(_("buttons.cancel"))
        self.cancel_btn.clicked.connect(self.reject)

        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)

        layout.addLayout(button_layout)

    def apply_styling(self) -> None:
        self.setStyleSheet(
            """
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
        """
        )

    def load_current_settings(self) -> None:
        """Load current auto-update settings from config."""
        try:
            settings = get_auto_update_settings()

            # Set checkbox
            self.enable_checkbox.setChecked(settings["enabled"])

            # Set frequency
            frequency = settings["frequency"]
            if frequency == "startup":
                self.startup_radio.setChecked(True)
            elif frequency == "weekly":
                self.weekly_radio.setChecked(True)
            else:  # daily
                self.daily_radio.setChecked(True)

            # Update status labels
            current_version = get_ytdlp_version()
            self.current_version_label.setText(_("auto_update.current_version", version=current_version))

            last_check = settings["last_check"]
            if last_check > 0:
                last_check_time = datetime.fromtimestamp(last_check).strftime("%Y-%m-%d %H:%M:%S")
                self.last_check_label.setText(_("auto_update.last_check", time=last_check_time))
            else:
                self.last_check_label.setText(_("auto_update.last_check_never"))

            # Calculate next check time
            self.update_next_check_label()

            # Update UI state
            self.on_enable_toggled(settings["enabled"])

        except Exception as e:
            logger.exception(f"Error loading auto-update settings: {e}")

    def update_next_check_label(self) -> None:
        """Update the next check label based on current settings."""
        try:
            if not self.enable_checkbox.isChecked():
                self.next_check_label.setText(_("auto_update.next_check_disabled"))
                return

            settings = get_auto_update_settings()
            last_check = settings["last_check"]
            frequency = self.get_selected_frequency()

            if last_check == 0:
                self.next_check_label.setText(_("auto_update.next_check_startup"))
                return

            next_check_time = last_check
            if frequency == "startup":
                next_check_time += 3600  # 1 hour
            elif frequency == "daily":
                next_check_time += 86400  # 24 hours
            elif frequency == "weekly":
                next_check_time += 604800  # 7 days

            current_time = time.time()
            if next_check_time <= current_time:
                self.next_check_label.setText(_("auto_update.next_check_overdue"))
            else:
                next_check_datetime = datetime.fromtimestamp(next_check_time)
                self.next_check_label.setText(_("auto_update.next_check", time=next_check_datetime.strftime('%Y-%m-%d %H:%M:%S')))

        except Exception as e:
            self.next_check_label.setText(_("auto_update.next_check_error"))
            logger.exception(f"Error calculating next check time: {e}")

    def on_enable_toggled(self, enabled) -> None:
        """Handle enable/disable checkbox toggle."""
        # Enable/disable frequency options
        for i in range(self.frequency_group.buttons().__len__()):
            self.frequency_group.button(i).setEnabled(enabled)

        self.update_next_check_label()

    def get_selected_frequency(self) -> str:
        """Get the selected frequency setting."""
        if self.startup_radio.isChecked():
            return "startup"
        elif self.weekly_radio.isChecked():
            return "weekly"
        else:
            return "daily"

    def manual_check(self) -> None:
        """Perform a manual update check."""
        self.manual_check_btn.setEnabled(False)
        self.manual_check_btn.setText(_("auto_update.checking"))

        # Force an immediate update check
        def check_in_thread() -> None:
            try:
                result = check_and_update_ytdlp_auto()

                # Update UI in main thread
                QTimer.singleShot(0, lambda: self.manual_check_finished(result))
            except Exception as e:
                logger.exception(f"Error during manual check: {e}")
                QTimer.singleShot(0, lambda: self.manual_check_finished(False))

        # Run in separate thread to avoid blocking UI
        threading.Thread(target=check_in_thread, daemon=True).start()

    def _create_styled_message_box(self, icon, title, text) -> QMessageBox:
        """Create a styled QMessageBox that matches the app theme."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setWindowIcon(self.windowIcon())
        msg_box.setStyleSheet(
            """
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
        """
        )
        return msg_box

    def manual_check_finished(self, success) -> None:
        """Handle completion of manual update check."""
        self.manual_check_btn.setEnabled(True)
        self.manual_check_btn.setText(_("auto_update.check_now"))

        if success:
            msg_box = self._create_styled_message_box(
                QMessageBox.Icon.Information,
                "Update Check",
                "✅ Update check completed successfully!\nCheck the console for details.",
            )
            msg_box.exec()
        else:
            msg_box = self._create_styled_message_box(
                QMessageBox.Icon.Warning,
                "Update Check",
                "❌ Update check failed.\nCheck the console for error details.",
            )
            msg_box.exec()

        # Refresh the current settings display
        self.load_current_settings()

    def save_settings(self) -> None:
        """Save the auto-update settings."""
        try:
            enabled = self.enable_checkbox.isChecked()
            frequency = self.get_selected_frequency()

            if update_auto_update_settings(enabled, frequency):
                msg_box = self._create_styled_message_box(
                    QMessageBox.Icon.Information,
                    _("settings.settings_saved_title"),
                    _("settings.settings_saved_successfully"),
                )
                msg_box.exec()
                self.accept()
            else:
                msg_box = self._create_styled_message_box(
                    QMessageBox.Icon.Warning,
                    _("settings.error_title"),
                    _("settings.failed_save_settings"),
                )
                msg_box.exec()
        except Exception as e:
            logger.exception(f"Error saving auto-update settings: {e}")
            msg_box = self._create_styled_message_box(QMessageBox.Icon.Critical, _("settings.error_title"), _("settings", "error_saving", error=str(e)))
            msg_box.exec()
