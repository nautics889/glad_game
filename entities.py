import pygame

class GreenSpace(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()

        self.image = pygame.Surface([50, 20])
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))

        pygame.draw.circle(screen, (255, 0, 0), [40, 40], 10)

        self.rect = self.image.get_rect()

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("textures/ball.gif").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()

class Bar(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.image.load("textures/bar_{0}.gif".format(pos)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (90, 30))
        self.rect = self.image.get_rect()
        self.pos = pos

class Glad(pygame.sprite.Sprite):
    def __init__(self, CENTER, SCREENHEIGHT, side='left'):
        super().__init__()

        self.image = pygame.image.load("textures/glad.gif").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = CENTER[0]-46
        self.rect.y = SCREENHEIGHT-40
        self.side = side

    def leap(self):
        if self.side=='left':
            self.rect.x -= 60
        elif self.side=='right':
            self.rect.x += 60

class Speech:
    def __init__(self, speech):
        self.font = pygame.font.Font('fonts/speeches.otf', 30)
        self.text = self.font.render(speech, 1, (0, 0, 0))
        self.rect = self.text.get_rect()