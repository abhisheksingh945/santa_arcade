import pygame
import random
from pygame import mixer

# initializing pygame
pygame.init()
# creating window
screen = pygame.display.set_mode((1000, 667))

mixer.music.load("backgroundMusic.mp3")
mixer.music.play(-1)

running = True
# loading background image
background = pygame.image.load('background.png')
# window title
pygame.display.set_caption("SantaArcade")
# window icon
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

gameOver = False
numOfGifts = 25

#santa
santaImg = pygame.image.load('santa.png')
santaX = 470
santaY = 536
santaX_change = 0

#gifts
giftImg = []
giftX = []
giftY = []
giftY_change = 7
giftType = []
for i in range(numOfGifts):
    if i < 17:
        r = i % 5
    else:
        r = i % 2 + 5
    giftImg.append(pygame.image.load('gift{}.png'.format(r)))
    giftX.append(random.randint(0, 14) * 64)
    giftY.append(random.randint(-12, -1) * 72)
    if r > 4:
        giftType.append("bomb")
    else:
        giftType.append("present")

global scoreValue
global score
global highScoreValue
global highScore
scoreValue = 0
font = pygame.font.Font('freesansbold.ttf', 32)
highScoreValue = 0
highScore = font.render("High Score : " + str(scoreValue), True, (255, 255, 255))
score = font.render("Score : " + str(scoreValue), True, (255, 255, 255))
gameOver = False

#increase the score if santa touches a present
def updateScore():
    global highScore
    global scoreValue
    global highScoreValue
    global score
    scoreValue += 1
    highScoreValue = max(highScoreValue, scoreValue)
    highScore = font.render("High Score : " + str(highScoreValue), True, (255, 255, 255))
    score = font.render("Score : " + str(scoreValue), True, (255, 255, 255))

# check if the hitboxes of santa and the gifts are intersecting
def isCollision(x, w, y, h):
    flag = True
    if x + w < santaX + 33 or x > santaX + 94:
        flag = False
    if y + h < santaY or y > santaY + 148:
        flag = False
    return flag
#collision detection
def collision(i):
    if giftType[i] is "bomb":
        if isCollision(giftX[i] + 17, 26, giftY[i], 56):
            global gameOver
            gameOver = True
    else:
        if isCollision(giftX[i], 64, giftY[i], 64):
            updateScore()
            giftY[i] = random.randint(-3, -1) * 72
            giftX[i] = random.randint(0, 14) * 64

def showScore(x, y):
    screen.blit(score, (x, y))
    screen.blit(highScore, (x, y-50))

def displayGift(i, x, y):
    screen.blit(giftImg[i], (x, y))

def displaySanta(x, y):
    screen.blit(santaImg, (x, y))

over_font = pygame.font.Font('freesansbold.ttf', 64)

leftPressed = False
rightPressed = False

while running:
    #check if gifts are going out of screen
    for i in range(numOfGifts):
        if giftY[i] >= 630:
            giftY[i] = random.randint(-3, -1) * 72
            giftX[i] = random.randint(0, 14) * 64

    if gameOver:
        over_text = over_font.render("GAME OVER", True, (255, 0, 0))
        over_text = over_font.render("GAME OVER", True, (255, 0, 0))

        screen.blit(over_text, (200, 250))
        scoreValue = 0
        score = font.render("Score : 0", True, (255, 255, 255))
        santaX_change = 0
        leftPressed = False
        rightPressed = False
        for i in range(numOfGifts):
            giftY[i] = random.randint(-12, -1) * 72
            giftX[i] = random.randint(0, 14) * 64
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameOver = False
        pygame.display.update()
        continue
    screen.blit(background, (0, 0))
    #processing the key presses
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                santaX_change = -5
                leftPressed = True
            if event.key == pygame.K_RIGHT:
                santaX_change = 5
                rightPressed = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                leftPressed = False
            if event.key == pygame.K_RIGHT:
                rightPressed = False
        if not (leftPressed) and not (rightPressed):
            santaX_change = 0
        if not (leftPressed) and rightPressed:
            santaX_change = 5
        if leftPressed and not (rightPressed):
            santaX_change = -5
    santaX += santaX_change
    if santaX >= 890:
        santaX = 890
    elif santaX <= -22:
        santaX = -22
    for i in range(numOfGifts):
        giftY[i] += giftY_change
        displayGift(i, giftX[i], giftY[i])
    showScore(40, 60)
    displaySanta(santaX, santaY)
    for i in range(numOfGifts):
        collision(i)
    pygame.display.update()
