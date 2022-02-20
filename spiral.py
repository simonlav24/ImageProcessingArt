from math import fabs, sqrt, cos, sin, pi, floor, ceil
from random import uniform, randint, choice
import pygame, common
from pygame import gfxdraw
pygame.init()

image = common.loadAndResize("assets/image.jpg", 1)

winWidth = image.get_width()
winHeight = image.get_height()
win = pygame.display.set_mode((winWidth,winHeight))

result = pygame.Surface(image.get_size())
result.fill((255,255,255))

center = (winWidth/2, winHeight/2)
edge = int(sqrt(winWidth * winWidth + winHeight * winHeight))

t = 0
dt = 0.005

wideness = 2

def f(x):
	return x

while t < edge:
	
	point = (int(center[0] + wideness * f(t) * cos(t)), int(center[1] + wideness * f(t) * sin(t)))
	
	if point[0] < 0 or point[0] >= winWidth or point[1] < 0 or point[1] >= winHeight:
		t += dt
		# dt *= 0.99999
		continue
	
	color = image.get_at(point)
			
	radius = max(0, int(((255 - color[0])/255) * pi * wideness)-1)
	
	pygame.gfxdraw.filled_circle(result, point[0], point[1], radius, (0,0,0))
	pygame.gfxdraw.aacircle(result, point[0], point[1], radius, (0,0,0))
	
	win.blit(result, (0,0))
	pygame.display.update()

	t += dt


################################################################################ Main Loop
run = True
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	keys = pygame.key.get_pressed()
	if keys[pygame.K_ESCAPE]:
		run = False
	
	run = False
	pygame.display.update()
	
pygame.image.save(result, "spiral.jpg")

pygame.quit()
