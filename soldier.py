from gameobject import GameObject


class Soldier(GameObject):
    def __init__(self, x, y, color, avatar):
        super().__init__(x, y, 40, 40, avatar)
        self._color = color
        self.move_left = 1

    def color(self):
        return self._color

    def type(self):
        return 'soldier'

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))

    def newturn(self):
        self.move_left = 1


class Soldier_blue(Soldier):
    def __init__(self, x, y):
        super().__init__(x, y, 'blue', 'game2images/g2soldier_blue_new.png')


class Soldier_blue_clicked(Soldier):
    def __init__(self, x, y):
        super().__init__(x, y, 'blue', 'game2images/g2soldier_blue_clickanim5.png')


class Soldier_red(Soldier):
    def __init__(self, x, y):
        super().__init__(x, y, 'red', 'game2images/g2soldier_red_new.png')


class Soldier_red_clicked(Soldier):
    def __init__(self, x, y):
        super().__init__(x, y, 'red', 'game2images/g2soldier_red_clickanim5.png')
