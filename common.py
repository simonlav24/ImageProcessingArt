
import tkinter
from tkinter.filedialog import askopenfile

def browseFile():
	root = tkinter.Tk()
	root.withdraw()
	file = askopenfile(mode ='r', filetypes =[('Image Files', '*.png, *.jpg')])
	if file is not None: 
		return file.name

def colorValue(color):
	return color[0] * 0.3 + color[1] * 0.59 + color[2] * 0.11