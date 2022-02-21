import glob, sys, os
import PySimpleGUI as sg
from PIL import Image

def make_gif(frame_folder, resize, crop, name):
	frames = [Image.open(image) for image in glob.glob(f"{frame_folder}/*.png")]
	if resize != 1.0:
		for frame in frames:
			frame.thumbnail((int(frame.size[0] * resize), int(frame.size[1] * resize)))
	cropped = []
	for frame in frames:
		cropped.append(frame.crop((crop[0], crop[1], frame.size[0] - crop[2], frame.size[1] - crop[3])))

	frame_one = cropped[0]
	frame_one.save("./results/" + name + ".gif", format="GIF", append_images=cropped[1:], save_all=True, duration=100, loop=0)
	print("created Gif " + "./results/" + name + ".gif " + "frame count: ", len(frames))

def unpackFrames(path):
	im = Image.open(path)
	name = path.split('/')[-1].split('.')[0]
	dir = path.split('/')[:-1]
	dir = '/'.join(dir)

	framesCount = im.n_frames
	if not os.path.exists(dir + "/" + name + "_unpack"):
		os.makedirs(dir + "/" + name + "_unpack")
	for i in range(framesCount):
		im.seek(i)
		num = str(i).zfill(3)
		im.save(f"{dir}/{name}_unpack/_{num}.png")
	print("unpacked to " + dir + "/" + name + "_unpack")

def processEvents(event, values):
	print(event)
	if event == 'Create':
		crop = (int(values['crop_left']), int(values['crop_top']), int(values['crop_right']), int(values['crop_bottom']))
		resize = float(values['resize'])
		frame_folder = values['frame_folder']
		name = values['name']
		make_gif(frame_folder, resize, crop, name)
	
	elif event == 'Unpack':
		file = sg.popup_get_file('Choose a gif', no_window=True)
		unpackFrames(file)

sg.theme('Reddit')

layout =   [[sg.Text("GIF Tool", font=("Helvetica", 25))],
			[sg.Text("Frames Path:"), sg.InputText("", key="frame_folder", size=(20, 1)), sg.FolderBrowse()],
			[sg.Text("Name"), sg.InputText("result", key="name", size=(20, 1))],
			[sg.Text("Resize:"), sg.InputText("1.0", key="resize", size=(7, 1))],
			[sg.Text("Crop Values:")],
			[sg.InputText("0", key="crop_top", size=(7, 1))],
			[sg.InputText("0", key="crop_left", size=(7, 1)), sg.InputText("0", key="crop_right", size=(7, 1))],
			[sg.InputText("0", key="crop_bottom", size=(7, 1))],
			[sg.Button("Create"), sg.Button("Unpack")],
]

window = sg.Window('Gif Tool', layout, grab_anywhere=True, element_justification='center')

while True:
	event, values = window.read()
	if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
		break
	
	processEvents(event, values)
	window.Refresh()
	
window.close()

