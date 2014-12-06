from PIL import Image

im = Image.new('RGB', (256, 256))
pixels = im.load()


def gradient(s, t):
    return (s, t, 0.5)

for x in range(im.size[0]):
    for y in range(im.size[1]):
        s = x / im.size[0]
        t = y / im.size[1]

        color = gradient(s, t)

        pixels[x, y] = (int(color[0] * 255),
                        int(color[1] * 255),
                        int(color[2] * 255))

im.show()
