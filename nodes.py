from utils import blend, clamp, even, mix, odd, smoothstep, wrap
import math


class Port:
    def __init__(self, type, value):
        self.debuggable = type in ('point',)
        self.is_connected = False
        self.node = None
        self.type = type
        self.value = value

    def connect(self, node):
        self.is_connected = True
        self.node = node

        return self

    def disconnect(self):
        self.is_connected = False
        self.node = None

        return self

    def get(self, s, t):
        if self.is_connected:
            return self.node.get(s, t)
        else:
            return self.value


class Node:
    def __init__(self, **args):
        self.debug = False       # Visual debug
        self.debuggable = False  # True if there are debuggable ports
        self.ports = {}
        self.type = None

        self.define()

        # Check if node can have visual debug
        for key, port in self.ports.items():
            # Only color nodes with debuggable ports can have visual debug
            if port.debuggable and (self.type is 'color'):
                self.debuggable = True

        # Update port values with args
        for key, value in args.items():
            if key in self.ports:
                self.ports[key].value = value

    def define(self):
        pass

    def add_port(self, key, type, value):
        self.ports[key] = Port(type, value)

    def compute(self, s, t):
        value = self.get(s, t)

        if self.debug and self.debuggable:
            return blend(value, (1.0, 0.0, 1.0, 0.4))
        else:
            return value

    def get(self, s, t):
        return (0.0, 0.0, 0.0, 0.0)

    def get_port(self, key):
        if key in self.ports:
            return self.ports[key]


class Checker(Node):
    def define(self):
        self.type = 'color'
        self.add_port('color_1', 'color', (1.0, 1.0, 1.0, 1.0))
        self.add_port('color_2', 'color', (0.1, 0.1, 0.1, 1.0))
        self.add_port('x_repeat', 'int', 4)
        self.add_port('y_repeat', 'int', 4)
        self.add_port('fuzz', 'float', 0.01)

    def get(self, s, t):
        x_repeat = self.get_port('x_repeat').get(s, t)
        y_repeat = self.get_port('y_repeat').get(s, t)
        fuzz = self.get_port('fuzz').get(s, t)
        is_inverted = False

        # Let's calculate in wich column and row we are.
        column = int(s * x_repeat)
        row = int(t * y_repeat)

        # Scale the fuzz using the smallest repeat, and
        # set it to the half, as we share the fuzz between
        # two tiles.
        fuzz = (fuzz / (1 / (y_repeat if x_repeat > y_repeat else x_repeat))) / 2.0

        # When the column and row are not even, or are not odd,
        # we invert the colors. So, color_1 = color_2 and
        # color_2 = color_1
        if (not (even(column) and even(row))) and (not (odd(column) and odd(row))):
            is_inverted = True

        # Tile the coordinates so that we have ss and tt,
        # which range between 0 and 1.0.
        ss = wrap(s * x_repeat)
        tt = wrap(t * y_repeat)

        #  ____          __
        # |\  /|        |\ |
        # | \/ |        | \|         __
        # | /\ |   =>   | /|   =>   | /|
        # |/__\|        |/_|        |/_|
        #
        # We "fold" the coordinates to simplify the edge
        # detection. ss and tt would range in [ 0, 0.5 )
        #
        ss = ss if ss < 0.5 else 0.5 - (ss - 0.5)
        tt = tt if tt < 0.5 else 0.5 - (tt - 0.5)

        # If we are in the upper triangle we do a simetry.
        # So that we even simplify more the operation.
        if tt > ss:
            ss, tt = tt, ss

        # If we are in the fuzz range we do a gradient between
        # the two colors. Otherwise we just return a plain color.
        #
        # ^tt   /|
        # |    / |
        # |   /__| <- Fuzz range
        # |  /___|
        # |--------->ss
        # 0,0
        #
        if tt < fuzz:
            color_1 = self.get_port('color_1').get(s, t)
            color_2 = self.get_port('color_2').get(s, t)

            if is_inverted:
                color_1, color_2 = color_2, color_1

            fuzz = ((tt / fuzz) / 2.0) + 0.5
            fuzz = smoothstep(0.0, 1.0, fuzz)

            return mix(color_1, color_2, 1.0 - fuzz)
        else:
            if is_inverted:
                return self.get_port('color_2').get(s, t)
            else:
                return self.get_port('color_1').get(s, t)


class Color2Int(Node):
    def define(self):
        self.type = 'int'
        self.add_port('color', 'color', (1.0, 1.0, 1.0, 1.0))
        self.add_port('channel', 'int', 0)
        self.add_port('min', 'int', 0)
        self.add_port('max', 'int', 10)

    def get(self, s, t):
        color = self.get_port('color').get(s, t)
        channel = self.get_port('channel').get(s, t)
        min = self.get_port('min').get(s, t)
        max = self.get_port('max').get(s, t)

        if max < min:
            max, min = min, max

        return int((color[channel] * (max - min)) + min)


class Color2Float(Node):
    def define(self):
        self.type = 'float'
        self.add_port('color', 'color', (1.0, 1.0, 1.0, 1.0))
        self.add_port('channel', 'int', 0)
        self.add_port('min', 'float', 0.0)
        self.add_port('max', 'float', 1.0)

    def get(self, s, t):
        color = self.get_port('color').get(s, t)
        channel = self.get_port('channel').get(s, t)
        min = self.get_port('min').get(s, t)
        max = self.get_port('max').get(s, t)

        if max < min:
            max, min = min, max

        return (color[channel] * (max - min)) + min


class Flat(Node):
    def define(self):
        self.type = 'color'
        self.add_port('color', 'color', (1.0, 1.0, 1.0, 1.0))

    def get(self, s, t):
        return self.get_port('color').get(s, t)


class Gradient(Node):
    def define(self):
        self.type = 'color'

    def get(self, s, t):
        return (smoothstep(0.0, 1.0, s),
                smoothstep(0.0, 1.0, t),
                smoothstep(0.0, 1.0, smoothstep(0.0, 1.0, s)),
                1.0)


class Offset(Node):
    def define(self):
        self.type = 'color'
        self.add_port('color', 'color', (1.0, 1.0, 1.0, 1.0))
        self.add_port('x', 'float', 0.5)
        self.add_port('y', 'float', 0.5)

    def get(self, s, t):
        return self.get_port('color').get(
            wrap(s + self.get_port('x').get(s, t)),
            wrap(t + self.get_port('y').get(s, t))
        )


class Scales(Node):
    def define(self):
        self.add_port('x_repeat', 'int', 4)
        self.add_port('y_repeat', 'int', 6)
        self.add_port('shadow', 'color', (0.318, 0.267, 0.157, 1.0))
        self.add_port('color', 'color', (0.902, 0.882, 0.816, 1.0))
        self.add_port('highlight', 'color', (0.984, 0.984, 0.992, 1.0))
        self.add_port('type', 'int', 0)

    def get(self, s, t):
        x_repeat = self.get_port('x_repeat').get(s, t)
        y_repeat = self.get_port('y_repeat').get(s, t)
        shadow = self.get_port('shadow').get(s, t)
        color = self.get_port('color').get(s, t)
        highlight = self.get_port('highlight').get(s, t)
        type = self.get_port('type').get(s, t)

        # Let's calculate in wich column and row we are.
        column = int(s * x_repeat)
        row = int(t * y_repeat)

        # New coordinates
        ss = wrap(s * x_repeat)
        tt = wrap(t * y_repeat)

        if (odd(row)):
            ss = wrap(ss + 0.5)

        # Fold coordinates
        #  ____        __
        # |\  /|      |\ |
        # |_\/_|  =>  |_\|
        #
        ss = ss if ss < 0.5 else 0.5 - (ss - 0.5)

        # Calculate cut height for the given ss
        # Separates the top and bot region of the scale
        #        ss
        #       __|_
        #      |\   |  TOP TRIANGLE
        #      | \. |_ cut
        # BOT  |  \ |
        # TRI. |___\|
        if type == 0:
            cut = math.sin(ss * math.pi)
        elif type == 1:
            cut = clamp(ss * 3.0)
        else:
            cut = ss * 2.0

        # DRAWING
        # Width of the scale border
        border = 0.08
        border = border + (border * (1 - cut)) * 0.5  # modulate width

        # Mid position (%) when border color is darkest
        # ROTATED visualization:
        #
        #          mid
        #           .
        #        .   .
        #     .       .
        #     ######### <- border
        #     ^       ^
        #     Start   End
        #  ----------------> tt
        mid = 0.6

        # Border position
        border_start = cut - border
        border_mid = border_start + (mid * border)
        border_end = cut

        # Change origin based on triangle (top/bot)
        if tt < border_mid:
            origin = (0.5, -1.0)
        else:
            origin = (0.0, 0.0)

        # Calculate distance to scale origin
        # Multiply horizontal (x2.5) axis to exagerate roundness
        dist = math.hypot((ss - origin[0]) * 2.5, tt - origin[1])

        # Calculate color
        color = mix(highlight, color, smoothstep(0.0, 1.0, (dist * 1.25) - 0.75))  # Highlight
        color = mix(shadow, color, smoothstep(0.0, 1.0, (tt - origin[1]) * 2.7))   # Origin shadow

        # Scale shadow
        cut = (math.sin((ss + origin[0]) * math.pi) * 1.2) - 0.85
        color = mix(shadow, color, smoothstep(0.0, 1.0, tt - origin[1] - cut))

        # Border Highlight
        hl_width = 0.15
        hl_start = border_start - hl_width
        hl_end = hl_start + hl_width

        if tt > hl_start and tt <= hl_end:
            pos = (tt - hl_start) / hl_width
            color = mix(color, highlight, (
                smoothstep(0.0, 1.0, ss * 2) *       # Horizontal control
                smoothstep(0.0, 1.0, pos * 2) *      # Start slope _/'
                smoothstep(0.0, 1.0, 2 - pos * 2) *  # End slope '\_
                0.3                                  # Reduce intensity
            ))

        # Draw border
        if tt > border_start and tt <= border_end:
            # Map from border_start = 0.0 to border_end = 1.0
            #    |
            #    |  border_start -------
            # tt |
            #    |  border_end   -------
            #    v
            pos = (tt - border_start) / border

            return mix(color, shadow, (
                smoothstep(0.0, 1.0, clamp(pos / mid)) *
                smoothstep(1.0, 0.0, clamp((pos - mid) / (1 - mid))) *
                0.5
            ))
        else:
            return color


class WaveDistort(Node):
    def define(self):
        self.type = 'color'
        self.add_port('color', 'color', (1.0, 1.0, 1.0, 1.0))
        self.add_port('x_freq', 'int', 2)
        self.add_port('x_amp', 'float', 0.05)
        self.add_port('y_freq', 'int', 2)
        self.add_port('y_amp', 'float', 0.1)

    def get(self, s, t):
        x_freq = self.get_port('x_freq').get(s, t) * 2 * math.pi
        y_freq = self.get_port('y_freq').get(s, t) * 2 * math.pi

        ss = s + math.sin(t * x_freq) * self.get_port('x_amp').get(s, t)
        tt = t + math.cos(s * y_freq) * self.get_port('y_amp').get(s, t)

        ss = wrap(ss)
        tt = wrap(tt)

        return self.get_port('color').get(ss, tt)
