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
STAGENUM = 2
velocity=0
jump_time = 0
max_jump_time = 100
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
hpcolor = 0
spell = [1,0] #0 초시계 1 점멸 2 유체화 3 회복 4 방어막 수정 끝나면 -1 -1로 초기화해
player_rigid = False
player_invincible = False
blink_distance = 300
heart_img = [pygame.image.load("images/heart.png"), pygame.image.load("images/yellowheart.png"), pygame.image.load("images/whiteheart.png")]
spell_img = [pygame.image.load("images/stopwatch.jpg"), pygame.image.load("images/blink.png"),pygame.image.load("images/ghost.png"),pygame.image.load("images/heal.png"),pygame.image.load("images/barrier.png")]
coin_img = [pygame.image.load("images/c"+str(i)+".png") for i in range(1,7)]
obs_img = [] #[pygame.image.load("images/sagam.png") for i in range(10)]
platform = [] #[[100, 800, 600, 5], [1320, 800, 600, 5], [250, 600, 300, 5], [1470, 600, 300, 5], [810, 500, 300, 5]]
obstacle = [] #[[random.randint(0,1900), random.randint(0,500), 100, 100] for i in range(10)]
obsspeed = [] #[[0,0-random.randint(0,15)] for i in range(10)]
obsacc = []
obs_color = red
invinciblet = -10000
barrier_activated = False
spell_item_display = False
coin_item_display = False
coin_number = 1
score_tick = 1
game_finish = False
stop_thread = False
game_start = False
obsnumber = 0

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
    for i in range(len(platform)):
        pygame.draw.rect(screen, white, platform[i])
    for i in range(len(obstacle)):
        screen.blit(pygame.transform.scale(obs_img[i], (obstacle[i][2], obstacle[i][3])), (obstacle[i][0], obstacle[i][1]))

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
    global player_color, player_rigid, player_speed, hp, player_invincible,playerXpos, playerYpos, barrier_activated, hpcolor, obs_color
    # spell_sound[spell_num].play()
    if spell_num == 0:
        tmp = player_color
        player_color = yellow
        player_rigid = True
        player_invincible = True

        time.sleep(1.5)
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
        if hp < 5:
            hp +=1
    elif spell_num == 4:
        barrier_activated = True
        hpcolor = 1

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
        velocity = 0
    if playerYpos < 0:
        playerYpos = 0
        velocity = 0
    if playerXpos > SCREEN_WIDTH-SIZE:
        playerXpos = SCREEN_WIDTH-SIZE
    if playerXpos < 0:
        playerXpos = 0

def stayon_platform():
    global playerXpos, playerYpos, velocity, jump_time, max_jump_time
    for i in range(len(platform)):
        if playerXpos > platform[i][0]-SIZE and playerXpos < platform[i][0]+platform[i][2] and playerYpos > platform[i][1]-SIZE and playerYpos < platform[i][1]+10-SIZE-velocity:
            playerYpos = platform[i][1]-SIZE
            velocity = 0
            jump_time = max_jump_time



def display_score():
    global score
    score_str = str(score)
    score_x = 1800 - 50*len(str(score))
    score_y = 100
    score_img = game_font1.render(score_str,True,white)
    screen.blit(score_img, (score_x,score_y))

def display_health():
    global hp, hpcolor
    hpx = 100
    for i in range(hp):
        screen.blit(pygame.transform.scale(heart_img[hpcolor],(50,50)),(hpx,100))
        # pygame.draw.rect(screen,red,(hpx,100,50,50))
        hpx += 60
    for i in range(5-hp):
        screen.blit(pygame.transform.scale(heart_img[2], (50, 50)), (hpx, 100))
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
    while not game_finish:
        #time.sleep(random.randint(5,10))
        time.sleep(1)
        spell_item_display = True
        spell_number = random.randint(0,4)
        spell_x = random.randint(0,1870)
        spell_y = random.randint(420,620)

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



def stage_loop():
    global obsnumber
    while True:
        stage(0)
        time.sleep(5)
        stage_num = random.randint(1,STAGENUM)
        obsnumber = random.randint(5,8)
        stage(stage_num)
        time.sleep(25)

def stage(stage_num):
    global obs_img,platform,obstacle,obsspeed,obsacc
    if stage_num == 0:
        obs_img = []
        platform = []
        obstacle = []
        obsspeed = []
        obsacc = []
    if stage_num == 1:
        obs_img = [pygame.image.load("images/sagam.png") for i in range(obsnumber)]
        platform = [[100, 800, 600, 5], [1320, 800, 600, 5], [250, 600, 300, 5], [1470, 600, 300, 5], [810, 500, 300, 5]]
        obstacle = [[random.randint(0,1900), random.randint(0,200), 100, 100] for i in range(obsnumber)]
        obsspeed = [[random.randint(-10,10),0-random.randint(0,15)] for i in range(obsnumber)]
        obsacc = [0.5 for i in range(obsnumber)]
    elif stage_num == 2:
        obs_img = [pygame.image.load("images/liwon.jfif") for i in range(obsnumber)]
        platform = [[100, 800, 600, 5], [1320, 800, 600, 5], [250, 600, 300, 5], [1470, 600, 300, 5], [810, 500, 300, 5]]
        obstacle = [[random.randint(0,1900), random.randint(0,200), 100, 100] for i in range(obsnumber)]
        obsspeed = [[random.randint(-10,10),0-random.randint(0,15)] for i in range(obsnumber)]
        obsacc = [0.5 for i in range(obsnumber)]
    # elif stage_num == 3:
    #
    # elif stage_num == 4:
    #
    # elif stage_num == 5:

def random_coin():
    global coin_item_display
    while not game_finish:
        time.sleep(random.randint(5,10))
        coin_item_display = True
        coin_x = random.randint(0,1870)
        coin_y = random.randint(320,620)
        th4 = Thread(target=display_coin,args = (coin_x,coin_y))
        th5 = Thread(target=check_if_collide_coin_item,args = (coin_x,coin_y))
        th4.start()
        th5.start()
        time.sleep(2)
        coin_item_display = False
def display_coin(cx,cy):
    global coin_item_display,coin_number
    while coin_item_display:
        screen.blit(pygame.transform.scale(coin_img[coin_number-1],(50,50)),(cx,cy))
def change_coin_number():
    global coin_number
    while not game_finish:
        time.sleep(0.1)
        coin_number += 1
        if coin_number>6:
            coin_number = 1
def check_if_collide_coin_item(cx,cy):
    global playerXpos,playerYpos,coin_item_display,score
    while coin_item_display:
        time.sleep(1/60)
        if (playerXpos-cx)**2 + (playerYpos-cy)**2 < 10000:
            score += 1000
            coin_item_display = False


def obstacle_hit():
    global playerXpos, playerYpos, hp, hpcolor, player_color, obshit, player_invincible, score, invinciblet, barrier_activated
    for i in range(len(obstacle)):
        if playerXpos > obstacle[i][0]-SIZE and playerXpos < obstacle[i][0]+obstacle[i][2] and playerYpos > obstacle[i][1]-SIZE and playerYpos < obstacle[i][1]+obstacle[i][3]:
            if player_invincible == True:
                hp += 0
            elif hpcolor == 1:
                hpcolor =0
                barrier_activated = False
                invinciblet = score
                player_color = red
                player_invincible = True
            else:
                if hp > 0:
                    hp -= 1
                    invinciblet = score
                    player_color = red
                    player_invincible = True


def invincible():
    global player_color, invinciblet, player_invincible
    if score == invinciblet +50:
        player_color = white
        player_invincible = False

def obstacle_vel():
    for i in range(len(obstacle)):
        obsspeed[i][1] += -obsacc[i]

def obstacle_movebyvel():
    for i in range(len(obstacle)):
        obstacle[i][0] += obsspeed[i][0]
        obstacle[i][1] -= obsspeed[i][1]

def reset_obstacle():
    for i in range(len(obstacle)):
        if obstacle[i][0]>1920 or obstacle[i][0]<-20 or obstacle[i][1]>1080 :
            obstacle[i][0] = random.randint(0,1900)
            obstacle[i][1] = random.randint(0,500)-300
            obsspeed[i][0] = random.randint(-10,10)
            obsspeed[i][1] = 0-random.randint(0,15)


def dead_check():
    global hp,game_finish
    if hp <= 0:
        game_finish = True

def start_screen():
    pygame.draw.rect(screen, black, [0, 0, 1920, 1080])
    screen.blit(pygame.transform.scale(pygame.image.load("images/startbutton.png"), (400, 150)), (760, 600))

def end_screen():
    global score
    pygame.draw.rect(screen, black, [0, 0, 1920, 1080])
    gameover_str = "GAME OVER"
    gameover_img = game_font1.render(gameover_str,True,red)
    screen.blit(gameover_img,(960-25*len(gameover_str),400))
    score_str = str(score)
    score_x = 960 - 25 * len(str(score))
    score_y = 500
    score_img = game_font1.render(score_str, True, white)
    screen.blit(score_img, (score_x, score_y))

    grade_str = "GRADE: "
    if score >= 1000000:
        grade_str += "GOD"
    elif score > 500000:
        grade_str += "S+"
    elif score > 200000:
        grade_str+="S"
    elif score > 100000:
        grade_str += "S-"
    elif score>=90000:
        grade_str += "A+"
    elif score>=85000:
        grade_str += "A0"
    elif score>=80000:
        grade_str += "A-"
    elif score>=75000:
        grade_str += "B+"
    elif score>=70000:
        grade_str += "B0"
    elif score>=65000:
        grade_str += "B-"
    elif score>=60000:
        grade_str += "C+"
    elif score>=55000:
        grade_str += "C0"
    elif score>=50000:
        grade_str += "C-"
    elif score>=45000:
        grade_str += "D+"
    elif score>=40000:
        grade_str += "D0"
    elif score>=35000:
        grade_str += "D-"
    elif score>=30000:
        grade_str += "E"
    else:
        grade_str += "F"
    grade_img = game_font1.render(grade_str,True,white)
    screen.blit(grade_img,(960-25*len(grade_str),600))

if __name__ == '__main__':
    bgm.play(-1)
    th2 = Thread(target=stage_loop)
    th2.start()
    th3 = Thread(target=random_spell)
    th3.start()
    th0 = Thread(target=change_coin_number)
    th0.start()
    th4 = Thread(target=random_coin)
    th4.start()
    while True:
        clock.tick(60)

        check_quit()
        if not game_finish:
            add_score()
            if not player_rigid:
                movebykey(player_speed)
                vel()
                movebyvelocity(velocity)

            obstacle_vel()
            obstacle_movebyvel()
            reset_obstacle()
            stayinside()
            stayon_platform()
            obstacle_hit()
            invincible()
            display_player()
            display_score()
            display_health()
            display_spell()
            display_barrier()
        else:

            end_screen()


        dead_check()
        th1 = Thread(target=spell_check)
        th1.start()
        pygame.display.update()



