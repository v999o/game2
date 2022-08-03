from gameobject import GameObject


class Fieldsquare_neutral(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, 'game2images/g2fieldsquare_v2.png')

    def color(self):
        return 'neutral'

    def type(self):
        return 'fieldsquare'

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))


class Fieldsquare_red(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, 'game2images/g2fieldsquare_red.png')

    def color(self):
        return 'red'

    def type(self):
        return 'fieldsquare'

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))


class Fieldsquare_blue(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, 'game2images/g2fieldsquare_blue.png')

    def color(self):
        return 'blue'

    def type(self):
        return 'fieldsquare'

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))


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


class Blue_turn_pointer(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, 'game2images/g2_blue_turn_pointer.png')

    def color(self):
        return 'blue'

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))

    def type(self):
        return 'pointer'


class Red_turn_pointer(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, 'game2images/g2_red_turn_pointer.png')

    def color(self):
        return 'red'

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))

    def type(self):
        return 'pointer'
