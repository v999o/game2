import pygame
import config as c
from gameobject import GameObject

class Soldier(GameObject):
    def __init__(self, x, y, color, avatar):
        super().__init__(x, y, 40, 40, avatar)
        self.color = color
        self.move_left = 1

    def color(self):
        return self.color

    def type(self):
        return 'soldier'

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))

class Soldier_blue(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, blue, 'game2images/g2soldier_blue.png')
        self.move_left = 1

    def color(self):
        return 'blue'

    def type(self):
        return 'soldier'

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))

class Soldier_blue_clicked(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, 'game2images/g2soldier_blue_clicked.png')
        # self.move_left = 1

    def color(self):
        return 'blue'

    def type(self):
        return 'soldier'

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))

class Soldier_red(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, 'game2images/g2soldier_red.png')
        self.move_left = 1

    def color(self):
        return 'red'

    def type(self):
        return 'soldier'

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))

class Soldier_red_clicked(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, 'game2images/g2soldier_red_clicked.png')
        # self.move_left = 1

    def color(self):
        return 'red'

    def type(self):
        return 'soldier'

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))