from gameobject import GameObject


class Capital_blue(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, 'game2images/g2capital_new_blue.png')

    def type(self):
        return 'capital'

    def color(self):
        return 'blue'

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))


class Capital_blue_clicked(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, 'game2images/g2capital_blue_clickanim5.png')

    def type(self):
        return 'capital'

    def color(self):
        return 'blue'

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))


class Capital_red(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, 'game2images/g2capital_new_red.png')

    def type(self):
        return 'capital'

    def color(self):
        return 'red'

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))


class Capital_red_clicked(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, 'game2images/g2capital_red_clickanim_5.png')

    def type(self):
        return 'capital'

    def color(self):
        return 'red'

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))


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
