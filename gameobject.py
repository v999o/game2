from pygame.rect import Rect
import pygame


class GameObject:
    def __init__(self, x, y, w, h, image):
        self._rect = Rect(x, y, w, h)
        if image is None:
            self.image = None
        else:
            self.image = self._load_image(image)

    def type(self):
        return 'game_object'

    def color(self):
        return "no_color"

    def draw(self, surface):
        surface.blit(self.image, (self._rect.left, self._rect.top))

    def collidepoint(self, x, y):
        return self._rect.collidepoint(x, y)

    def newturn(self):
        pass

    def update(self):
        pass

    @staticmethod
    def _load_image(image):
        return pygame.image.load(image)

    @property
    def x(self):
        return self._rect.x

    @property
    def y(self):
        return self._rect.y
