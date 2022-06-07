import pygame
import config as c
from gameobject import GameObject

class Bg_for_button(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, 'game2images/g2_bg_for_buttons.png')

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))

class Move_button(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 80, 80, 'game2images/g2_movebutton_1.png')

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))

class Move_button_clicked(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 80, 80, 'game2images/g2_movebutton_clicked.png')

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))