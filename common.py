
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

def loadFrames(path):
	# load all frames of gif file into list of surfaces
	frames = []
	for file in glob.glob(path):
		frames.append(pygame.image.load(file))
	return frames
	