from math import fabs, sqrt, cos, sin, pi, floor, ceil
from random import uniform, randint, choice
from socket import timeout
import pygame, os, argparse, sys
from vector import *
import common

def transformation(vec, z, time=0):
    # return vec
    z/=255
    
    dista = 5
    z = 1 - z
    
    center = Vector(image.get_width()/2, image.get_height()/2)
    vec -= center
    z = zDistort(vec, z, time)
    result = Vector((vec.x) / (z + dista), (vec.y) / (z + dista))
    result *= dista
    result += center
    
    return result

def zDistort(vec, z, time):
    r = sqrt(vec.x**2 + vec.y**2)
    return z + 0.2 * sin(0.05*r - time)

def makeImage(image, time=0):
    pos = Vector(0,0)
    lastPos = Vector(0,0)
    for y in range(0, image.get_height(), 10):
        for x in range(0, image.get_width(), 3):
            value = common.colorValue(image.get_at((x, y)))
            lastPos = vectorCopy(pos)
            pos = transformation(Vector(x, y), value + 0 * sin(x / 100 + time / 10), time)
            if x == 0:
                lastPos = vectorCopy(pos)
            pygame.draw.line(win, (value,value,value,value), lastPos, pos)

image = pygame.image.load(".\\assets\\image.jpg")

frames = common.loadFrames(".\\assets\\dancer.gif")
for frame in frames:
    print(frame.get_size())

winWidth = image.get_width()
winHeight = image.get_height()
win = pygame.display.set_mode((winWidth, winHeight))

pygame.init()

interval = 1
time = 0

makeGif1 = False
if makeGif1:
    framesFolder = ".\\assets\\gif"
    files = os.listdir(framesFolder)
    for file in files:
        win.fill((255,255,255))
        frame = pygame.image.load(framesFolder + "\\" + file)
        makeImage(frame)
        pygame.image.save(win, ".\\assets\\gif\\done\\" + file)

makeGif2 = True
if makeGif2:
	time = 0
	end = 30
	while time < end:
		t = 2 * pi * time / end 
		win.fill((0,0,0))
		makeImage(image, t)
		pygame.image.save(win, ".\\render\\3dline\\line" + str(time).zfill(3) + ".png")
		pygame.display.update()
		time += 1
	sys.exit()


run = True
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
			pygame.image.save(win, 'resultLine.png')
		if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
			filepath = common.browseFile()
			if filepath:
				image = pygame.image.load(filepath)
				winWidth = image.get_width()
				winHeight = image.get_height()
				win = pygame.display.set_mode((winWidth, winHeight))
	keys = pygame.key.get_pressed()
	if keys[pygame.K_ESCAPE]:
		run = False
		
	win.fill((0,0,0))
	makeImage(image, time)
    
	pygame.display.update()
	time += 1
pygame.quit()
