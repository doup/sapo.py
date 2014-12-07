from utils import even, mix, odd, smoothstep, wrap


class Port:
    def __init__(self, type, value):
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

    def set_value(self, value):
        self.value = value

        return self


class Node:
    def __init__(self, **args):
        self.ports = {}
        self._init()

        for port, value in args.items():
            if port in self.ports:
                self.ports[port].set_value(value)

    def add_port(self, key, type, value):
        self.ports[key] = Port(type, value)

    def get_port(self, key):
        if key in self.ports:
            return self.ports[key]

    def _init(self):
        pass

    def get(self, s, t):
        return (0.0, 0.0, 0.0, 0.0)


class Checker(Node):
    def _init(self):
        self.add_port('color_1', 'color', (1.0, 1.0, 1.0, 1.0))
        self.add_port('color_2', 'color', (0.0, 0.0, 0.0, 1.0))
        self.add_port('x_repeat', 'int', 4)
        self.add_port('y_repeat', 'int', 4)
        self.add_port('fuzz', 'float', 0.01)

    def get(self, s, t):
        color_1 = self.get_port('color_1').get(s, t)
        color_2 = self.get_port('color_2').get(s, t)
        x_repeat = self.get_port('x_repeat').get(s, t)
        y_repeat = self.get_port('y_repeat').get(s, t)
        fuzz = self.get_port('fuzz').get(s, t)

        ss = s * x_repeat
        tt = t * y_repeat

        s = wrap(ss)
        t = wrap(tt)

        if (even(ss) and even(tt)) or (odd(ss) and odd(tt)):
            alpha = 1.0
        else:
            alpha = (
                smoothstep(1.0 - fuzz, 1.0, s) +
                (1 - smoothstep(0.0, fuzz, s)) +
                smoothstep(1.0 - fuzz, 1.0, t) +
                (1 - smoothstep(0.0, fuzz, t))
            )

        return mix(color_1, color_2, alpha)


class Flat(Node):
    def _init(self):
        self.add_port('color', 'color', (1.0, 1.0, 1.0, 1.0))

    def get(self, s, t):
        return self.get_port('color').get(s, t)


class Gradient(Node):
    def get(self, s, t):
        return (smoothstep(0.0, 1.0, s),
                smoothstep(0.0, 1.0, t),
                smoothstep(0.0, 1.0, smoothstep(0.0, 1.0, s)),
                1.0)
