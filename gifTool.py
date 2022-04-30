import glob, sys, os
import PySimpleGUI as sg
from PIL import Image
import ast

def make_gif(values, frame_folder, resize, crop, name, skip_frames):
	frames = [Image.open(image) for image in glob.glob(f"{frame_folder}/*.png")]
	frames = [frames[i] for i in range(values['start_frame'], values['end_frame'], skip_frames)]
	if resize != 1.0:
		width, height = frames[0].size
		for i in range(len(frames)):
			frames[i] = frames[i].resize((int(width * resize), int(height * resize)), Image.NEAREST)
			# frame.thumbnail((int(frame.size[0] * resize), int(frame.size[1] * resize)))
	cropped = []
	for frame in frames:
		cropped.append(frame.crop((crop[0], crop[1], frame.size[0] - crop[2], frame.size[1] - crop[3])))

	frame_one = cropped[0]
	frame_one.save(f"{name}.png")
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
		skip_frames = int(values['skip_frame'])
		make_gif(values, frame_folder, resize, crop, name, skip_frames)
	
	elif event == 'Unpack':
		file = sg.popup_get_file('Choose a gif', no_window=True)
		unpackFrames(file)

	elif event == 'frame_folder':
		# find a png file in the folder
		files = glob.glob(f"{values['frame_folder']}/*.png")
		window.Element('end_frame').Update(len(files) - 1)
			
# load the settings
settings = None
if os.path.exists('gifTool.ini'):
	with open('gifTool.ini', 'r') as f:
		settings = ast.literal_eval(f.read())
if settings is None:
	settings = {
		'frame_folder': '',
		'crop_left': 0,
		'crop_top': 0,
		'crop_right': 0,
		'crop_bottom': 0,
		'resize': 1.0,
		'start_frame': 0,
		'end_frame': 0,
		'name': 'animation',
		'skip_frame': 1
	}

sg.theme('Reddit')
layout =   [[sg.Text("GIF Tool", font=("Helvetica", 25))],
			[sg.Text("Frames Path:"), sg.InputText(settings['frame_folder'], enable_events=True, key="frame_folder", size=(20, 1)), sg.FolderBrowse(enable_events=True, key="browse_folder")],
			[sg.Text("Name"), sg.InputText(settings['name'], key="name", size=(20, 1))],
			[sg.Text("Resize:"), sg.InputText(settings['resize'], key="resize", size=(7, 1))],
			[sg.Text("Step Frames:"), sg.Spin([i for i in range(0, 9)], size=(6, 1), initial_value=settings['skip_frame'], key="skip_frame")],
			[sg.Text("Start Frame:"), sg.Spin([i for i in range(0, 300)], size=(6, 1), initial_value=settings['start_frame'], key="start_frame"),
			 sg.Text("End Frame:"), sg.Spin([i for i in range(-1, 300)], size=(6, 1), initial_value=settings['end_frame'], key="end_frame")],
			[sg.Text("Crop Values:")],
			[sg.InputText(settings['crop_top'], key="crop_top", size=(7, 1))],
			[sg.InputText(settings['crop_left'], key="crop_left", size=(7, 1)), sg.InputText(settings['crop_right'], key="crop_right", size=(7, 1))],
			[sg.InputText(settings['crop_bottom'], key="crop_bottom", size=(7, 1))],
			[sg.Button("Create"), sg.Button("Unpack")],
]

window = sg.Window('Gif Tool', layout, grab_anywhere=True, element_justification='center')

while True:
	event, values = window.read()
	if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
		break
	
	processEvents(event, values)
	with open('gifTool.ini', 'w') as f:
		f.write(str(values))

	window.Refresh()


window.close()

