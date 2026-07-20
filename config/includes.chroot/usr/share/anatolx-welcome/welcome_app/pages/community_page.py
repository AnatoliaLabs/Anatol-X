"""5. Sayfa: Topluluk ve destek bağlantıları."""

from __future__ import annotations

import json
import os

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from welcome_app.constants import LINKS_JSON_PATH


def _load_links() -> list[dict]:
    if not os.path.exists(LINKS_JSON_PATH):
        return []
    try:
        with open(LINKS_JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return []


class _LinkCard(QFrame):
    """Tek bir topluluk/destek bağlantısı kartı."""

    def __init__(self, link_data: dict, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("class", "card")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(8)

        title = QLabel(f"{link_data.get('icon', '🔗')}  {link_data.get('name', '')}")
        title.setProperty("class", "cardTitle")
        layout.addWidget(title)

        desc = QLabel(link_data.get("description", ""))
        desc.setProperty("class", "cardDescription")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        url = link_data.get("url", "")
        button = QPushButton("Aç")
        button.setObjectName("installButton")
        button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(url)))
        layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignRight)


class CommunityPage(QWidget):
    """Forum, Discord, Telegram, Matrix, GitHub gibi bağlantıları listeler."""

    title = "Topluluk ve Destek"

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        heading = QLabel("Topluluğumuza Katılın")
        heading.setProperty("class", "pageTitle")
        layout.addWidget(heading)

        subtitle = QLabel(
            "Sorularınız için topluluğumuzla iletişime geçin, gelişmeleri takip edin."
        )
        subtitle.setProperty("class", "pageSubtitle")
        layout.addWidget(subtitle)

        grid_container = QWidget()
        grid = QGridLayout(grid_container)
        grid.setHorizontalSpacing(14)
        grid.setVerticalSpacing(14)

        for index, link_data in enumerate(_load_links()):
            row, col = divmod(index, 2)
            grid.addWidget(_LinkCard(link_data), row, col)

        layout.addWidget(grid_container)
        layout.addStretch(1)
