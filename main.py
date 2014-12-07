from renderer import Renderer
from nodes import Checker, Flat, Gradient

# Create some nodes
checker = Checker(x_repeat=8, y_repeat=8, fuzz=0.01)
flat = Flat(color=(1.0, 1.0, 0.0, 1.0))
gradient = Gradient()

# Connect nodes
checker.get_port('color_1').connect(gradient)
checker.get_port('color_2').connect(flat)

# Render
canvas = Renderer(300, 300)
canvas.render(checker)
