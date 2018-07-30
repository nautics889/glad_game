import pygame
from entities import Bar, Glad, Speech
from random import randint, choice
from db_connector import DataBase

pygame.init()

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

SCREENWIDTH = 1000
SCREENHEIGHT = 600
CENTER = (SCREENWIDTH//2, SCREENHEIGHT//2)
SPEECHES = ['ШО?', 'ТЕБЕ ВЪЕБАТЬ?', 'ПОПАВСЬ!', 'ХУЯНДОК', 'ДАБДА', 'ДАДАЯБДЯ', 'ДАДАЯ', 'ДАЭ', 'ЗДРАВСТВУЙТЕ']
TIME_OUT_SPEECHES = ['ТА ЗА ШО?', 'ЗА ШО ДЕДА?', 'ТЬФУ СУКА', 'У СУКА ЗА ШО']

def timer(screen, timer_width):
    time_line = pygame.image.load("textures/time_line.gif").convert_alpha()
    time_line = pygame.transform.scale(time_line, (timer_width, 30))
    screen.blit(time_line, (20, 20))

def display_score(screen, score):
    font = pygame.font.Font(None, 24)
    text = font.render('СчётЭ: {}'.format(score), 1, (0, 0, 0))
    screen.blit(text, ((20, SCREENHEIGHT-44)))

def display_hint(screen):
    font = pygame.font.Font(None, 24)
    text = font.render('Нажимайте стрелки ВПРАВО/ВЛЕВО', 1, (150, 150, 150))
    screen.blit(text, ((CENTER[0] + 150, 0)))

    font = pygame.font.Font(None, 18)
    text = font.render('Избегайте банов и следите за временем слева', 1, (150, 150, 150))
    screen.blit(text, ((CENTER[0] + 150, 34)))

def check_collision(glad, bar):
    if glad.side == bar.pos and bar.rect.y >= SCREENHEIGHT-60:
        return True
    else:
        return False

def display_time_out_speech(screen, speech):
    pygame.draw.ellipse(screen, (0, 0, 0), (30,50,161,61), 2)
    pygame.draw.line(screen, (0, 0, 0), [30, 40], [40, 65], 2)
    pygame.draw.line(screen, (0, 0, 0), [30, 40], [50, 60], 2)
    pygame.draw.line(screen, (255, 255, 255), [48, 60], [42, 65], 6)
    font = pygame.font.Font(None, 24)
    text = font.render(speech, 1, (0, 0, 0))
    screen.blit(text, ((55, 72)))

def lossing(screen, db):
    font = pygame.font.Font('fonts/ban.otf', 72)
    text = font.render('Не ну это БАН', 1, (255,0,0))
    screen.blit(text, ((CENTER[0]-text.get_width()//2, CENTER[1])))

    font = pygame.font.Font(None, 24)
    text = font.render('Нажмите r для рестарта', 1, (150, 150, 150))
    screen.blit(text, ((CENTER[0]+150, 0)))

    text = font.render('Рекорд: {}'.format(db.get_highest_score()), 1, (0, 0, 0))
    screen.blit(text, ((SCREENWIDTH-120, SCREENHEIGHT-44)))

screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('sample')

db = DataBase()

bar_sprites_list = list()
player_sprites_list = pygame.sprite.Group()

glad = Glad(CENTER, SCREENHEIGHT)

player_sprites_list.add(glad)

amount_of_blocks = SCREENHEIGHT//40
timer_width = 230
score = 0
coef = 0.003
speeches = list()
time_out_speech = choice(TIME_OUT_SPEECHES)

running = True
restart = False
loss = False
score_added = False
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            restart = True

        elif event.type == pygame.KEYDOWN and not loss:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                for item in bar_sprites_list:
                    item.rect.y += 40
                prob = randint(0, 4)
                if prob is 0:
                    bar = Bar('left')
                    bar.rect.x = CENTER[0] - 106
                    bar.rect.y = 0

                    bar_sprites_list.append(bar)
                elif prob is 1:
                    bar = Bar('right')
                    bar.rect.x = CENTER[0] + 15
                    bar.rect.y = 0

                    bar_sprites_list.append(bar)
                if event.key == pygame.K_RIGHT:
                    if glad.side == 'right':
                        glad.side = 'left'
                        glad.leap()
                    speech = Speech(choice(SPEECHES))
                    speech.rect.x = CENTER[0] - 120 - speech.text.get_width()
                    speech.rect.y = SCREENHEIGHT - 52
                    speeches.append(speech)

                elif event.key == pygame.K_LEFT:
                    if glad.side == 'left':
                        glad.side = 'right'
                        glad.leap()
                    speech = Speech(choice(SPEECHES))
                    speech.rect.x = CENTER[0] + 120
                    speech.rect.y = SCREENHEIGHT - 52
                    speeches.append(speech)

                timer_width += 10
                score += 1

    if restart:
        bar_sprites_list.clear()
        restart = False
        loss = False
        score_added = False
        score = 0
        timer_width = 230
        time_out_speech = choice(TIME_OUT_SPEECHES)

    player_sprites_list.update()

    screen.fill(WHITE)

    if score == 0 and not loss:
        display_hint(screen)

    if timer_width > 0 and loss == False:
        timer(screen, round(timer_width))
        surcharge = score*coef
        timer_width -= 1 + surcharge
    else:
        loss = True
        display_time_out_speech(screen, time_out_speech)

    for i in range(amount_of_blocks):
        stem = pygame.image.load("textures/stem.gif").convert_alpha()
        screen.blit(stem, (CENTER[0] - 15, 40*i))

    for bar in bar_sprites_list:
        screen.blit(bar.image, (bar.rect.x, bar.rect.y))

    player_sprites_list.draw(screen)
    display_score(screen, score)

    for speech in speeches:
        screen.blit(speech.text, ((speech.rect.x, speech.rect.y)))
        speech.rect.y -= 3
        if speech.rect.y < 0:
            del speech

    if loss:
        lossing(screen, db)
        if not score_added:
            db.add_score(score)
            score_added = True

    list_not_empty = len(bar_sprites_list) != 0
    if list_not_empty:
        bar_out = bar_sprites_list[0].rect.y >= SCREENHEIGHT
        if bar_out:
            del bar_sprites_list[0]
        collision_with_bar = bar_sprites_list[0].rect.y >= SCREENHEIGHT - 60 and glad.side == bar_sprites_list[0].pos
        if list_not_empty and collision_with_bar:
            loss = True

    pygame.display.flip()

    clock.tick(60)

pygame.quit()