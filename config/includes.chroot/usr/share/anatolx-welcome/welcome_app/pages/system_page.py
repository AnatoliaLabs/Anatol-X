"""2. Sayfa: Sistem hakkında bilgi."""

from __future__ import annotations

from PyQt6.QtWidgets import QGridLayout, QLabel, QVBoxLayout, QWidget

from welcome_app.system_info import collect_system_summary
from welcome_app.widgets import make_card_with_title

# (etiket, sözlük anahtarı, ikon)
_INFO_ROWS = [
    ("Dağıtım", "distro", "🐧"),
    ("Çekirdek Sürümü", "kernel", "🧩"),
    ("Mimari", "architecture", "🖥️"),
    ("KDE Plasma Sürümü", "plasma", "🎨"),
    ("Qt Sürümü", "qt", "🔷"),
    ("İşlemci", "cpu", "⚙️"),
    ("İşlemci Çekirdek Sayısı", "cpu_cores", "🔢"),
    ("Toplam RAM", "ram_total", "💾"),
    ("Kullanılabilir RAM", "ram_available", "📈"),
    ("Disk Durumu", "disk_free", "🗄️"),
]


class SystemInfoPage(QWidget):
    """Sistem hakkında temel donanım/yazılım bilgisini kart olarak gösterir."""

    title = "Sistem Bilgisi"

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        heading = QLabel("Sisteminiz Hakkında")
        heading.setProperty("class", "pageTitle")
        layout.addWidget(heading)

        subtitle = QLabel("Yeni sisteminizin donanım ve yazılım özeti aşağıdadır.")
        subtitle.setProperty("class", "pageSubtitle")
        layout.addWidget(subtitle)

        summary = collect_system_summary()

        grid_container = QWidget()
        grid = QGridLayout(grid_container)
        grid.setHorizontalSpacing(14)
        grid.setVerticalSpacing(14)

        for index, (label, key, icon) in enumerate(_INFO_ROWS):
            row, col = divmod(index, 2)
            card = make_card_with_title(label, summary.get(key, "Bilinmiyor"), icon)
            grid.addWidget(card, row, col)

        layout.addWidget(grid_container)
        layout.addStretch(1)
