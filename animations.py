import pygame
from gameobject import GameObject

class Animation(GameObject):
    def type(self):
        return 'animation'


class Soldier_blue_click_anim(Animation):
    def __init__(self, x, y):

        self.image1 = pygame.image.load(f'game2images/g2soldier_blue_clickanim1.png')
        self.image2 = pygame.image.load(f'game2images/g2soldier_blue_clickanim2.png')
        self.image3 = pygame.image.load(f'game2images/g2soldier_blue_clickanim3.png')
        self.image4 = pygame.image.load(f'game2images/g2soldier_blue_clickanim4.png')
        self.image5 = pygame.image.load(f'game2images/g2soldier_blue_clickanim5.png')

        GameObject.__init__(self, x, y, 40, 40, 'game2images/g2soldier_blue_clickanim3.png')
        self.life = 25

    def anim_type(self):
        pass

    def draw(self, surface):
        if self.life > 20:
            surface.blit(self.image1, (self._rect.x, self._rect.y))
        elif self.life > 15 and self.life <= 20:
            surface.blit(self.image2, (self._rect.x, self._rect.y))
        elif self.life > 10 and self.life <= 15:
            surface.blit(self.image3, (self._rect.x, self._rect.y))
        elif self.life > 5 and self.life <= 10:
            surface.blit(self.image4, (self._rect.x, self._rect.y))
        elif self.life <= 5:
            surface.blit(self.image5, (self._rect.x, self._rect.y))

    def update(self):
        if self.life > 0:
            self.life = self.life - 1
        super().update()

class Choose_fieldsquare_anim(Animation):
    def __init__(self, x, y):

        self.image1 = pygame.image.load(f'game2images/g2fieldsquare_choose_anim1.png')
        self.image2 = pygame.image.load(f'game2images/g2fieldsquare_choose_anim2.png')
        self.image3 = pygame.image.load(f'game2images/g2fieldsquare_choose_anim3.png')
        self.image4 = pygame.image.load(f'game2images/g2fieldsquare_choose_anim4.png')
        self.image5 = pygame.image.load(f'game2images/g2fieldsquare_choose_anim5.png')

        GameObject.__init__(self, x, y, 40, 40, 'game2images/g2fieldsquare_choose_anim1.png')
        self.life = 25

    def anim_type(self):
        return 'choose_fieldsquare'

    def draw(self, surface):
        if self.life > 20:
            surface.blit(self.image1, (self._rect.x, self._rect.y))
        elif self.life > 15 and self.life <= 20:
            surface.blit(self.image2, (self._rect.x, self._rect.y))
        elif self.life > 10 and self.life <= 15:
            surface.blit(self.image3, (self._rect.x, self._rect.y))
        elif self.life > 5 and self.life <= 10:
            surface.blit(self.image4, (self._rect.x, self._rect.y))
        elif self.life <= 5:
            surface.blit(self.image5, (self._rect.x, self._rect.y))

    def update(self):
        if self.life > 0:
            self.life = self.life - 1
        super().update()

class Fieldsquares_others_anim(Animation):
    def __init__(self, x, y):

        self.image1 = pygame.image.load(f'game2images/g2fieldsquare_anim_1.png')
        self.image2 = pygame.image.load(f'game2images/g2fieldsquare_anim_2.png')
        self.image3 = pygame.image.load(f'game2images/g2fieldsquare_anim_3.png')
        self.image4 = pygame.image.load(f'game2images/g2fieldsquare_anim_4.png')
        self.image5 = pygame.image.load(f'game2images/g2fieldsquare_anim_5.png')

        GameObject.__init__(self, x, y, 40, 40, 'game2images/g2fieldsquare_anim_1.png')
        self.life = 25

    def anim_type(self):
        return 'fieldsquare_other'

    def draw(self, surface):
        if self.life > 20:
            surface.blit(self.image1, (self._rect.x, self._rect.y))
        elif self.life > 15 and self.life <= 20:
            surface.blit(self.image2, (self._rect.x, self._rect.y))
        elif self.life > 10 and self.life <= 15:
            surface.blit(self.image3, (self._rect.x, self._rect.y))
        elif self.life > 5 and self.life <= 10:
            surface.blit(self.image4, (self._rect.x, self._rect.y))
        elif self.life <= 5:
            surface.blit(self.image5, (self._rect.x, self._rect.y))

    def update(self):
        if self.life > 0:
            self.life = self.life - 1
        super().update()