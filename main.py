import pygame
import sys

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SIZE=90
velocity=0
white = (255,255,255)
black = (0,0,0)
#asdf
playerXpos = 800
playerYpos = 400

pygame.display.set_caption("설곽 밈 피하기")
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()

def display_player():
    screen.fill(black)
    #pygame.draw.circle(screen,white,(playerXpos,playerYpos),100)
    pygame.draw.rect(screen, white, (playerXpos, playerYpos, SIZE, SIZE))
    pygame.draw.rect(screen, white, (0, 1030, 1920, 50))

def movebykey(speed):
    global playerXpos, playerYpos, velocity
    key_event = pygame.key.get_pressed()
    if key_event[pygame.K_LEFT]:
        playerXpos -= speed
    if key_event[pygame.K_RIGHT]:
        playerXpos += speed

    display_player()
    vel()
    movebyvelocity(velocity)
    stayinside()

def vel():
    global playerXpos, playerYpos, velocity
    key_event = pygame.key.get_pressed()
    if key_event[pygame.K_UP]:
         velocity += 5
    velocity -= 1

def movebyvelocity(v):
    global playerYpos
    playerYpos -= v

def stayinside():
    global playerXpos, playerYpos, velocity
    if playerYpos >= 940:
        playerYpos -= velocity
        velocity = 0

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    movebykey(20)
    pygame.display.update()