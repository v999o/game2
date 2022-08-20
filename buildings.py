from gameobject import GameObject


class Capital(GameObject):
    def __init__(self, x, y, color):
        super().__init__(x, y, 40, 40, 'game2images/g2capital_new_' + color + '.png')
        self.__clicked_image = self._load_image('game2images/g2capital_' + color + '_clickanim_5.png')
        self.__color = color
        self.clicked = False

    def type(self):
        return 'capital'

    def color(self):
        return self.__color

    def draw(self, surface):
        if self.clicked:
            surface.blit(self.__clicked_image, (self._rect.x, self._rect.y))
        else:
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
