import pygame
from gameobject import GameObject


class Animation(GameObject):
    def __init__(self, x, y, i1, i2, i3, i4, i5, life):
        super(Animation, self).__init__(x, y, 40, 40, i1)
        self.image1 = pygame.image.load(i1)
        self.image2 = pygame.image.load(i2)
        self.image3 = pygame.image.load(i3)
        self.image4 = pygame.image.load(i4)
        self.image5 = pygame.image.load(i5)
        self.life = life
        self.max_life = life

    def type(self):
        return 'animation'

    def anim_type(self):
        pass

    def finished(self):
        return self.life <= 0

    def draw(self, surface):
        if self.life > (self.max_life // 5) * 4:
            surface.blit(self.image1, (self._rect.x, self._rect.y))
        elif (self.max_life // 5) * 3 < self.life <= (self.max_life // 5) * 4:
            surface.blit(self.image2, (self._rect.x, self._rect.y))
        elif (self.max_life // 5) * 2 < self.life <= (self.max_life // 5) * 3:
            surface.blit(self.image3, (self._rect.x, self._rect.y))
        elif (self.max_life // 5) < self.life <= (self.max_life // 5) * 2:
            surface.blit(self.image4, (self._rect.x, self._rect.y))
        elif self.life <= self.max_life // 5:
            surface.blit(self.image5, (self._rect.x, self._rect.y))

    def update(self):
        if self.life > 0:
            self.life = self.life - 1
        super().update()

    def restart(self):
        self.life = self.max_life


class Soldier_blue_click_anim(Animation):
    def __init__(self, x, y):
        super(Soldier_blue_click_anim, self).__init__(x, y, 'game2images/g2soldier_blue_clickanim1.png',
                                                      'game2images/g2soldier_blue_clickanim2.png',
                                                      'game2images/g2soldier_blue_clickanim3.png',
                                                      'game2images/g2soldier_blue_clickanim4.png',
                                                      'game2images/g2soldier_blue_clickanim5.png', 25)

    def anim_type(self):
        return 'soldier_blue_click_anim'


class Soldier_red_click_anim(Animation):
    def __init__(self, x, y):
        super(Soldier_red_click_anim, self).__init__(x, y, 'game2images/g2soldier_red_clickanim1.png',
                                                     'game2images/g2soldier_red_clickanim2.png',
                                                     'game2images/g2soldier_red_clickanim3.png',
                                                     'game2images/g2soldier_red_clickanim4.png',
                                                     'game2images/g2soldier_red_clickanim5.png', 25)

    def anim_type(self):
        return 'soldier_red_click_anim'


class Choose_fieldsquare_anim(Animation):
    def __init__(self, x, y):
        super(Choose_fieldsquare_anim, self).__init__(x, y, 'game2images/g2fieldsquare_choose_anim1.png',
                                                      'game2images/g2fieldsquare_choose_anim2.png',
                                                      'game2images/g2fieldsquare_choose_anim3.png',
                                                      'game2images/g2fieldsquare_choose_anim4.png',
                                                      'game2images/g2fieldsquare_choose_anim5.png', 20)

    def anim_type(self):
        return 'choose_fieldsquare'


class Fieldsquares_others_anim(Animation):
    def __init__(self, x, y):
        super(Fieldsquares_others_anim, self).__init__(x, y, 'game2images/g2fieldsquare_anim_1.png',
                                                       'game2images/g2fieldsquare_anim_2.png',
                                                       'game2images/g2fieldsquare_anim_3.png',
                                                       'game2images/g2fieldsquare_anim_4.png',
                                                       'game2images/g2fieldsquare_anim_5.png', 15)

    def anim_type(self):
        return 'fieldsquare_other'


class CapitalAnim(Animation):
    def __init__(self, x, y, color):
        super(CapitalAnim, self).__init__(x, y, 'game2images/g2capital_clickanim_1_' + color + '.png',
                                          'game2images/g2capital_clickanim_2_' + color + '.png',
                                          'game2images/g2capital_clickanim_3_' + color + '.png',
                                          'game2images/g2capital_clickanim_4_' + color + '.png',
                                          'game2images/g2capital_clickanim_5_' + color + '.png', 25)
