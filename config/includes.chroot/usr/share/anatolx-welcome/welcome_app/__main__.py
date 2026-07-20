"""Paket içi giriş noktası (``python3 -m welcome_app`` veya kurulu ``welcome-app`` komutu).

Autostart ile başlatıldığında, kullanıcı "açılışta gösterme" tercihini
kapatmışsa herhangi bir pencere oluşturmadan sessizce çıkar.
"""

from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication

from welcome_app.config import should_show_on_startup
from welcome_app.constants import APP_ID, APP_NAME, ORG_NAME
from welcome_app.theme import apply_theme


def run() -> int:
    """Uygulamayı başlatır, çıkış kodunu döndürür."""
    force_show = "--force" in sys.argv[1:]
    if not force_show and not should_show_on_startup():
        return 0

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationDisplayName(APP_NAME)
    app.setOrganizationName(ORG_NAME)
    app.setDesktopFileName(APP_ID)

    apply_theme(app)

    # main_window import'u burada yapılır ki QApplication her zaman
    # widget'lardan önce oluşturulmuş olsun.
    from welcome_app.main_window import MainWindow

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(run())
