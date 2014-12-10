import sys
from PIL import Image


class Renderer:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def render(self, node):
        im = Image.new('RGBA', (self.width, self.height))
        pixels = im.load()

        for x in range(self.width):
            for y in range(self.height):
                s = x / self.width
                t = y / self.height

                pixels[x, y] = tuple(int(x * 255) for x in node.compute(s, t))

            if x % 32 == 0:
                sys.stdout.write((str(int((x / im.size[0]) * 100)) + '%\r').rjust(10))
                sys.stdout.flush()

        im.show()
