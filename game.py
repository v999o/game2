import pygame
from pygame.locals import *
import config as c
import sys
from text_object import TextObject
from button import Button
from gameobject import GameObject
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
from field_objects import Blue_turn_pointer
from field_objects import Red_turn_pointer
from collections import defaultdict

class Game:
    def __init__(self, caption, width, height, back_image_filename, gamesquare_image_filename, capital_image_filename, soldier_image_filename, fieldsquare_red_image_filename, fieldsquare_blue_image_filename, frame_rate):
        self.background_image = pygame.image.load(back_image_filename)
        self.gamesquare_image = pygame.image.load(gamesquare_image_filename)
        self.capital_image = pygame.image.load(capital_image_filename)
        self.soldier_image = pygame.image.load(soldier_image_filename)
        self.fieldsquare_red_image = pygame.image.load(fieldsquare_red_image_filename)
        self.fieldsquare_blue_image = pygame.image.load(fieldsquare_blue_image_filename)
        self.frame_rate = frame_rate
        self.next_turn = False
        self.objects = []
        self.colors = []
        self.pause = True
        self.counter = False
        self.remover = None
        self.soldier_buttons = False
        self.capital_buttons = False
        self.move_soldier = False
        self.attack_soldier = False
        self.capture_soldier = False
        self.spawn_soldier = False
        self.spawn_factory = False

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

        self.blue_turn_pointer = Blue_turn_pointer(400, 10)
        self.red_turn_pointer = Red_turn_pointer(400, 10)
        self.objects.append(self.blue_turn_pointer)

        self.capital_red = Capital_red(0, 280)
        self.capital_clicked_red = Capital_red_clicked(0, 280)
        self.capital_clicked_blue = Capital_blue_clicked(760, 280)
        self.capital_blue = Capital_blue(760, 280)

        self.bg_for_buttons = Bg_for_button(0, 440)
        self.move_button = Move_button(80, 480)
        self.move_button_clicked = Move_button_clicked(80, 480)
        self.attack_button = Attack_button(360, 480)
        self.attack_button_clicked = Attack_button_clicked(360, 480)
        self.capture_button = Capture_button(640, 480)
        self.capture_button_clicked = Capture_button_clicked(640, 480)
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
        self.surface = pygame.display.set_mode((width, height), FULLSCREEN)
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

    def handle_events(self):
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
            if self.attack_button_clicked.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and not self.is_attack_button_clicked:
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
                            self.objects.remove(self.bg_for_buttons)
                            self.objects.remove(self.spawn_soldier_button)
                            self.objects.remove(self.spawn_factory_button)
                            self.objects.remove(self.capital_clicked_blue)
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


                        if self.move_soldier or self.attack_soldier or self.capture_soldier:
                            self.soldier_blue = Soldier_blue(self.soldier_blue_clicked._rect.x,
                                                         self.soldier_blue_clicked._rect.y)
                            self.objects.append(self.soldier_blue)
                            self.objects.remove(self.soldier_blue_clicked)
                            self.move_soldier = False
                            self.attack_soldier = False
                            self.capture_soldier = False
                            self.counter = False

                        if self.spawn_soldier or self.spawn_factory:
                            self.objects.remove(self.capital_clicked_blue)
                            self.spawn_factory = False
                            self.spawn_soldier = False

                    elif self.next_turn:
                        if self.capital_buttons:
                            self.objects.remove(self.bg_for_buttons)
                            self.objects.remove(self.spawn_soldier_button)
                            self.objects.remove(self.spawn_factory_button)
                            self.objects.remove(self.capital_clicked_red)
                            self.capital_buttons = False

                        if self.soldier_buttons:
                            self.soldier_red = Soldier_red(self.soldier_red_clicked._rect.x, self.soldier_red_clicked._rect.y)
                            self.objects.append(self.soldier_red)
                            self.objects.remove(self.soldier_red_clicked)
                            self.objects.remove(self.bg_for_buttons)
                            self.objects.remove(self.move_button)
                            self.objects.remove(self.attack_button)
                            self.objects.remove(self.capture_button)
                            self.soldier_buttons = False
                            self.counter = False
                            self.is_move_button_clicked = False

                        if self.move_soldier or self.attack_soldier or self.capture_soldier:
                            self.soldier_red = Soldier_red(self.soldier_red_clicked._rect.x,
                                                         self.soldier_red_clicked._rect.y)
                            self.objects.append(self.soldier_red)
                            self.objects.remove(self.soldier_red_clicked)
                            self.move_soldier = False
                            self.attack_soldier = False
                            self.capture_soldier = False
                            self.counter = False

                        if self.spawn_soldier or self.spawn_factory:
                            self.objects.remove(self.capital_clicked_red)
                            self.spawn_factory = False
                            self.spawn_soldier = False


                else:
                    if not self.next_turn and not self.soldier_buttons and not self.capital_buttons:  # переход хода к красным
                        self.next_turn = True
                        self.balance_blue += self.income_blue
                        self.objects.remove(self.blue_turn_pointer)
                        self.objects.append(self.red_turn_pointer)
                    elif not self.soldier_buttons and not self.capital_buttons:  # переход хода к синим
                        for i in self.objects:
                            i.newturn()
                        self.balance_red += self.income_red
                        self.next_turn = False
                        self.objects.append(self.blue_turn_pointer)
                        self.objects.remove(self.red_turn_pointer)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.next_turn:
                    if self.capital_blue.collidepoint(event.pos[0], event.pos[1]) and not self.capital_buttons and not self.spawn_factory and not self.spawn_soldier and not self.soldier_buttons:
                        self.capital_buttons = True
                        self.objects.append(self.bg_for_buttons)
                        self.objects.append(self.spawn_soldier_button)
                        self.objects.append(self.spawn_factory_button)
                        self.objects.append(self.capital_clicked_blue)
                    elif self.capital_buttons and self.spawn_soldier_button_clicked.collidepoint(event.pos[0], event.pos[1]) and not self.soldier_buttons:
                        self.objects.remove(self.bg_for_buttons)
                        self.objects.remove(self.spawn_soldier_button)
                        self.objects.remove(self.spawn_soldier_button_clicked)
                        self.objects.remove(self.spawn_factory_button)
                        self.capital_buttons = False
                        self.spawn_soldier = True
                        self.is_spawn_soldier_button_clicked = False
                    elif self.capital_buttons and self.spawn_factory_button_clicked.collidepoint(event.pos[0], event.pos[1]) and not self.soldier_buttons:
                        self.objects.remove(self.bg_for_buttons)
                        self.objects.remove(self.spawn_soldier_button)
                        self.objects.remove(self.spawn_factory_button)
                        self.objects.remove(self.spawn_factory_button_clicked)
                        self.capital_buttons = False
                        self.spawn_factory = True
                        self.is_spawn_factory_button_clicked = False

                    elif self.spawn_soldier and self.balance_blue >= 10:
                        for j in self.objects:
                            if j.type() == 'fieldsquare' and j.collidepoint(event.pos[0], event.pos[1]) and j.color() == 'blue':
                                for i in self.objects:
                                    if (i.type() == 'factory' or i.type() == 'capital') and i.color() == 'blue' and ((j._rect.x//40+1 == i._rect.x//40 and j._rect.y//40 == i._rect.y//40) or (j._rect.x//40-1 == i._rect.x//40 and j._rect.y//40 == i._rect.y//40) or (j._rect.x//40 == i._rect.x//40 and j._rect.y//40+1 == i._rect.y//40) or (j._rect.x//40 == i._rect.x//40 and j._rect.y//40-1 == i._rect.y//40)):
                                        self.objects.remove(self.capital_clicked_blue)
                                        self.soldier_blue = Soldier_blue((event.pos[0] // 40) * 40, (event.pos[1] // 40) * 40)
                                        self.objects.append(self.soldier_blue)
                                        self.spawn_soldier = False
                                        self.balance_blue -= 10
                                        break

                    elif self.spawn_factory and self.balance_blue >= 12:
                        for i in self.objects:
                            if i.type() == 'fieldsquare' and i.collidepoint(event.pos[0], event.pos[1]) and i.color() == 'blue':
                                self.objects.remove(self.capital_clicked_blue)
                                self.factory_blue = Factory_blue((event.pos[0] // 40) * 40, (event.pos[1] // 40) * 40)
                                self.objects.append(self.factory_blue)
                                self.spawn_factory = False
                                self.balance_blue -= 12
                                self.income_blue += 6

                    elif not self.counter:
                        for i in self.objects:
                            if i.type() == 'soldier' and i.collidepoint(event.pos[0], event.pos[1]) and i.color() == 'blue' and i.move_left == 1:
                                self.remover = i
                                self.counter = True
                        if self.counter == True:
                            self.soldier_blue_clicked = Soldier_blue_clicked((event.pos[0]//40)*40, (event.pos[1]//40)*40)
                            self.objects.append(self.soldier_blue_clicked)
                            self.objects.remove(self.remover)
                            self.objects.append(self.bg_for_buttons)
                            self.objects.append(self.move_button)
                            self.objects.append(self.attack_button)
                            self.objects.append(self.capture_button)
                            self.soldier_buttons = True
                        elif self.move_soldier:
                            if (event.pos[0]//40 == self.soldier_blue_clicked._rect.x//40+1
                                    or event.pos[0]//40 == self.soldier_blue_clicked._rect.x//40-1
                                    or event.pos[1]//40 == self.soldier_blue_clicked._rect.y//40+1
                                    or event.pos[1]//40 == self.soldier_blue_clicked._rect.y//40-1) and not (event.pos[0]//40 != self.soldier_blue_clicked._rect.x//40 and event.pos[1]//40 != self.soldier_blue_clicked._rect.y//40):


                                self.soldier_blue = Soldier_blue((event.pos[0]//40)*40, (event.pos[1]//40)*40)
                                self.soldier_blue.move_left -= 1
                                self.objects.append(self.soldier_blue)
                                self.objects.remove(self.soldier_blue_clicked)
                                self.move_soldier = False

                    elif self.is_move_button_clicked:
                        self.soldier_blue = Soldier_blue((event.pos[0] // 40) * 40, (event.pos[1] // 40) * 40)
                        self.objects.remove(self.bg_for_buttons)
                        self.objects.remove(self.move_button)
                        self.objects.remove(self.attack_button)
                        self.objects.remove(self.capture_button)
                        self.objects.remove(self.move_button_clicked)
                        self.soldier_buttons = False
                        self.counter = False
                        self.is_move_button_clicked = False
                        self.move_soldier = True
                    elif self.is_attack_button_clicked:
                        self.objects.remove(self.bg_for_buttons)
                        self.objects.remove(self.move_button)
                        self.objects.remove(self.attack_button)
                        self.objects.remove(self.capture_button)
                        self.objects.remove(self.attack_button_clicked)
                        self.soldier_buttons = False
                        self.is_attack_button_clicked = False
                        self.attack_soldier = True
                    elif self.is_capture_button_clicked:
                        self.objects.remove(self.bg_for_buttons)
                        self.objects.remove(self.move_button)
                        self.objects.remove(self.attack_button)
                        self.objects.remove(self.capture_button)
                        self.objects.remove(self.capture_button_clicked)
                        self.soldier_buttons = False
                        self.is_capture_button_clicked = False
                        self.capture_soldier = True
                    elif self.attack_soldier:
                        if not (event.pos[0]//40 > self.soldier_blue_clicked._rect.x//40+1
                                    or event.pos[0]//40 < self.soldier_blue_clicked._rect.x//40-1
                                    or event.pos[1]//40 > self.soldier_blue_clicked._rect.y//40+1
                                    or event.pos[1]//40 < self.soldier_blue_clicked._rect.y//40-1) and not (event.pos[0]//40 != self.soldier_blue_clicked._rect.x//40 and event.pos[1]//40 != self.soldier_blue_clicked._rect.y//40):
                            for i in self.objects:
                                if i.type() == 'factory' and i.color() == 'red' and i.collidepoint(event.pos[0], event.pos[1]):
                                    self.objects.remove(i)
                                    self.income_red -= 6
                                    break
                            self.soldier_blue = Soldier_blue(self.soldier_blue_clicked._rect.x, self.soldier_blue_clicked._rect.y)
                            self.soldier_blue.move_left -= 1
                            self.objects.append(self.soldier_blue)
                            self.objects.remove(self.soldier_blue_clicked)
                            self.attack_soldier = False
                            self.counter = False
                    elif self.capture_soldier:
                        if not (event.pos[0] // 40 > self.soldier_blue_clicked._rect.x // 40 + 1
                                or event.pos[0] // 40 < self.soldier_blue_clicked._rect.x // 40 - 1
                                or event.pos[1] // 40 > self.soldier_blue_clicked._rect.y // 40 + 1
                                or event.pos[1] // 40 < self.soldier_blue_clicked._rect.y // 40 - 1) and not (
                                event.pos[0] // 40 != self.soldier_blue_clicked._rect.x // 40 and event.pos[1] // 40 != self.soldier_blue_clicked._rect.y // 40):
                            for i in self.objects:
                                if i.type() != 'textobject' and i.collidepoint(event.pos[0], event.pos[1]):
                                    if i == 'fieldsquare' and i.color() == 'red':
                                        self.income_red -= 1
                                        break
                            self.fieldsquare_blue = Fieldsquare_blue(event.pos[0]//40*40, event.pos[1]//40*40)
                            self.objects.append(self.fieldsquare_blue)
                            self.soldier_blue = Soldier_blue(self.soldier_blue_clicked._rect.x, self.soldier_blue_clicked._rect.y)
                            self.soldier_blue.move_left -= 1
                            self.objects.append(self.soldier_blue)
                            self.objects.remove(self.soldier_blue_clicked)
                            self.income_blue += 1
                            self.capture_soldier = False
                            self.counter = False

                else:  # ход красных
                    if self.capital_red.collidepoint(event.pos[0], event.pos[1]) and not self.capital_buttons and not self.spawn_factory and not self.spawn_soldier and not self.soldier_buttons:
                        self.capital_buttons = True
                        self.objects.append(self.bg_for_buttons)
                        self.objects.append(self.spawn_soldier_button)
                        self.objects.append(self.spawn_factory_button)
                        self.objects.append(self.capital_clicked_red)
                    elif self.capital_buttons and self.spawn_soldier_button_clicked.collidepoint(event.pos[0], event.pos[1]) and not self.soldier_buttons:
                        self.objects.remove(self.bg_for_buttons)
                        self.objects.remove(self.spawn_soldier_button)
                        self.objects.remove(self.spawn_soldier_button_clicked)
                        self.objects.remove(self.spawn_factory_button)
                        self.capital_buttons = False
                        self.spawn_soldier = True
                        self.is_spawn_soldier_button_clicked = False
                    elif self.capital_buttons and self.spawn_factory_button_clicked.collidepoint(event.pos[0], event.pos[1]) and not self.soldier_buttons:
                        self.objects.remove(self.bg_for_buttons)
                        self.objects.remove(self.spawn_soldier_button)
                        self.objects.remove(self.spawn_factory_button)
                        self.objects.remove(self.spawn_factory_button_clicked)
                        self.capital_buttons = False
                        self.spawn_factory = True
                        self.is_spawn_factory_button_clicked = False

                    elif self.spawn_soldier and self.balance_red >= 10:
                        for j in self.objects:
                            if j.type() == 'fieldsquare' and j.collidepoint(event.pos[0], event.pos[1]) and j.color() == 'red':
                                for i in self.objects:
                                    if (i.type() == 'factory' or i.type() == 'capital') and i.color() == 'red' and ((j._rect.x//40+1 == i._rect.x//40 and j._rect.y//40 == i._rect.y//40) or (j._rect.x//40-1 == i._rect.x//40 and j._rect.y//40 == i._rect.y//40) or (j._rect.x//40 == i._rect.x//40 and j._rect.y//40+1 == i._rect.y//40) or (j._rect.x//40 == i._rect.x//40 and j._rect.y//40-1 == i._rect.y//40)):
                                        print(1)
                                        self.soldier_red = Soldier_red((event.pos[0] // 40) * 40, (event.pos[1] // 40) * 40)
                                        self.objects.append(self.soldier_red)
                                        self.spawn_soldier = False
                                        self.balance_red -= 10
                                        self.objects.remove(self.capital_clicked_red)
                                        break

                    elif self.spawn_factory and self.balance_red >= 12:
                        for i in self.objects:
                            if i.type() == 'fieldsquare' and i.collidepoint(event.pos[0], event.pos[1]) and i.color() == 'red':
                                self.objects.remove(self.capital_clicked_red)
                                self.factory_red = Factory_red((event.pos[0] // 40) * 40, (event.pos[1] // 40) * 40)
                                self.objects.append(self.factory_red)
                                self.spawn_factory = False
                                self.balance_red -= 12
                                self.income_red += 6

                    elif self.counter == False:
                        for i in self.objects:
                            if i.type() == 'soldier' and i.collidepoint(event.pos[0], event.pos[1]) and i.color() == 'red' and i.move_left == 1:
                                self.remover = i
                                self.counter = True
                        if self.counter == True:
                            self.soldier_red_clicked = Soldier_red_clicked((event.pos[0]//40)*40, (event.pos[1]//40)*40)
                            self.objects.append(self.soldier_red_clicked)
                            self.objects.remove(self.remover)
                            self.objects.append(self.bg_for_buttons)
                            self.objects.append(self.move_button)
                            self.objects.append(self.attack_button)
                            self.objects.append(self.capture_button)
                            self.soldier_buttons = True
                        elif self.move_soldier:
                            if (event.pos[0]//40 == self.soldier_red_clicked._rect.x//40+1
                                    or event.pos[0]//40 == self.soldier_red_clicked._rect.x//40-1
                                    or event.pos[1]//40 == self.soldier_red_clicked._rect.y//40+1
                                    or event.pos[1]//40 == self.soldier_red_clicked._rect.y//40-1) and not (event.pos[0]//40 != self.soldier_red_clicked._rect.x//40 and event.pos[1]//40 != self.soldier_red_clicked._rect.y//40):


                                self.soldier_red = Soldier_red((event.pos[0]//40)*40, (event.pos[1]//40)*40)
                                self.soldier_red.move_left -= 1
                                self.objects.append(self.soldier_red)
                                self.objects.remove(self.soldier_red_clicked)
                                self.move_soldier = False

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
                        self.move_soldier = True
                    elif self.is_attack_button_clicked:
                        self.objects.remove(self.bg_for_buttons)
                        self.objects.remove(self.move_button)
                        self.objects.remove(self.attack_button)
                        self.objects.remove(self.capture_button)
                        self.objects.remove(self.attack_button_clicked)
                        self.soldier_buttons = False
                        self.is_attack_button_clicked = False
                        self.attack_soldier = True
                    elif self.is_capture_button_clicked:
                        self.objects.remove(self.bg_for_buttons)
                        self.objects.remove(self.move_button)
                        self.objects.remove(self.attack_button)
                        self.objects.remove(self.capture_button)
                        self.objects.remove(self.capture_button_clicked)
                        self.soldier_buttons = False
                        self.is_capture_button_clicked = False
                        self.capture_soldier = True
                    elif self.attack_soldier:
                        if not (event.pos[0]//40 > self.soldier_red_clicked._rect.x//40+1
                                    or event.pos[0]//40 < self.soldier_red_clicked._rect.x//40-1
                                    or event.pos[1]//40 > self.soldier_red_clicked._rect.y//40+1
                                    or event.pos[1]//40 < self.soldier_red_clicked._rect.y//40-1) and not (event.pos[0]//40 != self.soldier_red_clicked._rect.x//40 and event.pos[1]//40 != self.soldier_red_clicked._rect.y//40):
                            for i in self.objects:
                                if i.type() != 'textobject' and i.color() == 'blue' and i.collidepoint(event.pos[0], event.pos[1]):
                                    self.objects.remove(i)
                            self.soldier_red = Soldier_red(self.soldier_red_clicked._rect.x, self.soldier_red_clicked._rect.y)
                            self.objects.append(self.soldier_red)
                            self.soldier_red.move_left -= 1
                            self.objects.remove(self.soldier_red_clicked)
                            self.attack_soldier = False
                            self.counter = False
                    elif self.capture_soldier:
                        if not (event.pos[0] // 40 > self.soldier_red_clicked._rect.x // 40 + 1
                                or event.pos[0] // 40 < self.soldier_red_clicked._rect.x // 40 - 1
                                or event.pos[1] // 40 > self.soldier_red_clicked._rect.y // 40 + 1
                                or event.pos[1] // 40 < self.soldier_red_clicked._rect.y // 40 - 1) and not (
                                event.pos[0] // 40 != self.soldier_red_clicked._rect.x // 40 and event.pos[1] // 40 != self.soldier_red_clicked._rect.y // 40):
                            self.fieldsquare_red = Fieldsquare_red(event.pos[0]//40*40, event.pos[1]//40*40)
                            self.objects.append(self.fieldsquare_red)
                            self.soldier_red = Soldier_red(self.soldier_red_clicked._rect.x, self.soldier_red_clicked._rect.y)
                            self.soldier_red.move_left -= 1
                            self.objects.append(self.soldier_red)
                            self.objects.remove(self.soldier_red_clicked)
                            self.income_red += 1
                            self.capture_soldier = False
                            self.counter = False


    def draw(self):
        for o in self.objects:
            o.draw(self.surface)


    def run(self):
        while 1:
       # while not self.next_turn:
            self.surface.blit(self.background_image, (0, 0))
            self.surface.blit(self.gamesquare_image, (200, 200))
            for y in range(0, 599, 40):
                for x in range(0, 799, 40):
                    self.surface.blit(self.gamesquare_image, (x, y))

            self.surface.blit(self.capital_image, (0, 280))
            self.surface.blit(self.capital_image, (760, 280))


            self.handle_events()
            # self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(self.frame_rate)