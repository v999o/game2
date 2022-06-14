import pygame
import config as c
from gameobject import GameObject

class Spawn_soldier_button(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 80, 80, 'game2images/g2_spawn_soldier_button.png')

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))

class Spawn_soldier_button_clicked(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 80, 80, 'game2images/g2_spawn_soldier_button_clicked.png')

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))

class Spawn_factory_button(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 80, 80, 'game2images/g2_spawn_factory_button.png')

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))

class Spawn_factory_button_clicked(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 80, 80, 'game2images/g2_spawn_factory_button_clicked.png')

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))