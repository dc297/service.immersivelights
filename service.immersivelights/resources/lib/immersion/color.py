import colorsys

class Color:
    def calc_next_rgb(target_rgb, current_rgb, difference):
        if abs(current_rgb - target_rgb) < difference:
            return target_rgb
        if target_rgb < current_rgb:
            current_rgb -= difference
        elif target_rgb > current_rgb:
            current_rgb += difference
        return current_rgb

    def calc_next_color(target_color, current_color, difference):
        curr_color = []
        for i in range(0, len(target_color)):
            curr_color.append(calc_next_rgb(target_color[i], current_color[i], difference))
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

    def calculate_brightness_gradient(target, current, steps):
        target_brightness = rgb_to_brightness(target)
        current_brightness = rgb_to_brightness(current)
        return lerp(target_brightness, current_brightness, steps)

    def get_saturated_color(color):
        """Increase the saturation of the current color."""
        hls = colorsys.rgb_to_hls(color[0] / 255, color[1] / 255, color[2] / 255)
        rgb_saturated = colorsys.hls_to_rgb(hls[0], 0.5, hls[1])
        return [int(rgb_saturated[0] * 255), int(rgb_saturated[1] * 255), int(rgb_saturated[2] * 255)]

    def calculate_gradient(target, current, saturated, max_steps):
        target = target
        current = current
        steps = calculate_steps(target, current, max_steps)
        if steps <= 1:
            return [target], [rgb_to_brightness(target)]
        color_gradient = lerp_vector(target, current, steps)
        color_gradient_saturated = [get_saturated_color(col) for col in color_gradient] if saturated else color_gradient
        brightness_gradient = calculate_brightness_gradient(target, current, steps)
        return color_gradient_saturated, brightness_gradient

    def to_terminal_color(rgb_color: list):
        return '\x1b[38;2;' + ';'.join([str(i) for i in rgb_color]) + 'm' + str(rgb_color) + '\x1b[0m'