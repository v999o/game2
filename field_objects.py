from gameobject import GameObject

class Fieldsquare(GameObject):
    def __init__(self, x, y, color, image):
        super().__init__(x, y, 40, 40, image)
        self._color = color

    def type(self):
        return 'fieldsquare'

    def color(self):
        return self._color

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))

class Fieldsquare_neutral(Fieldsquare):
    def __init__(self, x, y):
        super().__init__(x, y, 'neutral', 'game2images/g2fieldsquare_v2.png')

class Fieldsquare_red(Fieldsquare):
    def __init__(self, x, y):
        super().__init__(x, y, 'red', 'game2images/g2fieldsquare_red.png')

class Fieldsquare_blue(Fieldsquare):
    def __init__(self, x, y):
        super().__init__(x, y, 'blue', 'game2images/g2fieldsquare_blue.png')

class Fieldsquare_choose(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, 'game2images/g2fieldsquare_choose_anim5.png')

    def color(self):
        return 'highlighted'

    def type(self):
        return 'choose_fieldsquare'

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))


class Fieldsquare_other(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, 'game2images/g2fieldsquare_anim_5.png')

    def color(self):
        return 'highlighted'

    def type(self):
        return 'fieldsquare_other'

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))


class TurnPointer(GameObject):
    def __init__(self, x, y, color):
        super().__init__(x, y, 40, 40, 'game2images/g2_' + color + '_turn_pointer.png')
        self.__color = color

    def color(self):
        return self.__color

    def type(self):
        return 'pointer'
