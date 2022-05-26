import pygame
import sys
import time
import math
import random
from threading import Thread

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SIZE=50
STAGENUM = 15
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
spell = [1,0] #0 초시계 1 점멸 2 유체화 3 회복 4 방어막 수정 끝나면 -1 -1로 초기화해
player_rigid = False
player_invincible = False
blink_distance = 300
heart_img = pygame.image.load("images/heart.png")
spell_img = [pygame.image.load("images/stopwatch.jpg"), pygame.image.load("images/blink.png"),pygame.image.load("images/ghost.png"),pygame.image.load("images/heal.png"),pygame.image.load("images/barrier.png")]
barrier_activated = False
spell_item_display = False

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
    # spell_sound[spell_num].play()
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
        screen.blit(pygame.transform.scale(heart_img,(50,50)),(hpx,100))
        # pygame.draw.rect(screen,red,(hpx,100,50,50))
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

def random_spell():
    global spell_item_display
    while True:
        time.sleep(random.randint(5,10))
        spell_item_display = True
        spell_number = random.randint(0,4)
        spell_x = random.randint(0,1870)
        spell_y = random.randint(720,920)

        th4 = Thread(target=display_spell_item,args=(spell_number,spell_x,spell_y))
        th4.start()
        th5 = Thread(target=check_if_collide_spell_item,args=(spell_number,spell_x,spell_y))
        th5.start()
        time.sleep(2)
        spell_item_display = False

def check_if_collide_spell_item(snum,sx,sy):
    global playerXpos,playerYpos,spell_item_display
    while spell_item_display:
        time.sleep(1/60)
        if (playerXpos-sx)**2 + (playerYpos-sy)**2 < 10000:

            if spell[0] == -1:
                spell[0] = snum
            elif spell[1] == -1:
                spell[1] = snum
            spell_item_display = False
def display_spell_item(spellnum,sx,sy):
    global spell_item_display
    while spell_item_display:
        screen.blit(pygame.transform.scale(spell_img[spellnum],(50,50)),(sx,sy))

def draw_platform(n):
    if n == 1:
        pygame.draw.rect(screen, white, (500, 900, 200, 20))

def stayon_platform(n):
    global playerXpos, playerYpos, velocity
    draw_platform(n)
    if n == 1:
        if playerXpos > 500-SIZE and playerXpos < 700 and velocity > 0 and playerYpos < 920:
            playerYpos = 900 -SIZE
            velocity = 0


# def stage_loop():
#     while True:
#         stage_num = random.randint(1,STAGENUM)
#         stage(stage_num)
#
# def stage(stage_num):
#     #추가바람
if __name__ == '__main__':
    bgm.play(-1)
    # th2 = Thread(target=stage_loop)
    # th2.start()
    th3 = Thread(target=random_spell)
    th3.start()
    while True:
        clock.tick(60)

        check_quit()
        add_score()

        if not player_rigid:
            movebykey(player_speed)
            vel()
            movebyvelocity(velocity)

        stayinside()

        display_player()
        display_score()
        display_health()
        display_spell()
        display_barrier()
        stayon_platform(1)
        th1 = Thread(target=spell_check)
        th1.start()

        pygame.display.update()