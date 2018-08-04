import pygame

class Bar(pygame.sprite.Sprite):
    '''Define bars, inherits from base sprite model'''
    def __init__(self, pos, PATH):
        super().__init__()

        self.image = pygame.image.load(PATH.format(pos)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (90, 30))
        self.rect = self.image.get_rect()
        self.pos = pos

class Glad(pygame.sprite.Sprite):
    '''Define player, inherits from base sprite model'''
    def __init__(self, CENTER, SCREENHEIGHT, PATH, side='left'):
        super().__init__()

        self.image = pygame.image.load(PATH).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = CENTER[0]-46
        self.rect.y = SCREENHEIGHT-40
        self.side = side

    def leap(self):
        '''Move to side according to self.side'''
        if self.side=='left':
            self.rect.x -= 60
        elif self.side=='right':
            self.rect.x += 60

class Speech:
    '''Define speech'''
    def __init__(self, speech, PATH):
        self.font = pygame.font.Font(PATH, 30)
        self.text = self.font.render(speech, 1, (0, 0, 0))
        self.rect = self.text.get_rect()