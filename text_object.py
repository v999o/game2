import pygame
from gameobject import GameObject


class TextObject(GameObject):
    def __init__(self, x, y, text_func, color, font_name, font_size):
        super().__init__(x, y, 0, 0, None)
        self.__text_func = text_func
        self.__color = color
        self.__font = pygame.font.SysFont(font_name, font_size)
        surface = self.__get_surface()
        self._rect.width = surface.get_rect().width
        self._rect.height = surface.get_rect().height

    def type(self):
        return 'textobject'

    def color(self):
        return self.__color

    def draw(self, surface, centralized=False):
        text_surface = self.__get_surface()
        if centralized:
            pos = (self.x - text_surface.get_rect().width // 2, self.y)
        else:
            pos = (self.x, self.y)
        surface.blit(text_surface, pos)

    def newturn(self):
        pass

    def collidepoint(self, x, y):
        return False

    def update(self):
        pass

    def __get_surface(self):
        return self.__font.render(self.__text_func(), False, self.__color)
