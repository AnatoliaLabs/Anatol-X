"""Sayfalarda tekrar kullanılan küçük yardımcı widget'lar."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget


class Card(QFrame):
    """Köşeleri yuvarlatılmış, ince kenarlıklı basit bir kart konteyneri."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("class", "card")
        self.setFrameShape(QFrame.Shape.NoFrame)

    def setLayoutMargins(self, h: int = 16, v: int = 14) -> None:
        layout = self.layout()
        if layout is not None:
            layout.setContentsMargins(h, v, h, v)


def make_card_with_title(
    title: str, description: str = "", icon_text: str = ""
) -> Card:
    """Başlık + açıklama içeren standart bir kart üretir."""
    card = Card()
    card.setProperty("class", "card")
    outer = QHBoxLayout(card)
    outer.setContentsMargins(16, 14, 16, 14)
    outer.setSpacing(12)

    if icon_text:
        icon_label = QLabel(icon_text)
        icon_label.setStyleSheet("font-size: 22pt;")
        icon_label.setFixedWidth(40)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        outer.addWidget(icon_label)

    text_col = QVBoxLayout()
    text_col.setSpacing(4)
    title_label = QLabel(title)
    title_label.setProperty("class", "cardTitle")
    title_label.setWordWrap(True)
    text_col.addWidget(title_label)
    if description:
        desc_label = QLabel(description)
        desc_label.setProperty("class", "cardDescription")
        desc_label.setWordWrap(True)
        text_col.addWidget(desc_label)
    outer.addLayout(text_col, stretch=1)

    return card
