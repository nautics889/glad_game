import pygame
import os

from random import randint, choice
from entities import Bar, Glad, Speech
from parameters import *
from db_connector import DataBase

#define the path to the current file
PATH = os.getcwd()

def timer(screen, timer_width):
    '''Display a timer on the top left side of a screen'''
    time_line = pygame.image.load(os.path.join(PATH, r'textures\time_line.gif')).convert_alpha()
    time_line = pygame.transform.scale(time_line, (timer_width, 30))
    screen.blit(time_line, (20, 20))

def display_score(screen, score):
    '''Display a scorebar on the bottom left side of a screen'''
    font = pygame.font.Font(None, 24)
    text = font.render('СчётЭ: {}'.format(score), 1, (0, 0, 0))
    screen.blit(text, ((20, SCREENHEIGHT-44)))

def display_hint(screen):
    '''Display hints of the top right side of a screen
       Calling only at the beginning of a game (when score==0)'''
    font = pygame.font.Font(None, 24)
    text = font.render('Нажимайте стрелки ВПРАВО/ВЛЕВО', 1, (150, 150, 150))
    screen.blit(text, ((CENTER[0] + 150, 20)))

    font = pygame.font.Font(None, 18)
    text = font.render('Избегайте банов и следите за временем слева', 1, (150, 150, 150))
    screen.blit(text, ((CENTER[0] + 150, 54)))

def display_time_out_speech(screen, speech):
    '''Draw and display speech with cloud when timer's time runned out'''
    pygame.draw.ellipse(screen, (0, 0, 0), (30,50,161,61), 2)
    pygame.draw.line(screen, (0, 0, 0), [30, 40], [40, 65], 2)
    pygame.draw.line(screen, (0, 0, 0), [30, 40], [50, 60], 2)
    pygame.draw.line(screen, (255, 255, 255), [48, 60], [42, 65], 6)

    font = pygame.font.Font(None, 24)
    text = font.render(speech, 1, (0, 0, 0))
    screen.blit(text, ((55, 72)))

def losing(screen, db):
    '''Display info when it's lost'''
    #main expression
    font = pygame.font.Font(os.path.join(PATH, r'fonts\ban.otf'), 72)
    text = font.render('Не ну это БАН', 1, (255,0,0))
    screen.blit(text, ((CENTER[0]-text.get_width()//2, CENTER[1])))

    #hint for restart
    font = pygame.font.Font(None, 24)
    text = font.render('Нажмите r для рестарта', 1, (150, 150, 150))
    screen.blit(text, ((CENTER[0]+150, 20)))

    #recordbar
    text = font.render('Рекорд: {}'.format(db.get_highest_score()), 1, (0, 0, 0))
    screen.blit(text, ((SCREENWIDTH-120, SCREENHEIGHT-44)))

#initialize pygame library
pygame.init()

#define a screen
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('Glad-Arcade')

#define database's interface
db = DataBase()

#create sprite's list
bar_sprites_list = list()
player_sprites_list = pygame.sprite.Group()

#define player object
glad = Glad(CENTER, SCREENHEIGHT, os.path.join(PATH, r'textures\glad.png'))

#add player object to sprites list
player_sprites_list.add(glad)

#define other resources for game
background = pygame.image.load(os.path.join(PATH, r'textures\background.gif')).convert_alpha()
speeches = list()
time_out_speech = choice(TIME_OUT_SPEECHES)

#set flags
running = True
restart = False
loss = False
score_added = False

#define clock
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #restart event
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            restart = True

        #move event
        elif event.type == pygame.KEYDOWN and not loss:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                #move bars down
                for item in bar_sprites_list:
                    item.rect.y += 40
                #create new bar
                prob = randint(0, 4)
                if prob is 0:
                    bar = Bar('left', os.path.join(PATH, r'textures/bar_{0}.png'))
                    bar.rect.x = CENTER[0] - 106
                    bar.rect.y = 0

                    bar_sprites_list.append(bar)
                elif prob is 1:
                    bar = Bar('right', os.path.join(PATH, r'textures/bar_{0}.png'))
                    bar.rect.x = CENTER[0] + 15
                    bar.rect.y = 0

                    bar_sprites_list.append(bar)
                #move player left if it's right
                if event.key == pygame.K_LEFT:
                    if glad.side == 'right':
                        glad.side = 'left'
                        glad.leap()
                    speech = Speech(choice(SPEECHES), os.path.join(PATH, r'fonts\speeches.otf'))
                    speech.rect.x = CENTER[0] - 120 - speech.text.get_width()
                    speech.rect.y = SCREENHEIGHT - 52
                    speeches.append(speech)
                #move player right if it's left
                elif event.key == pygame.K_RIGHT:
                    if glad.side == 'left':
                        glad.side = 'right'
                        glad.leap()
                    speech = Speech(choice(SPEECHES), os.path.join(PATH, r'fonts\speeches.otf'))
                    speech.rect.x = CENTER[0] + 120
                    speech.rect.y = SCREENHEIGHT - 52
                    speeches.append(speech)

                #expend timebar and increase score
                TIMER_WIDTH += 10
                SCORE += 1

    #reset game resources and flags when restart==True
    if restart:
        bar_sprites_list.clear()
        restart = False
        loss = False
        score_added = False
        time_out_speech = choice(TIME_OUT_SPEECHES)
        SCORE = 0
        TIMER_WIDTH = 230

    player_sprites_list.update()

    #render background
    screen.blit(background, (0, 0))

    #display hint at start
    if SCORE == 0 and not loss:
        display_hint(screen)

    #check timebar and running it out
    if TIMER_WIDTH > 0 and loss == False:
        timer(screen, round(TIMER_WIDTH))
        surcharge = SCORE*COEF
        TIMER_WIDTH -= 1 + surcharge
    else:
        loss = True
        display_time_out_speech(screen, time_out_speech)

    #display stems
    for i in range(AMOUNT_OF_BLOCKS):
        stem = pygame.image.load(os.path.join(PATH, r'textures\stem.gif')).convert_alpha()
        screen.blit(stem, (CENTER[0] - 15, 40*i))

    #display bars
    for bar in bar_sprites_list:
        screen.blit(bar.image, (bar.rect.x, bar.rect.y))

    #render player and score
    player_sprites_list.draw(screen)
    display_score(screen, SCORE)

    #display and move speeches
    for speech in speeches:
        screen.blit(speech.text, ((speech.rect.x, speech.rect.y)))
        speech.rect.y -= 3
        if speech.rect.y < 0:
            del speech

    #display losing items and add score to database
    if loss:
        losing(screen, db)
        if not score_added:
            db.add_score(SCORE)
            score_added = True

    #check either bar_sprite_list has items and set it into a variable
    list_not_empty = len(bar_sprites_list) != 0

    if list_not_empty:
        #check either the lowerest bar has run out from window
        bar_out = bar_sprites_list[0].rect.y >= SCREENHEIGHT
        #delete it if it has
        if bar_out:
            del bar_sprites_list[0]
        #check collision between player and the lowerest bar
        collision_with_bar = bar_sprites_list[0].rect.y >= SCREENHEIGHT - 60 and glad.side == bar_sprites_list[0].pos
        if list_not_empty and collision_with_bar:
            loss = True

    pygame.display.flip()

    clock.tick(60)

pygame.quit()