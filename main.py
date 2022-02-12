import pygame
import random
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 480))
pygame.display.set_caption("Zombies")

mixer.music.load("./sounds/lofisoftchord.mp3")
mixer.music.play(-1)

bulletSFX = mixer.Sound("./sounds/bullet.mp3")
bulletImg = pygame.image.load("./images/bullet.png")
bulletX = 30
bulletY = 240
bulletRect = bulletImg.get_rect()

GOfont = pygame.font.Font("./fonts/prstart.ttf", 64)

playerImg = pygame.image.load("./images/player.png")
playerRect = playerImg.get_rect()
playerRect.center = (32, 32)
playerRect.x = 10
playerYspeed = 0
playerRect.y = 240

enemyImg = pygame.image.load("./images/enemy.png")
enemyIMAGES = []
enemies = []

for enemy in range(4):
    enemies.append(enemyImg.get_rect())
    enemyIMAGES.append(enemyImg)

def drawPlayer():
    screen.blit(playerImg, playerRect)

def drawEnemy(i):
    screen.blit(enemyIMAGES[i], (enemies[i].x, enemies[i].y))

def enemyMovement(i):
    enemies[i].x -= 2.5

def isPlayerCollision(enemyRct):
    return playerRect.colliderect(enemyRct) or enemyRct.x <= 30

def isBulletCollision(enemyRct):
    return bulletRect.colliderect(enemyRct)

def setRandomEnemy(i):
    enemies[i].y = random.randint(0, 416)
    enemies[i].x = 700

bulletState = "ready"

score = 0

def shootBullet():
    global bulletState
    global score
    global soundCheck

    if bulletState == "ready":
        bulletRect.y = playerRect.y
        bulletRect.x = playerRect.x + 5
        soundCheck = True

    elif bulletState == "fire":
        screen.blit(bulletImg, bulletRect)
        if soundCheck:
            bulletSFX.play()
            soundCheck = False
        bulletRect.x += 16
        for enemy in range(len(enemies)):
            if isBulletCollision(enemies[enemy]):
                bulletState = "ready"
                setRandomEnemy(enemy)
                score += 1

    if bulletRect.x > 800:
        bulletState = "ready"

def main():
    playerRect.y += playerYspeed

    if playerRect.y >= 416:
        playerRect.y = 416
    elif playerRect.y <= 0:
        playerRect.y = 0
    
    for i in range(len(enemies)):
        drawEnemy(i)
        enemyMovement(i)

    shootBullet()
    drawPlayer()

clock = pygame.time.Clock()
collision = False
running = True

for enemy in range(len(enemies)):
    enemies[enemy].y = random.randint(0, 416)
    enemies[enemy].x = 700

while running:
    screen.fill((255, 92, 35))

    for i in range(len(enemies)):
        if isPlayerCollision(enemies[i]):
            collision = True

    if collision != True:
        main()
    else:
        gotext = GOfont.render("GAME OVER", True, (0, 0, 0))
        scoretext = GOfont.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(gotext, (50, 200))
        screen.blit(scoretext, (50, 265))

    pygame.display.update()

    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                playerYspeed = -10

            elif event.key == pygame.K_DOWN:
                playerYspeed = 10

            elif event.key == pygame.K_SPACE and collision:
                collision = False
                playerRect.y = 240
                score = 0
                for i in range(len(enemies)):
                    setRandomEnemy(i)

            elif event.key == pygame.K_SPACE and not collision:
                bulletState = "fire"

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerYspeed = 0

        elif event.type == pygame.QUIT:
            running = False
            pygame.quit()