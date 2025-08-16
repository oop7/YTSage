"""
Selection dialogs for YTSage application.
Contains dialogs for selecting subtitles, playlist videos, and SponsorBlock categories.
"""

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QScrollArea, QWidget,
                             QCheckBox, QDialogButtonBox, QGroupBox)
from PySide6.QtCore import Qt


class SubtitleSelectionDialog(QDialog):
    def __init__(self, available_manual, available_auto, previously_selected, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Subtitles")
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)

        self.available_manual = available_manual
        self.available_auto = available_auto
        self.previously_selected = set(previously_selected)  # Use a set for quick lookups
        self.selected_subtitles = list(previously_selected)  # Initialize with previous selection

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Filter input
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Filter languages (e.g., en, es)...")
        self.filter_input.textChanged.connect(self.filter_list)
        self.filter_input.setStyleSheet("""
            QLineEdit {
                background-color: #363636;
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                padding: 5px;
                min-height: 30px;
                color: white;
            }
            QLineEdit:focus {
                border-color: #ff0000;
            }
        """)
        layout.addWidget(self.filter_input)

        # Scroll Area for the list
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")  # Remove border around scroll area
        layout.addWidget(scroll_area)

        # Container widget for list items (needed for scroll area)
        self.list_container = QWidget()
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(2)  # Compact spacing
        self.list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # Align items to top
        scroll_area.setWidget(self.list_container)

        # Populate the list initially
        self.populate_list()

        # OK and Cancel buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        # Style the buttons
        for button in button_box.buttons():
             button.setStyleSheet("""
                 QPushButton {
                     background-color: #363636;
                     border: 2px solid #3d3d3d;
                     border-radius: 4px;
                     padding: 5px 15px; /* Adjust padding */
                     min-height: 30px; /* Ensure consistent height */
                     color: white;
                 }
                 QPushButton:hover {
                     background-color: #444444;
                 }
                 QPushButton:pressed {
                     background-color: #555555;
                 }
             """)
             # Style the OK button specifically if needed
             if button_box.buttonRole(button) == QDialogButtonBox.ButtonRole.AcceptRole:
                 button.setStyleSheet(button.styleSheet() + "QPushButton { background-color: #ff0000; border-color: #cc0000; } QPushButton:hover { background-color: #cc0000; }")

        layout.addWidget(button_box)

    def populate_list(self, filter_text=""):
        # Clear existing checkboxes from layout
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        filter_text = filter_text.lower()
        combined_subs = {}

        # Add manual subs
        for lang_code, sub_info in self.available_manual.items():
             if not filter_text or filter_text in lang_code.lower():
                 combined_subs[lang_code] = f"{lang_code} - Manual"

        # Add auto subs (only if no manual exists and matches filter)
        for lang_code, sub_info in self.available_auto.items():
            if lang_code not in combined_subs:  # Don't overwrite manual
                 if not filter_text or filter_text in lang_code.lower():
                     combined_subs[lang_code] = f"{lang_code} - Auto-generated"

        if not combined_subs:
            no_subs_label = QLabel("No subtitles available" + (f" matching '{filter_text}'" if filter_text else ""))
            no_subs_label.setStyleSheet("color: #aaaaaa; padding: 10px;")
            self.list_layout.addWidget(no_subs_label)
            return

        # Sort by language code
        sorted_lang_codes = sorted(combined_subs.keys())

        for lang_code in sorted_lang_codes:
            item_text = combined_subs[lang_code]
            checkbox = QCheckBox(item_text)
            checkbox.setProperty("subtitle_id", item_text)  # Store the identifier
            checkbox.setChecked(item_text in self.previously_selected)  # Check if previously selected
            checkbox.stateChanged.connect(self.update_selection)
            checkbox.setStyleSheet("""
                 QCheckBox {
                     color: #ffffff;
                     padding: 5px;
                 }
                 QCheckBox::indicator {
                     width: 18px;
                     height: 18px;
                     border-radius: 4px; /* Square checkboxes */
                 }
                 QCheckBox::indicator:unchecked {
                     border: 2px solid #666666;
                     background: #2b2b2b;
                 }
                 QCheckBox::indicator:checked {
                     border: 2px solid #ff0000;
                     background: #ff0000;
                 }
             """)
            self.list_layout.addWidget(checkbox)

        self.list_layout.addStretch()  # Pushes items up if list is short

    def filter_list(self):
        self.populate_list(self.filter_input.text())

    def update_selection(self, state):
        sender = self.sender()
        subtitle_id = sender.property("subtitle_id")
        if state == Qt.CheckState.Checked.value:
            if subtitle_id not in self.previously_selected:
                self.previously_selected.add(subtitle_id)
        else:
            if subtitle_id in self.previously_selected:
                self.previously_selected.remove(subtitle_id)

    def get_selected_subtitles(self):
        # Return the final set as a list
        return list(self.previously_selected)

    def accept(self):
        # Update the final list before closing
        self.selected_subtitles = self.get_selected_subtitles()
        super().accept()


class PlaylistSelectionDialog(QDialog):
    def __init__(self, playlist_entries, previously_selected_string, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Playlist Videos")
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)  # Allow more vertical space

        self.playlist_entries = playlist_entries
        self.checkboxes = []

        # Main layout
        main_layout = QVBoxLayout(self)

        # Top buttons (Select/Deselect All)
        button_layout = QHBoxLayout()
        select_all_btn = QPushButton("Select All")
        deselect_all_btn = QPushButton("Deselect All")
        select_all_btn.clicked.connect(self._select_all)
        deselect_all_btn.clicked.connect(self._deselect_all)
        # Style the buttons to match the subtitle dialog
        select_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #363636;
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                padding: 5px 15px;
                min-height: 30px;
                color: white;
            }
            QPushButton:hover {
                background-color: #444444;
            }
            QPushButton:pressed {
                background-color: #555555;
            }
        """)
        deselect_all_btn.setStyleSheet(select_all_btn.styleSheet())
        button_layout.addWidget(select_all_btn)
        button_layout.addWidget(deselect_all_btn)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        # Scrollable area for checkboxes
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")  # Remove border around scroll area
        scroll_widget = QWidget()
        self.list_layout = QVBoxLayout(scroll_widget)  # Layout for checkboxes
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(2)  # Compact spacing
        self.list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # Align items to top
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)

        # Populate checkboxes
        self._populate_list(previously_selected_string)

        # Dialog buttons (OK/Cancel)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        # Style the buttons to match subtitle dialog
        for button in button_box.buttons():
            button.setStyleSheet("""
                QPushButton {
                    background-color: #363636;
                    border: 2px solid #3d3d3d;
                    border-radius: 4px;
                    padding: 5px 15px;
                    min-height: 30px;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #444444;
                }
                QPushButton:pressed {
                    background-color: #555555;
                }
            """)
            # Style the OK button specifically if needed
            if button_box.buttonRole(button) == QDialogButtonBox.ButtonRole.AcceptRole:
                button.setStyleSheet(button.styleSheet() + "QPushButton { background-color: #ff0000; border-color: #cc0000; } QPushButton:hover { background-color: #cc0000; }")
        
        main_layout.addWidget(button_box)

        # Apply styling to match subtitle dialog
        self.setStyleSheet("""
            QDialog { background-color: #15181b; }
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
                background: #2b2b2b;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #ff0000;
                background: #ff0000;
            }
            QWidget { background-color: #15181b; }
        """)

    def _parse_selection_string(self, selection_string):
        """Parses a yt-dlp playlist selection string (e.g., '1-3,5,7-9') into a set of 1-based indices."""
        selected_indices = set()
        if not selection_string:
            # If no previous selection, assume all are selected initially
            return set(range(1, len(self.playlist_entries) + 1))
        
        parts = selection_string.split(',')
        for part in parts:
            part = part.strip()
            if '-' in part:
                try:
                    start, end = map(int, part.split('-'))
                    if start <= end:
                        selected_indices.update(range(start, end + 1))
                except ValueError:
                    pass  # Ignore invalid ranges
            else:
                try:
                    selected_indices.add(int(part))
                except ValueError:
                    pass  # Ignore invalid numbers
        return selected_indices

    def _populate_list(self, previously_selected_string):
        """Populates the scroll area with checkboxes for each video."""
        selected_indices = self._parse_selection_string(previously_selected_string)
        
        # Clear existing checkboxes if any (e.g., if repopulating)
        while self.list_layout.count():
            child = self.list_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.checkboxes.clear()

        for index, entry in enumerate(self.playlist_entries):
            if not entry: 
                continue  # Skip None entries if yt-dlp returns them

            video_index = index + 1  # yt-dlp uses 1-based indexing
            title = entry.get('title', f'Video {video_index}')
            # Shorten title if too long
            display_title = (title[:70] + '...') if len(title) > 73 else title
            
            checkbox = QCheckBox(f"{video_index}. {display_title}")
            checkbox.setChecked(video_index in selected_indices)
            checkbox.setProperty("video_index", video_index)  # Store index
            checkbox.setStyleSheet("""
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
                    background: #2b2b2b;
                }
                QCheckBox::indicator:checked {
                    border: 2px solid #ff0000;
                    background: #ff0000;
                }
            """)
            self.list_layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)
        self.list_layout.addStretch()  # Push checkboxes to the top

    def _select_all(self):
        for checkbox in self.checkboxes:
            checkbox.setChecked(True)

    def _deselect_all(self):
        for checkbox in self.checkboxes:
            checkbox.setChecked(False)

    def _condense_indices(self, indices):
        """Condenses a list of 1-based indices into a yt-dlp selection string."""
        if not indices:
            return ""
        indices = sorted(list(set(indices)))
        if not indices:  # Check again after sorting/set conversion
            return ""
            
        ranges = []
        start = indices[0]
        end = indices[0]
        for i in range(1, len(indices)):
            if indices[i] == end + 1:
                end = indices[i]
            else:
                if start == end:
                    ranges.append(str(start))
                else:
                    ranges.append(f"{start}-{end}")
                start = indices[i]
                end = indices[i]
        # Add the last range
        if start == end:
            ranges.append(str(start))
        else:
            ranges.append(f"{start}-{end}")
        return ",".join(ranges)

    def get_selected_items_string(self):
        """Returns the selection string based on checked boxes."""
        selected_indices = [
            cb.property("video_index") for cb in self.checkboxes if cb.isChecked()
        ]
        
        # Check if all items are selected
        if len(selected_indices) == len(self.playlist_entries):
             return None  # yt-dlp default is all items, so return None or empty string

        return self._condense_indices(selected_indices)


class SponsorBlockCategoryDialog(QDialog):
    """Dialog for selecting SponsorBlock categories to remove from videos."""
    
    # Default SponsorBlock categories with descriptions
    SPONSORBLOCK_CATEGORIES = {
        'sponsor': {
            'name': 'Sponsor',
            'description': 'Paid promotion, paid referrals and direct advertisements',
            'default': True
        },
        'selfpromo': {
            'name': 'Unpaid/Self Promotion', 
            'description': 'Unpaid promotion of creators\' own content',
            'default': True
        },
        'interaction': {
            'name': 'Interaction Reminder',
            'description': 'Asking viewers to like, subscribe, or follow social media',
            'default': True
        },
        'intro': {
            'name': 'Intro',
            'description': 'Video introduction that can be skipped',
            'default': False
        },
        'outro': {
            'name': 'Outro/End Cards',
            'description': 'Credits or when the video ends',
            'default': False
        },
        'preview': {
            'name': 'Preview/Recap',
            'description': 'Quick recap of previous videos or preview of what\'s coming up',
            'default': False
        },
        'music_offtopic': {
            'name': 'Non-Music Section',
            'description': 'Only for music videos. Marks non-music sections',
            'default': False
        },
        'filler': {
            'name': 'Filler Tangent',
            'description': 'Tangential scenes added only for filler or humor',
            'default': False
        }
    }
    
    def __init__(self, previously_selected=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SponsorBlock Categories")
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        
        # Set the window icon to match the main app
        if parent:
            self.setWindowIcon(parent.windowIcon())
        
        self.previously_selected = set(previously_selected) if previously_selected else set()
        self.checkboxes = {}
        
        self.init_ui()
        self.apply_styling()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Title and description
        title_label = QLabel("SponsorBlock Categories")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff; margin: 10px;")
        layout.addWidget(title_label)
        
        desc_label = QLabel(
            "Select which types of video segments to automatically remove during download.\n"
            "SponsorBlock uses community-submitted data to identify these segments."
        )
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setStyleSheet("color: #cccccc; margin: 10px; font-size: 11px;")
        layout.addWidget(desc_label)
        
        # Scroll area for categories
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setContentsMargins(10, 0, 10, 0)
        scroll_layout.setSpacing(8)
        
        # Add category checkboxes
        for category_id, category_info in self.SPONSORBLOCK_CATEGORIES.items():
            # Create a container widget for each category
            category_widget = QWidget()
            category_layout = QVBoxLayout(category_widget)
            category_layout.setContentsMargins(0, 0, 0, 0)
            category_layout.setSpacing(2)
            
            # Create checkbox with just the name
            checkbox = QCheckBox(category_info['name'])
            checkbox.setProperty("category_id", category_id)
            
            # Determine if this category should be checked
            if self.previously_selected:
                # Use previously selected categories
                is_checked = category_id in self.previously_selected
            else:
                # Use default values for first time
                is_checked = category_info['default']
            
            checkbox.setChecked(is_checked)
            
            checkbox.setStyleSheet("""
                QCheckBox {
                    color: #ffffff;
                    padding: 4px;
                    spacing: 10px;
                    font-weight: bold;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                    border-radius: 4px;
                }
                QCheckBox::indicator:unchecked {
                    border: 2px solid #666666;
                    background: #2b2b2b;
                }
                QCheckBox::indicator:checked {
                    border: 2px solid #ff0000;
                    background: #ff0000;
                }
            """)
            
            # Create description label
            desc_label = QLabel(category_info['description'])
            desc_label.setStyleSheet("color: #aaaaaa; font-size: 11px; margin-left: 28px; margin-bottom: 8px;")
            desc_label.setWordWrap(True)
            
            category_layout.addWidget(checkbox)
            category_layout.addWidget(desc_label)
            
            self.checkboxes[category_id] = checkbox
            scroll_layout.addWidget(category_widget)
        
        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)
        
        # Quick selection buttons
        button_layout = QHBoxLayout()
        
        select_defaults_btn = QPushButton("Select Defaults")
        select_defaults_btn.clicked.connect(self.select_defaults)
        select_defaults_btn.setStyleSheet(self._get_button_style())
        
        select_all_btn = QPushButton("Select All")
        select_all_btn.clicked.connect(self.select_all)
        select_all_btn.setStyleSheet(self._get_button_style())
        
        deselect_all_btn = QPushButton("Deselect All")
        deselect_all_btn.clicked.connect(self.deselect_all)
        deselect_all_btn.setStyleSheet(self._get_button_style())
        
        button_layout.addWidget(select_defaults_btn)
        button_layout.addWidget(select_all_btn)
        button_layout.addWidget(deselect_all_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        # Style the dialog buttons
        for button in button_box.buttons():
            button.setStyleSheet(self._get_button_style())
            if button_box.buttonRole(button) == QDialogButtonBox.ButtonRole.AcceptRole:
                button.setStyleSheet(button.styleSheet() + 
                    "QPushButton { background-color: #ff0000; border-color: #cc0000; } " +
                    "QPushButton:hover { background-color: #cc0000; }")
        
        layout.addWidget(button_box)
    
    def _get_button_style(self):
        """Returns the standard button style for this dialog."""
        return """
            QPushButton {
                background-color: #363636;
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                padding: 5px 15px;
                min-height: 30px;
                color: white;
            }
            QPushButton:hover {
                background-color: #444444;
            }
            QPushButton:pressed {
                background-color: #555555;
            }
        """
    
    def apply_styling(self):
        """Apply the dialog styling to match the rest of the application."""
        self.setStyleSheet("""
            QDialog {
                background-color: #15181b;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
            QWidget {
                background-color: #15181b;
            }
        """)
    
    def select_defaults(self):
        """Select only the default categories."""
        for category_id, checkbox in self.checkboxes.items():
            default_value = self.SPONSORBLOCK_CATEGORIES[category_id]['default']
            checkbox.setChecked(default_value)
    
    def select_all(self):
        """Select all categories."""
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(True)
    
    def deselect_all(self):
        """Deselect all categories."""
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(False)
    
    def get_selected_categories(self):
        """Returns a list of selected category IDs."""
        selected = []
        for category_id, checkbox in self.checkboxes.items():
            if checkbox.isChecked():
                selected.append(category_id)
        return selected
    
    def get_selected_categories_string(self):
        """Returns a comma-separated string of selected categories for yt-dlp."""
        selected = self.get_selected_categories()
        return ','.join(selected) if selected else ''
