from math import fabs, sqrt, cos, sin, pi, floor, ceil
from random import uniform, randint, choice
import pygame
#from pygame import gfxdraw
pygame.init()

pygame.font.init()
myfont = pygame.font.SysFont('Arial', 72)

image = pygame.image.load("assets/image.jpg")

win_width = image.get_width()
win_height = image.get_height()
win = pygame.display.set_mode((win_width,win_height))


################################################################################ Setup

result = pygame.Surface(image.get_size())
used = pygame.Surface(image.get_size())

radius = 10
letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
small = ["a", "b", "c", "d", "e", "f", "G", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
numerical = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
symbols = ["!", "?", "@", "#", "$", "%", "&", "(", ")", "[", "]", "/"]

poll = letters + small

for y in range(win_height):
	for x in range(win_width):
	
		currentPos = (x,y)
		draw = True
		
		if used.get_at(currentPos) == (255,0,0):
			continue
		
		
		currentCol = image.get_at(currentPos)
		col = currentCol[0]/255

		rad = radius*col + 2
		
		for i in range(10):
			checkX = int(currentPos[0] + rad * cos(2*pi*i/10))
			checkY = int(currentPos[1] + rad * sin(2*pi*i/10))
			
			if checkX < 0 or checkX >= win_width or checkY < 0 or checkY >= win_height:
				continue
			
			if used.get_at((checkX, checkY)) == (255,0,0):
				draw = False
				break
		
		if draw:
		
			letter = choice(poll)
			surf = myfont.render(letter, True, currentCol)
			
			scale =  max([int(rad*2),1])*2/surf.get_height()
			
			surf = pygame.transform.rotozoom(surf, randint(0,360), scale)
			result.blit(surf, (currentPos[0] - surf.get_width()//2, currentPos[1] - surf.get_height()//2))
			
			pygame.draw.circle(used, (255,0,0), currentPos, int(rad))
			
			win.blit(result, (0,0)); pygame.display.update()
			
		
		
		




################################################################################ Main Loop
run = True
while run:
	#pygame.time.delay(1)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	keys = pygame.key.get_pressed()
	if keys[pygame.K_ESCAPE]:
		run = False
		
	# step:
	win.blit(result, (0,0))
	
	
	# draw:
	
	
	pygame.display.update()
	
pygame.image.save(result, "letters.jpg")	

pygame.quit()














