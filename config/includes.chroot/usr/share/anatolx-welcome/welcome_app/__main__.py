"""Paket içi giriş noktası (``python3 -m welcome_app`` veya ``anatolx-welcome`` komutu).

Autostart ile başlatıldığında, uygulama **yalnızca ilk açılışta** bir kez
gösterilir: ilk çalıştırmada pencere açılır ve "açılışta göster" tercihi
otomatik olarak kapatılır. Sonraki oturum açılışlarında sessizce çıkar.
Kullanıcı daha sonra pencere içindeki seçeneği tekrar işaretlerse,
otomatik başlatma yeniden etkinleşir.
"""

from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication

from welcome_app.config import (
    has_completed_first_run,
    set_first_run_completed,
    set_show_on_startup,
    should_show_on_startup,
)
from welcome_app.constants import APP_ID, APP_NAME, ORG_NAME
from welcome_app.theme import apply_theme


def run() -> int:
    """Uygulamayı başlatır, çıkış kodunu döndürür."""
    force_show = "--force" in sys.argv[1:]
    first_run = not has_completed_first_run()

    # Otomatik başlatma: ilk açılış değilse ve kullanıcı "açılışta göster"
    # tercihini açmamışsa hiç pencere oluşturmadan sessizce çık.
    if not force_show and not first_run and not should_show_on_startup():
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

    # İlk çalıştırma tamamlandı: bir daha otomatik başlatmayla kendiliğinden
    # açılmasın (kullanıcı pencere içindeki seçenekten tekrar açabilir).
    if first_run:
        set_first_run_completed()
        set_show_on_startup(False)

    return app.exec()


if __name__ == "__main__":
    sys.exit(run())
