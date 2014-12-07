from PIL import Image
import math

im = Image.new('RGB', (350, 350))
pixels = im.load()


def clamp(x, min=0.0, max=1.0):
    if x < min:
        x = min
    elif x > max:
        x = max

    return x


def even(x):
    return int(x) % 2 == 0


def lerp(a, b, x):
    return a * x + (b * (1 - x))


def mix(ca, cb, x):
    return (lerp(ca[0], cb[0], x),
            lerp(ca[1], cb[1], x),
            lerp(ca[2], cb[2], x))


def odd(x):
    return not even(x)


def smoothstep(a, b, x):
    x = clamp((x - a) / (b - a))
    return x * x * (3 - 2 * x)


def wrap(x, min=0.0, max=1.0):
    x = x - int((x - min) / (max - min)) * (max - min)

    if x < 0:
        x = x + max - min

    return x


def gradient(s, t):
    return (smoothstep(0.0, 1.0, s),
            smoothstep(0.0, 1.0, t),
            smoothstep(0.0, 1.0, smoothstep(0.0, 1.0, s)))


def checker(s, t, xRepeat, yRepeat, fuzz=0.01):
    ss = s * xRepeat
    tt = t * yRepeat

    s = wrap(ss)
    t = wrap(tt)

    if (even(ss) and even(tt)) or (odd(ss) and odd(tt)):
        alpha = 1.0
    else:
        alpha = (
            smoothstep(1.0 - fuzz, 1.0, s) + (1 - smoothstep(0.0, fuzz, s)) +
            smoothstep(1.0 - fuzz, 1.0, t) + (1 - smoothstep(0.0, fuzz, t))
        )

    return mix((1.0, 1.0, 1.0), (0.0, 0.0, 0.0), alpha)

for x in range(im.size[0]):
    for y in range(im.size[1]):
        s = x / im.size[0]
        t = y / im.size[1]

        color = checker(s, t, 4, 4, fuzz=0.01)

        pixels[x, y] = (int(color[0] * 255),
                        int(color[1] * 255),
                        int(color[2] * 255))

im.show()
