import pygame
import config as c
from gameobject import GameObject

class Soldier(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, 'game2images/g2soldier.png')

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))

class Soldier_clicked(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, 'game2images/g2soldier_clicked.png')

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))