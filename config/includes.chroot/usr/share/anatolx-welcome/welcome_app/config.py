"""Kalıcı ayarların (QSettings) yönetimi.

"Açılışta gösterme" tercihi burada saklanır ve autostart mantığı
(``main.py``) tarafından okunur.
"""

from __future__ import annotations

from PyQt6.QtCore import QSettings

from welcome_app.constants import APP_ID, ORG_NAME, SETTINGS_SHOW_ON_STARTUP


def get_settings() -> QSettings:
    """QSettings örneğini döndürür (INI formatında ~/.config altına yazılır)."""
    return QSettings(ORG_NAME, APP_ID)


def should_show_on_startup() -> bool:
    """Açılışta pencerenin gösterilip gösterilmeyeceğini döndürür. Varsayılan: True."""
    settings = get_settings()
    value = settings.value(SETTINGS_SHOW_ON_STARTUP, True)
    # QSettings bool değerleri bazen string olarak saklayabilir ("true"/"false").
    if isinstance(value, str):
        return value.lower() in ("1", "true", "yes")
    return bool(value)


def set_show_on_startup(value: bool) -> None:
    """Açılışta gösterme tercihini kalıcı olarak kaydeder."""
    settings = get_settings()
    settings.setValue(SETTINGS_SHOW_ON_STARTUP, bool(value))
    settings.sync()
