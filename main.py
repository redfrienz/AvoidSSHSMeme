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
    pygame.draw.rect(screen, white, (playerXpos, playerYpos, 300, 300))
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    display_player()
    pygame.display.update()