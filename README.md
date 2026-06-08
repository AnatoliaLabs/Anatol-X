# 🚀 Anatol-X Linux

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/AnatoliaLabs/Anatol-X/.github/workflows/iso-builder.yml?branch=main&style=for-the-badge&label=ISO%20Build)
![License](https://img.shields.io/github/license/AnatoliaLabs/Anatol-X)
![Fedora Version](https://img.shields.io/badge/Fedora-44-darkblue?style=for-the-badge&logo=fedora)

**Anatol-X** is a modern, versatile, and robust Fedora-based Linux distribution crafted by **Anatolia Labs**. Our core mission is simple yet ambitious: **To cure the endless cycle of "Distro Hopping"** by providing everything a user could ever need in a single, bulletproof operating system.

---

## ✨ Key Features (Our Vision)

* **🦎 Chameleon Interface (Layout Switcher):** Change the entire desktop layout (macOS, Windows, Ubuntu, or Stock KDE/GNOME styles) with a single click. Never switch distros just for a change of scenery.
* **🌌 Infinite Package Universe:** Built on top of Fedora's stable core, Anatol-X comes pre-configured with Flatpak, Snap, RPM Fusion, and a seamless **Distrobox** integration. Want an Arch or Ubuntu package? Run it out of the box.
* **🛡️ Bulletproof System (Btrfs + Snapper):** Never worry about a broken system. Thanks to native Btrfs snapshotting, you can roll back to yesterday's working state directly from the GRUB bootloader menu.
* **👋 Anatol-X Welcome App:** A post-install wizard that lets you install proprietary drivers, your favorite web browsers, and gaming tools (Steam, Lutris, Heroic) with one-click efficiency.

---

## 📅 1-Month Development Roadmap

| Phase | Milestone | Status |
| :--- | :--- | :---: |
| **Week 1** | Base ISO Infrastructure & GitHub Actions CI/CD Setup | 🔄 In Progress |
| **Week 2** | Repository Integrations & Welcome App Development | ⏳ Pending |
| **Week 3** | Layout Switcher (Themes) & Performance Tuning | ⏳ Pending |
| **Week 4** | Bare-Metal Hardware Testing, Bug Fixing & v1.0 Stable Release | ⏳ Pending |

---

## 🛠️ Infrastructure & Automation

Anatol-X is fully automated and compiled in the cloud using **GitHub Actions**. Our CI/CD pipeline located in `.github/workflows/` utilizes Fedora's `kickstart` (`livecd-tools`) to build a fresh, secure, and ready-to-test `.iso` file on every single code push.

### Building Locally (For Developers)
If you want to build the ISO on your local machine:

```bash
git clone [https://github.com/AnatoliaLabs/Anatol-X.git](https://github.com/AnatoliaLabs/Anatol-X.git)
cd Anatol-X
sudo livecd-creator --config=config/anatol-x.ks --fslabel=
Anatol-X-Beta
```

## 👥 Anatolia Labs Team
Anatol-X is actively developed and maintained by a dynamic 3-person team during an intensive 1-month sprint:
 * **[[@TheE1even11](https://github.com/TheE1even11)]** - *ISO & Infrastructure (DevOps)*
 * **[[@cumaturanyenilmez-rgb](https://github.com/cumaturanyenilmez-rgb)]** - *Website administrator & Desktop Customization*
 * **[[@kagankiriktas80-create](https://github.com/kagankiriktas80-create)]** - *App Developer & Product Lead*

## 📄 License
Anatol-X is open-source software licensed under the **GNU General Public License v3.0 (GPL-3.0)**. You are free to share, modify, and distribute this project, provided that all derivatives remain open-source under the same terms. For more details, please refer to the [LICENSE](LICENSE) file.
