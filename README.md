<div align="center">

<img src="assets/anatol-x-logo.png" alt="Anatol-X logo" width="180">

# Anatol-X Linux

**A desktop Linux experience built on Debian.**

[Website](https://anatolialabs.github.io/Anatol-X/) ·
[Anatolia Labs](https://anatolialabs.github.io/) ·
[Report an issue](https://github.com/AnatoliaLabs/Anatol-X/issues)

</div>

---

## About

**Anatol-X** is a Linux distribution in development by Anatolia Labs.
It brings together a Debian foundation, the KDE Plasma desktop, and
Anatolia Labs applications for gaming, productivity, and everyday use.

🚧 **Anatol-X is under development. A public stable release is coming soon.**

## What's planned

The current development configuration for the amd64 image includes:

- **Debian 13 Trixie** as the distribution base.
- **KDE Plasma 6**, with Wayland as the default session.
- The **Liquorix kernel** and matching headers.
- **Anatolium**, a system browser based on Firefox ESR.
- **KDE Discover**, with Flatpak as the preferred application source
  and Flathub configured.
- **Wine**, including 32-bit and 64-bit support.
- A custom **Anatol-X GRUB theme** for the live image and installed system.
- **Calamares** for graphical installation.
- Anatolia Labs applications and system packages from a
  signature-verified APT repository.

These features describe the development configuration and may change
before release. Recent changes still need testing in a booted image.

## Download

The public stable release is **not available yet**.

Download information and installation instructions will be shared on
the [Anatol-X website](https://anatolialabs.github.io/Anatol-X/) when
the release is ready.

## Compatibility notes

- **Architecture:** the current development image targets amd64 / x86-64.
- **Secure Boot:** Liquorix kernels are not signed for standard Secure
  Boot. Disabling Secure Boot may be necessary unless you use a suitable
  custom signing and enrollment setup.
- **Hardware:** graphics drivers, Wi-Fi, and other hardware should be
  tested on the intended device.
- **Wine:** compatibility varies by application. Some Windows software,
  games, and anti-cheat systems may not work.

## Packages and updates

Anatol-X uses APT for Debian and Anatolia Labs packages. The Anatol-X
APT repository is signed, and APT verifies repository signatures.

Flatpak and Flathub are also configured for application installation
through KDE Discover. Users can change their preferred source in
Discover's settings.

The Updater included in the development configuration is experimental
and remains a local package for now.

[Anatol-X APT repository →](https://github.com/AnatoliaLabs/anatol-x-apt)

## Development

Anatol-X is built using Debian's
[live-build](https://live-team.pages.debian.net/live-manual/) tools.
Development builds are intended for testing and may be incomplete or
change without notice.

The current image configuration is maintained separately during
development. The files in this public repository may not yet reflect
the latest development build.

## Developers & core team

- **Yusuf Baran Kolsuzoğlu** — [@TheE1even11](https://github.com/yusufbaran11)
- **Kağan Kırıktaş** — [@C-Stone-Labs](https://github.com/C-Stone-Labs)
- **Cuma Turan Yenilmez** — [@cumaturanyenilmez-rgb](https://github.com/cumaturanyenilmez-rgb)
- **Ali Turan Dal** — [@ATDNexus](https://github.com/ATDNexus)

## Feedback and contact

Found a problem or have an idea? Open an issue:

[GitHub Issues →](https://github.com/AnatoliaLabs/Anatol-X/issues)

For direct contact:

- **Primary email:** [anatoliaosf@proton.me](mailto:anatoliaosf@proton.me)
- **Secondary email:** [anatoliaosf@gmail.com](mailto:anatoliaosf@gmail.com)

## License and acknowledgments

This repository is licensed under the
[GNU General Public License v3.0](LICENSE). Individual packages and
third-party components may use their own licenses.

Thanks to the projects and communities that make Anatol-X possible:

- [Debian](https://www.debian.org/)
- [KDE Plasma](https://kde.org/plasma-desktop/)
- [Liquorix](https://liquorix.net/)
- [Debian Live](https://live-team.pages.debian.net/)

---

<div align="center">

**Anatol-X** · Made by Anatolia Labs

</div>
