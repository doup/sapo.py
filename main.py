from PIL import Image
from sapo.renderer import PillowRender
from sapo.nodes import (Checker, Color2Int, Color2Float, Flat, Gradient,
                        Offset, Scales, WaveDistort)

canvas = PillowRender(Image.new('RGBA', (300, 300)))
"""
# Create some nodes
checker = Checker(x_repeat=8, y_repeat=8, fuzz=0.1)
color2int = Color2Int(min=2, max=8)
color2float = Color2Float(min=0.01, max=0.05, channel=1)
flat = Flat(color=(0.9, 0.9, 0.9, 1.0))
gradient = Gradient()
offset = Offset(x=0.25, y=0.25)
wave = WaveDistort(x_freq=4, x_amp=0.05, y_freq=4, y_amp=0.05)

# Connect nodes
color2int.get_port('color').connect(gradient)
color2float.get_port('color').connect(gradient)

#checker.get_port('color_1').connect(gradient)
#checker.get_port('color_2').connect(flat)
#checker.get_port('x_repeat').connect(color2int)
#checker.get_port('fuzz').connect(color2float)
checker.debug = True

wave.get_port('color').connect(checker)

offset.get_port('color').connect(wave)

# Render

#canvas.render(checker)
#canvas.render(offset)

checker2 = Checker(x_repeat=8, y_repeat=8)
c2f2 = Color2Float(min=0.01, max=0.1)
c2f2.get_port('color').connect(wave)
checker2.get_port('fuzz').connect(c2f2)
canvas.render(checker2)
"""
"""
# 1) Checker pattern
checker = Checker(x_repeat=8, y_repeat=8, fuzz=0.01)
wave = WaveDistort(x_freq=4, x_amp=0.05, y_freq=4, y_amp=0.05)
wave.get_port('color').connect(checker)
canvas.render(wave)
"""
"""
# 2) WaveDistorted pattern as fuzz input for checker, oil painting? :-)
base = Checker(x_repeat=8, y_repeat=8, fuzz=0.1)
wave = WaveDistort(x_freq=4, x_amp=0.05, y_freq=4, y_amp=0.05)
checker = Checker(x_repeat=8, y_repeat=8)
fuzzC2F = Color2Float(min=0.01, max=0.1)

wave.get_port('color').connect(base)
fuzzC2F.get_port('color').connect(wave)
checker.get_port('fuzz').connect(fuzzC2F)

canvas.render(checker)
"""

# 3) Scales
scales = Scales(x_repeat=4, y_repeat=6)
canvas.render(scales)
