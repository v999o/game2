from typing import List, Union

import pygame
import config as c
from text_object import TextObject
from animations import Soldier_blue_click_anim
from animations import Soldier_red_click_anim
from animations import Choose_fieldsquare_anim
from animations import Fieldsquares_others_anim
from animations import Capital_blue_click_anim
from animations import Capital_red_click_anim
from soldier import Soldier
from soldier import Soldier_blue
from soldier import Soldier_blue_clicked
from soldier import Soldier_red
from soldier import Soldier_red_clicked
from buildings import Capital_blue
from buildings import Capital_blue_clicked
from buildings import Capital_red
from buildings import Capital_red_clicked
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
from buttons_capital import Spawn_soldier_button
from buttons_capital import Spawn_soldier_button_clicked
from buttons_capital import Spawn_factory_button
from buttons_capital import Spawn_factory_button_clicked
from field_objects import Fieldsquare_red
from field_objects import Fieldsquare_blue
from field_objects import Fieldsquare_neutral
from field_objects import Blue_turn_pointer
from field_objects import Red_turn_pointer
from field_objects import Fieldsquare_choose
from field_objects import Fieldsquare_other
from collections import defaultdict
from gameobject import GameObject


class Game:
    objects: List[Union[GameObject]]

    def __init__(self, caption, width, height, back_image_filename, gamesquare_image_filename, fieldsquare_red_image_filename, fieldsquare_blue_image_filename, frame_rate):
        self.background_image = pygame.image.load(back_image_filename)
        self.gamesquare_image = pygame.image.load(gamesquare_image_filename)
        self.fieldsquare_red_image = pygame.image.load(fieldsquare_red_image_filename)
        self.fieldsquare_blue_image = pygame.image.load(fieldsquare_blue_image_filename)
        self.frame_rate = frame_rate
        self.next_turn = False
        self.objects = []
        self.capital_squares = []
        self.colors = []
        self.anims = []
        self.is_square_repeating = False
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

        self.is_first_pointer = True

        self.balance_blue = 10
        self.income_blue = 10
        self.balance_red = 10
        self.income_red = 10

        for y in range(0, 599, 40):
            for x in range(0, 799, 40):
                if (x in [18*40, 19*40]) and (y in [6*40, 7*40, 8*40]):
                    self.fieldsquare_blue = Fieldsquare_blue(x, y)
                    self.objects.append(self.fieldsquare_blue)
                elif (x in [0, 1*40]) and (y in [6*40, 7*40, 8*40]):
                    self.fieldsquare_red = Fieldsquare_red(x, y)
                    self.objects.append(self.fieldsquare_red)
                else:
                    self.fieldsquare_neutral = Fieldsquare_neutral(x, y)
                    self.objects.append(self.fieldsquare_neutral)

        self.blue_turn_pointer = Blue_turn_pointer(400, 10)
        self.red_turn_pointer = Red_turn_pointer(400, 10)
        self.objects.append(self.blue_turn_pointer)

        self.capital_red = Capital_red(0, 280)
        self.objects.append(self.capital_red)
        self.capital_blue = Capital_blue(760, 280)
        self.objects.append(self.capital_blue)
        self.capital_clicked = Capital_blue_clicked(0, 280)

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

    def create_soldier_click_anim(self, x, y, color):
        if color == 'blue':
            anim = Soldier_blue_click_anim(x, y)
        elif color == 'red':
            anim = Soldier_red_click_anim(x, y)
        else:
            return
        self.anims.append(anim)
        self.objects.append(anim)

    def fieldsquare_choose_anim(self, x, y):
        anim = Choose_fieldsquare_anim(x, y)
        self.anims.append(anim)

    def fieldsquare_others_anim(self, x, y):
        anim = Fieldsquares_others_anim(x, y)
        self.anims.append(anim)

    def create_capital_click_anim(self, x, y, color):
        if color == 'blue':
            anim = Capital_blue_click_anim(x, y)
        elif color == 'red':
            anim = Capital_red_click_anim(x, y)
        else:
            return
        self.anims.append(anim)
        self.objects.append(anim)

    def update(self):
        for o in self.objects:
            o.update()

    def is_soldier_buttons_clicked(self, button):
        self.objects.remove(self.bg_for_buttons)
        self.objects.remove(self.move_button)
        self.objects.remove(self.attack_button)
        self.objects.remove(self.capture_button)
        if button == 'is_move_button_clicked':
            self.objects.remove(self.move_button_clicked)
        if button == 'is_attack_button_clicked':
            self.objects.remove(self.attack_button_clicked)
        if button == 'is_capture_button_clicked':
            self.objects.remove(self.capture_button_clicked)
        self.soldier_buttons = False
        self.counter = False
        self.is_move_button_clicked = False
        self.is_attack_button_clicked = False
        self.is_capture_button_clicked = False
        if button == 'is_move_button_clicked':
            self.soldier_actions = 'move_soldier'
        if button == 'is_attack_button_clicked':
            self.soldier_actions = 'attack_soldier'
        if button == 'is_capture_button_clicked':
            self.soldier_actions = 'capture_soldier'

    def is_capital_buttons_clicked(self, button):
        self.objects.remove(self.bg_for_buttons_capital)
        self.objects.remove(self.spawn_soldier_button)
        self.objects.remove(self.spawn_factory_button)
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

    def escape_capital_1(self):
        self.objects.remove(self.bg_for_buttons_capital)
        self.objects.remove(self.spawn_soldier_button)
        self.objects.remove(self.spawn_factory_button)
        self.objects.remove(self.capital_clicked)
        self.capital_buttons = False
        if self.is_spawn_soldier_button_clicked:
            self.objects.remove(self.spawn_soldier_button_clicked)
            self.is_spawn_soldier_button_clicked = False
        elif self.is_spawn_factory_button_clicked:
            self.objects.remove(self.spawn_factory_button_clicked)
            self.is_spawn_factory_button_clicked = False

    def escape_capital_2(self):
        self.objects.remove(self.capital_clicked)
        self.capital_actions = 'none'

    def escape_soldier_1(self, color):
        if color == 'blue':
            soldier_blue = Soldier_blue(self.soldier_blue_clicked.x, self.soldier_blue_clicked.y)
            self.objects.append(soldier_blue)
            self.objects.remove(self.soldier_blue_clicked)
        elif color == 'red':
            soldier_red = Soldier_red(self.soldier_red_clicked.x, self.soldier_red_clicked.y)
            self.objects.append(soldier_red)
            self.objects.remove(self.soldier_red_clicked)
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

    def escape_soldier_2(self, color):
        if color == 'blue':
            soldier_blue = Soldier_blue(self.soldier_blue_clicked.x, self.soldier_blue_clicked.y)
            self.objects.append(soldier_blue)
            self.objects.remove(self.soldier_blue_clicked)
        elif color == 'red':
            soldier_red = Soldier_red(self.soldier_red_clicked.x, self.soldier_red_clicked.y)
            self.objects.append(soldier_red)
            self.objects.remove(self.soldier_red_clicked)
        self.soldier_actions = 'none'
        self.counter = False

    def delete_fieldsquares(self):
        for obj in self.objects[::-1]:
            if obj.type() == 'choose_fieldsquare' or obj.type() == 'fieldsquare_other':
                self.objects.remove(obj)

    def move_soldier_conditions(self, color):
        for obj in self.objects:
            if obj.type() == 'fieldsquare':
                if color == 'blue':
                    self.do_move_soldier_conditions(obj, self.soldier_blue_clicked)
                elif color == 'red':
                    self.do_move_soldier_conditions(obj, self.soldier_red_clicked)
            elif obj.type() in ['capital', 'factory', 'soldier']:
                self.fieldsquare_others_anim(obj.x, obj.y)

    def do_move_soldier_conditions(self, fieldsquare, soldier):
        if (fieldsquare.x // 40 == soldier.x // 40 + 1
            or fieldsquare.x // 40 == soldier.x // 40 - 1
            or fieldsquare.y // 40 == soldier.y // 40 + 1
            or fieldsquare.y // 40 == soldier.y // 40 - 1) and not (
                fieldsquare.x // 40 != soldier.x // 40 and fieldsquare.y // 40 != soldier.y // 40):
            for obj in self.objects:
                if obj.type() in ['capital', 'factory', 'soldier'] and obj.x == fieldsquare.x and obj.y == fieldsquare.y:
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

    def attack_soldier_conditions(self, color):
        for i in self.objects:
            if i.type() == 'fieldsquare':
                if color == 'blue':
                    self.do_attack_soldier_conditions(i, self.soldier_blue_clicked, 'red')
                elif color == 'red':
                    self.do_attack_soldier_conditions(i, self.soldier_red_clicked, 'blue')
            elif i.type() not in ['textobject', 'pointer']:
                self.fieldsquare_others_anim(i.x, i.y)
        for anim1 in self.anims[::-1]:
            if anim1.anim_type() == 'choose_fieldsquare':
                for anim2 in self.anims[::-1]:
                    if anim2.anim_type() == 'fieldsquare_other' and anim1.x == anim2.x and anim1.y == anim2.y:
                        self.anims.remove(anim2)

    def do_attack_soldier_conditions(self, i, soldier, enemy_color):
        if (
                i.x // 40 == soldier.x // 40 + 1
                or i.x // 40 == soldier.x // 40 - 1
                or i.y // 40 == soldier.y // 40 + 1
                or i.y // 40 == soldier.y // 40 - 1) and not (
                i.x // 40 != soldier.x // 40 and i.y // 40 != soldier.y // 40):
            for obj in self.objects:
                if obj.type() in ['capital', 'factory',
                                  'soldier'] and obj.x == i.x and obj.y == i.y:
                    self.is_building_intersection = True
                    if obj.color() == enemy_color:
                        self.fieldsquare_choose_anim(i.x, i.y)
                        break
            if not self.is_building_intersection:
                self.fieldsquare_others_anim(i.x, i.y)
            self.is_building_intersection = False
        else:
            for obj in self.objects:
                if obj.type() in ['capital', 'factory',
                                  'soldier'] and obj.x == i.x and obj.y == i.y:
                    self.is_building_intersection = True
            if not self.is_building_intersection:
                self.fieldsquare_others_anim(i.x, i.y)
            self.is_building_intersection = False

    def capture_soldier_conditions(self, color):
        for i in self.objects:
            if i.type() == 'fieldsquare':
                if color == 'blue':
                    self.do_capture_soldier_conditions(i, self.soldier_blue_clicked, 'blue')
                elif color == 'red':
                    self.do_capture_soldier_conditions(i, self.soldier_red_clicked, 'red')
            elif i.type() in ['soldier', 'factory', 'capital']:
                self.fieldsquare_others_anim(i.x, i.y)
        for anim1 in self.anims[::-1]:
            if anim1.anim_type() == 'choose_fieldsquare':
                for anim2 in self.anims[::-1]:
                    if anim2.anim_type() == 'fieldsquare_other' and anim1.x == anim2.x and anim1.y == anim2.y:
                        self.anims.remove(anim1)

    def do_capture_soldier_conditions(self, i, soldier, color):
        if (i.x // 40 == soldier.x // 40 + 1
                or i.x // 40 == soldier.x // 40 - 1
                or i.y // 40 == soldier.y // 40 + 1
                or i.y // 40 == soldier.y // 40 - 1) and not (
                i.x // 40 != soldier.x // 40 and i.y // 40 != soldier.y // 40) and i.color() != color:
            for obj in self.objects:
                if obj.type() in ['capital', 'factory',
                                  'soldier'] and obj.x == i.x and obj.y == i.y:
                    self.is_building_intersection = True
            if not self.is_building_intersection:
                self.fieldsquare_choose_anim(i.x, i.y)
            self.is_building_intersection = False
        else:
            for obj in self.objects:
                if obj.type() in ['capital', 'factory',
                                  'soldier'] and obj.x == i.x and obj.y == i.y:
                    self.is_building_intersection = True
            if not self.is_building_intersection:
                self.fieldsquare_others_anim(i.x, i.y)
            self.is_building_intersection = False

    def handle_events(self):
        def create_soldier_buttons(a, b):
            if 705 >= a >= 95:
                a = a - 95
            elif a > 705:
                a = 610
            elif a < 95:
                a = 0
            if b <= 530:
                b = b
            elif b > 530:
                b = 530
            self.bg_for_buttons = Bg_for_button(a, b)
            self.objects.append(self.bg_for_buttons)
            self.attack_button = Attack_button(self.bg_for_buttons.x + 10, self.bg_for_buttons.y + 10)
            self.attack_button_clicked = Attack_button_clicked(self.attack_button.x, self.attack_button.y)
            self.objects.append(self.attack_button)
            self.move_button = Move_button(self.bg_for_buttons.x + 70, self.bg_for_buttons.y + 10)
            self.move_button_clicked = Move_button_clicked(self.move_button.x, self.move_button.y)
            self.objects.append(self.move_button)
            self.capture_button = Capture_button(self.bg_for_buttons.x + 130, self.bg_for_buttons.y + 10)
            self.capture_button_clicked = Capture_button_clicked(self.capture_button.x,
                                                                 self.capture_button.y)
            self.objects.append(self.capture_button)

        def create_capital_buttons(a, b):
            if 725 >= a >= 75:
                a = a - 75
            elif a > 725:
                a = 670
            elif a < 95:
                a = 0
            if b <= 530:
                b = b
            elif b > 530:
                b = 530
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

        def capital_click(color):
            self.capital_buttons = True
            if color == 'blue':
                self.capital_clicked = Capital_blue_clicked(760, 280)
            elif color == 'red':
                self.capital_clicked = Capital_red_clicked(0, 280)
            else:
                return 
            self.objects.append(self.capital_clicked)
            self.create_capital_click_anim(self.capital_clicked.x, self.capital_clicked.y, color)

        mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]
        if self.soldier_buttons:
            if self.move_button_clicked.collidepoint(mouse_x, mouse_y) and not self.is_move_button_clicked:
                # if pygame.mouse.get_pos()[0] > 80 and pygame.mouse.get_pos()[0] < 160 and pygame.mouse.get_pos()[1] > 480 and pygame.mouse.get_pos()[1] < 560 and not self.buttons_clicked:
                # self.move_button_clicked = Move_button_clicked(80, 480)
                self.objects.append(self.move_button_clicked)
                self.is_move_button_clicked = True
            elif not self.move_button_clicked.collidepoint(mouse_x, mouse_y) and self.is_move_button_clicked:
                # elif (pygame.mouse.get_pos()[0] < 80 or pygame.mouse.get_pos()[0] > 160 or pygame.mouse.get_pos()[1] < 480 or pygame.mouse.get_pos()[1] > 560) and self.buttons_clicked:
                self.objects.remove(self.move_button_clicked)
                self.is_move_button_clicked = False
            if self.attack_button.collidepoint(mouse_x, mouse_y) and not self.is_attack_button_clicked:
                self.objects.append(self.attack_button_clicked)
                self.is_attack_button_clicked = True
            elif not self.attack_button_clicked.collidepoint(mouse_x, mouse_y) and self.is_attack_button_clicked:
                self.objects.remove(self.attack_button_clicked)
                self.is_attack_button_clicked = False
            if self.capture_button_clicked.collidepoint(mouse_x, mouse_y) and not self.is_capture_button_clicked:
                self.objects.append(self.capture_button_clicked)
                self.is_capture_button_clicked = True
            elif not self.capture_button_clicked.collidepoint(mouse_x, mouse_y) and self.is_capture_button_clicked:
                self.objects.remove(self.capture_button_clicked)
                self.is_capture_button_clicked = False

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
                else:
                    self.do_keydown_next_turn()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x = event.pos[0]
                mouse_y = event.pos[1]
                if not self.next_turn:
                    if self.capital_blue.collidepoint(mouse_x, mouse_y) and not self.capital_buttons and self.capital_actions == 'none' and self.soldier_actions == 'none' and not self.soldier_buttons:
                        capital_click('blue')
                        create_capital_buttons(mouse_x, mouse_y)
                    elif self.capital_buttons and self.spawn_soldier_button_clicked.collidepoint(mouse_x, mouse_y) and not self.soldier_buttons:
                        self.is_capital_buttons_clicked('is_spawn_soldier_button_clicked')
                        for j in self.objects:
                            if j.type() in ['factory', 'capital'] and j.color() == 'blue':
                                for i in self.objects:
                                    if i.type() == 'fieldsquare':
                                        if i.color() == 'blue' and ((
                                                                            j.x // 40 + 1 == i.x // 40 and j.y // 40 == i.y // 40) or (
                                                                            j.x // 40 - 1 == i.x // 40 and j.y // 40 == i.y // 40) or (
                                                                            j.x // 40 == i.x // 40 and j.y // 40 + 1 == i.y // 40) or (
                                                                            j.x // 40 == i.x // 40 and j.y // 40 - 1 == i.y // 40)):
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
                                                    if obj.type() in ['capital', 'factory', 'soldier'] and obj.x == i.x and obj.y == i.y:
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
                        for anim in self.anims:
                            self.objects.append(anim)
                    elif self.capital_buttons and self.spawn_factory_button_clicked.collidepoint(mouse_x, mouse_y) and not self.soldier_buttons:
                        self.is_capital_buttons_clicked('is_spawn_factory_button_clicked')
                        for j in self.objects:
                            if j.type() in ['factory', 'capital'] and j.color() == 'blue':
                                for i in self.objects:
                                    if i.type() == 'fieldsquare':
                                        if i.color() == 'blue' and ((
                                                                            j.x // 40 + 1 == i.x // 40 and j.y // 40 == i.y // 40) or (
                                                                            j.x // 40 - 1 == i.x // 40 and j.y // 40 == i.y // 40) or (
                                                                            j.x // 40 == i.x // 40 and j.y // 40 + 1 == i.y // 40) or (
                                                                            j.x // 40 == i.x // 40 and j.y // 40 - 1 == i.y // 40)):
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
                                                    if  obj.type() in ['capital', 'factory', 'soldier'] and obj.x == i.x and obj.y == i.y:
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
                        for anim in self.anims:
                            self.objects.append(anim)

                    elif self.capital_actions == 'spawn_soldier' and self.balance_blue >= 10:
                        for j in self.objects:
                            if j.type() == 'choose_fieldsquare' and j.collidepoint(mouse_x, mouse_y):
                                self.objects.remove(self.capital_clicked)
                                soldier_blue = Soldier_blue((mouse_x // 40) * 40, (mouse_y // 40) * 40)
                                self.objects.append(soldier_blue)
                                self.capital_actions = 'none'
                                self.balance_blue -= 10
                                break
                        self.delete_fieldsquares()
                    elif self.capital_actions == 'spawn_factory' and self.balance_blue >= 12:
                        for i in self.objects:
                            if i.type() == 'choose_fieldsquare' and i.collidepoint(mouse_x, mouse_y):
                                self.objects.remove(self.capital_clicked)
                                factory_blue = Factory_blue((mouse_x // 40) * 40, (mouse_y // 40) * 40)
                                self.objects.append(factory_blue)
                                self.capital_actions = 'none'
                                self.balance_blue -= 12
                                self.income_blue += 6
                        self.delete_fieldsquares()

                    elif self.is_move_button_clicked:
                        self.is_soldier_buttons_clicked('is_move_button_clicked')
                        self.move_soldier_conditions('blue')
                        for anim in self.anims:
                            self.objects.append(anim)

                    elif self.is_attack_button_clicked:
                        self.is_soldier_buttons_clicked('is_attack_button_clicked')
                        self.attack_soldier_conditions('blue')
                        for anim in self.anims:
                            self.objects.append(anim)

                    elif self.is_capture_button_clicked:
                        self.is_soldier_buttons_clicked('is_capture_button_clicked')
                        self.capture_soldier_conditions('blue')
                        for anim in self.anims:
                            self.objects.append(anim)

                    elif self.soldier_actions == 'move_soldier':
                        for i in self.objects:
                            if i.type() == 'choose_fieldsquare' and mouse_x // 40 == i.x // 40 and mouse_y // 40 == i.y // 40:
                                soldier_blue = Soldier_blue((mouse_x // 40) * 40, (mouse_y // 40) * 40)
                                soldier_blue.move_left -= 1
                                self.objects.append(soldier_blue)
                                self.objects.remove(self.soldier_blue_clicked)
                                self.soldier_actions = 'none'
                                self.delete_fieldsquares()

                    elif self.soldier_actions == 'attack_soldier':
                        for i in self.objects:
                            if i.type() == 'choose_fieldsquare' and mouse_x // 40 == i.x // 40 and mouse_y // 40 == i.y // 40:
                                for j in self.objects:
                                    if j.type() == 'factory' and j.color() == 'red' and i.x == j.x and i.y == j.y:
                                        self.objects.remove(j)
                                        self.income_red -= 6
                                        soldier_blue = Soldier_blue(self.soldier_blue_clicked.x,
                                                                    self.soldier_blue_clicked.y)
                                        soldier_blue.move_left -= 1
                                        self.objects.append(soldier_blue)
                                        self.objects.remove(self.soldier_blue_clicked)
                                        self.soldier_actions = 'none'
                                        self.counter = False
                                        self.delete_fieldsquares()
                                        break
                                    if j.type() == 'soldier' and j.color() == 'red' and i.x == j.x and i.y == j.y:
                                        self.objects.remove(j)
                                        soldier_blue = Soldier_blue(self.soldier_blue_clicked.x,
                                                                    self.soldier_blue_clicked.y)
                                        soldier_blue.move_left -= 1
                                        self.objects.append(soldier_blue)
                                        self.objects.remove(self.soldier_blue_clicked)
                                        self.soldier_actions = 'none'
                                        self.counter = False
                                        self.delete_fieldsquares()
                                        break

                    elif self.soldier_actions == 'capture_soldier':
                        for i in self.objects:
                            if i.type() == 'choose_fieldsquare' and mouse_x // 40 == i.x // 40 and mouse_y // 40 == i.y // 40:
                                for j in self.objects[::-1]:
                                    if j.type() == 'fieldsquare' and j.color() == 'red' and i.x == j.x and i.y == j.y:
                                        self.income_red -= 1
                                        self.fieldsquare_blue = Fieldsquare_blue(j.x, j.y)
                                        self.objects.append(self.fieldsquare_blue)
                                        self.objects.remove(j)
                                        self.income_blue += 1
                                        break
                                    elif j.type() == 'fieldsquare' and j.color() == 'neutral' and i.x == j.x and i.y == j.y:
                                        self.fieldsquare_blue = Fieldsquare_blue(j.x, j.y)
                                        self.objects.append(self.fieldsquare_blue)
                                        self.objects.remove(j)
                                        self.income_blue += 1
                                        break
                        soldier_blue = Soldier_blue(self.soldier_blue_clicked.x,
                                                    self.soldier_blue_clicked.y)
                        soldier_blue.move_left -= 1
                        self.objects.append(soldier_blue)
                        self.objects.remove(self.soldier_blue_clicked)
                        self.soldier_actions = 'none'
                        self.counter = False
                        self.delete_fieldsquares()

                    elif not self.counter:
                        for i in self.objects:
                            if isinstance(i, Soldier):
                                if i.collidepoint(mouse_x, mouse_y) and i.color() == 'blue' and i.move_left == 1 and self.capital_actions == 'none' and not self.capital_buttons:
                                    self.remover = i
                                    self.counter = True
                        if self.counter and self.soldier_actions == 'none':
                            self.soldier_blue_clicked = Soldier_blue_clicked((mouse_x // 40) * 40,
                                                                             (mouse_y // 40) * 40)
                            self.objects.append(self.soldier_blue_clicked)
                            self.create_soldier_click_anim((mouse_x // 40) * 40, (mouse_y // 40) * 40, 'blue')
                            self.objects.remove(self.remover)
                            create_soldier_buttons(mouse_x, mouse_y)
                            self.soldier_buttons = True

                else:  # ход красных
                    if self.capital_red.collidepoint(mouse_x, mouse_y) and not self.capital_buttons and self.capital_actions == 'none' and self.soldier_actions == 'none' and not self.soldier_buttons:
                        capital_click('red')
                        create_capital_buttons(mouse_x, mouse_y)
                    elif self.capital_buttons and self.spawn_soldier_button_clicked.collidepoint(mouse_x, mouse_y) and not self.soldier_buttons:
                        self.is_capital_buttons_clicked('is_spawn_soldier_button_clicked')
                    elif self.capital_buttons and self.spawn_factory_button_clicked.collidepoint(mouse_x, mouse_y) and not self.soldier_buttons:
                        self.is_capital_buttons_clicked('is_spawn_factory_button_clicked')

                    elif self.capital_actions == 'spawn_soldier' and self.balance_red >= 10:
                        for j in self.objects:
                            if j.type() == 'fieldsquare' and j.collidepoint(mouse_x,
                                                                            mouse_y) and j.color() == 'red':
                                for i in self.objects:
                                    if (i.type() == 'factory' or i.type() == 'capital') and i.color() == 'red' and ((
                                                                                                                            j.x // 40 + 1 == i.x // 40 and j.y // 40 == i.y // 40) or (
                                                                                                                            j.x // 40 - 1 == i.x // 40 and j.y // 40 == i.y // 40) or (
                                                                                                                            j.x // 40 == i.x // 40 and j.y // 40 + 1 == i.y // 40) or (
                                                                                                                            j.x // 40 == i.x // 40 and j.y // 40 - 1 == i.y // 40)):
                                        soldier_red = Soldier_red((mouse_x // 40) * 40,
                                                                  (mouse_y // 40) * 40)
                                        self.objects.append(soldier_red)
                                        self.capital_actions = 'none'
                                        self.balance_red -= 10
                                        self.objects.remove(self.capital_clicked)
                                        break

                    elif self.capital_actions == 'spawn_factory' and self.balance_red >= 12:
                        for i in self.objects:
                            if i.type() == 'fieldsquare' and i.collidepoint(mouse_x,
                                                                            mouse_y) and i.color() == 'red':
                                self.objects.remove(self.capital_clicked)
                                factory_red = Factory_red((mouse_x // 40) * 40, (mouse_y // 40) * 40)
                                self.objects.append(factory_red)
                                self.capital_actions = 'none'
                                self.balance_red -= 12
                                self.income_red += 6

                    elif self.is_move_button_clicked:
                        self.is_soldier_buttons_clicked('is_move_button_clicked')
                        self.move_soldier_conditions('red')
                        for anim in self.anims:
                            self.objects.append(anim)
                    elif self.is_attack_button_clicked:
                        self.is_soldier_buttons_clicked('is_attack_button_clicked')
                        self.attack_soldier_conditions('red')
                        for anim in self.anims:
                            self.objects.append(anim)
                    elif self.is_capture_button_clicked:
                        self.is_soldier_buttons_clicked('is_capture_button_clicked')
                        self.capture_soldier_conditions('red')
                        for anim in self.anims:
                            self.objects.append(anim)
                    elif self.soldier_actions == 'move_soldier':
                        if (mouse_x // 40 == self.soldier_red_clicked.x // 40 + 1
                            or mouse_x // 40 == self.soldier_red_clicked.x // 40 - 1
                            or mouse_y // 40 == self.soldier_red_clicked.y // 40 + 1
                            or mouse_y // 40 == self.soldier_red_clicked.y // 40 - 1) and not (
                                mouse_x // 40 != self.soldier_red_clicked.x // 40 and mouse_y // 40 != self.soldier_red_clicked.y // 40):

                            for i in self.objects:
                                if i.type() == 'fieldsquare' and i.collidepoint(mouse_x, mouse_y):
                                    soldier_red = Soldier_red((mouse_x // 40) * 40, (mouse_y // 40) * 40)
                                    soldier_red.move_left -= 1
                                    self.objects.append(soldier_red)
                                    self.objects.remove(self.soldier_red_clicked)
                                    self.soldier_actions = 'none'

                    elif self.soldier_actions == 'attack_soldier':
                        if not (mouse_x // 40 > self.soldier_red_clicked.x // 40 + 1
                                or mouse_x // 40 < self.soldier_red_clicked.x // 40 - 1
                                or mouse_y // 40 > self.soldier_red_clicked.y // 40 + 1
                                or mouse_y // 40 < self.soldier_red_clicked.y // 40 - 1) and not (
                                mouse_x // 40 != self.soldier_red_clicked.x // 40 and mouse_y // 40 != self.soldier_red_clicked.y // 40):
                            for i in self.objects:
                                if i.type() == 'factory' and i.color() == 'blue' and i.collidepoint(mouse_x, mouse_y):
                                    self.objects.remove(i)
                                    self.income_blue -= 6
                                    soldier_red = Soldier_red(self.soldier_red_clicked.x,
                                                              self.soldier_red_clicked.y)
                                    soldier_red.move_left -= 1
                                    self.objects.append(soldier_red)
                                    self.objects.remove(self.soldier_red_clicked)
                                    self.soldier_actions = 'none'
                                    self.counter = False
                                if i.type() == 'soldier' and i.color() == 'red' and i.collidepoint(mouse_x,
                                                                                                   mouse_y):
                                    self.objects.remove(i)
                                    soldier_red = Soldier_red(self.soldier_red_clicked.x,
                                                              self.soldier_red_clicked.y)
                                    soldier_red.move_left -= 1
                                    self.objects.append(soldier_red)
                                    self.objects.remove(self.soldier_red_clicked)
                                    self.soldier_actions = 'none'
                                    self.counter = False
                    elif self.soldier_actions == 'capture_soldier':
                        if not (mouse_x // 40 > self.soldier_red_clicked.x // 40 + 1
                                or mouse_x // 40 < self.soldier_red_clicked.x // 40 - 1
                                or mouse_y // 40 > self.soldier_red_clicked.y // 40 + 1
                                or mouse_y // 40 < self.soldier_red_clicked.y // 40 - 1) and not (
                                mouse_x // 40 != self.soldier_red_clicked.x // 40 and mouse_y // 40 != self.soldier_red_clicked.y // 40):
                            for i in self.objects:
                                if i.type() != 'textobject' and i.color() != 'red' and i.collidepoint(mouse_x,
                                                                                                      mouse_y):
                                    if i == 'fieldsquare' and i.color() == 'blue':
                                        self.income_red -= 1
                                        break
                                    self.fieldsquare_red = Fieldsquare_red(mouse_x // 40 * 40,
                                                                           mouse_y // 40 * 40)
                                    self.objects.append(self.fieldsquare_red)
                                    for o2 in self.objects:
                                        if o2.type() == 'fieldsquare' and o2.color() == 'neutral' and o2.x // 40 == \
                                                mouse_x // 40 and o2.y // 40 == mouse_y // 40:
                                            self.objects.remove(o2)
                                    soldier_red = Soldier_red(self.soldier_red_clicked.x,
                                                              self.soldier_red_clicked.y)
                                    soldier_red.move_left -= 1
                                    self.objects.append(soldier_red)
                                    self.objects.remove(self.soldier_red_clicked)
                                    self.income_red += 1
                                    self.soldier_actions = 'none'
                                    self.counter = False
                    elif not self.counter:
                        for i in self.objects:
                            if isinstance(i, Soldier):
                                if i.collidepoint(mouse_x, mouse_y) and i.color() == 'red' and i.move_left == 1 and self.capital_actions == 'none' and not self.capital_buttons:
                                    self.remover = i
                                    self.counter = True
                        if self.counter:
                            self.soldier_red_clicked = Soldier_red_clicked((mouse_x // 40) * 40,
                                                                           (mouse_y // 40) * 40)
                            self.objects.append(self.soldier_red_clicked)
                            self.objects.remove(self.remover)
                            self.create_soldier_click_anim((mouse_x // 40) * 40, (mouse_y // 40) * 40, 'red')
                            create_soldier_buttons(mouse_x, mouse_y)
                            self.soldier_buttons = True

        for anim in self.anims[::-1]:
            if anim.finished():
                if anim.anim_type() == 'fieldsquare_other':
                    fieldsquare_other = Fieldsquare_other(anim.x, anim.y)
                    self.objects.append(fieldsquare_other)
                elif anim.anim_type() == 'choose_fieldsquare':
                    fieldsquare_choose = Fieldsquare_choose(anim.x, anim.y)
                    self.objects.append(fieldsquare_choose)
                self.anims.remove(anim)
                self.objects.remove(anim)

    def do_keydown_next_turn(self):
        if not self.next_turn and not self.soldier_buttons and not self.capital_buttons and self.capital_actions == 'none' and self.soldier_actions == 'none':  # переход хода к красным
            self.next_turn = True
            self.balance_blue += self.income_blue
            self.objects.remove(self.blue_turn_pointer)
            self.objects.append(self.red_turn_pointer)
        elif not self.soldier_buttons and not self.capital_buttons and self.capital_actions == 'none' and self.soldier_actions == 'none':  # переход хода к синим
            for i in self.objects:
                i.newturn()
            self.balance_red += self.income_red
            self.next_turn = False
            self.objects.append(self.blue_turn_pointer)
            self.objects.remove(self.red_turn_pointer)

    def do_keydown_escape(self):
        if not self.next_turn:
            if self.capital_buttons:
                self.escape_capital_1()

            if self.soldier_buttons:
                self.escape_soldier_1('blue')

            if self.soldier_actions != 'none':
                self.escape_soldier_2('blue')

            if self.capital_actions != 'none':
                self.escape_capital_2()
            self.delete_fieldsquares()

        elif self.next_turn:
            if self.capital_buttons:
                self.escape_capital_1()

            if self.soldier_buttons:
                self.escape_soldier_1('red')

            if self.soldier_actions != 'none':
                self.escape_soldier_2('red')

            if self.capital_actions != 'none':
                self.escape_capital_2()
            self.delete_fieldsquares()

    def draw(self):
        for o in self.objects:
            o.draw(self.surface)

    def run(self):
        while 1:
            # while not self.next_turn:
            self.surface.blit(self.background_image, (0, 0))
            self.surface.blit(self.gamesquare_image, (200, 200))

            # self.surface.blit(self.capital_image, (0, 280))
            # self.surface.blit(self.capital_image, (760, 280))

            self.handle_events()
            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(self.frame_rate)
