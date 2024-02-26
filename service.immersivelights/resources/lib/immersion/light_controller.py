from resources.lib.immersion.settings import SettingsManager
from resources.lib.immersion.logger import Logger
from resources.lib.immersion.color import Color
import resources.lib.paho.mqtt.client as mqtt
import json

class LightController:
    def __init__(self, settings: SettingsManager, logger: Logger) -> None:
        self.settings = settings
        self._logger = logger
        self.last_color = None
        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.mqttc.on_connect = self.on_connect
        self.mqttc.username_pw_set(settings.mqtt_user, settings.mqtt_pwd)
        logger.debug('Connecting to ' + settings.address + ':' + str(settings.port) + ' using ' + settings.mqtt_user)
        self.mqttc.connect(settings.address, settings.port, 60)
        self.mqttc.loop_start()

    def __del__(self) -> None:
        """Destructor."""
        # close the connection
        self.mqttc.disconnect()

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, reason_code, properties):
        self._logger.debug(f"Connected with result code {reason_code}")


    def set_color(
        self, color_rgb
    ) -> None:
        if self.last_color == color_rgb or Color.close_enough(self.last_color, color_rgb, self.settings.min_distance):
            self._logger.debug('skipping setting color to ' + Color.to_terminal_color(color_rgb))
            return
        
        brightness = Color.rgb_to_brightness(color_rgb)

        try:
            self._logger.info('setting color to ' + Color.to_terminal_color(color_rgb) + ' brightness: ' + str(brightness))
            data = {
                "rgb_color": color_rgb,
                "brightness": brightness,
            }
            self._logger.debug('Publishing ' + json.dumps(data))
            self.mqttc.publish(self.settings.mqtt_topic, json.dumps(data))
            self.last_color = color_rgb
        except:
            self._logger.error('failed to update light color')
            pass