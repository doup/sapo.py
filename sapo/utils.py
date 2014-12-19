import math

# Probably needs a fix
def blend(cbot, ctop):
    return (lerp(cbot[0], ctop[0], ctop[3]),
            lerp(cbot[1], ctop[1], ctop[3]),
            lerp(cbot[2], ctop[2], ctop[3]),
            lerp(cbot[3], ctop[3], ctop[3]))


def clamp(x, min=0.0, max=1.0):
    if x < min:
        x = min
    elif x > max:
        x = max

    return x


def distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def even(x):
    return int(x) % 2 == 0


def lerp(a, b, x):
    return (a * (1 - x)) + (b * x)


def mix(ca, cb, x):
    return (lerp(ca[0], cb[0], x),
            lerp(ca[1], cb[1], x),
            lerp(ca[2], cb[2], x),
            lerp(ca[3], cb[3], x))


def odd(x):
    return not even(x)


# Probably needs a fix
def smoothstep(a, b, x):
    x = clamp((x - a) / (b - a))
    return x * x * (3 - 2 * x)


def wrap(x, min=0.0, max=1.0):
    x = x - int((x - min) / (max - min)) * (max - min)

    if x < 0:
        x = x + max - min

    return x
