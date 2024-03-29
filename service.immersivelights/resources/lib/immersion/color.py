import colorsys, math
from resources.lib.immersion.settings import SettingsManager

class Color:
    def __init__(self, settings: SettingsManager):
        self.settings = settings

    def calc_next_rgb(target_rgb, current_rgb, difference):
        if abs(current_rgb - target_rgb) < difference:
            return target_rgb
        if target_rgb < current_rgb:
            current_rgb -= difference
        elif target_rgb > current_rgb:
            current_rgb += difference
        return current_rgb

    def calc_next_color(self, target_color, current_color, difference):
        curr_color = []
        for i in range(0, len(target_color)):
            curr_color.append(self.calc_next_rgb(target_color[i], current_color[i], difference))
        return curr_color

    def clamp(rgb, low, high):
        return min(high, max(low, rgb))

    def lerp(target, current, steps):
        result = []
        delta = (target - current) / steps
        for i in range(0, steps):
            result.append(int(current + delta * (i + 1)))
        return result

    def lerp_vector(target, current, steps):
        result = []
        deltas = [(target[i] - current[i]) / steps for i in range(0, len(target))]
        for i in range(0, steps):
            result_i = []
            for j in range(0, len(target)):
                result_i.append(int(current[j] + deltas[j] * (i + 1)))
            result.append(result_i)
        return result

    def calculate_steps(target, current, max_steps):
        max_difference = max([abs(target[i] - current[i]) for i in range(0, len(target))])
        return int((max_difference * max_steps) / 255)

    def rgb_to_brightness(color):
        hls = colorsys.rgb_to_hls(color[0] / 255, color[1] / 255, color[2] / 255)
        return int(hls[1] * 255)

    def calculate_brightness_gradient(self, target, current, steps):
        target_brightness = self.rgb_to_brightness(target)
        current_brightness = self.rgb_to_brightness(current)
        return self.lerp(target_brightness, current_brightness, steps)

    def get_saturated_color(self, color):
        """Increase the saturation of the current color."""
        hls = colorsys.rgb_to_hls(color[0] / 255, color[1] / 255, color[2] / 255)
        rgb_saturated = colorsys.hls_to_rgb(hls[0], self.settings.saturation, hls[1])
        return [int(rgb_saturated[0] * 255), int(rgb_saturated[1] * 255), int(rgb_saturated[2] * 255)]

    def calculate_gradient(self, target, current, saturated, max_steps):
        target = target
        current = current
        steps = self.calculate_steps(target, current, max_steps)
        if steps <= 1:
            return [target], [self.rgb_to_brightness(target)]
        color_gradient = self.lerp_vector(target, current, steps)
        color_gradient_saturated = [self.get_saturated_color(col) for col in color_gradient] if saturated else color_gradient
        brightness_gradient = self.calculate_brightness_gradient(target, current, steps)
        return color_gradient_saturated, brightness_gradient

    def to_terminal_color(rgb_color: list):
        return '\x1b[38;2;' + ';'.join([str(i) for i in rgb_color]) + 'm' + str(rgb_color) + '\x1b[0m'
    
    def close_enough(rgb1, rgb2, min_difference):
        if rgb1 is None or rgb2 is None:
            return False

        hls1 = colorsys.rgb_to_hls(rgb1[0] / 255, rgb1[1] / 255, rgb1[2] / 255)
        hls2 = colorsys.rgb_to_hls(rgb2[0] / 255, rgb2[1] / 255, rgb2[2] / 255)

        # calculate the distance between two points in the hls cylinder
        distance = math.dist(hls1, hls2)

        # the maximum distance possible in the hls cylinder is sqrt(5) 
        # which is distance between two points on a cylinder is the length 
        # of the hypotenuse of the right-angled triangle formed by the 
        # cylinder's diameter (in this case 2 since s (radius) varies from range 0 to 1) 
        # and height (in this case 1 since l (height) varies from range 0 to 1). So, the 
        # max distance can be sqrt(2 ^ 2 + 1 ^ 2).
        max_distance = math.sqrt(5)

        
        return min_difference > (distance/max_distance)