"""Uygulama genelinde kullanılan sabitler.

Bu dosya, dağıtımın adı, sürümü ve marka bilgilerini tek bir yerden
yönetmek için tasarlanmıştır. Kendi dağıtımınıza uyarlamak için sadece
bu değerleri değiştirmeniz yeterlidir.
"""

from __future__ import annotations

import os

# --- Dağıtım / Marka Bilgileri -------------------------------------------------
DISTRO_NAME = os.environ.get("WELCOME_DISTRO_NAME", "Anatol-X")
DISTRO_TAGLINE = "Debian tabanlı, Liquorix çekirdekli maksimum performans dağıtımı."

# --- Uygulama Bilgileri ---------------------------------------------------------
APP_NAME = "Hoşgeldiniz"
APP_ID = "anatolx-welcome"
APP_VERSION = "1.0.0"
ORG_NAME = "AnatoliaLabs"
ORG_DOMAIN = "anatolialabs.github.io"

# --- QSettings anahtarları -------------------------------------------------------
# NOT: QSettings'in INI biçiminde "General" grup adı özel/ayrılmış bir anlam
# taşıdığından (Qt bunu dahili olarak "%General" olarak kodlar ve okurken
# beklenmedik sonuçlar verebilir), grup adı olarak "general" kullanılmıyor.
SETTINGS_SHOW_ON_STARTUP = "app/show_on_startup"

# --- Pencere Boyutları -----------------------------------------------------------
WINDOW_MIN_WIDTH = 880
WINDOW_MIN_HEIGHT = 620

# --- Veri Dosyaları ---------------------------------------------------------------
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
APPS_JSON_PATH = os.path.join(DATA_DIR, "apps.json")
LINKS_JSON_PATH = os.path.join(DATA_DIR, "links.json")
