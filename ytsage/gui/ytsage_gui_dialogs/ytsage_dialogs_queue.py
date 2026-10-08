"""Download queue dialog."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from ...utils.ytsage_download_queue import DownloadQueue
from ...utils.ytsage_localization import _


class QueueDialog(QDialog):
    """Display queued jobs and provide queue actions."""

    start_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(_("queue.title"))
        self.setMinimumSize(600, 400)

        layout = QVBoxLayout(self)
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        buttons = QHBoxLayout()
        self.remove_button = QPushButton(_("queue.remove"))
        self.remove_button.clicked.connect(self.remove_selected)
        self.clear_button = QPushButton(_("queue.clear_finished"))
        self.clear_button.clicked.connect(self.clear_finished)
        self.start_button = QPushButton(_("queue.start"))
        self.start_button.clicked.connect(self.start_requested.emit)
        close_button = QPushButton(_("buttons.close"))
        close_button.clicked.connect(self.accept)
        buttons.addWidget(self.remove_button)
        buttons.addWidget(self.clear_button)
        buttons.addStretch()
        buttons.addWidget(self.start_button)
        buttons.addWidget(close_button)
        layout.addLayout(buttons)
        self.refresh()

    def refresh(self) -> None:
        self.list_widget.clear()
        jobs = DownloadQueue.get_all()
        if not jobs:
            self.list_widget.addItem(QListWidgetItem(_("queue.empty")))
            self.remove_button.setEnabled(False)
            return
        for job in jobs:
            title = job.get("title") or job.get("url", _("queue.untitled"))
            status = _(f"queue.status_{job.get('status', 'queued')}")
            item = QListWidgetItem(f"{status}: {title}")
            item.setData(32, job.get("id"))
            self.list_widget.addItem(item)
        self.remove_button.setEnabled(True)

    def remove_selected(self) -> None:
        item = self.list_widget.currentItem()
        job_id = item.data(32) if item else None
        if job_id:
            DownloadQueue.remove(job_id)
            self.refresh()

    def clear_finished(self) -> None:
        DownloadQueue.clear_finished()
        self.refresh()
