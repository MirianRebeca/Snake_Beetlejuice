import os
import sys
import pygame
import random

pygame.init()
pygame.mixer.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)
purple = (75, 0, 130)

display_width = 600
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Snake_Beetlejuice".center(155))

def find_data_file(filename):
    if getattr(sys, "frozen", False):
        datadir = os.path.dirname(sys.executable)
    else:
        datadir = os.path.dirname(__file__)
    return os.path.join(datadir, filename)


img_path = find_data_file("snake.png")
appleimg_path = find_data_file('apple.png')
wallimg_path = find_data_file('walls.png')
icon_path = find_data_file('icon.png')
bj_path = find_data_file("bj.mp3")

img = pygame.image.load(img_path)
appleimg = pygame.image.load(appleimg_path)
wallimg = pygame.image.load(wallimg_path)
icon = pygame.image.load(icon_path)

pygame.display.set_icon(icon)
pygame.mixer.music.load(bj_path)

clock = pygame.time.Clock()

appleThickness = 30
block_size = 20

direction = "right"

smallfont  = pygame.font.SysFont('Juice ITC   ', 35)
mediumfont = pygame.font.SysFont('Juice ITC', 50)
largefont = pygame.font.SysFont('Juice ITC', 130)


def paused():
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    pause = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill(black)
        message_to_screen("Pause", green,-100, "large")
        message_to_screen("Press C to continue or Q to quit", green, 25)
        pygame.display.update()
        clock.tick(5)

def score(score):
    text = smallfont.render("Score: "+str(score), True, black)
    gameDisplay.blit(text,[30,20])
    if score <10:
        level =1
    else:
        level = 2
        gameDisplay.blit(wallimg, (0, 0))
    text = smallfont.render("Level: "+str(level), True, black)
    gameDisplay.blit(text,[470,20])

def randAppleGen():
    randAppleX = round(random.randrange(50, display_width - 50))
    randAppleY = round(random.randrange(100, display_height - 50))
    return randAppleX,randAppleY

def change_level():
    level = True
    while level:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_c:
                    level = False
                if event.key==pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(purple)
        message_to_screen("Level 1 Passed", black, -100, "large" )
        message_to_screen("Press C to Level 2 or Q to Quit", black, 100, "medium")
        pygame.display.update()
        clock.tick(5)

def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_c:
                    intro=False
                if event.key==pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(black)
        message_to_screen("Welcome", green, -180, "large")
        message_to_screen("Use the arrow keys to move and 'Shift' to pause", green, 60, "small")
        message_to_screen("Press C to Play or Q to Quit", green, 215, "medium")
        pygame.display.update()
        clock.tick(5)

def snake(block_size, snakelist):
    if direction=="right":
        head = pygame.transform.rotate(img,270)
    if direction=="left":
        head = pygame.transform.rotate(img,90)
    if direction=="up":
        head = img
    if direction=="down":
        head = pygame.transform.rotate(img,180)

    gameDisplay.blit(head, (snakelist[-1][0], snakelist[-1][1]))

    blackList = True
    for XnY in snakelist[:-1]:
        if (blackList):
            pygame.draw.rect(gameDisplay, black, [XnY[0], XnY[1], block_size, block_size])
            blackList = False
        else:
            pygame.draw.rect(gameDisplay, white, [XnY[0], XnY[1], block_size, block_size])
            blackList = True

def text_objects(text, color, size):
    if size=="small":
        textSurface = smallfont.render(text, True, color)
    elif size=="medium":
        textSurface = mediumfont.render(text, True, color)
    elif size=="large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg, color, y_displace=0, size="small"):
    textSurf, texRect = text_objects(msg, color, size)
    texRect.center = (display_width/2), (display_height/2)+y_displace
    gameDisplay.blit(textSurf, texRect)

def gameLoop():
    global direction
    direction="right"
    gameExit = False
    gameOver = False

    lead_x = display_width / 2
    lead_y = display_height / 2

    lead_x_change = 10
    lead_y_change = 0

    snakeList = []
    snakeLength = 1

    randAppleX, randAppleY = randAppleGen()

    while not gameExit:
        while gameOver==True:
            gameDisplay.fill(black)
            message_to_screen("Game over", red, y_displace=-100, size="large")
            message_to_screen("Press C to play again or Q to quit", red, 100, size="medium")
            pygame.display.update()

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    gameExit==True
                    gameOver=False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit=True
                        gameOver=False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                gameExit=True
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    direction="left"
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key==pygame.K_RIGHT:
                    direction="right"
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key==pygame.K_UP:
                    direction="up"
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key==pygame.K_DOWN:
                    direction="down"
                    lead_y_change = block_size
                    lead_x_change = 0
                elif event.key == pygame.K_RSHIFT:
                    paused()


            # pygame.display.update()
        lead_x += lead_x_change
        lead_y += lead_y_change

        gameDisplay.fill(purple)
        gameDisplay.blit(appleimg, (randAppleX,randAppleY))

        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]
        for eachSegment in snakeList[:-1]:
            if eachSegment==snakeHead:
                gameOver=True

        snake(block_size, snakeList)

        if snakeLength <=10:
            score(snakeLength - 1)
            if lead_x >= display_width:
                lead_x = 0
            elif lead_x < 0:
                lead_x = display_width

            elif lead_y == display_height:
                lead_y = 0
            elif lead_y < 0:
                lead_y = display_height
        if snakeLength == 11:
            change_level()
            snakeLength += 1
        if snakeLength >= 11:
            score(snakeLength - 2)
            if lead_x >= display_width-appleThickness or lead_x < appleThickness or lead_y >= display_height-appleThickness or lead_y < appleThickness:
                gameOver = True

        pygame.display.update()

        if lead_x > randAppleX and lead_x < randAppleX+appleThickness or lead_x+block_size > randAppleX and lead_x+block_size < randAppleX+appleThickness:
            if lead_y > randAppleY and lead_y < randAppleY+appleThickness:
                randAppleX, randAppleY = randAppleGen()
                snakeLength += 1
                pygame.mixer.music.play()
            elif lead_y+block_size > randAppleY and lead_y+block_size < randAppleY+appleThickness:
                randAppleX, randAppleY = randAppleGen()
                snakeLength += 1
                pygame.mixer.music.play()

        clock.tick(snakeLength+5)

    pygame.quit()
    quit()
game_intro()
gameLoop()
