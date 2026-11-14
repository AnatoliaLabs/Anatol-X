# Anatol-X — ISO Build Hatası Raporu

**Hata:** `E: Unable to locate package spectacle`
**Branch:** `arena/ac294556-anatol-x`
**Commit:** `d64b210`
**Tarih:** 2026-11-14

---

## 1. Özet (TL;DR)

`spectacle` bu depoda **hiçbir yerde tanımlı değil**. `main` dalının 127 commit'lik
tüm geçmişinde, tüm etiketlerde (`alpha2`, `alpha2.1`, `alpha2.2`), tüm açık/kapalı
PR'larda ve mevcut çalışma ağacında bu dizge **hiç geçmiyor**. Paket listesi, en son
**başarılı** ISO derlemesinin (1 Ağustos 2026) listesiyle **bayt bayt aynı**.

Dolayısıyla dosyadan `spectacle` satırı silinerek düzeltilecek bir şey yok.
Gerçek ve doğrulanmış kök neden **paket adının kendisi**:

> Debian'da ekran görüntüsü aracının paket adı `spectacle` **değil**, `kde-spectacle`'dır.
> `spectacle` yalnızca o paketin kurduğu `/usr/bin/spectacle` **ikilisinin** adıdır.

Yapılan düzeltme: pahalı ISO derlemesinden **önce** çalışan, tüm paket adlarını
Debian arşivine karşı doğrulayan ve `spectacle` yazılırsa **doğru adı (`kde-spectacle`)
önererek** derlemeyi 20+ dakika harcamadan durduran bir ön kontrol.

---

## 2. Görevlere göre sonuçlar

### 2.1 Depodaki tüm paket listeleri incelendi

| Dosya | Durum |
|---|---|
| `config/package-lists/anatol-x.list.chroot` | **Tek** live-build paket listesi — 31 paket |
| `config/package-lists/installer.list.chroot` | Geçmişte vardı, `c815d4f`'te silindi (3 paket, spectacle yok) |
| `config/includes.chroot/etc/calamares/netinstall.yaml` | Calamares **kurulum sonrası** seçim listesi (kde-standard, gnome-core, xfce4) |
| `config/includes.chroot/usr/share/anatolx-welcome/data/apps.json` | Hoş geldin uygulamasının önerdiği uygulamalar |
| `config/hooks/live/*.hook.chroot` (7 adet) | `apt-get install` çağrıları (liquorix, helium-bin) |
| `config/includes.chroot/etc/calamares/modules/packages.conf` | **Depoda yok** — hiç var olmadı (doğrulandı) |

Ayrıca tüm git blob'ları (`git cat-file --batch-all-objects`) ve 127 commit'in tamamı
taranarak `spectacle` dizgesi arandı → **0 sonuç**.

### 2.2 `spectacle` hangi dosyada tanımlı?

**Hiçbirinde.** Ne mevcut ağaçta, ne 127 commit'lik geçmişte, ne de PR diff'lerinde.
Yani bu bir "yanlış dosyayı düzelt" durumu değil, **paket adı çözümleme** sorunudur.

### 2.3 Debian 13 (Trixie) erişilebilirliği — doğrulandı

`packages.debian.org` (trixie, tüm bölümler/mimari) sorgusu:

```
You have searched for packages that names contain spectacle in suite(s) trixie
Found 1 matching packages.

### Package kde-spectacle
- trixie (stable) (graphics): Screenshot capture utility
  4:6.3.5-2: amd64 arm64 armel armhf i386 ppc64el riscv64 s390x
```

Debian'in yetkili `ftp-master` madison API'si de aynısını doğruluyor:

```
kde-spectacle | 4:6.3.5-2 | stable | source, amd64, arm64, armel, armhf, i386, ppc64el, riscv64, s390x
```

`spectacle` adında bir paket **hiçbir sürümde yok** (bullseye…sid).

### 2.4 Eksik KDE deposu / APT bileşeni var mı?

**Yok.** Bunu kesin olarak dışladım:

- `auto/config` zaten doğru: `main contrib non-free non-free-firmware`, `--distribution testing`.
- `kde-spectacle` **trixie `main`** bileşiminde. Hiçbir ek depo veya bileşen gerekmiyor.
- `apt-cache madison` ile doğrulandı: paket `stable` (trixie) sürümünde `main` içinde.

Yani "KDE deposu ekle" gibi bir düzeltme **yanlış** olurdu.

### 2.5 Gereksiz silme / toplu değişiklik yapılmadı

`config/` ve `auto/` altındaki **hiçbir dosya değiştirilmedi**:

```
$ git diff --stat -- config/ auto/
(boş)
```

`config/package-lists/anatol-x.list.chroot` içeriği **aynen korundu** — çünkü içinde
hatalı bir satır yok.

### 2.6 Yedek alındı

Düzeltmeden **önce**:

```
backups/2026-11-14-pre-spectacle-fix/
├── MANIFEST.txt          (taban commit, branch, geri alma komutu)
├── anatol-x.list.chroot  (değiştirilmeyen paket listesi)
└── build.yml             (değiştirilen workflow'un öncesi)
```

`.gitignore` eklendi (`backups/`) — çalışma ağacında duruyor, sürüm kontrolüne girmiyor.

### 2.7 APT paket erişimi doğrulandı

**Tüm 31 paket adı tek tek** Debian trixie arşivine karşı doğrulandı:

```
live-boot, live-config, live-config-systemd, systemd, systemd-sysv,
network-manager, firmware-linux (non-free-firmware), firmware-amd-graphics
(non-free-firmware), wireless-regdb, rfkill, sudo, nano, curl, wget,
build-essential, dkms, kde-plasma-desktop, sddm,
pipewire-audio-client-libraries, fonts-noto-core, calamares,
calamares-settings-debian, os-prober, python3-pyqt6, polkitd, pkexec,
polkit-kde-agent-1, grub2-common, grub-pc-bin, grub-efi-amd64-bin
```

→ **31/31 mevcut.** Mevcut liste sağlıklı; sorun yalnızca yeniden eklenen/eski bir
`spectacle` satırından kaynaklanıyor.

> **Not — önemli bir yan bulgu:** Listenin başındaki `firmware-*` yorumu
> "Debian 14 (forky)" varsayımına dayanıyor, ancak yapılandırma `--distribution testing`
> kullanıyor (bugün bu trixie). `firmware-linux` ve `firmware-amd-graphics` trixie'de
> `non-free-firmware` içinde mevcut olduğu için **build'i kırmıyor**; kapsam dışı olduğu
> için dokunulmadı.

### 2.8 Değişiklikler ve test sonuçları

**Değişen dosyalar (3):**

| Dosya | Değişiklik |
|---|---|
| `scripts/check-packages.sh` | **Yeni.** Paket listelerini APT dizinine karşı doğrular |
| `.github/workflows/build.yml` | `lb build`'den **önce** ön kontrol adımı eklendi |
| `.gitignore` | **Yeni.** `backups/` hariç tutulur |

#### Doğrulayıcının çalışma mantığı

Gerçek/sanal/bilinmeyen ayrımı **ampirik olarak** test edilip doğrulandı:

| Durum | Yöntem | Sonuç |
|---|---|---|
| Gerçek paket | `apt-cache policy` → `Candidate: <sürüm>` | ✅ geçer |
| Sanal paket | `apt-cache showpkg` → `Reverse Provides:` dolu | ✅ geçer |
| Bilinmeyen | İkisi de boş | ❌ hata + rapor |
| Yazılış hatası | `spectacle` | ❌ hata + **"doğru ad: kde-spectacle"** |

#### Test sonuçları (yerel APT indeksi ile)

| # | Senaryo | Beklenen | Sonuç |
|---|---|---|---|
| 1 | Listede `spectacle` var | exit ≠ 0, adı raporla | **✅ exit=1**, `- spectacle`, "Doğru paket adı: kde-spectacle" |
| 2 | Liste `kde-spectacle` | exit = 0 | **✅ exit=0** |
| 3 | Ağ erişimi yok | atla, exit = 0 (build kırılmasın) | **✅ exit=0** + UYARI |
| 4 | Sanal paket (`x-display-manager`) | exit = 0 | **✅ exit=0** |
| 5 | Yorumlar / `!` öneki / `pkg- [açıklama]` | doğru ayrıştır | **✅ 31 ad, kesilme yok** |
| 6 | Workflow YAML geçerliliği | geçerli | **✅ `yaml.safe_load` OK** |
| 7 | Adım shell sözdizimi | geçerli | **✅ `bash -n` OK** |

#### Test sürecinde yakalanan 3 gerçek hata (düzeltildi)

1. **Ayrıştırıcı hatası:** `kde-plasma-desktop` → `kde` olarak kesiliyordu
   (`[[:space:]]*-` deseni tireyi de yiyordu). Sadece gerçek bir paket listesiyle test
   etmek ortaya çıkardı; `[[:space:]]\+-` ile düzeltildi. (POSIX `sed` için `\+`)
2. **YAML girinti hatası:** heredoc gövdeleri 1. sütunda kalmıştı → `run: |` bloğunun
   dışına taşıyordu. `yaml.safe_load` yakaladı, girinti düzeltildi.
3. **Sessiz ağ hatası:** `apt-get update`, **tüm indirmeler başarısız olsa bile 0 döner.**
   Bu yüzden çevrimdışı durumda doğrulama "her paket eksik" diyip build'i kırıyordu.
   `lists/*_Packages*` varlığı kontrol edilerek düzeltildi.

---

## 3. Neden bu düzeltme?

Kısıt: *"Yalnızca doğrulanmış sorunu düzelt."*

- Düzeltilecek bir `spectacle` satırı **yok** (kanıtlandı), o yüzden uydurma bir silme
  yapmak yanlış olurdu.
- Sorunun **kendisi** (paket adı çözümlemesi) tekrar ettiğinde 20+ dakikalık build
  boşa gitmesin diye, hatayı **kaynağında ve anında** yakalayan bir ön kontrol eklendi.
- `spectacle` yazılırsa çıktı doğrudan şunu söylüyor:
  `Doğru paket adı: kde-spectacle`

## 4. Eğer `spectacle` eklemek istiyorsanız

`config/package-lists/anatol-x.list.chroot` içine **`kde-spectacle`** yazın
(`spectacle` değil). Doğrulayıcı bunu kabul eder ve trixie'de `main` içinde mevcuttur.

## 5. Geri alma

```bash
git checkout 93b9a03 -- .github/workflows/build.yml
rm -rf scripts/ .gitignore      # yeni eklenenler
```

Yedekler: `backups/2026-11-14-pre-spectacle-fix/`
