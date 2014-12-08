from renderer import Renderer
from nodes import Checker, Color2Int, Flat, Gradient

# Create some nodes
checker = Checker(x_repeat=8, y_repeat=8, fuzz=0.01)
color2int = Color2Int(min=2, max=8)
flat = Flat(color=(1.0, 1.0, 0.0, 1.0))
gradient = Gradient()

# Connect nodes
color2int.get_port('color').connect(gradient)

checker.get_port('color_1').connect(gradient)
checker.get_port('color_2').connect(flat)
checker.get_port('x_repeat').connect(color2int)

# Render
canvas = Renderer(300, 300)
canvas.render(checker)
