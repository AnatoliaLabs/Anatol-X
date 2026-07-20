"""3. Sayfa: Kurulum sonrası yapılacaklar (güncelleme, sürücüler)."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from welcome_app.apt_installer import SystemUpdater


class PostInstallPage(QWidget):
    """Sistem güncelleme ve sürücü kontrolü için aksiyon kartları içerir."""

    title = "Kurulum Sonrası"

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._updater: SystemUpdater | None = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        heading = QLabel("Kurulum Sonrası Adımlar")
        heading.setProperty("class", "pageTitle")
        layout.addWidget(heading)

        subtitle = QLabel(
            "Sisteminizi güncel ve sorunsuz tutmak için önerilen ilk adımlar."
        )
        subtitle.setProperty("class", "pageSubtitle")
        layout.addWidget(subtitle)

        # --- Güncelleme kartı ---------------------------------------------------
        update_card = QFrame()
        update_card.setProperty("class", "card")
        update_layout = QVBoxLayout(update_card)
        update_layout.setContentsMargins(18, 16, 18, 16)
        update_layout.setSpacing(10)

        row = QHBoxLayout()
        text_col = QVBoxLayout()
        title_label = QLabel("Sistemi Güncelle")
        title_label.setProperty("class", "cardTitle")
        text_col.addWidget(title_label)
        desc_label = QLabel(
            "APT paket listelerini yeniler ve mevcut güncellemeleri kurar "
            "(apt-get update && apt-get upgrade)."
        )
        desc_label.setProperty("class", "cardDescription")
        desc_label.setWordWrap(True)
        text_col.addWidget(desc_label)
        row.addLayout(text_col, stretch=1)

        self.update_button = QPushButton("Güncellemeleri Kontrol Et")
        self.update_button.setObjectName("primaryButton")
        self.update_button.clicked.connect(self._on_update_clicked)
        row.addWidget(self.update_button)
        update_layout.addLayout(row)

        self.update_log = QTextEdit()
        self.update_log.setObjectName("logOutput")
        self.update_log.setReadOnly(True)
        self.update_log.setFixedHeight(120)
        self.update_log.hide()
        update_layout.addWidget(self.update_log)

        layout.addWidget(update_card)

        # --- Sürücü kartı ---------------------------------------------------------
        driver_card = QFrame()
        driver_card.setProperty("class", "card")
        driver_layout = QHBoxLayout(driver_card)
        driver_layout.setContentsMargins(18, 16, 18, 16)

        driver_text_col = QVBoxLayout()
        driver_title = QLabel("Donanım Sürücüleri")
        driver_title.setProperty("class", "cardTitle")
        driver_text_col.addWidget(driver_title)
        driver_desc = QLabel(
            "Ekran kartı ve diğer donanımlar için ek sürücü gerekip gerekmediğini "
            "kontrol edin. Debian'ın 'Donanım Sürücüleri' aracını kullanabilir "
            "veya belgelere göz atabilirsiniz."
        )
        driver_desc.setProperty("class", "cardDescription")
        driver_desc.setWordWrap(True)
        driver_text_col.addWidget(driver_desc)
        driver_layout.addLayout(driver_text_col, stretch=1)

        driver_button = QPushButton("Belgelere Git")
        driver_button.setObjectName("installButton")
        driver_button.clicked.connect(self._open_driver_docs)
        driver_layout.addWidget(driver_button, alignment=Qt.AlignmentFlag.AlignTop)

        layout.addWidget(driver_card)
        layout.addStretch(1)

    def _on_update_clicked(self) -> None:
        if self._updater is not None:
            return
        self.update_log.show()
        self.update_log.clear()
        self.update_button.setEnabled(False)
        self.update_button.setText("Güncelleniyor...")

        self._updater = SystemUpdater(self)
        self._updater.output_received.connect(self._append_log)
        self._updater.finished.connect(self._on_update_finished)
        self._updater.run()

    def _append_log(self, text: str) -> None:
        self.update_log.moveCursor(self.update_log.textCursor().MoveOperation.End)
        self.update_log.insertPlainText(text)

    def _on_update_finished(self, success: bool, _exit_code: int) -> None:
        self.update_button.setEnabled(True)
        self.update_button.setText(
            "Tamamlandı ✓" if success else "Tekrar Dene"
        )
        self._updater = None

    def _open_driver_docs(self) -> None:
        QDesktopServices.openUrl(QUrl("https://wiki.debian.org/HowToIdentifyADevice/PCI"))
