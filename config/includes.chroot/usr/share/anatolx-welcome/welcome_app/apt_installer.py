"""``pkexec`` üzerinden apt paket kurulumu yapan yardımcı sınıf.

Kurulum işlemleri, arayüzü kilitlememesi için ``QProcess`` ile
asenkron olarak çalıştırılır. Çıktı satır satır sinyal aracılığıyla
iletilir; böylece arayüz canlı bir log gösterebilir.
"""

from __future__ import annotations

import shutil

from PyQt6.QtCore import QObject, QProcess, pyqtSignal


class AptInstaller(QObject):
    """Tek bir apt paketinin ``pkexec apt-get install`` ile kurulumunu yönetir."""

    output_received = pyqtSignal(str)
    finished = pyqtSignal(bool, int)  # (basarili_mi, cikis_kodu)
    started = pyqtSignal()

    def __init__(self, package_name: str, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.package_name = package_name
        self._process: QProcess | None = None

    @staticmethod
    def is_available() -> bool:
        """``pkexec`` ve ``apt-get`` sistemde mevcut mu kontrol eder."""
        return shutil.which("pkexec") is not None and shutil.which("apt-get") is not None

    def build_command(self) -> tuple[str, list[str]]:
        """Çalıştırılacak komutu ve argümanlarını döndürür."""
        return "pkexec", [
            "apt-get",
            "install",
            "-y",
            self.package_name,
        ]

    def install(self) -> None:
        """Kurulumu başlatır (asenkron)."""
        if self._process is not None:
            return

        program, args = self.build_command()
        self._process = QProcess(self)
        self._process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        self._process.readyReadStandardOutput.connect(self._on_ready_read)
        self._process.finished.connect(self._on_finished)
        self._process.errorOccurred.connect(self._on_error)
        self.started.emit()
        self._process.start(program, args)

    def cancel(self) -> None:
        """Devam eden kurulumu iptal eder."""
        if self._process is not None and self._process.state() != QProcess.ProcessState.NotRunning:
            self._process.kill()

    def _on_ready_read(self) -> None:
        if self._process is None:
            return
        data = self._process.readAllStandardOutput()
        text = bytes(data).decode("utf-8", errors="replace")
        if text:
            self.output_received.emit(text)

    def _on_finished(self, exit_code: int, _exit_status) -> None:
        self.finished.emit(exit_code == 0, exit_code)
        self._process = None

    def _on_error(self, _error) -> None:
        if self._process is not None and self._process.state() == QProcess.ProcessState.NotRunning:
            self.output_received.emit("[Hata] Kurulum başlatılamadı.\n")
            self.finished.emit(False, -1)
            self._process = None


class SystemUpdater(QObject):
    """``pkexec apt-get update && apt-get upgrade`` işlemini yönetir."""

    output_received = pyqtSignal(str)
    finished = pyqtSignal(bool, int)
    started = pyqtSignal()

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._process: QProcess | None = None

    def run(self) -> None:
        if self._process is not None:
            return
        self._process = QProcess(self)
        self._process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        self._process.readyReadStandardOutput.connect(self._on_ready_read)
        self._process.finished.connect(self._on_finished)
        self._process.errorOccurred.connect(self._on_error)
        self.started.emit()
        # tek pkexec çağrısında update + upgrade zinciri
        self._process.start(
            "pkexec",
            ["sh", "-c", "apt-get update && apt-get upgrade -y"],
        )

    def cancel(self) -> None:
        if self._process is not None and self._process.state() != QProcess.ProcessState.NotRunning:
            self._process.kill()

    def _on_ready_read(self) -> None:
        if self._process is None:
            return
        data = self._process.readAllStandardOutput()
        text = bytes(data).decode("utf-8", errors="replace")
        if text:
            self.output_received.emit(text)

    def _on_finished(self, exit_code: int, _exit_status) -> None:
        self.finished.emit(exit_code == 0, exit_code)
        self._process = None

    def _on_error(self, _error) -> None:
        if self._process is not None and self._process.state() == QProcess.ProcessState.NotRunning:
            self.output_received.emit("[Hata] Güncelleme başlatılamadı.\n")
            self.finished.emit(False, -1)
            self._process = None
