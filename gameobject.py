from pygame.rect import Rect
import pygame


class GameObject:
    def __init__(self, x, y, w, h, image):
        self._rect = Rect(x, y, w, h)
        self.image = pygame.image.load(image)

    def draw(self, surface):
        surface.blit(self.image, (self.rect.left, self.rect.top))

    def collidepoint(self, x, y):
        return self._rect.collidepoint(x, y)

    def newturn(self):
        pass

    def update(self):
        pass
