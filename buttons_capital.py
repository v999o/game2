from gameobject import GameObject


class Spawn_soldier_button(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50, 'game2images/g2_spawn_soldier_button_new.png')

    def type(self):
        return 'button'

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))


class Spawn_soldier_button_clicked(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50, 'game2images/g2_spawn_soldier_button_new_clicked.png')

    def type(self):
        return 'button'

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))


class Spawn_factory_button(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50, 'game2images/g2_spawn_factory_button_new.png')

    def type(self):
        return 'button'

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))


class Spawn_factory_button_clicked(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50, 'game2images/g2_spawn_factory_button_new_clicked.png')

    def type(self):
        return 'button'

    def draw(self, surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))
