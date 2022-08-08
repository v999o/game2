from gameobject import GameObject


class Bg_for_button(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 190, 70, 'game2images/g2_bg_for_buttons_2.png')

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))

    def type(self):
        pass


class Bg_for_buttons_capital(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 130, 70, 'game2images/g2_bg_for_buttons_capital.png')

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))

    def type(self):
        pass


class Move_button(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50, 'game2images/g2_movebutton_2.png')

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))

    def type(self):
        pass


class Move_button_clicked(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50, 'game2images/g2_movebutton_2_clicked.png')

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))

    def type(self):
        pass


class Attack_button(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50, 'game2images/g2_attackbutton_2.png')

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))

    def type(self):
        pass


class Attack_button_clicked(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50, 'game2images/g2_attackbutton_2_clicked.png')

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))

    def type(self):
        pass


class Capture_button(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50, 'game2images/g2_capturebutton_2.png')

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))

    def type(self):
        pass


class Capture_button_clicked(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50, 'game2images/g2_capturebutton_2_clicked.png')

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))

    def type(self):
        pass
