from animations import SoldierAnim
from gameobject import GameObject


class Soldier(GameObject):
    def __init__(self, x, y, color, avatar):
        super().__init__(x, y, 40, 40, avatar)
        self._color = color
        self.move_left = 1
        self.__anim = SoldierAnim(x, y, color)
        self.__clicked = False

    def __set_clicked(self, value):
        self.__clicked = value
        if value:
            self.__anim.restart()

    clicked = property(fget=lambda self: self.__clicked, fset=__set_clicked)

    def color(self):
        return self._color

    def type(self):
        return 'soldier'

    def draw(self, surface):
        if self.__clicked:
            if self.__anim.finished():
                surface.blit(self.__anim.image5, (self._rect.x, self._rect.y))
            else:
                self.__anim.draw(surface)
        else:
            surface.blit(self.image, (self._rect.x, self._rect.y))

    def update(self):
        if not self.__anim.finished():
            self.__anim.update()

    def newturn(self):
        self.move_left = 1

    def move(self, x, y):
        self.x = x
        self.y = y
        self.__anim.x = x
        self.__anim.y = y
        self.clicked = False
        self.move_left -= 1


class Soldier_blue(Soldier):
    def __init__(self, x, y):
        super().__init__(x, y, 'blue', 'game2images/g2soldier_blue_new.png')


class Soldier_red(Soldier):
    def __init__(self, x, y):
        super().__init__(x, y, 'red', 'game2images/g2soldier_red_new.png')
