from resources.lib.immersion.settings import SettingsManager
from resources.lib.immersion.logger import Logger
from resources.lib.immersion.color import Color
import requests
import json

class LightController:
    def __init__(self, settings: SettingsManager, logger: Logger) -> None:
        self.settings = settings
        self._logger = logger
        self.url = "http://" + settings.address + ":" + str(settings.port) + "/api/services/light/turn_on"
        self.headers = {
            "Authorization": "Bearer " + self.settings.token,
            "content-type": "application/json",
        }
        pass
    
    def set_color(
        self, color_brightness
    ) -> None:
        (color_rgb, brightness) = color_brightness
        self._logger.info('setting color to ' + Color.to_terminal_color(color_rgb) + ' brightness: ' + str(brightness))
        try:
            data = {
                "entity_id": self.settings.entity_name,
                "rgb_color": color_rgb,
                "brightness": brightness,
                "transition": 1
                }

            response = requests.request('post', self.url, headers=self.headers, data=json.dumps(data))
            if response.status_code != 200:
                print(response.text)
        except:
            self._logger.error('failed to update light color')
            pass