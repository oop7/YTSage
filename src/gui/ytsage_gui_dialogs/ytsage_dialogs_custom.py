"""
Custom functionality dialogs for YTSage application.
Contains dialogs for custom commands, cookies, time ranges, and other special features.
"""

import subprocess
import threading
from pathlib import Path
from typing import TYPE_CHECKING, cast

from PySide6.QtCore import Q_ARG, QMetaObject, QObject, Qt, Signal
from PySide6.QtWidgets import (
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
    QPlainTextEdit,
    QPushButton,
    QRadioButton,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from src.core.ytsage_yt_dlp import get_yt_dlp_path
from src.core.ytsage_utils import update_auto_update_settings
from src.utils.ytsage_constants import YTDLP_DOCS_URL
from src.utils.ytsage_config_manager import ConfigManager
from src.utils.ytsage_localization import LocalizationManager, _
from src.utils.ytsage_logger import logger
from src.gui.ytsage_gui_dialogs.ytsage_dialogs_updater import UpdaterTabWidget

if TYPE_CHECKING:
    from src.gui.ytsage_gui_main import YTSageApp  # only for type hints (no runtime import)


class CommandWorker(QObject):
    """Worker class for running yt-dlp commands in a separate thread"""

    # Signals for communicating with the main thread
    output_received = Signal(str)  # For command output lines
    command_finished = Signal(bool, int)  # For completion (success, exit_code)
    error_occurred = Signal(str)  # For errors

    def __init__(self, command, url, path):
        super().__init__()
        self.command = command
        self.url = url
        self.path = path

    def run_command(self):
        """Run the yt-dlp command and emit signals for output"""
        try:
            # Split command into arguments
            args = self.command.split()

            # Build the full command
            yt_dlp_path = get_yt_dlp_path()
            base_cmd = [yt_dlp_path] + args

            # Add download path if specified
            if self.path:
                base_cmd.extend(["-P", self.path])

            # Add URL at the end
            base_cmd.append(self.url)

            # Emit the full command
            self.output_received.emit(_('custom_command.full_command', command=' '.join(str(cmd) for cmd in base_cmd)))
            self.output_received.emit("=" * 50)

            # Run the command
            proc = subprocess.Popen(
                base_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
            )

            # Stream output
            for line in proc.stdout:  # type: ignore[reportOptionalIterable]
                if line.strip():  # Only show non-empty lines
                    self.output_received.emit(line.rstrip())

            ret = proc.wait()
            self.output_received.emit("=" * 50)

            if ret != 0:
                self.output_received.emit(_('custom_command.command_failed', code=ret))
                self.command_finished.emit(False, ret)
            else:
                self.output_received.emit(_('custom_command.command_success'))
                self.command_finished.emit(True, ret)

        except Exception as e:
            self.output_received.emit("=" * 50)
            self.error_occurred.emit(_('custom_command.command_error', error=str(e)))


class CustomOptionsDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._parent: YTSageApp = cast("YTSageApp", self.parent())  # cast will help with auto complete and type hint checking.
        self.setWindowTitle(_("dialogs.custom_options"))
        self.setMinimumSize(550, 400)  # Made even shorter
        layout = QVBoxLayout(self)

        # Create tab widget to organize content
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # === Cookies Tab ===
        cookies_tab = QWidget()

        cookies_layout = QVBoxLayout(cookies_tab)

        # Help text
        help_text = QLabel(_('cookies.help_text'))
        help_text.setWordWrap(True)
        help_text.setStyleSheet("color: #999999; padding: 10px;")
        cookies_layout.addWidget(help_text)

        # Cookie source selection
        cookie_source_group = QGroupBox(_('cookies.cookie_source'))
        cookie_source_layout = QVBoxLayout(cookie_source_group)

        # Radio buttons for cookie source
        self.cookie_browser_radio = QRadioButton(_('cookies.extract_from_browser') + f" ({_('cookies.recommended')})")
        self.cookie_browser_radio.setChecked(True)
        self.cookie_browser_radio.toggled.connect(self.on_cookie_source_changed)
        cookie_source_layout.addWidget(self.cookie_browser_radio)

        self.cookie_file_radio = QRadioButton(_('cookies.use_cookie_file'))
        self.cookie_file_radio.toggled.connect(self.on_cookie_source_changed)
        cookie_source_layout.addWidget(self.cookie_file_radio)

        cookies_layout.addWidget(cookie_source_group)

        # Cookie file section
        self.cookie_file_group = QGroupBox(_('cookies.cookie_file'))
        file_layout = QVBoxLayout(self.cookie_file_group)

        # File path input and browse button
        path_layout = QHBoxLayout()
        self.cookie_path_input = QLineEdit()
        self.cookie_path_input.setPlaceholderText(_('cookies.cookie_file_placeholder'))
        if hasattr(self._parent, "cookie_file_path") and self._parent.cookie_file_path:
            # Convert Path to string properly and validate
            cookie_path_str = str(self._parent.cookie_file_path)
            # Only set if it looks like a valid path (more than just a drive letter)
            if len(cookie_path_str) > 3 and not cookie_path_str.endswith(":"):
                self.cookie_path_input.setText(cookie_path_str)
        path_layout.addWidget(self.cookie_path_input)

        self.browse_button = QPushButton(_('buttons.browse'))
        self.browse_button.clicked.connect(self.browse_cookie_file)
        path_layout.addWidget(self.browse_button)
        file_layout.addLayout(path_layout)

        cookies_layout.addWidget(self.cookie_file_group)

        # Browser selection section
        self.cookie_browser_group = QGroupBox(_('cookies.browser_selection'))
        browser_layout = QVBoxLayout(self.cookie_browser_group)

        browser_help = QLabel(_('cookies.browser_help'))
        browser_help.setWordWrap(True)
        browser_help.setStyleSheet("color: #999999; font-size: 11px;")
        browser_layout.addWidget(browser_help)

        browser_select_layout = QHBoxLayout()
        browser_select_layout.addWidget(QLabel(_('cookies.browser_label')))

        self.browser_combo = QComboBox()
        self.browser_combo.addItems(["chrome", "firefox", "safari", "edge", "opera", "brave", "chromium", "vivaldi"])
        browser_select_layout.addWidget(self.browser_combo)
        browser_layout.addLayout(browser_select_layout)

        # Optional profile field
        profile_layout = QHBoxLayout()
        profile_layout.addWidget(QLabel(_('cookies.profile_label')))
        self.profile_input = QLineEdit()
        self.profile_input.setPlaceholderText(_('cookies.profile_placeholder'))
        profile_layout.addWidget(self.profile_input)
        browser_layout.addLayout(profile_layout)

        cookies_layout.addWidget(self.cookie_browser_group)

        # Initially show browser group (recommended default) and hide file group
        self.cookie_file_group.setVisible(False)
        self.cookie_browser_group.setVisible(True)

        # Apply button and status indicator
        apply_layout = QHBoxLayout()
        
        # Status indicator for active cookies
        self.cookies_active_status = QLabel()
        self._update_cookies_active_status()
        apply_layout.addWidget(self.cookies_active_status)
        
        apply_layout.addStretch()
        
        # Apply button
        self.apply_cookies_btn = QPushButton(_('buttons.apply'))
        self.apply_cookies_btn.clicked.connect(self.apply_cookies)
        self.apply_cookies_btn.setStyleSheet(
            """
            QPushButton {
                padding: 8px 20px;
                background-color: #c90000;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #a50000;
            }
        """
        )
        apply_layout.addWidget(self.apply_cookies_btn)
        
        cookies_layout.addLayout(apply_layout)

        cookies_layout.addStretch()

        # === Custom Command Tab ===
        command_tab = QWidget()
        command_layout = QVBoxLayout(command_tab)

        # Improved help text
        cmd_help_text = QLabel(_('custom_command.help_text', docs_url=YTDLP_DOCS_URL))
        cmd_help_text.setWordWrap(True)
        cmd_help_text.setOpenExternalLinks(True)  # Enable clicking links
        cmd_help_text.setTextFormat(Qt.TextFormat.RichText)  # Enable HTML rendering
        cmd_help_text.setStyleSheet(
            """
            QLabel {
                color: #cccccc; 
                font-size: 12px; 
                padding: 10px; 
                background-color: #1a1d20; 
                border-radius: 6px; 
                line-height: 1.4;
            }
            QLabel a {
                color: #4da6ff;
                text-decoration: underline;
            }
            QLabel a:hover {
                color: #66b3ff;
            }
        """
        )
        command_layout.addWidget(cmd_help_text)

        # Command input label
        input_label = QLabel(_('custom_command.input_label'))
        input_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #ffffff; margin-top: 10px;")
        command_layout.addWidget(input_label)

        # Command input
        self.command_input = QPlainTextEdit()
        self.command_input.setPlaceholderText(_('custom_command.input_placeholder'))
        self.command_input.setMinimumHeight(80)  # Reduced further from 100
        self.command_input.setStyleSheet(
            """
            QPlainTextEdit {
                background-color: #1d1e22;
                color: #ffffff;
                border: 2px solid #2a2d36;
                border-radius: 6px;
                padding: 12px;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 13px;
                line-height: 1.4;
            }
            QPlainTextEdit:focus {
                border-color: #c90000;
            }
        """
        )
        command_layout.addWidget(self.command_input)

        # Button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        clear_btn = QPushButton(_('buttons.clear'))
        clear_btn.clicked.connect(lambda: self.command_input.clear())
        clear_btn.setStyleSheet(
            """
            QPushButton {
                padding: 8px 15px;
                background-color: #444444;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """
        )
        button_layout.addWidget(clear_btn)

        button_layout.addStretch()  # Push run button to the right

        # Run command button
        self.run_btn = QPushButton(_('buttons.run_command'))
        self.run_btn.clicked.connect(self.run_custom_command)
        self.run_btn.setDefault(True)
        button_layout.addWidget(self.run_btn)

        command_layout.addLayout(button_layout)

        # Output label
        output_label = QLabel(_('custom_command.output_label'))
        output_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #ffffff; margin-top: 15px;")
        command_layout.addWidget(output_label)

        # Log output
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setPlaceholderText(_('custom_command.output_placeholder'))
        self.log_output.setMinimumHeight(100)  # Reduced further from 120
        self.log_output.setStyleSheet(
            """
            QTextEdit {
                background-color: #1d1e22;
                color: #ffffff;
                border: 2px solid #2a2d36;
                border-radius: 6px;
                padding: 12px;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 12px;
            }
            QTextEdit:focus {
                border-color: #c90000;
            }
        """
        )
        command_layout.addWidget(self.log_output)

        # === Proxy Tab ===
        proxy_tab = QWidget()
        proxy_layout = QVBoxLayout(proxy_tab)

        # Help text
        proxy_help_text = QLabel(_('proxy.help_text'))
        proxy_help_text.setWordWrap(True)
        proxy_help_text.setStyleSheet("color: #999999; padding: 10px;")
        proxy_layout.addWidget(proxy_help_text)

        # Main Proxy section
        main_proxy_group = QGroupBox(_('proxy.main_proxy'))
        main_proxy_layout = QVBoxLayout(main_proxy_group)

        main_proxy_help = QLabel(_('proxy.main_proxy_help'))
        main_proxy_help.setWordWrap(True)
        main_proxy_help.setStyleSheet("color: #999999; font-size: 11px;")
        main_proxy_layout.addWidget(main_proxy_help)

        # Main proxy input
        main_proxy_input_layout = QHBoxLayout()
        main_proxy_input_layout.addWidget(QLabel(_('proxy.proxy_url_label')))
        self.proxy_url_input = QLineEdit()
        self.proxy_url_input.setPlaceholderText(_('proxy.proxy_url_placeholder'))
        self.proxy_url_input.textChanged.connect(self.validate_proxy_inputs)
        main_proxy_input_layout.addWidget(self.proxy_url_input)
        main_proxy_layout.addLayout(main_proxy_input_layout)

        # Example text
        example_label = QLabel(_('proxy.proxy_examples'))
        example_label.setStyleSheet("color: #888888; font-size: 10px; font-style: italic;")
        main_proxy_layout.addWidget(example_label)

        proxy_layout.addWidget(main_proxy_group)

        # Geo-verification Proxy section
        geo_proxy_group = QGroupBox(_('proxy.geo_proxy'))
        geo_proxy_layout = QVBoxLayout(geo_proxy_group)

        geo_proxy_help = QLabel(_('proxy.geo_proxy_help'))
        geo_proxy_help.setWordWrap(True)
        geo_proxy_help.setStyleSheet("color: #999999; font-size: 11px;")
        geo_proxy_layout.addWidget(geo_proxy_help)

        # Geo proxy input
        geo_proxy_input_layout = QHBoxLayout()
        geo_proxy_input_layout.addWidget(QLabel(_('proxy.geo_proxy_url_label')))
        self.geo_proxy_url_input = QLineEdit()
        self.geo_proxy_url_input.setPlaceholderText(_('proxy.geo_proxy_url_placeholder'))
        self.geo_proxy_url_input.textChanged.connect(self.validate_proxy_inputs)
        geo_proxy_input_layout.addWidget(self.geo_proxy_url_input)
        geo_proxy_layout.addLayout(geo_proxy_input_layout)

        proxy_layout.addWidget(geo_proxy_group)

        # Proxy status indicator
        self.proxy_status = QLabel("")
        self.proxy_status.setStyleSheet("color: #999999; font-style: italic;")
        proxy_layout.addWidget(self.proxy_status)

        # Clear buttons
        clear_layout = QHBoxLayout()
        clear_main_proxy_btn = QPushButton(_('proxy.clear_main_proxy'))
        clear_main_proxy_btn.clicked.connect(lambda: self.proxy_url_input.clear())
        clear_main_proxy_btn.setStyleSheet(
            """
            QPushButton {
                padding: 6px 12px;
                background-color: #444444;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """
        )
        clear_layout.addWidget(clear_main_proxy_btn)

        clear_geo_proxy_btn = QPushButton(_('proxy.clear_geo_proxy'))
        clear_geo_proxy_btn.clicked.connect(lambda: self.geo_proxy_url_input.clear())
        clear_geo_proxy_btn.setStyleSheet(
            """
            QPushButton {
                padding: 6px 12px;
                background-color: #444444;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """
        )
        clear_layout.addWidget(clear_geo_proxy_btn)

        clear_layout.addStretch()
        proxy_layout.addLayout(clear_layout)

        proxy_layout.addStretch()

        # === Language Tab ===
        language_tab = QWidget()
        language_layout = QVBoxLayout(language_tab)

        # Help text
        language_help_text = QLabel(_("language.select_language"))
        language_help_text.setWordWrap(True)
        language_help_text.setStyleSheet("color: #ffffff; font-size: 14px; font-weight: bold; padding: 10px;")
        language_layout.addWidget(language_help_text)

        # Current language info
        current_lang = ConfigManager.get("language") or "en"
        available_languages = LocalizationManager.get_available_languages()
        current_lang_display = available_languages.get(current_lang, current_lang.upper())
        
        current_lang_label = QLabel(_("language.current_language", language=current_lang_display))
        current_lang_label.setWordWrap(True)
        current_lang_label.setStyleSheet("color: #999999; padding: 10px;")
        language_layout.addWidget(current_lang_label)

        # Language selection group
        language_group = QGroupBox(_("language.select_language"))
        language_group_layout = QVBoxLayout(language_group)

        # Language selection combo box
        language_select_layout = QHBoxLayout()
        language_select_layout.addWidget(QLabel(_("language.select_language") + ":"))

        self.language_combo = QComboBox()
        
        # Populate language combo with available languages
        for lang_code, display_name in available_languages.items():
            self.language_combo.addItem(display_name, lang_code)
        
        # Set current selection
        current_index = self.language_combo.findData(current_lang)
        if current_index >= 0:
            self.language_combo.setCurrentIndex(current_index)

        # Connect language change event
        self.language_combo.currentIndexChanged.connect(self.on_language_changed)
        
        language_select_layout.addWidget(self.language_combo)
        language_group_layout.addLayout(language_select_layout)

        language_layout.addWidget(language_group)

        # Restart notice
        self.restart_notice = QLabel(_("language.restart_required"))
        self.restart_notice.setWordWrap(True)
        self.restart_notice.setStyleSheet(
            "color: #ffaa00; font-style: italic; padding: 10px; "
            "background-color: #2a2d36; border-radius: 6px; margin: 10px;"
        )
        self.restart_notice.setVisible(False)  # Initially hidden
        language_layout.addWidget(self.restart_notice)

        language_layout.addStretch()

        # === Updater Tab ===
        self.updater_tab = UpdaterTabWidget(self)

        # Add tabs to the tab widget
        self.tab_widget.addTab(cookies_tab, _("tabs.cookies"))
        self.tab_widget.addTab(command_tab, _("tabs.custom_command"))
        self.tab_widget.addTab(proxy_tab, _("tabs.proxy"))
        self.tab_widget.addTab(self.updater_tab, _("tabs.updater"))
        self.tab_widget.addTab(language_tab, _("tabs.language"))

        # Dialog buttons
        button_box = QDialogButtonBox()
        ok_button = button_box.addButton(_("buttons.ok"), QDialogButtonBox.ButtonRole.AcceptRole)
        cancel_button = button_box.addButton(_("buttons.cancel"), QDialogButtonBox.ButtonRole.RejectRole)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        # Apply global styles
        self.setStyleSheet(
            """
            QDialog {
                background-color: #15181b;
            }
            QTabWidget::pane { 
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
            QLabel {
                color: #ffffff;
            }
            QGroupBox {
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                margin-top: 1.5ex;
                color: #ffffff;
                padding: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
            }
            QRadioButton {
                color: #ffffff;
                padding: 5px;
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
            QLineEdit {
                padding: 8px;
                border: 2px solid #1b2021;
                border-radius: 4px;
                background-color: #1b2021;
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
        )

        # Initialize dialog with current settings (after all widgets and styles are set)
        self._initialize_cookie_settings()
        self._initialize_proxy_settings()

    def _initialize_cookie_settings(self) -> None:
        """Initialize the dialog with current cookie settings from config"""
        # Load saved cookie settings from ConfigManager
        saved_source = ConfigManager.get("cookie_source") or "browser"
        saved_browser = ConfigManager.get("cookie_browser") or "chrome"
        saved_profile = ConfigManager.get("cookie_browser_profile") or ""
        saved_file_path = ConfigManager.get("cookie_file_path")
        
        # Set the cookie source radio button
        if saved_source == "file":
            self.cookie_file_radio.setChecked(True)
        else:
            self.cookie_browser_radio.setChecked(True)
        
        # Set browser selection
        index = self.browser_combo.findText(saved_browser)
        if index >= 0:
            self.browser_combo.setCurrentIndex(index)
        
        # Set profile
        self.profile_input.setText(saved_profile)
        
        # Set file path if saved
        if saved_file_path:
            self.cookie_path_input.setText(str(saved_file_path))
        
        # Update visibility based on selection
        self.on_cookie_source_changed()
    
    def _update_cookies_active_status(self) -> None:
        """Update the status indicator showing if cookies are currently active"""
        if hasattr(self._parent, "browser_cookies_option") and self._parent.browser_cookies_option:
            self.cookies_active_status.setText(
                _("cookies.active_browser", browser=self._parent.browser_cookies_option)
            )
            self.cookies_active_status.setStyleSheet("color: #00cc00; font-weight: bold;")
        elif hasattr(self._parent, "cookie_file_path") and self._parent.cookie_file_path:
            self.cookies_active_status.setText(
                _("cookies.active_file", file=self._parent.cookie_file_path.name)
            )
            self.cookies_active_status.setStyleSheet("color: #00cc00; font-weight: bold;")
        else:
            self.cookies_active_status.setText(_("cookies.none_active"))
            self.cookies_active_status.setStyleSheet("color: #888888; font-style: italic;")

    def _initialize_proxy_settings(self) -> None:
        """Initialize the dialog with current proxy settings from config"""
        # Load proxy settings from config
        proxy_url = ConfigManager.get("proxy_url")
        geo_proxy_url = ConfigManager.get("geo_proxy_url")
        
        # Set proxy field values if they exist
        if proxy_url:
            self.proxy_url_input.setText(proxy_url)
        
        if geo_proxy_url:
            self.geo_proxy_url_input.setText(geo_proxy_url)
            
        # Update validation status
        self.validate_proxy_inputs()

    def on_cookie_source_changed(self) -> None:
        """Handle cookie source radio button changes"""
        if self.cookie_file_radio.isChecked():
            self.cookie_file_group.setVisible(True)
            self.cookie_browser_group.setVisible(False)
        else:
            self.cookie_file_group.setVisible(False)
            self.cookie_browser_group.setVisible(True)

    def apply_cookies(self) -> None:
        """Apply cookie settings when user clicks Apply button"""
        # Handle cookies
        cookie_path = self.get_cookie_file_path()
        browser_cookies = self.get_browser_cookies_option()

        # Clear both first to avoid conflicts
        self._parent.cookie_file_path = None
        self._parent.browser_cookies_option = None

        # Save settings to ConfigManager for persistence
        if self.cookie_file_radio.isChecked():
            ConfigManager.set("cookie_source", "file")
            ConfigManager.set("cookie_file_path", str(cookie_path) if cookie_path else None)
        else:
            ConfigManager.set("cookie_source", "browser")
            ConfigManager.set("cookie_browser", self.browser_combo.currentText())
            ConfigManager.set("cookie_browser_profile", self.profile_input.text().strip())

        if cookie_path:
            self._parent.cookie_file_path = cookie_path
            ConfigManager.set("cookie_active", True)
            logger.info(f"Applied cookie file: {self._parent.cookie_file_path}")
            QMessageBox.information(
                self,
                _("cookies.file_selected_title"),
                _("cookies.file_applied_message", path=str(cookie_path)),
            )
        elif browser_cookies:
            self._parent.browser_cookies_option = browser_cookies
            ConfigManager.set("cookie_active", True)
            logger.info(f"Applied browser cookies: {self._parent.browser_cookies_option}")
            QMessageBox.information(
                self,
                _("cookies.browser_selected_title"),
                _("cookies.browser_applied_message", browser=browser_cookies),
            )
        else:
            # Clear cookies
            ConfigManager.set("cookie_active", False)
            ConfigManager.set("cookie_source", "browser")  # Reset to default
            ConfigManager.set("cookie_file_path", None)
            logger.info("Cookies cleared")
            QMessageBox.information(
                self,
                _("cookies.cleared_title"),
                _("cookies.cleared_message"),
            )
        
        # Update the status indicator
        self._update_cookies_active_status()

    def browse_cookie_file(self) -> None:
        # Open file dialog to select cookie file
        selected_files, _filter = QFileDialog.getOpenFileName(self, _("cookies.select_file_title"), "", _("cookies.file_filter"))

        if selected_files:
            # Ensure we have a valid full path
            cookie_path = Path(selected_files).resolve()
            self.cookie_path_input.setText(str(cookie_path))

    def get_cookie_file_path(self) -> Path | None:
        # Return the selected cookie file path if it's not empty and using file mode
        if self.cookie_file_radio.isChecked():
            path_text = self.cookie_path_input.text().strip()
            if path_text:
                path = Path(path_text)
                if path.exists() and path.is_file():
                    return path
                else:
                    # File doesn't exist or is not a file - still return path for user feedback
                    return path if len(path_text) > 3 else None  # Avoid single letters like 'C'
        return None

    def get_browser_cookies_option(self) -> str | None:
        """Returns the --cookies-from-browser option string if browser mode is selected"""
        if self.cookie_browser_radio.isChecked():
            browser = self.browser_combo.currentText()
            profile = self.profile_input.text().strip()

            if profile:
                return f"{browser}:{profile}"
            else:
                return browser
        return None

    def is_using_browser_cookies(self) -> bool:
        """Returns True if browser cookies mode is selected"""
        return self.cookie_browser_radio.isChecked()
    
    def get_proxy_url(self) -> str | None:
        """Returns the main proxy URL if specified"""
        proxy_url = self.proxy_url_input.text().strip()
        return proxy_url if proxy_url else None

    def get_geo_proxy_url(self) -> str | None:
        """Returns the geo-verification proxy URL if specified"""
        geo_proxy_url = self.geo_proxy_url_input.text().strip()
        return geo_proxy_url if geo_proxy_url else None

    def validate_proxy_url(self, url: str) -> bool:
        """Basic validation for proxy URL format"""
        if not url:
            return True  # Empty is OK
        
        # Check if it starts with a valid scheme
        valid_schemes = ['http://', 'https://', 'socks5://', 'socks4://']
        if not any(url.lower().startswith(scheme) for scheme in valid_schemes):
            return False
        
        # Basic URL format check (contains at least host:port)
        try:
            # Remove the scheme to check host:port part
            for scheme in valid_schemes:
                if url.lower().startswith(scheme):
                    host_port = url[len(scheme):]
                    break
            
            # Skip user:pass@ part if present
            if '@' in host_port:
                host_port = host_port.split('@')[1]
            
            # Should have at least host:port
            if ':' in host_port:
                host, port = host_port.split(':', 1)
                if host and port.isdigit():
                    return True
            
            return False
        except:
            return False

    def validate_proxy_inputs(self) -> None:
        """Validate proxy inputs and update status"""
        main_proxy = self.proxy_url_input.text().strip()
        geo_proxy = self.geo_proxy_url_input.text().strip()
        
        if not main_proxy and not geo_proxy:
            # Check if there are saved settings
            saved_main = ConfigManager.get("proxy_url")
            saved_geo = ConfigManager.get("geo_proxy_url")
            
            if saved_main or saved_geo:
                status_parts = []
                if saved_main:
                    status_parts.append(_("proxy.saved_main", proxy=saved_main))
                if saved_geo:
                    status_parts.append(_("proxy.saved_geo", proxy=saved_geo))
                self.proxy_status.setText(" | ".join(status_parts))
                self.proxy_status.setStyleSheet("color: #888888; font-style: italic;")
            else:
                self.proxy_status.setText("")
            return
            
        issues = []
        
        if main_proxy and not self.validate_proxy_url(main_proxy):
            issues.append(_("proxy.invalid_main_url"))
            
        if geo_proxy and not self.validate_proxy_url(geo_proxy):
            issues.append(_("proxy.invalid_geo_url"))
        
        if issues:
            self.proxy_status.setText(" | ".join(issues))
            self.proxy_status.setStyleSheet("color: #ff6666; font-style: italic;")
        else:
            status_parts = []
            if main_proxy:
                status_parts.append(_("proxy.main_configured"))
            if geo_proxy:
                status_parts.append(_("proxy.geo_configured"))
            
            self.proxy_status.setText(" | ".join(status_parts))
            self.proxy_status.setStyleSheet("color: #00cc00; font-style: italic;")

    def run_custom_command(self) -> None:
        url = self._parent.url_input.text().strip()
        if not url:
            self.log_output.append(_("custom_command.error_no_url"))
            return

        command = self.command_input.toPlainText().strip()
        if not command:
            self.log_output.append(_("custom_command.error_no_command"))
            return

        # Get download path from parent
        path = self._parent.last_path

        self.log_output.clear()
        self.log_output.append(_("custom_command.executing"))
        self.log_output.append(_("custom_command.url_label", url=url))
        self.log_output.append(_("custom_command.args_label", command=command))
        if path:
            self.log_output.append(_("custom_command.download_path_label", path=path))
        self.log_output.append(_("custom_command.separator"))
        self.run_btn.setEnabled(False)
        self.run_btn.setText(_("command.running"))

        # Create worker and thread
        self.worker = CommandWorker(command, url, path)
        self.worker_thread = threading.Thread(target=self.worker.run_command, daemon=True)

        # Connect worker signals to our slots
        self.worker.output_received.connect(self.on_output_received)
        self.worker.command_finished.connect(self.on_command_finished)
        self.worker.error_occurred.connect(self.on_error_occurred)

        # Start the thread
        self.worker_thread.start()

    def on_output_received(self, text: str):
        """Slot for receiving output from the worker"""
        self.log_output.append(text)

    def on_command_finished(self, success: bool, exit_code: int):
        """Slot for when command finishes"""
        self.run_btn.setEnabled(True)
        self.run_btn.setText(_("command.run_command"))

    def on_error_occurred(self, error_msg: str):
        """Slot for handling errors"""
        self.log_output.append(error_msg)
        self.run_btn.setEnabled(True)
        self.run_btn.setText(_("buttons.run_command"))

    def on_language_changed(self) -> None:
        """Handle language selection change"""
        selected_lang_code = self.language_combo.currentData()
        if selected_lang_code:
            current_lang = ConfigManager.get("language") or "en"
            if selected_lang_code != current_lang:
                # Save the new language preference
                ConfigManager.set("language", selected_lang_code)
                
                # Update LocalizationManager
                LocalizationManager.set_language(selected_lang_code)
                
                # Show restart notice
                self.restart_notice.setVisible(True)
                
                logger.info(f"Language changed to: {selected_lang_code}")
    
    def accept(self) -> None:
        """Override accept to save auto-update settings from the updater tab."""
        logger.info("CustomOptionsDialog.accept() called")
        try:
            # Save auto-update settings from the updater tab
            enabled, frequency = self.updater_tab.get_auto_update_settings()
            logger.info(f"Saving auto-update settings: enabled={enabled}, frequency={frequency}")
            result = update_auto_update_settings(enabled, frequency)
            logger.info(f"Auto-update settings save result: {result}")
        except Exception as e:
            logger.exception(f"Error saving auto-update settings: {e}")
        
        # Call the parent accept method to close the dialog
        super().accept()


class TimeRangeDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle(_('time_range.title'))
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)

        # Help text explaining the feature
        help_text = QLabel(_('time_range.help_text'))
        help_text.setWordWrap(True)
        help_text.setStyleSheet("color: #999999; padding: 10px;")
        layout.addWidget(help_text)

        # Time range section
        time_group = QGroupBox(_('time_range.time_range_group'))
        time_layout = QVBoxLayout()

        # Start time row
        start_layout = QHBoxLayout()
        start_layout.addWidget(QLabel(_('time_range.start_time')))
        self.start_time_input = QLineEdit()
        self.start_time_input.setPlaceholderText(_('time_range.start_time_placeholder'))
        start_layout.addWidget(self.start_time_input)
        time_layout.addLayout(start_layout)

        # End time row
        end_layout = QHBoxLayout()
        end_layout.addWidget(QLabel(_('time_range.end_time')))
        self.end_time_input = QLineEdit()
        self.end_time_input.setPlaceholderText(_('time_range.end_time_placeholder'))
        end_layout.addWidget(self.end_time_input)
        time_layout.addLayout(end_layout)

        time_group.setLayout(time_layout)
        layout.addWidget(time_group)

        # Force keyframes option
        self.force_keyframes = QCheckBox(_('time_range.force_keyframes'))
        self.force_keyframes.setChecked(True)
        self.force_keyframes.setStyleSheet(
            """
            QCheckBox {
                color: #ffffff;
                padding: 5px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #666666;
                background: #1d1e22;
                border-radius: 4px;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #c90000;
                background: #c90000;
                border-radius: 4px;
            }
        """
        )
        layout.addWidget(self.force_keyframes)

        # Buttons
        button_box = QDialogButtonBox()
        ok_button = button_box.addButton(_("buttons.ok"), QDialogButtonBox.ButtonRole.AcceptRole)
        cancel_button = button_box.addButton(_("buttons.cancel"), QDialogButtonBox.ButtonRole.RejectRole)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        # Apply styling
        self.setStyleSheet(
            """
            QDialog {
                background-color: #15181b;
            }
            QGroupBox {
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                margin-top: 1.5ex;
                color: #ffffff;
                padding: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
            }
            QLabel {
                color: #ffffff;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #1b2021;
                border-radius: 4px;
                background-color: #1b2021;
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
        )

        # Initialize preview
        # self.update_preview() # Removed preview functionality

    def get_download_sections(self) -> str | None:
        """Returns the download sections command arguments or None if no selection made"""
        start = self.start_time_input.text().strip()
        end = self.end_time_input.text().strip()

        if not start and not end:
            return None  # No selection made

        if start and end:
            time_range = f"*{start}-{end}"
        elif start:
            time_range = f"*{start}-"
        elif end:
            time_range = f"*-{end}"
        else:
            return None  # Shouldn't happen but just in case

        return time_range

    def get_force_keyframes(self) -> bool:
        """Returns whether to force keyframes at cuts"""
        return self.force_keyframes.isChecked()
