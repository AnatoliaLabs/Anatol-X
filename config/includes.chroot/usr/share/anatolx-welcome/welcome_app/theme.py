"""Görsel tema yardımcıları.

Uygulama, KDE Plasma / Breeze sistem paletini olduğu gibi kullanır
(native Qt stili zorlanmaz). Burada sadece okunabilirliği artıran
tipografi ayarları ve kart/buton görünümü için ince bir QSS katmanı
tanımlanır. Renkler doğrudan sabit (hardcoded) değil, sistem
paletinden (``QPalette``) türetilir; böylece açık/koyu Breeze
temalarının her ikisiyle de uyumlu çalışır.
"""

from __future__ import annotations

from PyQt6.QtGui import QColor, QFont, QPalette
from PyQt6.QtWidgets import QApplication


def _mix(c1: QColor, c2: QColor, t: float) -> QColor:
    """İki rengi t (0-1) oranında karıştırır."""
    return QColor(
        round(c1.red() * (1 - t) + c2.red() * t),
        round(c1.green() * (1 - t) + c2.green() * t),
        round(c1.blue() * (1 - t) + c2.blue() * t),
    )


def apply_base_typography(app: QApplication) -> None:
    """Okunabilirliği artırmak için biraz daha büyük/temiz bir taban font ayarlar."""
    font = app.font()
    # Kullanıcının sistem fontunu koru, sadece boyutu hafifçe büyüt.
    size = font.pointSizeF()
    if size > 0:
        font.setPointSizeF(max(size, 10.5))
    app.setFont(font)


def build_stylesheet(app: QApplication) -> str:
    """Sistem paletinden türetilmiş, kart/buton görünümü için QSS döndürür."""
    pal = app.palette()
    base = pal.color(QPalette.ColorRole.Window)
    text = pal.color(QPalette.ColorRole.WindowText)
    highlight = pal.color(QPalette.ColorRole.Highlight)
    button = pal.color(QPalette.ColorRole.Button)
    is_dark = base.lightness() < 128

    card_bg = _mix(base, QColor(255, 255, 255) if not is_dark else QColor(0, 0, 0), 0.06)
    card_border = _mix(base, text, 0.18)
    banner_start = highlight.name()
    banner_end = _mix(highlight, QColor(255, 255, 255), 0.28).name()
    muted_text = _mix(text, base, 0.35).name()

    return f"""
    QWidget#bannerWidget {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 {banner_start}, stop:1 {banner_end});
        border-radius: 14px;
    }}
    QLabel#bannerTitle {{
        color: white;
        font-size: 26pt;
        font-weight: 700;
    }}
    QLabel#bannerSubtitle {{
        color: rgba(255, 255, 255, 220);
        font-size: 12pt;
    }}
    QFrame[class="card"] {{
        background-color: {card_bg.name()};
        border: 1px solid {card_border.name()};
        border-radius: 10px;
    }}
    QLabel[class="pageTitle"] {{
        font-size: 18pt;
        font-weight: 700;
    }}
    QLabel[class="pageSubtitle"] {{
        font-size: 11pt;
        color: {muted_text};
    }}
    QLabel[class="cardTitle"] {{
        font-size: 12.5pt;
        font-weight: 600;
    }}
    QLabel[class="cardDescription"] {{
        font-size: 10.5pt;
        color: {muted_text};
    }}
    QPushButton {{
        padding: 8px 18px;
        border-radius: 8px;
    }}
    QPushButton#primaryButton {{
        background-color: {highlight.name()};
        color: white;
        font-weight: 600;
    }}
    QPushButton#primaryButton:disabled {{
        background-color: {_mix(highlight, base, 0.5).name()};
        color: rgba(255,255,255,160);
    }}
    QPushButton#installButton {{
        background-color: {button.name()};
        border: 1px solid {card_border.name()};
    }}
    QPushButton#installButton:disabled {{
        color: {muted_text};
    }}
    QFrame#stepDot {{
        border-radius: 5px;
        background-color: {_mix(text, base, 0.6).name()};
    }}
    QFrame#stepDotActive {{
        border-radius: 5px;
        background-color: {highlight.name()};
    }}
    QTextEdit#logOutput {{
        background-color: {_mix(base, QColor(0, 0, 0), 0.08 if not is_dark else 0.0).name()};
        border: 1px solid {card_border.name()};
        border-radius: 8px;
        font-family: monospace;
        font-size: 9.5pt;
    }}
    """


def apply_theme(app: QApplication) -> None:
    """Tipografi ve QSS'yi uygulamaya uygular."""
    apply_base_typography(app)
    app.setStyleSheet(build_stylesheet(app))
