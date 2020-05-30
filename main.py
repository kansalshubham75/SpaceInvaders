import pygame
import random
import math
from pygame import mixer
# initialize module
pygame.init()

# create window
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('./public/background.png')

#background sound
mixer.music.load('./public/music.mp3')
mixer.music.play(-1)

#title and icon
pygame.display.set_caption("SpaceInvader")
icon = pygame.image.load('./public/spaceship.png')
pygame.display.set_icon(icon)

# player img
playerImg = pygame.image.load('./public/user.png')
playerx = 368  # starting x coordinate
playery = 500  # starting y coordinate
playerx_change = 0

# Ufo Image
ufoImg = []
ufox = []
ufoy = []
ufo_xchange = []
ufo_ychange = []
num_of_enemies = 6
for i in range(num_of_enemies):
    ufoImg.append(pygame.image.load('./public/ufo.png'))
    ufox.append(random.randint(0, 734))  # starting x coordinate
    ufoy.append(random.randint(50, 150))  # starting y coordinate
    ufo_xchange.append(3)
    ufo_ychange.append(40)

# bullet img
bulletImg = pygame.image.load('./public/bullet.png')
bulletx = 0
bullety = 500
bullety_change = 10
bulletState = "ready"  # ready-bullet not fired yet, fire-bullet currentlt moving

#Score
score_value = 0
font=pygame.font.Font('./public/font.ttf',32)
scorex=10
scorey=10

def show_score(x,y):
    score=font.render("Score :" + str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def fire_bullet(x, y):
    bullet_sound=mixer.Sound('./public/laser.wav')
    bullet_sound.play()
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (x+16, y+10))


def drawPlayer(x, y):  # update player position
    screen.blit(playerImg, (x, y))


def drawUfo(x, y, i):  # update ufo position
    screen.blit(ufoImg[i], (x, y))


def didCollide(ufox, ufoy, bulletx, bullety):
    dist = math.sqrt(((ufox-bulletx)**2)+((ufoy-bullety)**2))
    if(dist < 27):
        return True
    else:
        return False

def game_over():
    font= pygame.font.Font('./public/font.ttf',64)
    final_score=font.render("GAME OVER!",True,(255,255,255))
    screen.blit(final_score,(250,250))
    explosion_sound=mixer.Sound('./public/explosion.wav')
    explosion_sound.play()


# GAME LOOP
running = True

while running:
    # change color of background using rgb
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -5
            if event.key == pygame.K_RIGHT:
                playerx_change = 5
            if event.key == pygame.K_SPACE:
                if bulletState is "ready":
                    bulletx = playerx
                    fire_bullet(bulletx, bullety)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    # ufo_xchange=random.randint(-9,9)*0.2
    # ufo_ychange=random.randint(-5,5)*0.1

    # display bullet if fired
    if bulletState is "fire":
        bullety -= bullety_change
        fire_bullet(bulletx, bullety)

    # Reset the bullet
    if bullety <= 0:
        bullety = 480
        bulletState = "ready"

    playerx += playerx_change
    if playerx < 0:
        playerx = 0
    if playerx > 736:
        playerx = 736
#Enemy Movement
    for i in range(num_of_enemies):
    #gameOver Screen
        if ufoy[i]>460:
            for j in range(num_of_enemies):
                ufoy[j]=2000
            game_over()
            break

        ufox[i] += ufo_xchange[i]
        if ufox[i] <= 0:
            ufoy[i] += ufo_ychange[i]
            ufo_xchange[i] = 3

        if ufox[i] >= 736:
            ufoy[i] += ufo_ychange[i]
            ufo_xchange[i] = -3



    # detect collision
        collision = didCollide(ufox[i], ufoy[i], bulletx, bullety)
        if collision:
            explosion_sound=mixer.Sound('./public/explosion.wav')
            explosion_sound.play()
            bullety = 480
            bulletState = "ready"
            score_value += 1
            # print(score_value)
            ufox[i] = random.randint(0, 736)
            ufoy[i] = random.randint(50, 150)
        drawUfo(ufox[i], ufoy[i], i)

    drawPlayer(playerx, playery)
    show_score(scorex,scorey)
    pygame.display.update()
