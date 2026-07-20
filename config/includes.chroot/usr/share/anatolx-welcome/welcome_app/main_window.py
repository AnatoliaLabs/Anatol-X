"""Ana pencere: sihirbaz tarzı sayfa navigasyonu."""

from __future__ import annotations

from PyQt6.QtWidgets import (
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from welcome_app.config import set_show_on_startup, should_show_on_startup
from welcome_app.constants import (
    APP_NAME,
    DISTRO_NAME,
    WINDOW_MIN_HEIGHT,
    WINDOW_MIN_WIDTH,
)
from welcome_app.pages import (
    AppsPage,
    CommunityPage,
    PostInstallPage,
    SystemInfoPage,
    WelcomePage,
)


class MainWindow(QMainWindow):
    """Sayfalar arasında İleri/Geri ile gezinilen ana pencere."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - {DISTRO_NAME}")
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(28, 24, 28, 20)
        root_layout.setSpacing(18)

        # --- Adım göstergesi (üst) ---------------------------------------------
        self.step_indicator = QWidget()
        self.step_indicator_layout = QHBoxLayout(self.step_indicator)
        self.step_indicator_layout.setContentsMargins(0, 0, 0, 0)
        self.step_indicator_layout.setSpacing(8)
        self.step_indicator_layout.addStretch(1)
        root_layout.addWidget(self.step_indicator)

        # --- Sayfa yığını --------------------------------------------------------
        self.stack = QStackedWidget()
        root_layout.addWidget(self.stack, stretch=1)

        self.pages = [
            WelcomePage(),
            SystemInfoPage(),
            PostInstallPage(),
            AppsPage(),
            CommunityPage(),
        ]
        for page in self.pages:
            self.stack.addWidget(page)

        self._step_dots: list[QFrame] = []
        for _ in self.pages:
            dot = QFrame()
            dot.setFixedSize(11, 11)
            dot.setObjectName("stepDot")
            self.step_indicator_layout.addWidget(dot)
            self._step_dots.append(dot)
        self.step_indicator_layout.addStretch(1)

        # --- Alt gezinme çubuğu ---------------------------------------------------
        footer = QHBoxLayout()
        footer.setSpacing(12)

        self.show_on_startup_checkbox = QCheckBox("Bu pencereyi açılışta gösterme")
        self.show_on_startup_checkbox.setChecked(not should_show_on_startup())
        self.show_on_startup_checkbox.toggled.connect(self._on_show_on_startup_toggled)
        footer.addWidget(self.show_on_startup_checkbox)

        footer.addStretch(1)

        self.back_button = QPushButton("Geri")
        self.back_button.setObjectName("installButton")
        self.back_button.clicked.connect(self._go_back)
        footer.addWidget(self.back_button)

        self.next_button = QPushButton("İleri")
        self.next_button.setObjectName("primaryButton")
        self.next_button.clicked.connect(self._go_next)
        footer.addWidget(self.next_button)

        self.close_button = QPushButton("Kapat")
        self.close_button.setObjectName("primaryButton")
        self.close_button.clicked.connect(self.close)
        footer.addWidget(self.close_button)

        root_layout.addLayout(footer)

        self._current_index = 0
        self._update_navigation()

    # --- İç yardımcılar -----------------------------------------------------------
    def _update_navigation(self) -> None:
        self.stack.setCurrentIndex(self._current_index)
        is_first = self._current_index == 0
        is_last = self._current_index == len(self.pages) - 1

        self.back_button.setVisible(not is_first)
        self.next_button.setVisible(not is_last)
        self.close_button.setVisible(is_last)

        for i, dot in enumerate(self._step_dots):
            dot.setObjectName("stepDotActive" if i == self._current_index else "stepDot")
            dot.style().unpolish(dot)
            dot.style().polish(dot)

    def _go_next(self) -> None:
        if self._current_index < len(self.pages) - 1:
            self._current_index += 1
            self._update_navigation()

    def _go_back(self) -> None:
        if self._current_index > 0:
            self._current_index -= 1
            self._update_navigation()

    def _on_show_on_startup_toggled(self, dont_show: bool) -> None:
        set_show_on_startup(not dont_show)
