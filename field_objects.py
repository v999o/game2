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

    def change_color(self, color):
        self._color = color

class FieldsquareUniversal(GameObject):
    def __init__(self, x, y, color):
        super().__init__(x, y, 40, 40, 'game2images/g2fieldsquare_v2.png')
        self._color = color
        self.__red_image = GameObject._load_image('game2images/g2fieldsquare_red.png')
        self.__blue_image = GameObject._load_image('game2images/g2fieldsquare_blue.png')


    def type(self):
        return 'fieldsquare'

    def color(self):
        return self._color

    def draw(self, surface):
        if self._color == 'neutral':
            surface.blit(self.image, (self._rect.x, self._rect.y))
        elif self._color == 'red':
            surface.blit(self.__red_image, (self._rect.x, self._rect.y))
        else:
            surface.blit(self.__blue_image, (self._rect.x, self._rect.y))

    def change_color(self, color):
        self._color = color


class Fieldsquare_choose(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, 'game2images/g2_choose_fieldsquare_v2.png')

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

class C_a(GameObject):
    def __init__(self, x, y, image):
        super().__init__(x, y, 40, 40, image)

    def color(self):
        return 'none'

    def type(self):
        return 'c_a'

class C_a_up(C_a):
    def __init__(self, x, y):
        super().__init__(x, y, 'game2images/g2_c_a_up_5.png')

class C_a_down(C_a):
    def __init__(self, x, y):
        super().__init__(x, y, 'game2images/g2_c_a_down_5.png')

class C_a_right(C_a):
    def __init__(self, x, y):
        super().__init__(x, y, 'game2images/g2_c_a_right_5.png')

class C_a_left(C_a):
    def __init__(self, x, y):
        super().__init__(x, y, 'game2images/g2_c_a_left_5.png')


class TurnPointer(GameObject):
    def __init__(self, x, y, color):
        super().__init__(x, y, 40, 40, 'game2images/g2_' + color + '_turn_pointer.png')
        self.__color = color

    def color(self):
        return self.__color

    def type(self):
        return 'pointer'
