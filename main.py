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

GOfont = pygame.font.Font("./fonts/prstart.ttf", 24)

playerImg = pygame.image.load("./images/player.png")
playerRect = playerImg.get_rect()
playerRect.center = (32, 32)
playerRect.x = 10
playerRect.y = 240
playerYspeed = 0


enemyImg = pygame.image.load("./images/enemy.png")
enemyIMAGES = []
enemies = []

for enemy in range(4):
    enemies.append(enemyImg.get_rect())
    enemyIMAGES.append(enemyImg)

def drawPlayer(): screen.blit(playerImg, playerRect)
def drawEnemy(i): screen.blit(enemyIMAGES[i], (enemies[i].x, enemies[i].y))

def isPlayerCollision(enemyRct): return playerRect.colliderect(enemyRct) or enemyRct.x <= 30
def isBulletCollision(enemyRct): return bulletRect.colliderect(enemyRct)

def enemyMovement(i): enemies[i].x -= 2.5
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

    if bulletRect.x > 800: bulletState = "ready"

def main():
    playerRect.y += playerYspeed

    playerRect.y = 416 if playerRect.y > 416 else 0 if playerRect.y < 0 else playerRect.y

    for i in range(len(enemies)):
        drawEnemy(i)
        enemyMovement(i)

    shootBullet()
    drawPlayer()

gameState = 0
collision = False
running = True

for enemy in range(len(enemies)):
    enemies[enemy].y = random.randint(0, 416)
    enemies[enemy].x = 700

while running:
    screen.fill((255, 92, 35))

    for i in range(len(enemies)):
        if isPlayerCollision(enemies[i]): gameState = 1

    match gameState:
        case 0: main()
        case 1:
            gotext = GOfont.render("GAME OVER", True, (0, 0, 0))
            scoretext = GOfont.render(f"Score: {score}", True, (0, 0, 0))
            screen.blit(gotext, (50, 200))
            screen.blit(scoretext, (50, 265))
        case 2:
            instructions = GOfont.render("Press the UP and DOWN Keys to move", True, (0, 0, 0))
            closeWindow = GOfont.render("Press Escape again to resume", True, (0, 0, 0))
            screen.blit(instructions, (50, 200))
            screen.blit(closeWindow, (50, 265))

    pygame.display.update()
    pygame.time.Clock().tick(60)

    for event in pygame.event.get():
        match event.type:
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_UP: playerYspeed = -10
                    case pygame.K_DOWN: playerYspeed = 10
                    case pygame.K_SPACE:
                        if gameState == 0: bulletState = "fire"
                        elif gameState == 1:
                            gameState = 0
                            playerRect.y = 240
                            score = 0
                            for i in range(len(enemies)):
                                setRandomEnemy(i)
                    case pygame.K_ESCAPE:
                         if gameState != 1: gameState = 2 if gameState != 2 else 0
            case pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN: playerYspeed = 0
            case pygame.QUIT:
                running = False
                pygame.quit()
