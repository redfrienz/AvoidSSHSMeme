import pygame
import sys

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
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
    pygame.draw.rect(screen, white, (playerXpos, playerYpos, 90, 90))
    pygame.draw.rect(screen, white, (0, 1030, 1920, 50))

def movebykey(speed):
    global playerXpos, playerYpos
    key_event = pygame.key.get_pressed()
    if key_event[pygame.K_LEFT]:
        playerXpos -= speed
    if key_event[pygame.K_RIGHT]:
        playerXpos += speed
    if key_event[pygame.K_UP]:
        playerYpos -= speed
    if key_event[pygame.K_DOWN]:
        playerYpos += speed

    display_player()
    stayinside(speed)

def stayinside(speed):
    global playerXpos, playerYpos
    if playerYpos >= 940:
        playerYpos -= speed

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    movebykey(20)
    pygame.display.update()