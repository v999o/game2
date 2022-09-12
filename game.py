from typing import List, Union

import pygame
from pygame.rect import Rect

import config
import config as c
import math
from text_object import TextObject
from animations import SoldierAnim
from animations import Choose_fieldsquare_anim
from animations import Fieldsquares_others_anim
from animations import C_a_up_anim, C_a_down_anim, C_a_right_anim, C_a_left_anim
from soldier import Soldier
from soldier import Soldier_blue
from soldier import Soldier_red
from buildings import Capital
from buildings import Factory_blue
from buildings import Factory_red
from bgforbuttons import Bg_for_button
from bgforbuttons import Bg_for_buttons_capital
from bgforbuttons import Move_button
from bgforbuttons import Move_button_clicked
from bgforbuttons import Attack_button
from bgforbuttons import Attack_button_clicked
from bgforbuttons import Capture_button
from bgforbuttons import Capture_button_clicked
from bgforbuttons import Win_label_blue, Win_label_red
from buttons_capital import Spawn_soldier_button
from buttons_capital import Spawn_soldier_button_clicked
from buttons_capital import Spawn_factory_button
from buttons_capital import Spawn_factory_button_clicked
from field_objects import FieldsquareUniversal
from field_objects import TurnPointer
from field_objects import Fieldsquare_choose
from field_objects import Fieldsquare_other
from field_objects import C_a_up, C_a_down, C_a_right, C_a_left
from collections import defaultdict
from gameobject import GameObject


class Game:
    objects: List[Union[GameObject]]

    def __init__(self, caption, width, height, back_image_filename, gamesquare_image_filename, fieldsquare_red_image_filename, fieldsquare_blue_image_filename, frame_rate):
        #self.background_image = pygame.image.load(back_image_filename)
        self.gamesquare_image = pygame.image.load(gamesquare_image_filename)
        self.fieldsquare_red_image = pygame.image.load(fieldsquare_red_image_filename)
        self.fieldsquare_blue_image = pygame.image.load(fieldsquare_blue_image_filename)
        self.frame_rate = frame_rate
        self.next_turn = False
        self.objects = []
        self.capital_squares = []
        self.colors = []
        self.anims = []
        self.pause = True
        self.counter = False
        self.remover = None
        self.soldier_buttons = False
        self.capital_buttons = False
        self.capital_actions = 'none'
        self.soldier_actions = 'none'
        self.s = 0

        self.is_move_button_clicked = False
        self.is_attack_button_clicked = False
        self.is_capture_button_clicked = False

        self.is_spawn_soldier_button_clicked = False
        self.is_spawn_factory_button_clicked = False

        self.is_building_intersection = False

        self.balance_blue = 10
        self.income_blue = 10
        self.balance_red = 10
        self.income_red = 10
        self.soldier_blue_cost = 4
        self.soldier_red_cost = 4
        self.factory_blue_cost = 6
        self.factory_red_cost = 6

        self.Undo = []

        for y in range(40, c.screen_height, 40):
            for x in range(0, c.screen_width, 40):
                if (x in [c.screen_width - 80, c.screen_width - 40]) and (y in [((c.screen_height-40)//2-60)+40, ((c.screen_height-40)//2-20)+40, ((c.screen_height-40)//2+20)+40]):
                    self.objects.append(FieldsquareUniversal(x, y, 'blue'))
                elif (x in [0, 1*40]) and (y in [((c.screen_height-40)//2-60)+40, ((c.screen_height-40)//2-20)+40, ((c.screen_height-40)//2+20)+40]):
                    self.objects.append(FieldsquareUniversal(x, y, 'red'))
                else:
                    self.objects.append(FieldsquareUniversal(x, y, 'neutral'))

        self.blue_turn_pointer = TurnPointer(c.screen_width//2, 10, 'blue')
        self.red_turn_pointer = TurnPointer(c.screen_width//2, 10, 'red')
        self.objects.append(self.blue_turn_pointer)

        self.capital_red = Capital(0, ((c.screen_height-40)//2-20)+40, 'red')
        self.objects.append(self.capital_red)
        self.capital_blue = Capital(c.screen_width-40, ((c.screen_height-40)//2-20)+40, 'blue')
        self.objects.append(self.capital_blue)

        self.bg_for_buttons = Bg_for_button(0, 440)
        self.bg_for_buttons_capital = Bg_for_buttons_capital(0, 0)
        self.move_button = Move_button(self.bg_for_buttons.x + 10, self.bg_for_buttons.y + 10)
        self.move_button_clicked = Move_button_clicked(self.move_button.x, self.move_button.y)
        self.attack_button = Attack_button(self.bg_for_buttons.x + 70, self.bg_for_buttons.y + 10)
        self.attack_button_clicked = Attack_button_clicked(self.attack_button.x, self.attack_button.y)
        self.capture_button = Capture_button(self.bg_for_buttons.x + 130, self.bg_for_buttons.y + 10)
        self.capture_button_clicked = Capture_button_clicked(self.capture_button.x, self.capture_button.y)
        self.spawn_soldier_button = Spawn_soldier_button(160, 480)
        self.spawn_soldier_button_clicked = Spawn_soldier_button_clicked(160, 480)
        self.spawn_factory_button = Spawn_factory_button(500, 480)
        self.spawn_factory_button_clicked = Spawn_factory_button_clicked(500, 480)



        self.soldier_blue_clicked = None
        self.soldier_red_clicked = None

        pygame.mixer.init(44100, -16, 2, 4096)
        pygame.init()
        pygame.font.init()

        self.create_labels()

        # self.surface = pygame.display.set_mode((width, height), FULLSCREEN)
        self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.mouse_handlers = []

    def create_labels(self):
        balance_label_blue = TextObject(c.balance_blue_offset,
                                        c.status_offset_y,
                                        lambda: f'$: {self.balance_blue}',
                                        c.text_color1,
                                        c.font_name,
                                        c.font_size)
        self.objects.append(balance_label_blue)
        income_label_blue = TextObject(c.income_blue_offset,
                                       c.status_offset_y,
                                       lambda: f'+: {self.income_blue}',
                                       c.text_color1,
                                       c.font_name,
                                       c.font_size)
        self.objects.append(income_label_blue)
        balance_label_red = TextObject(c.balance_red_offset,
                                       c.status_offset_y,
                                       lambda: f'$: {self.balance_red}',
                                       c.text_color2,
                                       c.font_name,
                                       c.font_size)
        self.objects.append(balance_label_red)
        income_label_red = TextObject(c.income_red_offset,
                                      c.status_offset_y,
                                      lambda: f'+: {self.income_red}',
                                      c.text_color2,
                                      c.font_name,
                                      c.font_size)
        self.objects.append(income_label_red)

    def create_win_label(self, color):
        if color == 'blue':
            self.win_label_blue = Win_label_blue(100, 100)
            self.objects.append(self.win_label_blue)
        else:
            self.win_label_red = Win_label_red(100, 100)
            self.objects.append(self.win_label_red)

    def create_soldier_click_anim(self, x, y, color):
        anim = SoldierAnim(x, y, color)
        self.anims.append(anim)
        self.objects.append(anim)

    def fieldsquare_choose_anim(self, x, y):
        anim = Choose_fieldsquare_anim(x, y)
        self.anims.append(anim)

    def fieldsquare_others_anim(self, x, y):
        anim = Fieldsquares_others_anim(x, y)
        self.anims.append(anim)

    def update(self):
        for o in self.objects:
            o.update()

    def is_capital_buttons_clicked(self, button):
        self.objects.remove(self.bg_for_buttons_capital)
        self.objects.remove(self.spawn_soldier_button)
        self.objects.remove(self.spawn_factory_button)
        self.objects.remove(self.soldier_cost_label)
        self.objects.remove(self.factory_cost_label)
        if button == 'is_spawn_soldier_button_clicked':
            self.objects.remove(self.spawn_soldier_button_clicked)
        if button == 'is_spawn_factory_button_clicked':
            self.objects.remove(self.spawn_factory_button_clicked)
        self.capital_buttons = False
        if button == 'is_spawn_soldier_button_clicked':
            self.capital_actions = 'spawn_soldier'
        if button == 'is_spawn_factory_button_clicked':
            self.capital_actions = 'spawn_factory'
        self.is_spawn_soldier_button_clicked = False
        self.is_spawn_factory_button_clicked = False

    def unclick_capital(self):
        self.capital_red.clicked = False
        self.capital_blue.clicked = False

    def escape_capital_1(self):
        self.objects.remove(self.bg_for_buttons_capital)
        self.objects.remove(self.spawn_soldier_button)
        self.objects.remove(self.spawn_factory_button)
        self.objects.remove(self.soldier_cost_label)
        self.objects.remove(self.factory_cost_label)
        self.unclick_capital()
        self.capital_buttons = False
        if self.is_spawn_soldier_button_clicked:
            self.objects.remove(self.spawn_soldier_button_clicked)
            self.is_spawn_soldier_button_clicked = False
        elif self.is_spawn_factory_button_clicked:
            self.objects.remove(self.spawn_factory_button_clicked)
            self.is_spawn_factory_button_clicked = False

    def escape_capital_2(self):
        self.unclick_capital()
        self.capital_actions = 'none'

    def escape_soldier_1(self):
        if self.soldier_blue_clicked is not None:
            self.soldier_blue_clicked.clicked = False
            self.soldier_blue_clicked = None
        if self.soldier_red_clicked is not None:
            self.soldier_red_clicked.clicked = False
            self.soldier_red_clicked = None
        self.objects.remove(self.bg_for_buttons)
        self.objects.remove(self.move_button)
        self.objects.remove(self.attack_button)
        self.objects.remove(self.capture_button)
        if self.is_move_button_clicked:
            self.objects.remove(self.move_button_clicked)
            self.is_move_button_clicked = False
        elif self.is_attack_button_clicked:
            self.objects.remove(self.attack_button_clicked)
            self.is_attack_button_clicked = False
        elif self.is_capture_button_clicked:
            self.objects.remove(self.capture_button_clicked)
            self.is_capture_button_clicked = False
        self.soldier_buttons = False
        self.counter = False

    def escape_soldier_2(self):
        if self.soldier_blue_clicked is not None:
            self.soldier_blue_clicked.clicked = False
            self.soldier_blue_clicked = None
        if self.soldier_red_clicked is not None:
            self.soldier_red_clicked.clicked = False
            self.soldier_red_clicked = None
        self.soldier_actions = 'none'
        self.counter = False

    def do_choose_animation(self):
        for anim1 in self.anims:
            if anim1.anim_type() == 'choose_fieldsquare':
                for anim2 in self.anims:
                    if anim2.x//40 == anim1.x//40+1 and anim2.y//40 == anim1.y//40 and anim2.anim_type() == 'fieldsquare_other':
                        self.anims.append(C_a_right_anim(anim1.x, anim1.y))
                    if anim2.x//40 == anim1.x//40-1 and anim2.y//40 == anim1.y//40 and anim2.anim_type() == 'fieldsquare_other':
                        self.anims.append(C_a_left_anim(anim1.x, anim1.y))
                    if anim2.x//40 == anim1.x//40 and anim2.y//40 == anim1.y//40+1 and anim2.anim_type() == 'fieldsquare_other':
                        self.anims.append(C_a_down_anim(anim1.x, anim1.y))
                    if anim2.x//40 == anim1.x//40 and anim2.y//40 == anim1.y//40-1 and anim2.anim_type() == 'fieldsquare_other':
                        self.anims.append(C_a_up_anim(anim1.x, anim1.y))


    def delete_fieldsquares(self):
        for obj in self.objects[::-1]:
            if obj.type() in ['fieldsquare_other', 'choose_fieldsquare', 'c_a']:
                self.objects.remove(obj)

    def spawn_soldier_conditions(self, color):
        for j in self.objects:
            if j.type() in ['factory', 'capital'] and j.color() == color:
                for i in self.objects:
                    if i.type() == 'fieldsquare':
                        '''if i.color() == color and ((
                                                            j.x // 40 + 1 == i.x // 40 and j.y // 40 == i.y // 40) or (
                                                            j.x // 40 - 1 == i.x // 40 and j.y // 40 == i.y // 40) or (
                                                            j.x // 40 == i.x // 40 and j.y // 40 + 1 == i.y // 40) or (
                                                            j.x // 40 == i.x // 40 and j.y // 40 - 1 == i.y // 40)):'''
                        if (math.fabs(j.x//40-i.x//40) in [0, 1] and math.fabs(j.y//40-i.y//40) in [0, 1]):

                            for obj in self.objects:
                                if obj.type() in ['capital', 'factory', 'soldier'] and obj.x == i.x and obj.y == i.y and obj.color() == color:
                                    self.is_building_intersection = True
                            if not self.is_building_intersection:
                                if self.s == 0:
                                    self.fieldsquare_choose_anim(i.x, i.y)
                                else:
                                    for k in self.anims[::-1]:
                                        if k.x == i.x and k.y == i.y and k.anim_type() == 'fieldsquare_other':
                                            self.anims.remove(k)
                                            self.fieldsquare_choose_anim(i.x, i.y)
                            self.is_building_intersection = False
                        else:
                            if self.s == 0:
                                for obj in self.objects:
                                    if obj.type() in ['capital', 'factory',
                                                      'soldier'] and obj.x == i.x and obj.y == i.y:
                                        self.is_building_intersection = True
                                if not self.is_building_intersection:
                                    self.fieldsquare_others_anim(i.x, i.y)
                                self.is_building_intersection = False
                    elif i.type() in ['capital', 'factory', 'soldier']:
                        if self.s == 0:
                            self.fieldsquare_others_anim(i.x, i.y)
                self.s += 1
        self.s = 0
        for anim1 in self.anims[::-1]:
            if anim1.anim_type() == 'fieldsquare_other':
                for anim2 in self.anims[::-1]:
                    if anim2.anim_type() == 'choose_fieldsquare' and anim1.x == anim2.x and anim1.y == anim2.y:
                        self.anims.remove(anim2)

    def spawn_factory_conditions(self, color):
        for j in self.objects:
            if j.type() in ['factory', 'capital'] and j.color() == color:
                for i in self.objects:
                    if i.type() == 'fieldsquare':
                        '''if i.color() == color and ((
                                                                                    j.x // 40 + 1 == i.x // 40 and j.y // 40 == i.y // 40) or (
                                                                                    j.x // 40 - 1 == i.x // 40 and j.y // 40 == i.y // 40) or (
                                                                                    j.x // 40 == i.x // 40 and j.y // 40 + 1 == i.y // 40) or (
                                                                                    j.x // 40 == i.x // 40 and j.y // 40 - 1 == i.y // 40)):'''
                        if i.color() == color and (math.fabs(j.x//40-i.x//40) in [0, 1] and math.fabs(j.y//40-i.y//40) in [0, 1]):
                            for obj in self.objects:
                                if obj.type() in ['capital', 'factory', 'soldier'] and obj.x == i.x and obj.y == i.y:
                                    self.is_building_intersection = True
                            if not self.is_building_intersection:
                                if self.s == 0:
                                    self.fieldsquare_choose_anim(i.x, i.y)
                                else:
                                    for k in self.anims[::-1]:
                                        if k.x == i.x and k.y == i.y and k.anim_type() == 'fieldsquare_other':
                                            self.anims.remove(k)
                                            self.fieldsquare_choose_anim(i.x, i.y)
                            self.is_building_intersection = False
                        else:
                            if self.s == 0:
                                for obj in self.objects:
                                    if obj.type() in ['capital', 'factory',
                                                      'soldier'] and obj.x == i.x and obj.y == i.y:
                                        self.is_building_intersection = True
                                if not self.is_building_intersection:
                                    self.fieldsquare_others_anim(i.x, i.y)
                                self.is_building_intersection = False
                    elif i.type() in ['capital', 'factory', 'soldier']:
                        if self.s == 0:
                            self.fieldsquare_others_anim(i.x, i.y)
                self.s += 1
        self.s = 0
        for anim1 in self.anims[::-1]:
            if anim1.anim_type() == 'fieldsquare_other':
                for anim2 in self.anims[::-1]:
                    if anim2.anim_type() == 'choose_fieldsquare' and anim1.x == anim2.x and anim1.y == anim2.y:
                        self.anims.remove(anim2)

    def move_soldier_conditions(self, soldier):
        for obj in self.objects:
            if obj.type() == 'fieldsquare':
                if soldier.color() == 'blue':
                    self.do_move_soldier_conditions(obj, self.soldier_blue_clicked)
                elif soldier.color() == 'red':
                    self.do_move_soldier_conditions(obj, self.soldier_red_clicked)
            elif obj.type() in ['capital', 'factory', 'soldier'] and not (obj.x == soldier.x and obj.y == soldier.y):
                self.fieldsquare_others_anim(obj.x, obj.y)
        for anim1 in self.anims[::-1]:
            if anim1.anim_type() == 'choose_fieldsquare':
                for anim2 in self.anims[::-1]:
                    if anim2.anim_type() == 'fieldsquare_other' and anim1.x == anim2.x and anim1.y == anim2.y:
                        self.anims.remove(anim2)

    def do_move_soldier_conditions(self, fieldsquare, soldier):
        if (fieldsquare.x // 40 == soldier.x // 40 + 1
            or fieldsquare.x // 40 == soldier.x // 40 - 1
            or fieldsquare.y // 40 == soldier.y // 40 + 1
            or fieldsquare.y // 40 == soldier.y // 40 - 1) and not (
                fieldsquare.x // 40 != soldier.x // 40 and fieldsquare.y // 40 != soldier.y // 40):
            for obj in self.objects:
                if obj.type() in ['capital', 'factory', 'soldier'] and obj.color() == soldier.color() and obj.x == fieldsquare.x and obj.y == fieldsquare.y:
                    self.is_building_intersection = True
            if not self.is_building_intersection:
                self.fieldsquare_choose_anim(fieldsquare.x, fieldsquare.y)
            self.is_building_intersection = False
        else:
            for obj in self.objects:
                if obj.type() in ['capital', 'factory', 'soldier'] and obj.x == fieldsquare.x and obj.y == fieldsquare.y:
                    self.is_building_intersection = True
            if not self.is_building_intersection:
                self.fieldsquare_others_anim(fieldsquare.x, fieldsquare.y)
            self.is_building_intersection = False

    def move_soldier(self, enemy_color, x, y):
        for i in self.objects:
            if i.type() == 'choose_fieldsquare' and x // 40 == i.x // 40 and y // 40 == i.y // 40:
                for j in self.objects:
                    if j.type() == 'fieldsquare' and j.x == i.x and j.y == i.y:
                        for k in self.objects:
                            if k.type() == 'factory' and k.color() == enemy_color and k.x == j.x and k.y == j.y:
                                self.is_building_intersection = True
                                self.objects.remove(k)
                                if enemy_color == 'red':
                                    self.income_red -= 6
                                    self.soldier_blue_clicked.attack(i.x, i.y)
                                else:
                                    self.income_blue -= 6
                                    self.soldier_red_clicked.attack(i.x, i.y)
                                self.soldier_actions = 'none'
                                self.counter = False
                                self.delete_fieldsquares()
                                break
                            if k.type() == 'soldier' and k.color() == enemy_color and k.x == j.x and k.y == j.y:
                                self.is_building_intersection = True
                                self.objects.remove(k)
                                if enemy_color == 'red':
                                    self.soldier_blue_clicked.attack(i.x, i.y)
                                else:
                                    self.soldier_red_clicked.attack(i.x, i.y)
                                self.soldier_actions = 'none'
                                self.counter = False
                                self.delete_fieldsquares()
                                break
                            if k.type() == 'capital' and k.color() == enemy_color and k.x == j.x and k.y == j.y:
                                self.is_building_intersection = True
                                self.objects.remove(k)
                                if enemy_color == 'red':
                                    self.soldier_blue_clicked.attack(i.x, i.y)
                                    self.create_win_label('blue')
                                else:
                                    self.soldier_red_clicked.attack(i.x, i.y)
                                    self.create_win_label('red')
                                self.soldier_actions = 'none'
                                self.counter = False
                                self.delete_fieldsquares()
                                break
                        if not self.is_building_intersection:
                            if enemy_color == 'red':
                                self.soldier_blue_clicked.move((x // 40) * 40, (y // 40) * 40)
                            else:
                                self.soldier_red_clicked.move((x // 40) * 40, (y // 40) * 40)
                            self.soldier_actions = 'none'
                            self.delete_fieldsquares()
                        else:
                            self.is_building_intersection = False
                        if j.color() == enemy_color:
                            if enemy_color == 'red':
                                j.change_color('blue')
                                self.income_red -= 1
                                self.income_blue += 1
                            else:
                                j.change_color('red')
                                self.income_blue -= 1
                                self.income_red += 1
                        elif j.color() == 'neutral':
                            if enemy_color == 'red':
                                j.change_color('blue')
                                self.income_blue += 1
                            else:
                                j.change_color('red')
                                self.income_red += 1

    def do_spawn_soldier(self, color, enemy_color, x, y):
        for j in self.objects:
            if j.type() == 'choose_fieldsquare' and j.collidepoint(x, y):
                self.unclick_capital()
                if color == 'blue':
                    soldier_blue = Soldier_blue((x // 40) * 40, (y // 40) * 40)
                    self.objects.append(soldier_blue)
                    self.balance_blue -= self.soldier_blue_cost
                    self.soldier_blue_cost += 1
                else:
                    soldier_red = Soldier_red((x//40)*40, (y//40)*40)
                    self.objects.append(soldier_red)
                    self.balance_red -= self.soldier_red_cost
                    self.soldier_red_cost += 1
                self.capital_actions = 'none'
                for k in self.objects:
                    if k.x == j.x and k.y == j.y:
                        if k.type() == 'soldier' and k.color() != color:
                            self.objects.remove(k)
                        if k.type() == 'fieldsquare' and k.color() != color:
                            k.change_color(color)
                            if color == 'blue':
                                soldier_blue.move_left -= 1
                                self.income_blue += 1
                            else:
                                soldier_red.move_left -= 1
                                self.income_red += 1

                            if k.color() == enemy_color:
                                if enemy_color == 'red':
                                    self.income_red -= 1
                                else:
                                    self.income_blue -= 1
                        if k.type() == 'factory' and k.color() == enemy_color:
                            self.objects.remove(k)
                            if color == 'blue':
                                self.income_red -= 6
                            else:
                                self.income_blue -= 6
                self.delete_fieldsquares()
                break

    def undo(self, Undo):
        print(Undo)
        if Undo[-1] == 'SpSo':
            self.objects.remove(Undo[-2])
            self.soldier_blue_cost -= 1
            self.balance_blue += self.soldier_blue_cost
            Undo.pop()
            Undo.pop()

    def handle_events(self):
        def create_capital_buttons(a, b, color):
            if c.screen_width-75 >= a >= 75:
                a = a - 75
            elif a > c.screen_width-75:
                a = c.screen_width-130
            elif a < 95:
                a = 0
            if (b//40+1)*40 <= c.screen_height-70:
                b = (b//40+1)*40
            elif b > c.screen_height-70:
                b = c.screen_height-70
            self.bg_for_buttons_capital = Bg_for_buttons_capital(a, b)
            self.objects.append(self.bg_for_buttons_capital)
            self.spawn_soldier_button = Spawn_soldier_button(self.bg_for_buttons_capital.x + 10,
                                                             self.bg_for_buttons_capital.y + 10)
            self.spawn_soldier_button_clicked = Spawn_soldier_button_clicked(self.spawn_soldier_button.x,
                                                                             self.spawn_soldier_button.y)
            self.objects.append(self.spawn_soldier_button)
            self.spawn_factory_button = Spawn_factory_button(self.bg_for_buttons_capital.x + 70,
                                                             self.bg_for_buttons_capital.y + 10)
            self.spawn_factory_button_clicked = Spawn_factory_button_clicked(self.spawn_factory_button.x,
                                                                             self.spawn_factory_button.y)
            self.objects.append(self.spawn_factory_button)
            self.capital_buttons = True

            if color == 'blue':
                self.soldier_cost_label = TextObject(self.bg_for_buttons_capital.x+20,
                                            self.bg_for_buttons_capital.y+60,
                                            lambda: f'$: {self.soldier_blue_cost}',
                                            c.text_color3,
                                            c.font_name,
                                            c.font_size)
                self.objects.append(self.soldier_cost_label)
                self.factory_cost_label = TextObject(self.bg_for_buttons_capital.x + 80,
                                                          self.bg_for_buttons_capital.y + 60,
                                                          lambda: f'$: {self.factory_blue_cost}',
                                                          c.text_color3,
                                                          c.font_name,
                                                          c.font_size)
                self.objects.append(self.factory_cost_label)
            else:
                self.soldier_cost_label = TextObject(self.bg_for_buttons_capital.x + 20,
                                                      self.bg_for_buttons_capital.y + 60,
                                                      lambda: f'$: {self.soldier_red_cost}',
                                                      c.text_color3,
                                                      c.font_name,
                                                      c.font_size)
                self.objects.append(self.soldier_cost_label)
                self.factory_cost_label = TextObject(self.bg_for_buttons_capital.x + 80,
                                                         self.bg_for_buttons_capital.y + 60,
                                                         lambda: f'$: {self.factory_red_cost}',
                                                         c.text_color3,
                                                         c.font_name,
                                                         c.font_size)
                self.objects.append(self.factory_cost_label)

        mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]

        if self.capital_buttons:
            if self.spawn_soldier_button_clicked.collidepoint(mouse_x, mouse_y) and not self.is_spawn_soldier_button_clicked:
                self.objects.append(self.spawn_soldier_button_clicked)
                self.is_spawn_soldier_button_clicked = True
            elif not self.spawn_soldier_button_clicked.collidepoint(mouse_x, mouse_y) and self.is_spawn_soldier_button_clicked:
                self.objects.remove(self.spawn_soldier_button_clicked)
                self.is_spawn_soldier_button_clicked = False
            if self.spawn_factory_button_clicked.collidepoint(mouse_x, mouse_y) and not self.is_spawn_factory_button_clicked:
                self.objects.append(self.spawn_factory_button_clicked)
                self.is_spawn_factory_button_clicked = True
            elif not self.spawn_factory_button_clicked.collidepoint(mouse_x, mouse_y) and self.is_spawn_factory_button_clicked:
                self.objects.remove(self.spawn_factory_button_clicked)
                self.is_spawn_factory_button_clicked = False

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.do_keydown_escape()
                elif event.key == pygame.K_BACKSPACE:
                    if len(self.Undo)>=2:
                        self.undo(self.Undo)
                else:
                    self.do_keydown_next_turn()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x = event.pos[0]
                mouse_y = event.pos[1]
                if not self.next_turn:
                    if self.capital_blue.collidepoint(mouse_x, mouse_y) and not self.capital_buttons and self.capital_actions == 'none' and self.soldier_actions == 'none' and not self.soldier_buttons:
                        self.capital_blue.clicked = True
                        create_capital_buttons(mouse_x, mouse_y, 'blue')
                    elif self.capital_buttons and self.spawn_soldier_button_clicked.collidepoint(mouse_x, mouse_y) and not self.soldier_buttons:
                        self.is_capital_buttons_clicked('is_spawn_soldier_button_clicked')
                        self.spawn_soldier_conditions('blue')
                        self.do_choose_animation()
                        for anim in self.anims:
                            self.objects.append(anim)
                    elif self.capital_buttons and self.spawn_factory_button_clicked.collidepoint(mouse_x, mouse_y) and not self.soldier_buttons:
                        self.is_capital_buttons_clicked('is_spawn_factory_button_clicked')
                        self.spawn_factory_conditions('blue')
                        for anim in self.anims:
                            self.objects.append(anim)

                    elif self.capital_actions == 'spawn_soldier' and self.balance_blue >= self.soldier_blue_cost:
                        self.do_spawn_soldier('blue', 'red', mouse_x, mouse_y)
                        '''self.Undo.append(soldier_blue)
                                self.Undo.append('SpSo')'''

                    elif self.capital_actions == 'spawn_factory' and self.balance_blue >= self.factory_blue_cost:
                        for i in self.objects:
                            if i.type() == 'choose_fieldsquare' and i.collidepoint(mouse_x, mouse_y):
                                self.unclick_capital()
                                factory_blue = Factory_blue((mouse_x // 40) * 40, (mouse_y // 40) * 40)
                                self.objects.append(factory_blue)
                                self.capital_actions = 'none'
                                self.balance_blue -= self.factory_blue_cost
                                self.income_blue += 6
                                self.factory_blue_cost += 2
                                self.delete_fieldsquares()
                                break

                    elif self.soldier_actions == 'move_soldier':
                        self.move_soldier('red', mouse_x, mouse_y)

                    elif not self.counter:
                        for i in self.objects:
                            if isinstance(i, Soldier):
                                if i.collidepoint(mouse_x, mouse_y) and i.color() == 'blue' and i.move_left == 1 and self.capital_actions == 'none' and not self.capital_buttons:
                                    self.remover = i
                                    self.counter = True
                        if self.counter and self.soldier_actions == 'none':
                            self.soldier_blue_clicked = self.remover
                            self.soldier_blue_clicked.clicked = True
                            self.move_soldier_conditions(self.soldier_blue_clicked)
                            self.soldier_actions = 'move_soldier'
                            self.counter = False
                            for anim in self.anims:
                                self.objects.append(anim)

                else:  # ход красных
                    if self.capital_red.collidepoint(mouse_x, mouse_y) and not self.capital_buttons and self.capital_actions == 'none' and self.soldier_actions == 'none' and not self.soldier_buttons:
                        self.capital_red.clicked = True
                        create_capital_buttons(mouse_x, mouse_y, 'red')
                    elif self.capital_buttons and self.spawn_soldier_button_clicked.collidepoint(mouse_x, mouse_y) and not self.soldier_buttons:
                        self.is_capital_buttons_clicked('is_spawn_soldier_button_clicked')
                        self.spawn_soldier_conditions('red')
                        for anim in self.anims:
                            self.objects.append(anim)
                    elif self.capital_buttons and self.spawn_factory_button_clicked.collidepoint(mouse_x, mouse_y) and not self.soldier_buttons:
                        self.is_capital_buttons_clicked('is_spawn_factory_button_clicked')
                        self.spawn_factory_conditions('red')
                        for anim in self.anims:
                            self.objects.append(anim)


                    elif self.capital_actions == 'spawn_soldier' and self.balance_red >= self.soldier_red_cost:
                        self.do_spawn_soldier('red', 'blue', mouse_x, mouse_y)

                    elif self.capital_actions == 'spawn_factory' and self.balance_red >= self.factory_red_cost:
                        for i in self.objects:
                            if i.type() == 'choose_fieldsquare' and i.collidepoint(mouse_x,
                                                                            mouse_y):
                                self.unclick_capital()
                                factory_red = Factory_red((mouse_x // 40) * 40, (mouse_y // 40) * 40)
                                self.objects.append(factory_red)
                                self.capital_actions = 'none'
                                self.balance_red -= self.factory_red_cost
                                self.income_red += 6
                                self.factory_red_cost += 2
                                self.delete_fieldsquares()
                                break

                    elif self.soldier_actions == 'move_soldier':
                        self.move_soldier('blue', mouse_x, mouse_y)

                    elif not self.counter:
                        for i in self.objects:
                            if isinstance(i, Soldier):
                                if i.collidepoint(mouse_x, mouse_y) and i.color() == 'red' and i.move_left == 1 and self.capital_actions == 'none' and not self.capital_buttons:
                                    self.remover = i
                                    self.counter = True
                        if self.counter:
                            self.soldier_red_clicked = self.remover
                            self.soldier_red_clicked.clicked = True
                            self.move_soldier_conditions(self.soldier_red_clicked)
                            self.soldier_actions = 'move_soldier'
                            self.counter = False
                            for anim in self.anims:
                                self.objects.append(anim)

        for anim in self.anims[::-1]:
            if anim.finished():
                if anim.anim_type() == 'fieldsquare_other':
                    fieldsquare_other = Fieldsquare_other(anim.x, anim.y)
                    self.objects.append(fieldsquare_other)
                elif anim.anim_type() == 'c_a_up':
                    c_a_up = C_a_up(anim.x, anim.y)
                    self.objects.append(c_a_up)
                elif anim.anim_type() == 'c_a_down':
                    c_a_down = C_a_down(anim.x, anim.y)
                    self.objects.append(c_a_down)
                elif anim.anim_type() == 'c_a_right':
                    c_a_right = C_a_right(anim.x, anim.y)
                    self.objects.append(c_a_right)
                elif anim.anim_type() == 'c_a_left':
                    c_a_left = C_a_left(anim.x, anim.y)
                    self.objects.append(c_a_left)
                '''elif anim.anim_type() == 'choose_fieldsquare':
                    fieldsquare_choose = Fieldsquare_choose(anim.x, anim.y)
                    self.objects.append(fieldsquare_choose)'''
                self.anims.remove(anim)
                self.objects.remove(anim)

    def do_keydown_next_turn(self):
        if not self.soldier_buttons and not self.capital_buttons and self.capital_actions == 'none' and self.soldier_actions == 'none':
            if not self.next_turn:  # переход хода к красным
                self.balance_blue += self.income_blue
                self.objects.remove(self.blue_turn_pointer)
                self.objects.append(self.red_turn_pointer)
            else:  # переход хода к синим
                for i in self.objects:
                    i.newturn()
                self.balance_red += self.income_red
                self.objects.append(self.blue_turn_pointer)
                self.objects.remove(self.red_turn_pointer)
            self.next_turn = not self.next_turn

    def do_keydown_escape(self):
        if not self.next_turn:
            self.__do_escape('blue')
        else:
            self.__do_escape('red')
        self.delete_fieldsquares()

    def __do_escape(self, color):
        if self.capital_buttons:
            self.escape_capital_1()
        if self.soldier_buttons:
            self.escape_soldier_1()
        if self.soldier_actions != 'none':
            self.escape_soldier_2()
        if self.capital_actions != 'none':
            self.escape_capital_2()

    def draw(self):
        pygame.draw.rect(self.surface, (200, 200, 200), Rect(0, 0, config.screen_width, config.screen_height))
        for o in self.objects:
            o.draw(self.surface)

    def run(self):
        while 1:

            self.handle_events()
            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(self.frame_rate)
