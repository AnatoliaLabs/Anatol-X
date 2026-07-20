"""Sistem hakkında bilgi toplayan yardımcı fonksiyonlar.

KDE Plasma sürümü, çekirdek sürümü, dağıtım adı, RAM ve CPU bilgisi
harici bağımlılık gerektirmeden (yalnızca standart kütüphane +
``plasmashell`` komutu) toplanır.
"""

from __future__ import annotations

import os
import platform
import shutil
import subprocess


def _run(cmd: list[str]) -> str | None:
    """Verilen komutu çalıştırır, çıktısını döndürür. Hata olursa None döner."""
    if shutil.which(cmd[0]) is None:
        return None
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=3, check=False
        )
        output = result.stdout.strip() or result.stderr.strip()
        return output or None
    except (subprocess.SubprocessError, OSError):
        return None


def get_os_release() -> dict[str, str]:
    """``/etc/os-release`` dosyasını ayrıştırır."""
    data: dict[str, str] = {}
    path = "/etc/os-release"
    if not os.path.exists(path):
        return data
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                data[key] = value.strip('"')
    except OSError:
        pass
    return data


def get_distro_name() -> str:
    """Dağıtımın güzel/tam ismini döndürür (örn. 'Debian GNU/Linux 12 (bookworm)')."""
    data = get_os_release()
    return data.get("PRETTY_NAME") or data.get("NAME") or "Bilinmeyen Dağıtım"


def get_kernel_version() -> str:
    """Çalışan çekirdek sürümünü döndürür (örn. '6.1.0-13-amd64')."""
    return platform.release() or "Bilinmiyor"


def get_architecture() -> str:
    """Sistem mimarisini döndürür (örn. 'x86_64')."""
    return platform.machine() or "Bilinmiyor"


def get_plasma_version() -> str:
    """KDE Plasma masaüstü sürümünü döndürür."""
    output = _run(["plasmashell", "--version"])
    if output:
        # Çıktı genelde "plasmashell 5.27.10" biçimindedir.
        parts = output.split()
        if parts:
            return parts[-1]
    return "Bulunamadı"


def get_qt_version() -> str:
    """Qt sürümünü döndürür (PyQt6 üzerinden)."""
    try:
        from PyQt6.QtCore import QT_VERSION_STR

        return QT_VERSION_STR
    except ImportError:
        return "Bilinmiyor"


def get_memory_info() -> dict[str, float]:
    """``/proc/meminfo`` üzerinden RAM bilgisini GiB cinsinden döndürür."""
    info = {"total_gib": 0.0, "available_gib": 0.0}
    path = "/proc/meminfo"
    if not os.path.exists(path):
        return info
    try:
        values: dict[str, int] = {}
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                key, _, rest = line.partition(":")
                rest = rest.strip()
                if rest.endswith("kB"):
                    try:
                        values[key.strip()] = int(rest.split()[0])
                    except (ValueError, IndexError):
                        continue
        if "MemTotal" in values:
            info["total_gib"] = round(values["MemTotal"] / (1024 * 1024), 1)
        if "MemAvailable" in values:
            info["available_gib"] = round(values["MemAvailable"] / (1024 * 1024), 1)
    except OSError:
        pass
    return info


def get_cpu_model() -> str:
    """``/proc/cpuinfo`` üzerinden CPU model adını döndürür."""
    path = "/proc/cpuinfo"
    if not os.path.exists(path):
        return platform.processor() or "Bilinmiyor"
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if line.lower().startswith("model name"):
                    return line.partition(":")[2].strip()
    except OSError:
        pass
    return platform.processor() or "Bilinmiyor"


def get_cpu_core_count() -> int:
    """Mantıksal CPU çekirdek sayısını döndürür."""
    return os.cpu_count() or 1


def get_disk_usage(path: str = "/") -> dict[str, float]:
    """Kök dizin için disk kullanım bilgisini GiB cinsinden döndürür."""
    # Bazı konteyner/sanal dosya sistemleri (ör. overlay/gVisor) gerçekçi
    # olmayan (neredeyse int64 sınırında) değerler döndürebilir. Bu tür
    # değerleri makul bir üst sınırla (16 PiB) filtreleyip 0 olarak ele alıyoruz.
    max_sane_bytes = 16 * 1024**5  # ~16 PiB
    try:
        usage = shutil.disk_usage(path)
        if usage.total <= 0 or usage.total > max_sane_bytes:
            return {"total_gib": 0.0, "free_gib": 0.0, "used_gib": 0.0}
        return {
            "total_gib": round(usage.total / (1024**3), 1),
            "free_gib": round(usage.free / (1024**3), 1),
            "used_gib": round(usage.used / (1024**3), 1),
        }
    except OSError:
        return {"total_gib": 0.0, "free_gib": 0.0, "used_gib": 0.0}


def collect_system_summary() -> dict[str, str]:
    """Sistem bilgi sayfasında gösterilecek özet bilgiyi tek seferde toplar."""
    mem = get_memory_info()
    disk = get_disk_usage()
    disk_text = (
        f"{disk['free_gib']} GiB boş / {disk['total_gib']} GiB"
        if disk["total_gib"] > 0
        else "Bilinmiyor"
    )
    return {
        "distro": get_distro_name(),
        "kernel": get_kernel_version(),
        "architecture": get_architecture(),
        "plasma": get_plasma_version(),
        "qt": get_qt_version(),
        "cpu": get_cpu_model(),
        "cpu_cores": str(get_cpu_core_count()),
        "ram_total": f"{mem['total_gib']} GiB",
        "ram_available": f"{mem['available_gib']} GiB",
        "disk_free": disk_text,
    }


if __name__ == "__main__":
    for key, value in collect_system_summary().items():
        print(f"{key}: {value}")
