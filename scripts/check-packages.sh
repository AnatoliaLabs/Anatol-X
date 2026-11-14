#!/bin/sh
# Anatol-X ISO derleme öncesi paket adı doğrulayıcı.
#
# Amaç: config/package-lists/*.list.chroot içindeki TÜM paket adlarını derleme
# başlamadan önce APT dizinine karşı doğrulamak. Böylece 20-30 dakika süren bir
# lb build, tek bir yanlış paket adı yüzünden ("E: Unable to locate package ...")
# en sonda değil, en başta durur.
#
# Bağlam — "E: Unable to locate package spectacle":
#   Debian'da ekran görüntüsü aracının PAKET adı `spectacle` değil,
#   `kde-spectacle`'tır. Debian'da "spectacle" adlı bir paket yoktur; bu ad
#   yalnızca kde-spectacle'ın kurduğu /usr/bin/spectacle ikilisi ve KDE'nin
#   kendi bileşen adıdır. Bu yüzden `apt-get install spectacle` kaçınılmaz
#   olarak "Unable to locate package spectacle" verir.
#   Düzeltme: paket listesine `kde-spectacle` yazılmalıdır (bu araç otomatik
#   olarak önerir).
#
# Kullanım:
#   sh scripts/check-packages.sh
#   SUITE=forky sh scripts/check-packages.sh   # başka sürüme göre
#
# Çıkış kodları:
#   0 = tüm adlar çözümlendi
#   1 = çözümlenemeyen paket adı var
#   2 = ön koşul eksik (apt-cache yok / dizin yok / dizin boş)

set -eu

LISTS_DIR="${LISTS_DIR:-config/package-lists}"

if [ ! -d "$LISTS_DIR" ]; then
    echo "E: Paket listesi dizini bulunamadı: $LISTS_DIR" >&2
    exit 2
fi

if ! command -v apt-cache >/dev/null 2>&1; then
    echo "E: apt-cache bulunamadı; paket adları doğrulanamıyor." >&2
    exit 2
fi

set -- "$LISTS_DIR"/*.list.chroot
if [ ! -f "$1" ]; then
    echo "E: $LISTS_DIR içinde .list.chroot dosyası yok." >&2
    exit 2
fi

# --- Paket adlarını çıkar -------------------------------------------------
# Yorumlar (#), boş satırlar, live-build "!" öneki ve "paket- [açıklama]"
# satır sonu ayıklayıcıları temizlenir.
extract_packages() {
    sed -e 's/#.*$//' \
        -e 's/[[:space:]]*$//' \
        -e '/^[[:space:]]*$/d' \
        -e 's/^![[:space:]]*//' \
        -e 's/[[:space:]]\+-.*$//' \
        "$1"
}

echo "I: Paket adları APT dizinine karşı doğrulanıyor ..."

total=0
failed=0
failed_pkgs=""
failed_report=""

for list in "$LISTS_DIR"/*.list.chroot; do
    [ -f "$list" ] || continue
    while IFS= read -r pkg; do
        [ -n "$pkg" ] || continue
        # Yalnızca geçerli Debian paket adı biçimini kabul et.
        case "$pkg" in
            *[!a-z0-9+.-]*) continue ;;
        esac
        total=$((total + 1))

        # 1) Gerçek paket: apt-cache policy bir Candidate sürümü listeler.
        candidate="$(apt-cache policy "$pkg" 2>/dev/null \
            | sed -n 's/^  Candidate:[[:space:]]*//p' | head -n 1)"
        if [ -n "$candidate" ] && [ "$candidate" != "(none)" ]; then
            continue
        fi

        # 2) Sanal paket: başka bir paket bu adı sağlıyorsa apt-cache showpkg
        #    çıktısında "Reverse Provides:" altında listelenir.
        if apt-cache showpkg "$pkg" 2>/dev/null | grep -q "^Reverse Provides:"; then
            continue
        fi

        # 3) Çözümlenemedi.
        failed=$((failed + 1))
        failed_pkgs="$failed_pkgs $pkg"
        failed_report="$failed_report
  - $pkg  (kaynak: ${list##*/})"
    done <<EOF
$(extract_packages "$list")
EOF
done

echo "I: Toplam $total paket adı incelendi."

if [ "$failed" -eq 0 ]; then
    echo "I: Tüm paket adları APT dizininde çözümlendi."
    exit 0
fi

echo "" >&2
echo "E: Çözümlenemeyen $failed paket adı ("Unable to locate package"):" >&2
echo "$failed_report" >&2
echo "" >&2

# Bilinen yazım hataları için doğrudan düzeltme öner.
for bad in $failed_pkgs; do
    case "$bad" in
        spectacle)
            echo "I: 'spectacle' Debian'da bir PAKET ADI değildir." >&2
            echo "   Doğru paket adı: kde-spectacle" >&2
            echo "   ('spectacle' yalnızca kde-spectacle'ın kurduğu /usr/bin/spectacle" >&2
            echo "    ikilisi ve KDE bileşen adıdır.)" >&2
            ;;
    esac
done

exit 1
