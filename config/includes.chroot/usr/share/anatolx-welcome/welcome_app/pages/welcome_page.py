"""1. Sayfa: Hoşgeldiniz / Tanıtım."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from welcome_app.constants import DISTRO_NAME, DISTRO_TAGLINE


class WelcomePage(QWidget):
    """Büyük bir banner ile dağıtımı tanıtan giriş sayfası."""

    title = "Hoşgeldiniz"

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(24)

        banner = QWidget()
        banner.setObjectName("bannerWidget")
        banner.setMinimumHeight(220)
        banner_layout = QVBoxLayout(banner)
        banner_layout.setContentsMargins(36, 32, 36, 32)
        banner_layout.setSpacing(10)
        banner_layout.addStretch(1)

        title_label = QLabel(f"{DISTRO_NAME}'a Hoşgeldiniz!")
        title_label.setObjectName("bannerTitle")
        title_label.setWordWrap(True)
        banner_layout.addWidget(title_label)

        subtitle_label = QLabel(DISTRO_TAGLINE)
        subtitle_label.setObjectName("bannerSubtitle")
        subtitle_label.setWordWrap(True)
        banner_layout.addWidget(subtitle_label)
        banner_layout.addStretch(1)

        layout.addWidget(banner)

        intro = QLabel(
            "Bu kısa sihirbaz; sisteminizi tanımanıza, güncellemenizi yapmanıza, "
            "önerilen bazı uygulamaları kurmanıza ve topluluğumuza katılmanıza "
            "yardımcı olacak. İleri butonuna basarak devam edebilirsiniz."
        )
        intro.setWordWrap(True)
        intro.setProperty("class", "cardDescription")
        intro.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(intro)

        layout.addStretch(1)
