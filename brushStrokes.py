from math import fabs, sqrt, cos, sin, pi, floor, ceil, exp
from random import uniform, randint, choice, gauss
import pygame, argparse
from pygame import gfxdraw
from vector import *
import common

def drawMethod1():

	x1 = randint(0, winWidth-1)
	y1 = randint(0, winHeight-1)

	if x1 < 0 or x1 > winWidth-1 or y1 < 0 or y1 > winHeight-1:
		pass
	else:
		col = image.get_at((x1, y1))
	
	sLength = abs(gauss(0, 1) * maxStrokeWidth)
	x2 = x1 + uniform(-sLength, sLength)
	y2 = y1 + uniform(-sLength, sLength)
	x3 = x1 + uniform(-sLength, sLength)
	y3 = y1 + uniform(-sLength, sLength)
	x4 = x1 + uniform(-sLength, sLength)
	y4 = y1 + uniform(-sLength, sLength)

	for i in range(bristleCount):
		color = (col[0], col[1], col[2], 64)
		col = mutate(col)
		bristleThickness = uniform(1,4)
		width = bristleThickness
		pygame.gfxdraw.bezier(win, [(x1, y1), (x2, y2), (x3, y3), (x4, y4)], 5, color)
		
		x1 += uniform(-strokeWidth, strokeWidth)
		y1 += uniform(-strokeWidth, strokeWidth)
		x2 += uniform(-strokeWidth, strokeWidth)
		y2 += uniform(-strokeWidth, strokeWidth)
		x3 += uniform(-strokeWidth, strokeWidth)
		y3 += uniform(-strokeWidth, strokeWidth)
		x4 += uniform(-strokeWidth, strokeWidth)
		y4 += uniform(-strokeWidth, strokeWidth)

def flow(pos, time = 0):
	mag = 0.01 * uniform(0.95,1.05)
	return Vector(sin(mag*pos[0] + time) + sin(mag*pos[1] + time), sin(mag*pos[0] + time) - sin(mag*pos[1] + time))
	return Vector(sin(mag*pos[0]) + sin(mag*pos[1]), cos(mag*pos[0]) - cos(mag*pos[1]))

def drawMethod2(time = 0):
	# dir = vectorUnitRandom()
	pos = Vector(randint(0, winWidth-1), randint(0,winHeight-1))
	# dir *= strokeLen
	dir = normalize(flow(pos, time)) * strokeLen * uniform(0.6, 1.4)
	
	p1 = pos
	p2 = pos + dir * 0.5
	p3 = pos + dir
	
	randomness = uniform(0,5)
	
	p1 += vectorUnitRandom() * randomness
	p2 += vectorUnitRandom() * randomness
	p3 += vectorUnitRandom() * randomness
	
	scatar = [vectorUnitRandom() * uniform(0, strokeWidth * uniform(0.8, 1.2)) for i in range(bristleCount)]
	points1 = [p1 + i for i in scatar]
	points2 = [p2 + i for i in scatar]
	points3 = [p3 + i for i in scatar]
	
	if p2[0] < 0 or p2[0] > winWidth-1 or p2[1] < 0 or p2[1] > winHeight-1:
		return
	else:
		color = image.get_at(p2.vec2tupint())
	
	# pygame.gfxdraw.line(win, pos[0], pos[1], int(pos[0] + dir[0]), int(pos[1] + dir[1]),  color)
	for i in range(bristleCount):
		pygame.gfxdraw.bezier(win, [points1[i].vec2tupint(), points2[i].vec2tupint(), points3[i].vec2tupint()], 5, alphaDown(mutate(color, 50)))

def clamp(x, lower, upper):
	if x > upper:
		x = upper
	if x < lower:
		x = lower
	return x

def mutate(col, amount = 10):
	mr = amount
	return (clamp(col[0] + randint(-mr, mr),0,255), clamp(col[1] + randint(-mr, mr),0,255), clamp(col[2] + randint(-mr, mr),0,255))

def alphaDown(color, alpha=64):
	return (color[0], color[1], color[2], alpha)
	
################################################################################ Setup
# parse arguments
parser = argparse.ArgumentParser(description='Brush Strokes')
parser.add_argument('-i', '--image', type=str, default='assets/housesMed.jpg', help='image to use')
args = parser.parse_args()

pygame.init()

image = pygame.image.load(args.image)
image = pygame.transform.scale(image, (tup2vec(image.get_size())*0.5).vec2tupint())

winWidth = image.get_width()
winHeight = image.get_height()
win = pygame.display.set_mode((winWidth,winHeight))

counter = 0
strokeWidth = 5#8
strokeLen = 25
maxStrokeWidth = 32
bristleCount = 16#6
bristleThickness = 3
col = None
mousePos = pygame.mouse.get_pos()

win.fill((255,255,255))

################################################################################ Main Loop
time = 0
end = 30
counter = 0
saveFrames = False

if saveFrames:
	for i in range(30000):
		drawMethod2(time)

run = True
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		#mouse pressed once(MOUSEBUTTONUP for release):
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			#mouse position:
			mouse_pos = pygame.mouse.get_pos()
		if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
			filepath = common.browseFile()
			if filepath:
				image = pygame.image.load(filepath)
				image = pygame.transform.scale(image, (tup2vec(image.get_size())/2).vec2tupint())
				winWidth = image.get_width()
				winHeight = image.get_height()
				win = pygame.display.set_mode((winWidth, winHeight))
	keys = pygame.key.get_pressed()
	if keys[pygame.K_ESCAPE]:
		run = False
	
	# draw:

	if saveFrames:
		for i in range(10000):
			t = (time / end) * 2 * pi
			drawMethod2(t)
	
		# counter with 3 leading zeros
		num = str(counter).zfill(3)
		pygame.image.save(win, "render/brushStrokes/frame" + num + ".png")
		counter += 1
		if counter > end:
			run = False
			break
		time += 1
	
	else:
		for i in range(100):
			drawMethod2()

	
	
	pygame.display.update()
pygame.quit()














