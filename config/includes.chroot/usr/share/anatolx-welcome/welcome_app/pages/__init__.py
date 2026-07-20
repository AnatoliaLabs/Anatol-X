"""Hoşgeldin uygulamasının sihirbaz sayfaları."""

from welcome_app.pages.apps_page import AppsPage
from welcome_app.pages.community_page import CommunityPage
from welcome_app.pages.post_install_page import PostInstallPage
from welcome_app.pages.system_page import SystemInfoPage
from welcome_app.pages.welcome_page import WelcomePage

__all__ = [
    "WelcomePage",
    "SystemInfoPage",
    "PostInstallPage",
    "AppsPage",
    "CommunityPage",
]
