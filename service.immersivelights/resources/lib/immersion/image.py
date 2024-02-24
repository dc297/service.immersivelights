from PIL import Image
from resources.lib.immersion.color import Color

class ImageUtils:
    def extract_color(saturated: bool, image: Image):
        bbox = image.convert("RGB").getbbox()
        if bbox:
            image = image.crop(bbox)
        
        palette = image.quantize(colors=1).getpalette()
        dominant_color = [palette[i:i + 3] for i in range(0, 3, 3)][0]
        result_color = dominant_color if not saturated else Color.get_saturated_color(dominant_color)
        return (result_color, Color.rgb_to_brightness(result_color))