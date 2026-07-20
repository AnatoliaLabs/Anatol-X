"""4. Sayfa: Önerilen/temel uygulamalar (gerçek apt kurulumu ile)."""

from __future__ import annotations

import json
import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from welcome_app.apt_installer import AptInstaller
from welcome_app.constants import APPS_JSON_PATH


def _load_apps() -> list[dict]:
    if not os.path.exists(APPS_JSON_PATH):
        return []
    try:
        with open(APPS_JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return []


class _AppRow(QFrame):
    """Tek bir önerilen uygulamayı ve kurulum butonunu temsil eder."""

    def __init__(self, app_data: dict, log_widget: QTextEdit, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.app_data = app_data
        self.log_widget = log_widget
        self._installer: AptInstaller | None = None

        self.setProperty("class", "card")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)

        icon_label = QLabel(app_data.get("icon", "📦"))
        icon_label.setStyleSheet("font-size: 20pt;")
        icon_label.setFixedWidth(36)
        layout.addWidget(icon_label)

        text_col = QVBoxLayout()
        title = QLabel(f"{app_data.get('name', '')}  ·  {app_data.get('category', '')}")
        title.setProperty("class", "cardTitle")
        text_col.addWidget(title)
        desc = QLabel(app_data.get("description", ""))
        desc.setProperty("class", "cardDescription")
        desc.setWordWrap(True)
        text_col.addWidget(desc)
        layout.addLayout(text_col, stretch=1)

        self.install_button = QPushButton("Kur")
        self.install_button.setObjectName("installButton")
        self.install_button.clicked.connect(self._on_install_clicked)
        layout.addWidget(self.install_button, alignment=Qt.AlignmentFlag.AlignVCenter)

    def _on_install_clicked(self) -> None:
        if self._installer is not None:
            return

        if not AptInstaller.is_available():
            QMessageBox.warning(
                self,
                "Kurulum Yapılamıyor",
                "'pkexec' veya 'apt-get' bulunamadı. Bu özellik yalnızca "
                "Debian tabanlı sistemlerde çalışır.",
            )
            return

        package = self.app_data.get("package", "")
        self.install_button.setEnabled(False)
        self.install_button.setText("Kuruluyor...")
        self.log_widget.show()
        self.log_widget.append(f"\n$ pkexec apt-get install -y {package}\n")

        self._installer = AptInstaller(package, self)
        self._installer.output_received.connect(self._append_log)
        self._installer.finished.connect(self._on_finished)
        self._installer.install()

    def _append_log(self, text: str) -> None:
        self.log_widget.moveCursor(self.log_widget.textCursor().MoveOperation.End)
        self.log_widget.insertPlainText(text)

    def _on_finished(self, success: bool, _exit_code: int) -> None:
        self.install_button.setEnabled(not success)
        self.install_button.setText("Kuruldu ✓" if success else "Tekrar Dene")
        self._installer = None


class AppsPage(QWidget):
    """Debian tabanlı dağıtım için önerilen uygulamaları listeler."""

    title = "Önerilen Uygulamalar"

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        heading = QLabel("Önerilen Uygulamalar")
        heading.setProperty("class", "pageTitle")
        layout.addWidget(heading)

        subtitle = QLabel(
            "İşinize yarayacağını düşündüğümüz bazı uygulamalar. 'Kur' butonuna "
            "basınca yönetici parolanız istenecek ve apt üzerinden kurulacaktır."
        )
        subtitle.setProperty("class", "pageSubtitle")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        list_container = QWidget()
        list_layout = QVBoxLayout(list_container)
        list_layout.setSpacing(10)
        list_layout.setContentsMargins(0, 0, 0, 0)

        self.log_widget = QTextEdit()
        self.log_widget.setObjectName("logOutput")
        self.log_widget.setReadOnly(True)
        self.log_widget.setFixedHeight(110)
        self.log_widget.hide()

        for app_data in _load_apps():
            list_layout.addWidget(_AppRow(app_data, self.log_widget))

        list_layout.addStretch(1)
        scroll.setWidget(list_container)
        layout.addWidget(scroll, stretch=1)
        layout.addWidget(self.log_widget)
