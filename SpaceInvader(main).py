import pygame
from pygame import mixer  # music library
import pyttsx3
import math  # math module
import random  # random int package

# initializing of pygame module !!
pygame.init()

# initializing text to speech module
a = pyttsx3.init()
a.say("welcome to space invaders")
a.runAndWait()

# Title and icon
pygame.display.set_caption("SPACE INVADERS !!")
icon = pygame.image.load("ufo.jpg")
pygame.display.set_icon(icon)

# creating a screen
screen = pygame.display.set_mode((801, 601))

# Background image
Background = pygame.image.load("bcg.jpg")

# Player

playerImg = pygame.image.load("space.png")
playerX = 370
playerY = 480
playerX_change = 0  # speed of Player in X direction

# Enemy:

# Creating an empty list to create MULTIPLE ENEMIES
EnemyImg = []
EnemyX = []
EnemyY = []
EnemyX_change = []  # speed of enemies in X direction
EnemyY_change = []  # speed of enemies in Y direction

# mutable number of enemies
num_of_enemies = 7

# for loop is used to add values to the empty list
for i in range(num_of_enemies):
    # using append func to add the specified number of enemies as the loop repeats
    EnemyImg.append(pygame.image.load("skull.png"))  # 1
    EnemyImg.append(pygame.image.load("ghost.png"))  # 2  # .append is use to add elements to list
    EnemyImg.append(pygame.image.load("ufo.png"))  # 3
    EnemyImg.append(pygame.image.load("sci-fi.png"))  # 4
    EnemyImg.append(pygame.image.load("rude.png"))  # 5
    EnemyX.append(random.randint(0, 736))
    EnemyY.append(random.randint(30, 130))
    EnemyX_change.append(5.5)  # speed of enemy in X direction
    EnemyY_change.append(25)  # speed of enemy in Y direction

# Bullets:

# Ready - bullet is not visible on the screen
# Fire - bullet is in motion
bulletImg = pygame.image.load("bullets.png")
bulletX = 370
bulletY = 480  # Y- coordinate of the ship does'nt changes
bulletX_change = 0
bulletY_change = 17  # Speed of the bullet
bullet_count = 0  # number of bullets
bullet_state = "ready"  # position of bullet

# Score bar
Score_value = 0
font = pygame.font.Font("freesansbold.ttf", 36)
textX = 10
textY = 10

# GAME_OVER coordinates
Game_over_font = pygame.font.Font("freesansbold.ttf", 110)

# background music:
mixer.music.load("background.wav")  # for long term play 'music' function is used
mixer.music.play(-1)  # '-1' will help play the music all the time


# collision function
def is_collision(EnemyX, EnemyY, bulletX, bulletY):
    # collision can be calculated using distance between the two objects
    distance = math.sqrt((math.pow(EnemyX - bulletX, 2)) + (math.pow(EnemyY - bulletY, 2)))
    if distance <= 27:
        return True
    else:
        return False


def player(x, y):
    screen.blit(playerImg, (x, y))  # blit means draw


def enemy(x, y, i):
    screen.blit(EnemyImg[i], (x, y))  # drawing enemy on screen


def fire_bullet(x, y):
    global bullet_state  # defining variable globally
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 20))  # drawing bullet on screen behind the spaceship


def show_score():
    score = font.render("Score: " + str(Score_value), True, (255, 255, 150), None)  # first we render the text
    screen.blit(score, (textX, textY))  # then we draw it out on screen


def game_over_text():
    game_over = Game_over_font.render("GAME OVER", True, (255, 255, 255), None)
    screen.blit(game_over, (75, 250))


# Game loop
'''Properties that are persistent throughout the game or that does'nt 
changes are going to be in while loop like background etc'''

running = True  # Game starting variable
while running:

    # screen background (RGB)
    screen.blit(Background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # KEYBOARD commands (key pressing etc)
        if event.type == pygame.KEYDOWN:  # KEY-DOWN means pressing of any button o keyboard
            if event.key == pygame.K_LEFT:
                playerX_change = -10
            elif event.key == pygame.K_RIGHT:
                playerX_change = 10
            elif event.key == pygame.K_UP:
                if bullet_state == "ready":
                    # get the current x coordinate of space ship
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)

                    # bullet fire music
                    bullet_sound = mixer.Sound("laser.wav")  # for short moment "sound" is used
                    mixer.Sound.play(bullet_sound)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # function player and enemy should be call after screen fill as it would disappear otherwise

    # Changing coordinates at x-axis of player
    playerX += playerX_change

    # Player boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # creating for loop for empty list of enemies

    for i in range(num_of_enemies):

        # GAME-OVER
        if EnemyY[i] > 440:  # if any enemy crosses the given coordinate this condition will proceed
            for j in range(num_of_enemies):  # calling ll enemies
                EnemyY[j] = 2000  # setting coordinate of enemies out of screen
            game_over_text()
            break  # break out of loop (one time needed)

            # Enemy movement
        EnemyX[i] += EnemyX_change[i]

        # Enemy boundaries
        if EnemyX[i] <= 0:  # [i] is used to access elements inside the list
            EnemyX_change[i] = 10
            EnemyY[i] += EnemyY_change[i]
        elif EnemyX[i] >= 736:
            EnemyX_change[i] = -12
            EnemyY[i] += EnemyY_change[i]

        # collision of bullet and Enemy
        collision = is_collision(EnemyX[i], EnemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            bullet_count += 1
            Score_value += 1
            EnemyX[i] = random.randint(0, 736)
            EnemyY[i] = random.randint(30, 130)

            # Collision sound
            collision_sound = mixer.Sound("explosion.wav")
            mixer.Sound.play(collision_sound)

        enemy(EnemyX[i], EnemyY[i], i)

    # bullet movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 480

    player(playerX, playerY)
    show_score()  # calling show_score in while loop

    pygame.display.update()
