
import tkinter, pygame, PIL, glob
from vector import *
from tkinter.filedialog import askopenfile

def browseFile():
	root = tkinter.Tk()
	root.withdraw()
	file = askopenfile(mode ='r', filetypes =[('Image Files', '*.png, *.jpg')])
	if file is not None: 
		return file.name

def colorValue(color):
	return color[0] * 0.3 + color[1] * 0.59 + color[2] * 0.11

def loadAndResize(path, scale):
	image = pygame.image.load(path)
	image = pygame.transform.scale(image, (tup2vec(image.get_size())/scale).vec2tupint())
	return image

def rgb2hsv(color):
    r, g, b, a = color
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = (df/mx)*100
    v = mx*100
    return (h, s, v)

def hsv2rgb(color):
	h, s, v = color
	h, s, v = h/360, s/100, v/100
	if s == 0.0:
		return (v, v, v)
	i = int(h*6)
	f = (h*6) - i
	p = v * (1 - s)
	q = v * (1 - s*f)
	t = v * (1 - s*(1-f))
	i = i % 6
	v = int(v * 255)
	t = int(t * 255)
	q = int(q * 255)

	if i == 0:
		return (v, t, p)
	elif i == 1:
		return (q, v, p)
	elif i == 2:
		return (p, v, t)
	elif i == 3:
		return (p, q, v)
	elif i == 4:
		return (t, p, v)
	elif i == 5:
		return (v, p, q)