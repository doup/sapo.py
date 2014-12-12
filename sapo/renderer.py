import sys


class PillowRender:
    def __init__(self, image):
        self.width = image.size[0]
        self.height = image.size[1]
        self.im = image
        self.pixels = image.load()

    def render(self, node):
        for x in range(self.width):
            for y in range(self.height):
                s = x / self.width
                t = y / self.height

                self.pixels[x, y] = tuple(int(x * 255) for x in node.compute(s, t))

            if x % 32 == 0:
                sys.stdout.write((str(int((x / self.width) * 100)) + '%\r').rjust(10))
                sys.stdout.flush()

        self.im.show()
