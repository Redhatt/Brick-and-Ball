import random
from collections.abc import Iterable

colors = {
		'red'	 : (255,0,0),
		'lime'	 : (0,255,0),
		'blue'	 : (0,0,255),
		'yellow' : (255,255,0),
		'cyan'	 : (0,255,255),
		'magenta': (255,0,255),
		'silver' : (152,152,152),
		'gray'	 : (128,128,128),
		'maroon' : (128,0,0),
		'olive'	 : (128,128,0),
		'green'	 : (0,128,0),
		'purple' : (128,0,128),
		'teal'	 : (0,128,128),
		'navy'	 : (0,0,128)
}

backgroud = {
	'white': (200, 200, 200),
	'black': (0, 0, 0)
}

def clr(color=None, space=False):
	c = [255,0,0]
	if space:
		c = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
	elif color is None:
		c = random.choice(tuple(colors.values()))
	else:
		if color in colors.keys():
			c = colors[color]
		elif color in backgroud.keys():
			c =	backgroud[color]
		elif isinstance(color, Iterable):
			for i in range(len(color)):
				c[i] = color[i]
			for i in range(len(color), 3):
				c[i] = color[-1]
		elif isinstance(color, int):
			c = (color, color, color)

	return tuple(c)



