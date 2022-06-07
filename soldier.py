import pygame
import config as c
from gameobject import GameObject

class Soldier_blue(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, 'game2images/g2soldier_blue.png')

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))

class Soldier_blue_clicked(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, 'game2images/g2soldier_blue_clicked.png')

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))

class Soldier_red(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, 'game2images/g2soldier_red.png')

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))

class Soldier_red_clicked(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, 'game2images/g2soldier_red_clicked.png')

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))