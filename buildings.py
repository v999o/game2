from animations import CapitalAnim
from gameobject import GameObject


class Capital(GameObject):
    def __init__(self, x, y, color):
        super().__init__(x, y, 40, 40, 'game2images/g2capital_new_' + color + '.png')
        self.__color = color
        self.__clicked = False
        self.__anim = CapitalAnim(x, y, color)
        self.__clicked_image = self.__anim.image5

    def __set_clicked(self, value):
        self.__clicked = value
        if value:
            self.__anim.restart()

    clicked = property(fget=lambda self: self.__clicked, fset=__set_clicked)

    def type(self):
        return 'capital'

    def color(self):
        return self.__color

    def draw(self, surface):
        if self.__clicked:
            if not self.__anim.finished():
                self.__anim.draw(surface)
            else:
                surface.blit(self.__clicked_image, (self._rect.x, self._rect.y))
        else:
            surface.blit(self.image, (self._rect.x, self._rect.y))

    def update(self):
        if not self.__anim.finished():
            self.__anim.update()


class Factory_red(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, 'game2images/g2factory_red_new.png')

    def color(self):
        return 'red'

    def type(self):
        return 'factory'

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))


class Factory_blue(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, 'game2images/g2factory_blue_new.png')

    def color(self):
        return 'blue'

    def type(self):
        return 'factory'

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))
