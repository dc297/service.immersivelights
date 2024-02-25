from PIL import Image
from resources.lib.immersion.color import Color
from resources.lib.immersion.settings import SettingsManager

class ImageUtils:
    def __init__(self, settings: SettingsManager):
        self.settings = settings
        self.color = Color(settings)
        self.saturated = settings.saturated_colors

    def extract_color(self, image: Image):
        bbox = image.getbbox()
        if bbox:
            image = image.crop(bbox)
        
        palette = image.quantize(colors=1).getpalette()
        dominant_color = [palette[i:i + 3] for i in range(0, 3, 3)][0]
        return dominant_color if not self.saturated else self.color.get_saturated_color(dominant_color)
