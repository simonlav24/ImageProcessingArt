from math import sin, pi
import pygame, common
pygame.init()

image = common.loadAndResize("assets/image.jpg", 1)

winWidth = image.get_width()
winHeight = image.get_height()
win = pygame.display.set_mode((winWidth,winHeight))

def mapColor(x, a, b):
	return ((a-b)/(-255)) * x + a

def drawSine(y, height, time=0):
	xVals = [(common.colorValue(image.get_at((x,y)))) for x in range(image.get_width())]
	p = 20
	# smooth the xvals with a moving average of size p
	smoothed = [sum(xVals[i:i+p])/p for i in range(len(xVals)-p)]

	lastPos = [0, y]
	for x in range(len(smoothed)):
		waveLength = mapColor(smoothed[x], 5, 30)
		freq = 1 / waveLength
		yValue = y + height * sin(x * freq + time)
		pygame.draw.line(win, (0,0,0), lastPos, (x, yValue))
		lastPos = [x, yValue]

time = 0
height = 5

saveFrame = False
if saveFrame:
	time = 0
	end = 20
	while time < end:
		t = 2 * pi * time / end 
		win.fill((255,255,255))
		for y in range(0,image.get_height(), height * 2):
			drawSine(y, height, t)
		pygame.display.update()
		num = str(time).zfill(3)
		pygame.image.save(win, "./render/sine/sine" + num + ".png")
		time += 1

################################################################################ Main Loop
run = True
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	keys = pygame.key.get_pressed()
	if keys[pygame.K_ESCAPE]:
		run = False
	
	win.fill((255,255,255))
	for y in range(0,image.get_height(), height * 2):
		drawSine(y, height, time)
	
	pygame.display.update()
	time += 0.5
	
pygame.quit()
