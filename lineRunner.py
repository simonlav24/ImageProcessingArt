from math import fabs, sqrt, cos, sin, pi, floor, ceil
from random import uniform, randint, choice
from cv2 import threshold
import pygame, os, argparse
from pygame import gfxdraw
from vector import *
import common

def smap(value,a,b,c,d,constrained=False):
	res = (value - a)/(b - a) * (d - c) + c
	if constrained:
		if res > d:
			return d
		if res < c:
			return c
		return res
	else:
		return res

def safeGetAt(pos, surf):
	if pos[0] < 0 or pos[0] >= surf.get_width() or pos[1] < 0 or pos[1] >= surf.get_height():
		return (0,0,0)
	return surf.get_at(pos.vec2tupint())

class Vehicle:
	def __init__(self, pos):
		self.pos = vectorCopy(pos)
		self.oldPos = vectorCopy(pos)
		self.vel = Vector()
		self.acc = Vector()
		self.maxSpeed = 3
		self.maxForce = 0.2
		self.color = (255,255,255,10)
	def applyForce(self, force):
		self.acc = vectorCopy(force)
	def flee(self, target):
		return self.seek(target) * -1
	def seek(self, target, arrival=False):
		force = tup2vec(target) - self.pos
		desiredSpeed = self.maxSpeed
		if arrival:
			slowRadius = 50
			distance = force.getMag()
			if (distance < slowRadius):
				desiredSpeed = smap(distance, 0, slowRadius, 0, self.maxSpeed)
				force.setMag(desiredSpeed)
		force.setMag(desiredSpeed)
		force -= self.vel
		force.limit(self.maxForce)
		return force
	def pursue(self, targetVehicle):
		target = targetVehicle.pos + targetVehicle.vel * 10
		return self.seek(target)
	def evade(self, targetVehicle):
		return self.pursue(targetVehicle) * -1
	def arrive(self, target):
		return self.seek(target, True)
	def step(self):
		self.vel += self.acc
		self.vel.limit(self.maxSpeed)
		self.oldPos = vectorCopy(self.pos)
		self.pos += self.vel
	def wrapAround(self, square):
		if self.pos.x >= square:
			self.pos.x = -square
		elif self.pos.x < -square:
			self.pos.x = square
		if self.pos.y >= square:
			self.pos.y = -square
		elif self.pos.y < -square:
			self.pos.y = square
	def draw(self):
		# draw line using gfx drfaw
		gfxdraw.line(win, int(self.oldPos.x), int(self.oldPos.y), int(self.pos.x), int(self.pos.y), self.color)

		# pygame.draw.line(win, self.color, self.oldPos, self.pos, 1)
		# pygame.draw.circle(win, self.color, self.pos, 1)

def getTarget():
	found = False
	tries = 0
	while not found:
		tries += 1
		found = True
		target = lineRunner.pos + uniform(0, 100 + tries) * vectorUnitRandom()
		if target.x < 0 or target.x >= win.get_width() or target.y < 0 or target.y >= win.get_height():
			found = False
			continue

		color = image.get_at(target.vec2tupint())
		value = common.colorValue(color)
		if value <= 1:
			found = False
			continue
	
	radius = ((255 - value)/255) **2 * 60 + 1
	# get random colors around the target
	values = [common.colorValue(safeGetAt(target + radius * vectorUnitRandom(), image)) for i in range(50)]
	# print(values)
	# if there is a value that is far from the target value by epsilon reduce the radius

	epsilon = 50
	for v in values:
		if fabs(v - value) > epsilon:
			radius /= 5
			# print(2)
			break

	radius = max(radius, 1)
	return target, value, radius

def newTarget():
	global target, targetTime
	# random point
	target, value, radius = getTarget()
	targetTime = 100000

	pygame.draw.circle(image, (0,0,0), target.vec2tupint(), radius)

image = common.loadAndResize("D:\\python\\assets\\simon.jpg", 2)

winWidth = image.get_width()
winHeight = image.get_height()
win = pygame.display.set_mode((winWidth, winHeight))

pygame.init()

lineRunner = Vehicle(Vector(winWidth//2, winHeight//2))

interval = 1000
time = 0

target = Vector()
targetTime = 0

showImage = False

run = True
while run:
	time += 1
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
			pygame.image.save(win, 'resultLine.png')
	keys = pygame.key.get_pressed()
	if keys[pygame.K_ESCAPE]:
		run = False
	
	force = lineRunner.seek(target)
	lineRunner.applyForce(force)

	lineRunner.step()
	
	
	targetTime -= 1
	if targetTime <= 0:
		newTarget()
	if distus(lineRunner.pos, target) < 10:
		newTarget()

	lineRunner.draw()

	if showImage:
		smallImage = pygame.transform.scale(image, tup2vec(image.get_size()) / 8)
		win.blit(smallImage, (0,0))

	if time % interval == 0:
		pygame.display.update()
pygame.quit()
