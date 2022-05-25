import pygame
import sys
import datetime

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SIZE=50
velocity=0
jump_time = 0
max_jump_time = 3
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
score = 0
game_font1 = pygame.font.Font("fonts/PressStart2P-vaV7.ttf",50)
hp = 5
spell = [0,1] #0 초시계 1 점멸 2 유체화 3 회복 4 방어막 수정 끝나면 -1 -1로 초기화해
player_rigid = False
player_invinsible = False

spell_img = [pygame.image.load("images/stopwatch.jpg"), pygame.image.load("images/blink.png"),pygame.image.load("images/ghost.png"),pygame.image.load("images/heal.png"),pygame.image.load("images/barrier.png")]

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
        use_spell(spell[0])
        spell[0] = -1
    if key_event[pygame.K_f] and spell[1]!=-1:
        use_spell(spell[1])
        spell[1] = -1
def use_spell(spell_num):
    global player_color, player_rigid, player_speed, hp, player_invincible
    if spell_num == 0:
        tmp = player_color
        player_color = yellow
        player_rigid = True
        t1 = datetime.datetime.now()
        while True:
            t2 = datetime.datetime.now()
            if (t2-t1).seconds > 2.5:
                break
        player_color = tmp
        player_rigid = False
    elif spell_num == 1:
        key_event = pygame.key.get_pressed()
        # if key_event[pygame.K_LEFT] and key_event[pygame.K_UP]:
    elif spell_num == 2:
        player_speed = 30
        time.sleep(5)
        player_speed = 20
    elif spell_num == 3:
        hp += 1
    elif spell_num == 4:
        player_invincible = True
        player_color = green
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

bgm.play(-1)
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    score += score_tick

    stayinside()

    movebykey(player_speed)
    vel()
    movebyvelocity(velocity)

    display_player()
    display_score()
    display_health()
    display_spell()
    spell_check()
    pygame.display.update()