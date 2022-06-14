import pygame
import config as c
from gameobject import GameObject

class Fieldsquare_red(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, 'game2images/g2fieldsquare_red.png')

    def color(self):
        return 'red'

    def type(self):
        return 'fieldsquare'

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))

class Fieldsquare_blue(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, 'game2images/g2fieldsquare_blue.png')

    def color(self):
        return 'blue'

    def type(self):
        return 'fieldsquare'

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))
