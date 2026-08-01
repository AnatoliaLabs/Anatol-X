"""Kalıcı ayarların (QSettings) yönetimi.

"Açılışta gösterme" tercihi burada saklanır ve autostart mantığı
(``__main__.py``) tarafından okunur. Ayrıca uygulamanın ilk kez
çalıştırılıp çalıştırılmadığını tutan bir "ilk açılış" işareti bulunur:
Anatol-X'te hoşgeldin penceresi otomatik olarak yalnızca ilk açılışta
gösterilir, sonraki oturumlarda kendiliğinden açılmaz.
"""

from __future__ import annotations

from PyQt6.QtCore import QSettings

from welcome_app.constants import (
    APP_ID,
    ORG_NAME,
    SETTINGS_FIRST_RUN_DONE,
    SETTINGS_SHOW_ON_STARTUP,
)


def get_settings() -> QSettings:
    """QSettings örneğini döndürür (INI formatında ~/.config altına yazılır)."""
    return QSettings(ORG_NAME, APP_ID)


def _as_bool(value: object) -> bool:
    """QSettings değerini (bool veya string) güvenli şekilde bool'a çevirir."""
    if isinstance(value, str):
        return value.lower() in ("1", "true", "yes")
    return bool(value)


def should_show_on_startup() -> bool:
    """Açılışta pencerenin gösterilip gösterilmeyeceğini döndürür. Varsayılan: True."""
    return _as_bool(get_settings().value(SETTINGS_SHOW_ON_STARTUP, True))


def set_show_on_startup(value: bool) -> None:
    """Açılışta gösterme tercihini kalıcı olarak kaydeder."""
    settings = get_settings()
    settings.setValue(SETTINGS_SHOW_ON_STARTUP, bool(value))
    settings.sync()


def has_completed_first_run() -> bool:
    """Uygulamanın daha önce en az bir kez çalıştırılıp çalıştırılmadığını döndürür."""
    return _as_bool(get_settings().value(SETTINGS_FIRST_RUN_DONE, False))


def set_first_run_completed() -> None:
    """Uygulamanın ilk kez çalıştırıldığını kalıcı olarak işaretler."""
    settings = get_settings()
    settings.setValue(SETTINGS_FIRST_RUN_DONE, True)
    settings.sync()
