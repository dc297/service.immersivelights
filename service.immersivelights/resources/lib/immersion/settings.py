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
        self.mqtt_user: str
        self.mqtt_pwd: str
        self.mqtt_topic: str
        self.saturated_colors: bool
        self.saturation: float
        self.min_distance: float
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
        self.mqtt_user = settings.getString("hass_mqtt_user")
        self.mqtt_pwd = settings.getString("hass_mqtt_pwd")
        self.mqtt_topic = settings.getString("hass_mqtt_topic")
        self.saturated_colors = settings.getBool("saturated_colors")
        self.saturation = settings.getNumber("saturation")
        self.min_distance = settings.getNumber("min_distance")
        self._log_settings()

    def _log_settings(self) -> None:
        log = self._logger.debug
        log("Settings updated!")
        log(f"Hass ip:                {self.address}")
        log(f"Hass port:              {self.port}")
        log(f"Hass MQTT topic:        {self.mqtt_topic}")
        log(f"Hass MQTT user:         {self.mqtt_user}")
        log(f"enabled:                {self.enable}")
        log(f"enabled on screensaver: {self.enable_screensaver}")
        log(f"timeout:                {self.timeout}")
        log(f"capture width:          {self.capture_width}")
        log(f"framerate:              {self.framerate}")
        log(f"saturated colors:       {self.saturated_colors}")
        log(f"saturation:             {self.saturation}")
        log(f"min_distance:           {self.min_distance}")