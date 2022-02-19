from math import fabs, sqrt, cos, sin, pi, floor, ceil
from random import uniform, randint, choice
from socket import timeout
import pygame, os, argparse
from vector import *
import common

def transformation(vec, z):
    # return vec
    z/=255
    dista = 5
    z = 1 - z
    
    center = Vector(image.get_width()/2, image.get_height()/2)
    vec -= center
    result = Vector((vec.x) / (z + dista), (vec.y) / (z + dista))
    result *= dista
    result += center
    
    return result

def makeImage(time):
    pos = Vector(0,0)
    lastPos = Vector(0,0)
    for y in range(0, image.get_height(), 10):
        for x in range(0, image.get_width(), 3):
            value = common.colorValue(image.get_at((x, y)))
            lastPos = vectorCopy(pos)
            pos = transformation(Vector(x, y), value + 0 * sin(x / 100 + time / 10))
            if x == 0:
                lastPos = vectorCopy(pos)
            pygame.draw.line(win, (value,value,value,value), lastPos, pos)

image = pygame.image.load("D:\\python\\assets\\image3.jpg")

winWidth = image.get_width()
winHeight = image.get_height()
win = pygame.display.set_mode((winWidth, winHeight))

pygame.init()

interval = 1
time = 0

run = True
while run:
	time += 1
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
	makeImage(time)
    
	pygame.display.update()
pygame.quit()
