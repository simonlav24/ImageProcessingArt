from math import sin, cos, pi
import pygame, common
pygame.init()


image_path = "../assets/image3.jpg"
image_name = image_path.split("/")[-1].split(".")[0]
image = common.loadAndResize(image_path, 1)

winWidth = image.get_width()
winHeight = image.get_height()
win = pygame.display.set_mode((winWidth,winHeight))

win.fill((255,255,255))
# win.blit(image, (0,0))

WAVE_HEIGHT = 20
WAVE_WIDTH = 20

WAVE_SIZE = 4

def drawWave(yLevel, offset):
    x = 0
    dx = 2

    points1 = []
    points2 = []

    while x < winWidth:
        y = yLevel + WAVE_HEIGHT * sin(x / WAVE_WIDTH - offset)

        if x >= winWidth or y >= winHeight or y < 0 or x < 0:
            value = 0
        else:
            value = common.colorValue(image.get_at((int(x), int(y))))
        value = 255 - value
        y = yLevel + WAVE_HEIGHT * sin(x / WAVE_WIDTH - offset) - (value / 255) * 8

        points1.append((x, y))
        x += dx
    
    x = 0

    while x < winWidth:
        y = yLevel + WAVE_HEIGHT * sin(x / WAVE_WIDTH - offset) + 4

        points2.append((x, y))
        x += dx

    points2.reverse()

    pygame.draw.polygon(win, (0,0,0), points1 + points2)

k = 0
for y in range(-15, winHeight + 30, 15):
    k += 0.08
    drawWave(y, k)

animation = True
if animation:
    time = 0
    frame = 0

    frames = 30

    while frame < 30:
        win.fill((255,255,255))
        k = 0
        for y in range(-15, winHeight + 30, 15):
            k += 0.08
            drawWave(y, k + time)
        pygame.display.update()
        pygame.image.save(win, "./render/wavyBlackAndWhite/anim/" + image_name + str(frame).zfill(3) + ".png")
        frame += 1
        time += 2 * pi / frames

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        run = False
        
    pygame.display.update()

pygame.image.save(win, "./render/wavyBlackAndWhite/" + image_name + ".png")	
pygame.quit()
