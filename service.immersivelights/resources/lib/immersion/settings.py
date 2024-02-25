"""
Kodi video capturer for Hyperion.

Copyright (c) 2013-2023 Hyperion Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from resources.lib.immersion.logger import Logger

if TYPE_CHECKING:
    import xbmcaddon


class SettingsManager:
    """Class which contains all addon settings."""

    def __init__(self, settings: xbmcaddon.Settings, logger: Logger) -> None:
        self._logger = logger
        self.rev = 0
        self._settings = settings
        self.address = "localhost"
        self.port = 19445
        self.enable: bool
        self.enable_screensaver: bool
        self.timeout: int
        self.capture_width: int
        self.framerate: int
        self.sleep_time: int
        self.token: str
        self.entity_name: str
        self.saturated_colors: bool
        self.read_settings()

    def read_settings(self) -> None:
        """Read all settings."""
        settings = self._settings
        self.enable = settings.getBool("enable")
        self.enable_screensaver = settings.getBool("screensaver_enable")
        self.timeout = settings.getInt("reconnect_timeout")
        self.capture_width = settings.getInt("capture_width")
        self.framerate = settings.getInt("framerate")
        self.sleep_time = int(1.0 / self.framerate * 1000)
        self.address = settings.getString("hass_ip")
        self.port = settings.getInt("hass_port")
        self.rev += 1
        self.token = settings.getString("hass_token")
        self.entity_name = settings.getString("hass_entity")
        self.saturated_colors = settings.getBool("saturated_colors")
        self._log_settings()

    def _log_settings(self) -> None:
        log = self._logger.debug
        log("Settings updated!")
        log(f"Hass ip:                {self.address}")
        log(f"Hass port:              {self.port}")
        log(f"Hass entity name:       {self.entity_name}")
        log(f"enabled:                {self.enable}")
        log(f"enabled on screensaver: {self.enable_screensaver}")
        log(f"timeout:                {self.timeout}")
        log(f"capture width:          {self.capture_width}")
        log(f"framerate:              {self.framerate}")
        log(f"saturated colors:       {self.saturated_colors}")