"""Network and yt-dlp diagnostics dialog."""

import json
import subprocess
from pathlib import Path
from typing import Any

import requests
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from ...core.ytsage_yt_dlp import get_yt_dlp_path
from ...utils.ytsage_config_manager import ConfigManager
from ...utils.ytsage_localization import _
from ...utils.ytsage_logger import logger


YOUTUBE_TEST_URL = "https://youtu.be/7xz9s8cVFE4?si=dlDEz1Y7oDPBOmyf"
NETWORK_TIMEOUT = 15


def _request_proxies(proxy_url: str | None) -> dict[str, str] | None:
    return {"http": proxy_url, "https": proxy_url} if proxy_url else None


def _cookie_arguments() -> list[str]:
    """Return local cookie arguments without reading or exporting cookie data."""
    if ConfigManager.get("cookie_active") is not True:
        return []

    source = ConfigManager.get("cookie_source")
    if source == "file":
        path = ConfigManager.get("cookie_file_path")
        if path and Path(path).is_file():
            return ["--cookies", str(path)]
    elif source == "browser":
        browser = ConfigManager.get("cookie_browser")
        profile = ConfigManager.get("cookie_browser_profile")
        if browser:
            return ["--cookies-from-browser", f"{browser}:{profile}" if profile else str(browser)]
    return []


class DiagnosticsThread(QThread):
    status_update = Signal(str, bool, str)
    recommendation_ready = Signal(str)
    finished_signal = Signal()

    def __init__(self, url: str, proxy_url: str | None, geo_proxy_url: str | None) -> None:
        super().__init__()
        self.url = url
        self.proxy_url = proxy_url
        self.geo_proxy_url = geo_proxy_url

    def _request_test(self, proxy_url: str | None) -> tuple[bool, str]:
        try:
            response = requests.get(
                "https://www.youtube.com/generate_204",
                proxies=_request_proxies(proxy_url),
                timeout=NETWORK_TIMEOUT,
                allow_redirects=False,
            )
            if response.status_code in {200, 204, 301, 302}:
                return True, _("diagnostics.youtube_reachable", code=response.status_code)
            return False, _("diagnostics.youtube_http_error", code=response.status_code)
        except requests.RequestException as error:
            logger.debug("Diagnostics YouTube request failed: %s", error)
            return False, str(error)

    def _ip_test(self, proxy_url: str | None) -> tuple[bool, str]:
        try:
            response = requests.get(
                "https://ipwho.is/",
                proxies=_request_proxies(proxy_url),
                timeout=NETWORK_TIMEOUT,
            )
            response.raise_for_status()
            data: Any = response.json()
            if data.get("success") is False:
                return False, _("diagnostics.unavailable")
            ip = data.get("ip", _("diagnostics.unavailable"))
            country = data.get("country")
            return True, f"{ip} ({country})" if country else str(ip)
        except (requests.RequestException, ValueError) as error:
            logger.debug("Diagnostics public IP request failed: %s", error)
            return False, _("diagnostics.unavailable")

    def _ytdlp_test(self, proxy_url: str | None) -> tuple[bool, str]:
        command = [
            get_yt_dlp_path(),
            "--dump-single-json",
            "--skip-download",
            "--no-playlist",
            "--no-warnings",
            "--ignore-config",
            "--socket-timeout",
            str(NETWORK_TIMEOUT),
            "--retries",
            "1",
        ]
        if proxy_url:
            command.extend(["--proxy", proxy_url])
        command.extend(_cookie_arguments())
        command.append(self.url)

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=35,
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            logger.debug("Diagnostics yt-dlp test failed: %s", error)
            return False, str(error)

        if result.returncode != 0:
            error = (result.stderr or result.stdout).strip().splitlines()
            return False, error[-1] if error else _("diagnostics.no_details")

        try:
            data = json.loads(result.stdout)
            title = data.get("title") or _("diagnostics.unknown_title")
            return True, str(title)
        except (TypeError, ValueError):
            return False, _("diagnostics.invalid_ytdlp_output")

    def run(self) -> None:
        try:
            targets: list[tuple[str, str | None]] = [
                (_("diagnostics.direct_connection"), None),
            ]
            if self.proxy_url:
                targets.append((_("diagnostics.main_proxy"), self.proxy_url))
            if self.geo_proxy_url and self.geo_proxy_url != self.proxy_url:
                targets.append((_("diagnostics.geo_proxy"), self.geo_proxy_url))

            direct_reachable = False
            direct_ip_ok = False
            proxy_reachable = True
            for label, proxy_url in targets:
                reachable, detail = self._request_test(proxy_url)
                if label == _("diagnostics.direct_connection"):
                    direct_reachable = reachable
                    self.status_update.emit("connection", reachable, detail)
                ip_ok, ip = self._ip_test(proxy_url) if reachable else (False, _("diagnostics.unavailable"))
                if label == _("diagnostics.direct_connection"):
                    direct_ip_ok = ip_ok
                    self.status_update.emit("ip", ip_ok, ip)
                elif proxy_url:
                    proxy_reachable = proxy_reachable and reachable
            extraction_targets = [( _("diagnostics.direct_connection"), None)]
            if self.proxy_url:
                extraction_targets.append((_("diagnostics.main_proxy"), self.proxy_url))
            extraction_passed = False
            extraction_detail = _("diagnostics.no_details")
            for label, proxy_url in extraction_targets:
                passed, detail = self._ytdlp_test(proxy_url)
                if label == _("diagnostics.direct_connection"):
                    extraction_passed = passed
                    extraction_detail = detail
                    self.status_update.emit("extraction", passed, detail)
            recommendations: list[str] = []
            if not direct_reachable:
                recommendations.append(_("diagnostics.advice_direct_failed"))
            if self.proxy_url and not proxy_reachable:
                recommendations.append(_("diagnostics.advice_proxy_failed"))
            extraction_error = extraction_detail.lower()
            if not extraction_passed and any(
                keyword in extraction_error
                for keyword in ("sign in", "cookies", "not a bot", "authentication")
            ):
                recommendations.append(_("diagnostics.advice_cookies"))
            elif not extraction_passed:
                recommendations.append(_("diagnostics.advice_extraction_failed"))
            if not recommendations and direct_ip_ok and extraction_passed:
                recommendations.append(_("diagnostics.advice_all_ok"))

            self.recommendation_ready.emit("\n".join(recommendations))
        except Exception as error:
            logger.exception("Unexpected diagnostics failure: %s", error)
            self.recommendation_ready.emit(_("diagnostics.unexpected_error", error=error))
        finally:
            self.finished_signal.emit()


class NetworkDiagnosticsDialog(QDialog):
    """Run local connectivity checks and show actionable results."""

    def __init__(self, current_url: str = "", parent=None) -> None:
        super().__init__(parent)
        self.thread: DiagnosticsThread | None = None
        self.setWindowTitle(_("diagnostics.title"))
        self.setMinimumSize(680, 300)

        layout = QVBoxLayout(self)
        explanation = QLabel(_("diagnostics.explanation"))
        explanation.setWordWrap(True)
        layout.addWidget(explanation)

        layout.addWidget(QLabel(_("diagnostics.url_label")))
        self.url_input = QLineEdit(current_url or YOUTUBE_TEST_URL)
        self.url_input.setPlaceholderText(YOUTUBE_TEST_URL)
        layout.addWidget(self.url_input)

        status_layout = QVBoxLayout()
        self.status_labels: dict[str, QLabel] = {}
        for key, label_key in (
            ("connection", "diagnostics.connection_status"),
            ("ip", "diagnostics.ip_status"),
            ("extraction", "diagnostics.extraction_status"),
        ):
            label = QLabel(_(label_key, status=_("diagnostics.waiting")))
            label.setWordWrap(True)
            label.setProperty("status", "waiting")
            self.status_labels[key] = label
            status_layout.addWidget(label)
        layout.addLayout(status_layout)

        self.recommendations = QLabel()
        self.recommendations.setWordWrap(True)
        self.recommendations.setVisible(False)
        self.recommendations.setProperty("status", "advice")
        layout.addWidget(self.recommendations)

        button_layout = QHBoxLayout()
        self.run_button = QPushButton(_("diagnostics.run"))
        self.run_button.clicked.connect(self.run_diagnostics)
        button_layout.addWidget(self.run_button)
        button_layout.addStretch()
        close_button = QPushButton(_("buttons.close"))
        close_button.clicked.connect(self.reject)
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)

        self.setStyleSheet(
            """
            QDialog { background-color: #15181b; color: #ffffff; }
            QLabel { color: #cccccc; }
            QLineEdit {
                background-color: #1b2021; color: #ffffff;
                border: 1px solid #3d3d3d; border-radius: 4px; padding: 6px;
            }
            QLabel[status="waiting"] { color: #cccccc; }
            QLabel[status="pass"] {
                color: #77dd77; background-color: #17351f;
                border: 1px solid #2e8b57; border-radius: 4px; padding: 7px;
            }
            QLabel[status="fail"] {
                color: #ff7777; background-color: #3a1c1c;
                border: 1px solid #b33a3a; border-radius: 4px; padding: 7px;
            }
            QLabel[status="advice"] {
                color: #f0c674; background-color: #382f19;
                border: 1px solid #8a6d1d; border-radius: 4px; padding: 7px;
            }
            QPushButton {
                padding: 8px 15px; background-color: #c90000;
                border: none; border-radius: 4px; color: white; font-weight: bold;
            }
            QPushButton:disabled { background-color: #666666; color: #aaaaaa; }
            """
        )

    def run_diagnostics(self) -> None:
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, _("diagnostics.title"), _("diagnostics.url_required"))
            return

        self.run_button.setEnabled(False)
        self.recommendations.clear()
        self.recommendations.setVisible(False)
        for label in self.status_labels.values():
            label.setProperty("status", "waiting")
            label.style().unpolish(label)
            label.style().polish(label)
        self.thread = DiagnosticsThread(
            url,
            ConfigManager.get("proxy_url"),
            ConfigManager.get("geo_proxy_url"),
        )
        self.thread.status_update.connect(self.update_status)
        self.thread.recommendation_ready.connect(self.show_recommendations)
        self.thread.finished_signal.connect(self._diagnostics_finished)
        self.thread.start()

    def update_status(self, key: str, passed: bool, detail: str) -> None:
        label = self.status_labels.get(key)
        if label is None:
            return
        state = "pass" if passed else "fail"
        marker = _("diagnostics.pass_marker") if passed else _("diagnostics.fail_marker")
        label.setText(f"{label.text().split(':', 1)[0]}: {marker} — {detail}")
        label.setProperty("status", state)
        label.style().unpolish(label)
        label.style().polish(label)

    def show_recommendations(self, recommendations: str) -> None:
        self.recommendations.setText(
            f"{_('diagnostics.recommendations')}: {recommendations.replace(chr(10), ' ')}"
        )
        self.recommendations.setVisible(bool(recommendations))

    def _diagnostics_finished(self) -> None:
        self.run_button.setEnabled(True)

    def closeEvent(self, event) -> None:
        if self.thread and self.thread.isRunning():
            event.ignore()
            return
        super().closeEvent(event)
