# 🚀 Anatol-X Linux

![Build Status](https://img.shields.io/github/actions/workflow/status/AnatoliaLabs/Anatol-X/build.yml?style=for-the-badge&logo=github)
![Version](https://img.shields.io/badge/Version-Alpha_2-blue?style=for-the-badge)
![Base](https://img.shields.io/badge/Base-Debian_Testing-A81D33?style=for-the-badge&logo=debian)
![Kernel](https://img.shields.io/badge/Kernel-Liquorix-black?style=for-the-badge&logo=linux)
![Desktop](https://img.shields.io/badge/Desktop-KDE_Plasma-1D99F3?style=for-the-badge&logo=kde)

**Anatol-X** is a modern Linux distribution built on the stability of Debian, specifically optimized for desktop fluidity and gaming performance. It aims to deliver maximum performance, ultra-low latency, and a clean user experience completely free of unnecessary bloatware.

🌐 **Official Website:** [anatolialabs.github.io/Anatol-X](https://anatolialabs.github.io/Anatol-X)

---

## ✨ Key Features

- 🏎️ **Liquorix Kernel:** Pre-installed with the high-performance Liquorix kernel to provide unmatched responsiveness, low-latency execution, and smooth multimedia/gaming performance.
- 📦 **Debian Testing Base:** Powered by Debian Testing, giving you access to up-to-date software packages without sacrificing core system stability.
- 🧹 **Debloated & Minimal:** Built with APT `Recommends` completely disabled. You get only the essential system packages and a pristine **KDE Plasma** desktop environment.
- ⚙️ **Pure Systemd:** Cleaned of legacy SysVinit scripts, utilizing a modern, pure Systemd initialization stack.
- 💿 **Fast & Easy Installation:** Features the intuitive **Calamares** installer, allowing you to deploy the OS to your drive in just a few clicks.

## 📥 Download & Installation

Anatol-X is currently in the **Alpha 2** stage. You can safely download the latest ISO image via SourceForge:

[![Download Anatol-X](https://a.fsdn.com/con/app/sf-download-button)](https://sourceforge.net/projects/anatolialabs/files/latest/download)

### Installation Steps
1. Download the `.iso` file.
2. Flash it onto a USB drive (minimum 4GB) using tools like [BalenaEtcher](https://etcher.balena.io/), [Rufus](https://rufus.ie/), or [Ventoy](https://www.ventoy.net/).
3. Boot your PC from the USB drive.
4. Explore the Live environment and double-click the **Install System (Calamares)** icon on the desktop to install it permanently.

## 🛠️ Build from Source

Anatol-X values transparency and is built entirely using open-source tools (`live-build`). If you want to build or customize the image yourself, follow these methods.

### 1. Automated Build via GitHub Actions (Recommended)
This repository includes a pre-configured CI/CD pipeline. 
1. Fork this repository to your account.
2. Go to the **Actions** tab.
3. Select the **Anatol-X CI Build** workflow and click **Run workflow**. 
GitHub runners will compile the ISO and deploy it based on your workflow configurations.

### 2. Local Build
To compile the ISO locally, you will need a Debian/Ubuntu-based machine and the `live-build` toolkit:

```bash
# Install required dependencies
sudo apt update
sudo apt install debootstrap curl git make gettext po4a

# Clone and install the latest Live-Build from Debian Salsa
git clone https://salsa.debian.org/live-team/live-build.git
cd live-build
sudo make install
cd ..

# Clone the official Anatol-X repository
git clone https://github.com/AnatoliaLabs/Anatol-X.git
cd Anatol-X

# Configure and build the ISO
sudo lb config
sudo lb build

```


## 👥 Developers & Core Team

**Yusuf Baran Kolsuzoğlu** ([@TheL1even11](https://github.com/TheE1even11)) - Founder & Core Team

**Kağan Kırıktaş** ([@kagan-labs](https://github.com/kagan-labs)) - Founder & Core Team

**Cuma Turan Yenilmez** ([@cumaturanyenilmez-rgb](https://github.com/cumaturanyenilmez-rgb)) - Founder & Core Team


## 📬 Contact & Feedback

Since Anatol-X is in its Alpha phase, your feedback is incredibly valuable to us! If you encounter bugs or want to suggest new features, please open an issue in the [GitHub Issues](https://github.com/AnatoliaLabs/Anatol-X/issues) section.

For direct communication, you can reach the core team exclusively via the following official channels:

* ✉️ **Primary Email:** [anatoliaosf@proton.me](mailto:anatoliaosf@proton.me)
* ✉️ **Secondary Email:** [anatoliaosf@gmail.com](mailto:anatoliaosf@gmail.com)

*Note: We do not use or support any other official communication platforms at this time.*

## 📜 License & Acknowledgments

This project is open-source. We extend our gratitude to the amazing open-source communities that made this distribution possible:

* [The Debian Project](https://www.debian.org/)
* [The Liquorix Kernel Team](https://liquorix.net/)
* [KDE Plasma](https://kde.org/plasma-desktop/)
* [The Live-Build Team](https://salsa.debian.org/live-team)

---

*Anatol-X Linux - Performance in its purest form.*

