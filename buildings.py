import pygame
import config as c
from gameobject import GameObject

class Capital_blue(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, 'game2images/g2capital.png')

    def type(self):
        return 'capital'

    def color(self):
        return 'blue'

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))

class Capital_blue_clicked(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, 'game2images/g2capital_clicked.png')

    def type(self):
        return 'capital'

    def color(self):
        return 'blue'

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))

class Capital_red(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, 'game2images/g2capital_clicked.png')

    def type(self):
        return 'capital'

    def color(self):
        return 'red'

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))

class Capital_red_clicked(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, 'game2images/g2capital_clicked.png')

    def type(self):
        return 'capital'

    def color(self):
        return 'red'

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))

class Factory_red(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, 'game2images/g2factory_red.png')

    def color(self):
        return 'red'

    def type(self):
        return 'factory'

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))

class Factory_blue(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, 'game2images/g2factory_blue.png')

    def color(self):
        return 'blue'

    def type(self):
        return 'factory'

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))




