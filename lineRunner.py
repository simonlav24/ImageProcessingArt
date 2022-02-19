from math import fabs, sqrt, cos, sin, pi, floor, ceil
from random import uniform, randint, choice
import pygame, os, argparse
from vector import *



class LineRunner0:
	def __init__(self):
		self.pos = Vector(randint(0, winWidth-1), randint(0, winHeight-1))
		self.prevPos = self.pos
		self.target = Vector(randint(0, winWidth-1), randint(0, winHeight-1))

		self.vel = vectorUnitRandom()
		self.acc = Vector()
		self.time = image.get_at(self.target)[0]

	def changeTarget(self):
		self.target = Vector(randint(0, winWidth-1), randint(0, winHeight-1))
		self.time = image.get_at(self.target)[0] * 10

	def step(self):
		maxForce = 8
		maxVel = 2.0

		self.time -= 1
		if self.time <= 0:
			self.changeTarget()
		
		distance = dist(self.pos, self.target)
		force = self.target - self.pos
		force.normalize()
		force *= 5/distance
		force.limit(maxForce)

		self.acc = force 
		self.vel += self.acc
		self.vel.limit(maxVel)
		self.prevPos = self.pos
		self.pos += self.vel

	def draw(self):
		value = 255 - int((self.vel.getMag() / 2.0) * 255)
		pygame.draw.line(win, (value,value,value,value), self.prevPos, self.pos)

class LineRunner:
	def __init__(self):
		self.pos = Vector(randint(0, winWidth-1), randint(0, winHeight-1))
		self.prevPos = self.pos
		self.target = Vector(randint(0, winWidth-1), randint(0, winHeight-1))

		self.vel = vectorUnitRandom()
		self.acc = Vector()
		self.time = image.get_at(self.target)[0] * 100

	def changeTarget(self):
		self.target = Vector(randint(0, winWidth-1), randint(0, winHeight-1))
		self.time = image.get_at(self.target)[0] * 100

	def seek(self, target):
		global maxForce
		global maxVel
		# maxForce = 2
		# maxVel = 0.1

		force = target - self.pos
		force.normalize()
		force *= 5/dist(self.pos, target)
		force.limit(maxForce)

		self.acc = force 
		self.vel += self.acc
		self.vel.limit(maxVel)
		self.prevPos = self.pos
		self.pos += self.vel

	def step(self):
		self.time -= 1
		if self.time <= 0:
			self.changeTarget()
		
		self.seek(self.target + vectorUnitRandom() * randint(0, 30))

	def draw(self):
		value = 255 #- int((self.vel.getMag() / 2.0) * 255)
		pygame.draw.line(win, (value,value,value,value), self.prevPos, self.pos)

image = pygame.image.load("D:\\python\\assets\\simonSmaller.png")

winWidth = image.get_width()
winHeight = image.get_height()
win = pygame.display.set_mode((winWidth, winHeight))

pygame.init()

lineRunner = LineRunner()

interval = 20
time = 0

maxForce = 2
maxVel = 0.2

run = True
while run:
	time += 1
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
			maxForce += 0.1
			print(maxForce)
		if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
			maxForce -= 0.1
			print(maxForce)
		if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
			maxVel += 0.001
			print(maxVel)
		if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
			maxVel -= 0.001
			print(maxVel)
		if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
			pygame.image.save(win, 'resultLine.png')
	keys = pygame.key.get_pressed()
	if keys[pygame.K_ESCAPE]:
		run = False
		
	lineRunner.step()
	lineRunner.draw()

	if time % interval == 0:
		pygame.display.update()
pygame.quit()
