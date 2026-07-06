#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Anatol-X Hoş Geldin Uygulaması
Debian tabanlı Anatol-X dağıtımı için basit karşılama ekranı.
"""

import os
import tkinter as tk

CONFIG_DIR = os.path.expanduser("~/.config/anatolx-welcome")
FLAG_FILE = os.path.join(CONFIG_DIR, "dont_show")

# --- Renk paleti ---
BG_COLOR = "#F5F0E6"        # krem zemin
HEADING_COLOR = "#0F6E6C"   # koyu turkuaz
TEXT_COLOR = "#333B4A"      # koyu gri-lacivert
ACCENT_COLOR = "#C6603D"    # terrakota
ACCENT_TEXT = "#FFFFFF"

# --- Fontlar ---
FONT_HEADING = ("Noto Sans", 20, "bold")
FONT_BODY = ("Noto Sans", 11)
FONT_BUTTON = ("Noto Sans", 11, "bold")

WINDOW_W, WINDOW_H = 480, 320


def should_show():
    return not os.path.exists(FLAG_FILE)


def save_dont_show():
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(FLAG_FILE, "w") as f:
        f.write("1")


def close_app(dont_show_var, root):
    if dont_show_var.get():
        save_dont_show()
    root.destroy()


def main():
    if not should_show():
        return

    root = tk.Tk()
    root.title("Anatol-X'e Hoş Geldiniz")
    root.configure(bg=BG_COLOR)
    root.resizable(False, False)

    # Pencereyi ekranın ortasına yerleştir
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (WINDOW_W // 2)
    y = (root.winfo_screenheight() // 2) - (WINDOW_H // 2)
    root.geometry(f"{WINDOW_W}x{WINDOW_H}+{x}+{y}")

    heading = tk.Label(
        root,
        text="Anatol-X'e Hoş Geldiniz",
        font=FONT_HEADING,
        fg=HEADING_COLOR,
        bg=BG_COLOR,
    )
    heading.pack(pady=(35, 15))

    # Güncellenmiş Anatol-X tanıtım metni
    description = (
        "Anatol-X, gücünü Debian'ın kararlılığından alan,\n"
        "maksimum performans ve düşük gecikme için optimize edilmiş\n"
        "modern ve saf bir Linux deneyimidir."
    )
    body = tk.Label(
        root,
        text=description,
        font=FONT_BODY,
        fg=TEXT_COLOR,
        bg=BG_COLOR,
        justify="center",
    )
    body.pack(pady=(0, 30))

    dont_show_var = tk.BooleanVar(value=False)
    check = tk.Checkbutton(
        root,
        text="Bir daha gösterme",
        variable=dont_show_var,
        font=FONT_BODY,
        fg=TEXT_COLOR,
        bg=BG_COLOR,
        activebackground=BG_COLOR,
        selectcolor="#FFFFFF",
    )
    check.pack(pady=(0, 20))

    close_btn = tk.Button(
        root,
        text="Tamam",
        font=FONT_BUTTON,
        bg=ACCENT_COLOR,
        fg=ACCENT_TEXT,
        activebackground=ACCENT_COLOR,
        activeforeground=ACCENT_TEXT,
        relief="flat",
        borderwidth=0,
        padx=24,
        pady=8,
        command=lambda: close_app(dont_show_var, root),
    )
    close_btn.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
