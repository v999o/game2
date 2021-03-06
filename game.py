import pygame
from pygame.locals import *
import config as c
import sys
from text_object import TextObject
from button import Button
from gameobject import GameObject
from animations import Soldier_blue_click_anim
from animations import Choose_fieldsquare_anim
from animations import Fieldsquares_others_anim
from soldier import Soldier_blue
from soldier import Soldier_blue_clicked
from soldier import Soldier_red
from soldier import Soldier_red_clicked
from buildings import Capital_blue
from buildings import Capital_blue_clicked
from buildings import Capital_red
from buildings import Capital_red_clicked
from buildings import Factory_blue
from buildings import  Factory_red
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

class Game:
    def __init__(self, caption, width, height, back_image_filename, gamesquare_image_filename, capital_image_filename, soldier_image_filename, fieldsquare_red_image_filename, fieldsquare_blue_image_filename, frame_rate):
        self.background_image = pygame.image.load(back_image_filename)
        self.gamesquare_image = pygame.image.load(gamesquare_image_filename)
        # self.capital_image = pygame.image.load(capital_image_filename)
        # self.soldier_image = pygame.image.load(soldier_image_filename)
        self.fieldsquare_red_image = pygame.image.load(fieldsquare_red_image_filename)
        self.fieldsquare_blue_image = pygame.image.load(fieldsquare_blue_image_filename)
        self.frame_rate = frame_rate
        self.next_turn = False
        self.objects = []
        self.objects_to_remove = []
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

        self.is_first_pointer = True

        self.balance_blue = 10
        self.income_blue = 10
        self.balance_red = 10
        self.income_red = 10

        for y in range(0, 599, 40):
            for x in range(0, 799, 40):
                if not ((x == 18*40 or x == 19*40 or x == 0 or x == 1*40) and (y == 6*40 or y == 7*40 or y == 8*40)):
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
        self.move_button = Move_button(self.bg_for_buttons._rect.x+10, self.bg_for_buttons._rect.y+10)
        self.move_button_clicked = Move_button_clicked(self.move_button._rect.x, self.move_button._rect.y)
        self.attack_button = Attack_button(self.bg_for_buttons._rect.x+70, self.bg_for_buttons._rect.y+10)
        self.attack_button_clicked = Attack_button_clicked(self.attack_button._rect.x, self.attack_button._rect.y)
        self.capture_button = Capture_button(self.bg_for_buttons._rect.x+130, self.bg_for_buttons._rect.y+10)
        self.capture_button_clicked = Capture_button_clicked(self.capture_button._rect.x, self.capture_button._rect.y)
        self.spawn_soldier_button = Spawn_soldier_button(160, 480)
        self.spawn_soldier_button_clicked = Spawn_soldier_button_clicked(160, 480)
        self.spawn_factory_button = Spawn_factory_button(500, 480)
        self.spawn_factory_button_clicked = Spawn_factory_button_clicked(500, 480)

        self.fieldsquare_blue = Fieldsquare_blue(18 * 40, 6 * 40)
        self.objects.append(self.fieldsquare_blue)
        self.fieldsquare_blue = Fieldsquare_blue(18 * 40, 7 * 40)
        self.objects.append(self.fieldsquare_blue)
        self.fieldsquare_blue = Fieldsquare_blue(18 * 40, 8 * 40)
        self.objects.append(self.fieldsquare_blue)
        self.fieldsquare_blue = Fieldsquare_blue(19 * 40, 6 * 40)
        self.objects.append(self.fieldsquare_blue)
        self.fieldsquare_blue = Fieldsquare_blue(19 * 40, 8 * 40)
        self.objects.append(self.fieldsquare_blue)
        self.fieldsquare_red = Fieldsquare_red(1 * 40, 6 * 40)
        self.objects.append(self.fieldsquare_red)
        self.fieldsquare_red = Fieldsquare_red(1 * 40, 7 * 40)
        self.objects.append(self.fieldsquare_red)
        self.fieldsquare_red = Fieldsquare_red(1 * 40, 8 * 40)
        self.objects.append(self.fieldsquare_red)
        self.fieldsquare_red = Fieldsquare_red(0 * 40, 6 * 40)
        self.objects.append(self.fieldsquare_red)
        self.fieldsquare_red = Fieldsquare_red(0 * 40, 8 * 40)
        self.objects.append(self.fieldsquare_red)

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
        self.balance_label_blue = TextObject(c.balance_blue_offset,
                                      c.status_offset_y,
                                      lambda: f'$: {self.balance_blue}',
                                      c.text_color1,
                                      c.font_name,
                                      c.font_size)
        self.objects.append(self.balance_label_blue)
        self.income_label_blue = TextObject(c.income_blue_offset,
                                      c.status_offset_y,
                                      lambda: f'+: {self.income_blue}',
                                      c.text_color1,
                                      c.font_name,
                                      c.font_size)
        self.objects.append(self.income_label_blue)
        self.balance_label_red = TextObject(c.balance_red_offset,
                                             c.status_offset_y,
                                             lambda: f'$: {self.balance_red}',
                                             c.text_color2,
                                             c.font_name,
                                             c.font_size)
        self.objects.append(self.balance_label_red)
        self.income_label_red = TextObject(c.income_red_offset,
                                             c.status_offset_y,
                                             lambda: f'+: {self.income_red}',
                                             c.text_color2,
                                             c.font_name,
                                             c.font_size)
        self.objects.append(self.income_label_red)

    def create_soldier_click_anim(self, x, y):
        anim = Soldier_blue_click_anim(x, y)
        self.anims.append(anim)
        self.objects.append(anim)

    def fieldsquare_choose_anim(self, x, y):
        anim = Choose_fieldsquare_anim(x, y)
        self.anims.append(anim)
        self.objects.append(anim)

    def fieldsquare_others_anim(self, x, y):
        anim = Fieldsquares_others_anim(x, y)
        self.anims.append(anim)
        self.objects.append(anim)

    def update(self):
        for o in self.objects:
            o.update()


    def handle_events(self):
        def create_soldier_buttons(a, b):
            if a <= 705 and a >= 95:
                a = a-95
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
            self.attack_button = Attack_button(self.bg_for_buttons._rect.x + 10, self.bg_for_buttons._rect.y + 10)
            self.attack_button_clicked = Attack_button_clicked(self.attack_button._rect.x, self.attack_button._rect.y)
            self.objects.append(self.attack_button)
            self.move_button = Move_button(self.bg_for_buttons._rect.x + 70, self.bg_for_buttons._rect.y + 10)
            self.move_button_clicked = Move_button_clicked(self.move_button._rect.x, self.move_button._rect.y)
            self.objects.append(self.move_button)
            self.capture_button = Capture_button(self.bg_for_buttons._rect.x + 130, self.bg_for_buttons._rect.y + 10)
            self.capture_button_clicked = Capture_button_clicked(self.capture_button._rect.x, self.capture_button._rect.y)
            self.objects.append(self.capture_button)

        def create_capital_buttons(a, b):
            if a <= 725 and a >= 75:
                a = a-75
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
            self.spawn_soldier_button = Spawn_soldier_button(self.bg_for_buttons_capital._rect.x + 10, self.bg_for_buttons_capital._rect.y + 10)
            self.spawn_soldier_button_clicked = Spawn_soldier_button_clicked(self.spawn_soldier_button._rect.x, self.spawn_soldier_button._rect.y)
            self.objects.append(self.spawn_soldier_button)
            self.spawn_factory_button = Spawn_factory_button(self.bg_for_buttons_capital._rect.x + 70, self.bg_for_buttons_capital._rect.y + 10)
            self.spawn_factory_button_clicked = Spawn_factory_button_clicked(self.spawn_factory_button._rect.x, self.spawn_factory_button._rect.y)
            self.objects.append(self.spawn_factory_button)



        if self.soldier_buttons == True:
            if self.move_button_clicked.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and not self.is_move_button_clicked:
            # if pygame.mouse.get_pos()[0] > 80 and pygame.mouse.get_pos()[0] < 160 and pygame.mouse.get_pos()[1] > 480 and pygame.mouse.get_pos()[1] < 560 and not self.buttons_clicked:
                # self.move_button_clicked = Move_button_clicked(80, 480)
                self.objects.append(self.move_button_clicked)
                self.is_move_button_clicked = True
            elif not self.move_button_clicked.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and self.is_move_button_clicked:
            # elif (pygame.mouse.get_pos()[0] < 80 or pygame.mouse.get_pos()[0] > 160 or pygame.mouse.get_pos()[1] < 480 or pygame.mouse.get_pos()[1] > 560) and self.buttons_clicked:
                self.objects.remove(self.move_button_clicked)
                self.is_move_button_clicked = False
            if self.attack_button.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and not self.is_attack_button_clicked:
                self.objects.append(self.attack_button_clicked)
                self.is_attack_button_clicked = True
            elif not self.attack_button_clicked.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and self.is_attack_button_clicked:
                self.objects.remove(self.attack_button_clicked)
                self.is_attack_button_clicked = False
            if self.capture_button_clicked.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and not self.is_capture_button_clicked:
                self.objects.append(self.capture_button_clicked)
                self.is_capture_button_clicked = True
            elif not self.capture_button_clicked.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and self.is_capture_button_clicked:
                self.objects.remove(self.capture_button_clicked)
                self.is_capture_button_clicked = False

        if self.capital_buttons == True:
            if self.spawn_soldier_button_clicked.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and not self.is_spawn_soldier_button_clicked:
                self.objects.append(self.spawn_soldier_button_clicked)
                self.is_spawn_soldier_button_clicked = True
            elif not self.spawn_soldier_button_clicked.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and self.is_spawn_soldier_button_clicked:
                self.objects.remove(self.spawn_soldier_button_clicked)
                self.is_spawn_soldier_button_clicked = False
            if self.spawn_factory_button_clicked.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and not self.is_spawn_factory_button_clicked:
                self.objects.append(self.spawn_factory_button_clicked)
                self.is_spawn_factory_button_clicked = True
            elif not self.spawn_factory_button_clicked.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and self.is_spawn_factory_button_clicked:
                self.objects.remove(self.spawn_factory_button_clicked)
                self.is_spawn_factory_button_clicked = False



        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not self.next_turn:
                        if self.capital_buttons:
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

                        if self.soldier_buttons:
                            self.soldier_blue = Soldier_blue(self.soldier_blue_clicked._rect.x, self.soldier_blue_clicked._rect.y)
                            self.objects.append(self.soldier_blue)
                            self.objects.remove(self.soldier_blue_clicked)
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


                        if self.soldier_actions != 'none':
                            self.soldier_blue = Soldier_blue(self.soldier_blue_clicked._rect.x,
                                                         self.soldier_blue_clicked._rect.y)
                            self.objects.append(self.soldier_blue)
                            self.objects.remove(self.soldier_blue_clicked)
                            self.soldier_actions = 'none'
                            self.counter = False

                        if self.capital_actions != 'none':
                            self.objects.remove(self.capital_clicked)
                            self.capital_actions = 'none'

                    elif self.next_turn:
                        if self.capital_buttons:
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

                        if self.soldier_buttons:
                            self.soldier_red = Soldier_red(self.soldier_red_clicked._rect.x,
                                                             self.soldier_red_clicked._rect.y)
                            self.objects.append(self.soldier_red)
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

                        if self.soldier_actions != 'none':
                            self.soldier_red = Soldier_red(self.soldier_red_clicked._rect.x,
                                                         self.soldier_red_clicked._rect.y)
                            self.objects.append(self.soldier_red)
                            self.objects.remove(self.soldier_red_clicked)
                            self.soldier_actions = 'none'
                            self.counter = False

                        if self.capital_actions != 'none':
                            self.objects.remove(self.capital_clicked)
                            self.capital_actions = 'none'


                else:
                    if not self.next_turn and not self.soldier_buttons and not self.capital_buttons and self.capital_actions == 'none' and self.soldier_actions == 'none':  # ?????????????? ???????? ?? ??????????????
                        self.next_turn = True
                        self.balance_blue += self.income_blue
                        self.objects.remove(self.blue_turn_pointer)
                        self.objects.append(self.red_turn_pointer)
                    elif not self.soldier_buttons and not self.capital_buttons and self.capital_actions == 'none' and self.soldier_actions == 'none':  # ?????????????? ???????? ?? ??????????
                        for i in self.objects:
                            i.newturn()
                        self.balance_red += self.income_red
                        self.next_turn = False
                        self.objects.append(self.blue_turn_pointer)
                        self.objects.remove(self.red_turn_pointer)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.next_turn:
                    if self.capital_blue.collidepoint(event.pos[0], event.pos[1]) and not self.capital_buttons and self.capital_actions == 'none' and self.soldier_actions == 'none' and not self.soldier_buttons:
                        self.capital_buttons = True
                        self.capital_clicked = Capital_blue_clicked(760, 280)
                        self.objects.append(self.capital_clicked)
                        create_capital_buttons(event.pos[0], event.pos[1])
                    elif self.capital_buttons and self.spawn_soldier_button_clicked.collidepoint(event.pos[0], event.pos[1]) and not self.soldier_buttons:
                        self.objects.remove(self.bg_for_buttons_capital)
                        self.objects.remove(self.spawn_soldier_button)
                        self.objects.remove(self.spawn_soldier_button_clicked)
                        self.objects.remove(self.spawn_factory_button)
                        self.capital_buttons = False
                        self.capital_actions = 'spawn_soldier'
                        self.is_spawn_soldier_button_clicked = False
                    elif self.capital_buttons and self.spawn_factory_button_clicked.collidepoint(event.pos[0], event.pos[1]) and not self.soldier_buttons:
                        self.objects.remove(self.bg_for_buttons_capital)
                        self.objects.remove(self.spawn_soldier_button)
                        self.objects.remove(self.spawn_factory_button)
                        self.objects.remove(self.spawn_factory_button_clicked)
                        self.capital_buttons = False
                        self.capital_actions = 'spawn_factory'
                        self.is_spawn_factory_button_clicked = False

                    elif self.capital_actions == 'spawn_soldier' and self.balance_blue >= 10:
                        for j in self.objects:
                            if j.type() == 'fieldsquare' and j.collidepoint(event.pos[0], event.pos[1]) and j.color() == 'blue':
                                for i in self.objects:
                                    if (i.type() == 'factory' or i.type() == 'capital') and i.color() == 'blue' and ((j._rect.x//40+1 == i._rect.x//40 and j._rect.y//40 == i._rect.y//40) or (j._rect.x//40-1 == i._rect.x//40 and j._rect.y//40 == i._rect.y//40) or (j._rect.x//40 == i._rect.x//40 and j._rect.y//40+1 == i._rect.y//40) or (j._rect.x//40 == i._rect.x//40 and j._rect.y//40-1 == i._rect.y//40)):
                                        self.objects.remove(self.capital_clicked)
                                        self.soldier_blue = Soldier_blue((event.pos[0] // 40) * 40, (event.pos[1] // 40) * 40)
                                        self.objects.append(self.soldier_blue)
                                        self.capital_actions = 'none'
                                        self.balance_blue -= 10
                                        break

                    elif self.capital_actions == 'spawn_factory' and self.balance_blue >= 12:
                        for i in self.objects:
                            if i.type() == 'fieldsquare' and i.collidepoint(event.pos[0], event.pos[1]) and i.color() == 'blue':
                                self.objects.remove(self.capital_clicked)
                                self.objects.remove(i)
                                self.factory_blue = Factory_blue((event.pos[0] // 40) * 40, (event.pos[1] // 40) * 40)
                                self.objects.append(self.factory_blue)
                                self.capital_actions = 'none'
                                self.balance_blue -= 12
                                self.income_blue += 6

                    elif not self.counter:
                        for i in self.objects:
                            if i.type() == 'soldier' and i.collidepoint(event.pos[0], event.pos[1]) and i.color() == 'blue' and i.move_left == 1 and self.capital_actions == 'none' and not self.capital_buttons:
                                self.remover = i
                                self.counter = True
                        if self.counter == True:
                            self.soldier_blue_clicked = Soldier_blue_clicked((event.pos[0]//40)*40, (event.pos[1]//40)*40)
                            self.objects.append(self.soldier_blue_clicked)
                            self.create_soldier_click_anim((event.pos[0] // 40) * 40, (event.pos[1] // 40) * 40)
                            self.objects.remove(self.remover)
                            create_soldier_buttons(event.pos[0], event.pos[1])
                            self.soldier_buttons = True
                        elif self.soldier_actions == 'move_soldier':
                            for i in self.objects:
                                if i.type() == 'choose_fieldsquare' and event.pos[0]//40 == i._rect.x//40 and event.pos[1]//40 == i._rect.y//40:
                                    self.soldier_blue = Soldier_blue((event.pos[0]//40)*40, (event.pos[1]//40)*40)
                                    self.soldier_blue.move_left -= 1
                                    self.objects.append(self.soldier_blue)
                                    self.objects.remove(self.soldier_blue_clicked)
                                    self.soldier_actions = 'none'
                                    for i in self.objects[::-1]:
                                        if i.type() == 'choose_fieldsquare' or i.type() == 'fieldsquare_other':
                                            self.objects_to_remove.append(i)
                                    for i in self.objects_to_remove[::-1]:
                                        self.objects.remove(i)
                                    self.objects_to_remove.clear()


                    elif self.is_move_button_clicked:
                        # self.soldier_blue = Soldier_blue((event.pos[0] // 40) * 40, (event.pos[1] // 40) * 40)
                        self.objects.remove(self.bg_for_buttons)
                        self.objects.remove(self.move_button)
                        self.objects.remove(self.attack_button)
                        self.objects.remove(self.capture_button)
                        self.objects.remove(self.move_button_clicked)
                        self.soldier_buttons = False
                        self.counter = False
                        self.is_move_button_clicked = False
                        self.soldier_actions = 'move_soldier'
                        for i in self.objects:
                            if i.type() == 'fieldsquare' or i.type() == 'capital':
                                if (i._rect.x // 40 == self.soldier_blue_clicked._rect.x // 40 + 1
                                    or i._rect.x // 40 == self.soldier_blue_clicked._rect.x // 40 - 1
                                    or i._rect.y // 40 == self.soldier_blue_clicked._rect.y // 40 + 1
                                    or i._rect.y // 40 == self.soldier_blue_clicked._rect.y // 40 - 1) and not (
                                        i._rect.x // 40 != self.soldier_blue_clicked._rect.x // 40 and i._rect.y // 40 != self.soldier_blue_clicked._rect.y // 40) and i.type() != 'capital':
                                    self.fieldsquare_choose_anim(i._rect.x, i._rect.y)
                                else:
                                    self.fieldsquare_others_anim(i._rect.x, i._rect.y)




                    elif self.is_attack_button_clicked:
                        self.objects.remove(self.bg_for_buttons)
                        self.objects.remove(self.move_button)
                        self.objects.remove(self.attack_button)
                        self.objects.remove(self.capture_button)
                        self.objects.remove(self.attack_button_clicked)
                        self.soldier_buttons = False
                        self.is_attack_button_clicked = False
                        self.soldier_actions = 'attack_soldier'
                    elif self.is_capture_button_clicked:
                        self.objects.remove(self.bg_for_buttons)
                        self.objects.remove(self.move_button)
                        self.objects.remove(self.attack_button)
                        self.objects.remove(self.capture_button)
                        self.objects.remove(self.capture_button_clicked)
                        self.soldier_buttons = False
                        self.is_capture_button_clicked = False
                        self.soldier_actions = 'capture_soldier'

                    elif self.soldier_actions == 'attack_soldier':
                        if not (event.pos[0]//40 > self.soldier_blue_clicked._rect.x//40+1
                                    or event.pos[0]//40 < self.soldier_blue_clicked._rect.x//40-1
                                    or event.pos[1]//40 > self.soldier_blue_clicked._rect.y//40+1
                                    or event.pos[1]//40 < self.soldier_blue_clicked._rect.y//40-1) and not (event.pos[0]//40 != self.soldier_blue_clicked._rect.x//40 and event.pos[1]//40 != self.soldier_blue_clicked._rect.y//40):
                            for i in self.objects:
                                if i.type() == 'factory' and i.color() == 'red' and i.collidepoint(event.pos[0], event.pos[1]):
                                    self.objects.remove(i)
                                    self.income_red -= 6
                                    self.objects.remove(i)
                                    self.soldier_blue = Soldier_blue(self.soldier_blue_clicked._rect.x,
                                                                     self.soldier_blue_clicked._rect.y)
                                    self.soldier_blue.move_left -= 1
                                    self.objects.append(self.soldier_blue)
                                    self.objects.remove(self.soldier_blue_clicked)
                                    self.soldier_actions = 'none'
                                    self.counter = False
                                if i.type() == 'soldier' and i.color() == 'red' and i.collidepoint(event.pos[0], event.pos[1]):
                                    self.objects.remove(i)
                                    self.soldier_blue = Soldier_blue(self.soldier_blue_clicked._rect.x, self.soldier_blue_clicked._rect.y)
                                    self.soldier_blue.move_left -= 1
                                    self.objects.append(self.soldier_blue)
                                    self.objects.remove(self.soldier_blue_clicked)
                                    self.soldier_actions = 'none'
                                    self.counter = False
                    elif self.soldier_actions == 'capture_soldier':
                        if not (event.pos[0] // 40 > self.soldier_blue_clicked._rect.x // 40 + 1
                                or event.pos[0] // 40 < self.soldier_blue_clicked._rect.x // 40 - 1
                                or event.pos[1] // 40 > self.soldier_blue_clicked._rect.y // 40 + 1
                                or event.pos[1] // 40 < self.soldier_blue_clicked._rect.y // 40 - 1) and not (
                                event.pos[0] // 40 != self.soldier_blue_clicked._rect.x // 40 and event.pos[1] // 40 != self.soldier_blue_clicked._rect.y // 40):
                            for i in self.objects:
                                if i.type() != 'textobject' and i.color() != 'blue' and i.collidepoint(event.pos[0], event.pos[1]):
                                    if i == 'fieldsquare' and i.color() == 'red':
                                        self.income_red -= 1
                                        break
                                    self.fieldsquare_blue = Fieldsquare_blue(event.pos[0]//40*40, event.pos[1]//40*40)
                                    self.objects.append(self.fieldsquare_blue)
                                    for i in self.objects:
                                        if i.type() == 'fieldsquare' and i.color() == 'neutral' and i._rect.x//40 == event.pos[0]//40 and i._rect.y//40 == event.pos[1]//40:
                                            self.objects.remove(i)
                                    self.soldier_blue = Soldier_blue(self.soldier_blue_clicked._rect.x, self.soldier_blue_clicked._rect.y)
                                    self.soldier_blue.move_left -= 1
                                    self.objects.append(self.soldier_blue)
                                    self.objects.remove(self.soldier_blue_clicked)
                                    self.income_blue += 1
                                    self.soldier_actions = 'none'
                                    self.counter = False

                else:  # ?????? ??????????????
                    if self.capital_red.collidepoint(event.pos[0], event.pos[1]) and not self.capital_buttons and self.capital_actions == 'none' and self.soldier_actions == 'none' and not self.soldier_buttons:
                        self.capital_buttons = True
                        self.capital_clicked = Capital_red_clicked(0, 280)
                        self.objects.append(self.capital_clicked)
                        create_capital_buttons(event.pos[0], event.pos[1])
                    elif self.capital_buttons and self.spawn_soldier_button_clicked.collidepoint(event.pos[0], event.pos[1]) and not self.soldier_buttons:
                        self.objects.remove(self.bg_for_buttons_capital)
                        self.objects.remove(self.spawn_soldier_button)
                        self.objects.remove(self.spawn_soldier_button_clicked)
                        self.objects.remove(self.spawn_factory_button)
                        self.capital_buttons = False
                        self.capital_actions = 'spawn_soldier'
                        self.is_spawn_soldier_button_clicked = False
                    elif self.capital_buttons and self.spawn_factory_button_clicked.collidepoint(event.pos[0], event.pos[1]) and not self.soldier_buttons:
                        self.objects.remove(self.bg_for_buttons_capital)
                        self.objects.remove(self.spawn_soldier_button)
                        self.objects.remove(self.spawn_factory_button)
                        self.objects.remove(self.spawn_factory_button_clicked)
                        self.capital_buttons = False
                        self.capital_actions = 'spawn_factory'
                        self.is_spawn_factory_button_clicked = False

                    elif self.capital_actions == 'spawn_soldier' and self.balance_red >= 10:
                        for j in self.objects:
                            if j.type() == 'fieldsquare' and j.collidepoint(event.pos[0], event.pos[1]) and j.color() == 'red':
                                for i in self.objects:
                                    if (i.type() == 'factory' or i.type() == 'capital') and i.color() == 'red' and ((j._rect.x//40+1 == i._rect.x//40 and j._rect.y//40 == i._rect.y//40) or (j._rect.x//40-1 == i._rect.x//40 and j._rect.y//40 == i._rect.y//40) or (j._rect.x//40 == i._rect.x//40 and j._rect.y//40+1 == i._rect.y//40) or (j._rect.x//40 == i._rect.x//40 and j._rect.y//40-1 == i._rect.y//40)):
                                        self.soldier_red = Soldier_red((event.pos[0] // 40) * 40, (event.pos[1] // 40) * 40)
                                        self.objects.append(self.soldier_red)
                                        self.capital_actions = 'none'
                                        self.balance_red -= 10
                                        self.objects.remove(self.capital_clicked)
                                        break

                    elif self.capital_actions == 'spawn_factory' and self.balance_red >= 12:
                        for i in self.objects:
                            if i.type() == 'fieldsquare' and i.collidepoint(event.pos[0], event.pos[1]) and i.color() == 'red':
                                self.objects.remove(self.capital_clicked)
                                self.factory_red = Factory_red((event.pos[0] // 40) * 40, (event.pos[1] // 40) * 40)
                                self.objects.append(self.factory_red)
                                self.capital_actions = 'none'
                                self.balance_red -= 12
                                self.income_red += 6

                    elif self.counter == False:
                        for i in self.objects:
                            if i.type() == 'soldier' and i.collidepoint(event.pos[0], event.pos[1]) and i.color() == 'red' and i.move_left == 1 and self.capital_actions == 'none' and not self.capital_buttons:
                                self.remover = i
                                self.counter = True
                        if self.counter == True:
                            self.soldier_red_clicked = Soldier_red_clicked((event.pos[0]//40)*40, (event.pos[1]//40)*40)
                            self.objects.append(self.soldier_red_clicked)
                            self.objects.remove(self.remover)
                            create_soldier_buttons(event.pos[0], event.pos[1])
                            self.soldier_buttons = True
                        elif self.soldier_actions == 'move_soldier':
                            if (event.pos[0]//40 == self.soldier_red_clicked._rect.x//40+1
                                    or event.pos[0]//40 == self.soldier_red_clicked._rect.x//40-1
                                    or event.pos[1]//40 == self.soldier_red_clicked._rect.y//40+1
                                    or event.pos[1]//40 == self.soldier_red_clicked._rect.y//40-1) and not (event.pos[0]//40 != self.soldier_red_clicked._rect.x//40 and event.pos[1]//40 != self.soldier_red_clicked._rect.y//40):

                                for i in self.objects:
                                    if i.type() == 'fieldsquare' and i.collidepoint(event.pos[0], event.pos[1]):
                                        self.soldier_red = Soldier_red((event.pos[0]//40)*40, (event.pos[1]//40)*40)
                                        self.soldier_red.move_left -= 1
                                        self.objects.append(self.soldier_red)
                                        self.objects.remove(self.soldier_red_clicked)
                                        self.soldier_actions = 'none'

                    elif self.is_move_button_clicked:
                        self.soldier_red = Soldier_red((event.pos[0] // 40) * 40, (event.pos[1] // 40) * 40)
                        self.objects.remove(self.bg_for_buttons)
                        self.objects.remove(self.move_button)
                        self.objects.remove(self.attack_button)
                        self.objects.remove(self.capture_button)
                        self.objects.remove(self.move_button_clicked)
                        self.soldier_buttons = False
                        self.counter = False
                        self.is_move_button_clicked = False
                        self.soldier_actions = 'move_soldier'
                    elif self.is_attack_button_clicked:
                        self.objects.remove(self.bg_for_buttons)
                        self.objects.remove(self.move_button)
                        self.objects.remove(self.attack_button)
                        self.objects.remove(self.capture_button)
                        self.objects.remove(self.attack_button_clicked)
                        self.soldier_buttons = False
                        self.is_attack_button_clicked = False
                        self.soldier_actions = 'attack_soldier'
                    elif self.is_capture_button_clicked:
                        self.objects.remove(self.bg_for_buttons)
                        self.objects.remove(self.move_button)
                        self.objects.remove(self.attack_button)
                        self.objects.remove(self.capture_button)
                        self.objects.remove(self.capture_button_clicked)
                        self.soldier_buttons = False
                        self.is_capture_button_clicked = False
                        self.soldier_actions = 'capture_soldier'
                    elif self.soldier_actions == 'attack_soldier':
                        if not (event.pos[0]//40 > self.soldier_red_clicked._rect.x//40+1
                                    or event.pos[0]//40 < self.soldier_red_clicked._rect.x//40-1
                                    or event.pos[1]//40 > self.soldier_red_clicked._rect.y//40+1
                                    or event.pos[1]//40 < self.soldier_red_clicked._rect.y//40-1) and not (event.pos[0]//40 != self.soldier_red_clicked._rect.x//40 and event.pos[1]//40 != self.soldier_red_clicked._rect.y//40):
                            for i in self.objects:
                                if i.type() == 'factory' and i.color() == 'blue' and i.collidepoint(event.pos[0], event.pos[1]):
                                    self.objects.remove(i)
                                    self.income_blue -= 6
                                    self.objects.remove(i)
                                    self.soldier_red = Soldier_red(self.soldier_red_clicked._rect.x,
                                                                 self.soldier_red_clicked._rect.y)
                                    self.soldier_red.move_left -= 1
                                    self.objects.append(self.soldier_red)
                                    self.objects.remove(self.soldier_red_clicked)
                                    self.soldier_actions = 'none'
                                    self.counter = False
                                if i.type() == 'soldier' and i.color() == 'red' and i.collidepoint(event.pos[0],
                                                                                               event.pos[1]):
                                    self.objects.remove(i)
                                    self.soldier_red = Soldier_red(self.soldier_red_clicked._rect.x,
                                                                 self.soldier_red_clicked._rect.y)
                                    self.soldier_blue.move_left -= 1
                                    self.objects.append(self.soldier_red)
                                    self.objects.remove(self.soldier_red_clicked)
                                    self.soldier_actions = 'none'
                                    self.counter = False
                    elif self.soldier_actions == 'capture_soldier':
                        if not (event.pos[0] // 40 > self.soldier_red_clicked._rect.x // 40 + 1
                                or event.pos[0] // 40 < self.soldier_red_clicked._rect.x // 40 - 1
                                or event.pos[1] // 40 > self.soldier_red_clicked._rect.y // 40 + 1
                                or event.pos[1] // 40 < self.soldier_red_clicked._rect.y // 40 - 1) and not (
                                event.pos[0] // 40 != self.soldier_red_clicked._rect.x // 40 and event.pos[1] // 40 != self.soldier_red_clicked._rect.y // 40):
                            for i in self.objects:
                                if i.type() != 'textobject' and i.color() != 'red' and i.collidepoint(event.pos[0], event.pos[1]):
                                    if i == 'fieldsquare' and i.color() == 'blue':
                                        self.income_red -= 1
                                        break
                                    self.fieldsquare_red = Fieldsquare_red(event.pos[0]//40*40, event.pos[1]//40*40)
                                    self.objects.append(self.fieldsquare_red)
                                    for i in self.objects:
                                        if i.type() == 'fieldsquare' and i.color() == 'neutral' and i._rect.x//40 == event.pos[0]//40 and i._rect.y//40 == event.pos[1]//40:
                                            self.objects.remove(i)
                                    self.soldier_red = Soldier_red(self.soldier_red_clicked._rect.x, self.soldier_red_clicked._rect.y)
                                    self.soldier_red.move_left -= 1
                                    self.objects.append(self.soldier_red)
                                    self.objects.remove(self.soldier_red_clicked)
                                    self.income_red += 1
                                    self.soldier_actions = 'none'
                                    self.counter = False

        for anim in self.anims:
            if anim.life <= 0:
                if anim.anim_type() == 'fieldsquare_other':
                    self.fieldsquare_other = Fieldsquare_other(anim._rect.x, anim._rect.y)
                    self.objects.append(self.fieldsquare_other)
                elif anim.anim_type() == 'choose_fieldsquare':
                    self.fieldsquare_choose = Fieldsquare_choose(anim._rect.x, anim._rect.y)
                    self.objects.append(self.fieldsquare_choose)
                self.anims.remove(anim)
                self.objects.remove(anim)


    def draw(self):
        for o in self.objects:
            o.draw(self.surface)


    def run(self):
        while 1:
       # while not self.next_turn:
            self.surface.blit(self.background_image, (0, 0))
            self.surface.blit(self.gamesquare_image, (200, 200))
            '''for y in range(0, 599, 40):
                for x in range(0, 799, 40):
                    self.surface.blit(self.gamesquare_image, (x, y))'''


            #self.surface.blit(self.capital_image, (0, 280))
            #self.surface.blit(self.capital_image, (760, 280))


            self.handle_events()
            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(self.frame_rate)