import pygame
import sys
import time
import math
from threading import Thread

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SIZE=50
velocity=0
jump_time = 0
max_jump_time = 2
player_speed = 20

white = (255,255,255)
red = (255,0,0)
black = (0,0,0)
yellow = (255,255,0)
green = (0,255,0)


playerXpos = 800
playerYpos = 400
player_color = white
up_key_pressed = False
bgm = pygame.mixer.Sound("audio/Super Mario Galaxy - Buoy Base Galaxy [Remix].mp3")
spell_sound = [pygame.mixer.Sound("audio/stopwatch.mp3"),pygame.mixer.Sound("audio/flash.mp3"),pygame.mixer.Sound("audio/heal.mp3")]
score = 0
game_font1 = pygame.font.Font("fonts/PressStart2P-vaV7.ttf",50)
hp = 5
spell = [0,1] #0 초시계 1 점멸 2 유체화 3 회복 4 방어막 수정 끝나면 -1 -1로 초기화해
player_rigid = False
player_invincible = False
blink_distance = 300
spell_img = [pygame.image.load("images/stopwatch.jpg"), pygame.image.load("images/blink.png"),pygame.image.load("images/ghost.png"),pygame.image.load("images/heal.png"),pygame.image.load("images/barrier.png")]
barrier_activated = False

score_tick = 1

pygame.display.set_caption("설곽 밈 피하기")
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()


def display_player():
    screen.fill(black)
    #pygame.draw.circle(screen,white,(playerXpos,playerYpos),100)
    pygame.draw.rect(screen, player_color, (playerXpos, playerYpos, SIZE, SIZE))
    pygame.draw.rect(screen, white, (0, 1030, 1920, 20))
    pygame.draw.rect(screen, white, (-20, 0, 20, 1080))
    pygame.draw.rect(screen, white, (1920, 0, 20, 1080))

def movebykey(speed):
    global playerXpos, playerYpos, velocity
    key_event = pygame.key.get_pressed()
    if key_event[pygame.K_LEFT]:
        playerXpos -= speed
    if key_event[pygame.K_RIGHT]:
        playerXpos += speed

def spell_check():
    key_event = pygame.key.get_pressed()
    if key_event[pygame.K_d] and spell[0]!=-1:
        args1 = []
        args1.append(spell[0])
        sth1 = Thread(target=use_spell,args=tuple(args1))
        sth1.start()
        spell[0] = -1
    if key_event[pygame.K_f] and spell[1]!=-1:
        args2 = []
        args2.append(spell[1])
        sth2 = Thread(target=use_spell,args=tuple(args2))
        sth2.start()
        spell[1] = -1
def use_spell(spell_num):
    global player_color, player_rigid, player_speed, hp, player_invincible,playerXpos, playerYpos, barrier_activated
    spell_sound[spell_num].play()
    if spell_num == 0:
        tmp = player_color
        player_color = yellow
        player_rigid = True
        player_invincible = True

        time.sleep(2.5)
        player_color = tmp
        player_rigid = False
        player_invincible = False
    elif spell_num == 1:
        key_event = pygame.key.get_pressed()
        if key_event[pygame.K_LEFT] and key_event[pygame.K_UP]:
            playerXpos -= blink_distance
            playerYpos -= blink_distance
        elif key_event[pygame.K_LEFT] and key_event[pygame.K_DOWN]:
            playerXpos -= blink_distance
            playerYpos += blink_distance
        elif key_event[pygame.K_LEFT]:
            playerXpos -= blink_distance * math.sqrt(2)
        elif key_event[pygame.K_RIGHT] and key_event[pygame.K_UP]:
            playerXpos += blink_distance
            playerYpos -= blink_distance
        elif key_event[pygame.K_RIGHT] and key_event[pygame.K_DOWN]:
            playerXpos += blink_distance
            playerYpos += blink_distance
        elif key_event[pygame.K_RIGHT]:
            playerXpos += blink_distance * math.sqrt(2)
        elif key_event[pygame.K_UP]:
            playerYpos -= blink_distance * math.sqrt(2)
        elif key_event[pygame.K_DOWN]:
            playerYpos += blink_distance * math.sqrt(2)
    elif spell_num == 2:
        player_speed = 40
        time.sleep(5)
        player_speed = 20
    elif spell_num == 3:
        hp += 1
    elif spell_num == 4:
        player_invincible = True
        barrier_activated = True
def vel():
    global playerXpos, playerYpos, velocity, jump_time, up_key_pressed
    key_event = pygame.key.get_pressed()
    if key_event[pygame.K_UP]:
        if jump_time > 0 and up_key_pressed:
            velocity = 20
            jump_time -= 1
        up_key_pressed = False
    else:
        up_key_pressed = True
    velocity -= 1

def movebyvelocity(v):
    global playerYpos
    playerYpos -= v

def stayinside():
    global playerXpos, playerYpos, velocity, jump_time, max_jump_time
    if playerYpos > 1030-SIZE:
        playerYpos = 1030-SIZE
        jump_time = max_jump_time
    if playerYpos < 0:
        playerYpos = 0
        velocity = 0
    if playerXpos > SCREEN_WIDTH-SIZE:
        playerXpos = SCREEN_WIDTH-SIZE
    if playerXpos < 0:
        playerXpos = 0

def display_score():
    global score
    score_str = str(score)
    score_x = 1800 - 50*len(str(score))
    score_y = 100
    score_img = game_font1.render(score_str,True,white)
    screen.blit(score_img, (score_x,score_y))

def display_health():
    global hp
    hpx = 100
    for i in range(hp):
        pygame.draw.rect(screen,red,(hpx,100,50,50))
        hpx += 60

def display_spell():
    global spell
    if spell[0] != -1:
        screen.blit(pygame.transform.scale(spell_img[spell[0]],(50,50)),(100,160))
    if spell[1] != -1:
        screen.blit(pygame.transform.scale(spell_img[spell[1]],(50,50)),(160,160))

def display_barrier():
    if barrier_activated:
        pygame.draw.circle(screen,yellow,(playerXpos+SIZE/2,playerYpos+SIZE/2),50,2)

def add_score():
    global score
    score += score_tick

def check_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
if __name__ == '__main__':
    bgm.play(-1)
    while True:
        clock.tick(60)

        check_quit()
        add_score()

        stayinside()
        if not player_rigid:
            movebykey(player_speed)
            vel()
            movebyvelocity(velocity)

        display_player()
        display_score()
        display_health()
        display_spell()
        display_barrier()
        th1 = Thread(target=spell_check)
        th1.start()
        pygame.display.update()