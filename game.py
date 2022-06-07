import pygame
from pygame.locals import *
import config as c
import sys
from text_object import TextObject
from button import Button
from soldier import Soldier_blue
from soldier import Soldier_blue_clicked
from soldier import Soldier_red
from soldier import Soldier_red_clicked
from bgforbuttons import Bg_for_button
from bgforbuttons import Move_button
from bgforbuttons import Move_button_clicked
from collections import defaultdict

class Game:
    def __init__(self, caption, width, height, back_image_filename, gamesquare_image_filename, capital_image_filename, soldier_image_filename, frame_rate):
        self.background_image = pygame.image.load(back_image_filename)
        self.gamesquare_image = pygame.image.load(gamesquare_image_filename)
        self.capital_image = pygame.image.load(capital_image_filename)
        self.soldier_image = pygame.image.load(soldier_image_filename)
        self.frame_rate = frame_rate
        self.next_turn = False
        self.objects = []
        self.pause = True
        self.counter = False
        self.remover = None
        self.buttons = False
        self.buttons_clicked = False
        pygame.mixer.init(44100, -16, 2, 4096)
        pygame.init()
        pygame.font.init()
        # self.surface = pygame.display.set_mode((width, height), FULLSCREEN)
        self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.mouse_handlers = []

    def handle_events(self):
        if self.buttons == True:
            if pygame.mouse.get_pos()[0] > 80 and pygame.mouse.get_pos()[0] < 160 and pygame.mouse.get_pos()[1] > 480 and pygame.mouse.get_pos()[1] < 560 and not self.buttons_clicked:
                self.move_button_clicked = Move_button_clicked(80, 480)
                self.objects.append(self.move_button_clicked)
                self.buttons_clicked = True
            elif (pygame.mouse.get_pos()[0] < 80 or pygame.mouse.get_pos()[0] > 160 or pygame.mouse.get_pos()[1] < 480 or pygame.mouse.get_pos()[1] > 560) and self.buttons_clicked:
                self.objects.remove(self.move_button_clicked)
                self.buttons_clicked = False

        def intersect(m, s):
            return m.left < s.right and m.right > s.left and m.top < s.bottom and m.bottom > s.top
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if not self.next_turn:
                    self.next_turn = True
                else:
                    self.next_turn = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.next_turn:
                    if self.counter == False:
                        for i in self.objects:
                            if i.collidepoint(event.pos[0], event.pos[1]):
                                self.remover = i
                                self.counter = True
                        if self.counter == True:
                            self.soldier_clicked = Soldier_blue_clicked((event.pos[0]//40)*40, (event.pos[1]//40)*40)
                            self.objects.append(self.soldier_clicked)
                            self.objects.remove(self.remover)
                        else:
                            self.soldier = Soldier_blue((event.pos[0]//40)*40, (event.pos[1]//40)*40)
                            self.objects.append(self.soldier)
                    else:
                        self.soldier = Soldier_blue((event.pos[0] // 40) * 40, (event.pos[1] // 40) * 40)
                        self.objects.append(self.soldier)
                        self.objects.remove(self.soldier_clicked)
                        self.counter = False

                else:
                    if self.counter == False:
                        for i in self.objects:
                            if i.collidepoint(event.pos[0], event.pos[1]):
                                self.remover = i
                                self.counter = True
                        if self.counter == True:
                            self.soldier_clicked = Soldier_red_clicked((event.pos[0]//40)*40, (event.pos[1]//40)*40)
                            self.objects.append(self.soldier_clicked)
                            self.objects.remove(self.remover)
                            self.bg_for_buttons = Bg_for_button(0, 440)
                            self.move_button = Move_button(80, 480)
                            self.objects.append(self.bg_for_buttons)
                            self.objects.append(self.move_button)
                            self.buttons = True
                        else:
                            self.soldier = Soldier_red((event.pos[0]//40)*40, (event.pos[1]//40)*40)
                            self.objects.append(self.soldier)
                    else:
                        self.soldier = Soldier_red((event.pos[0] // 40) * 40, (event.pos[1] // 40) * 40)
                        self.objects.append(self.soldier)
                        self.objects.remove(self.soldier_clicked)
                        self.objects.remove(self.bg_for_buttons)
                        self.objects.remove(self.move_button)
                        self.counter = False

                '''if c == 1:
                    self.soldier = Soldier((event.pos[0] // 40) * 40, (event.pos[1] // 40) * 40)
                    self.objects.append(self.soldier)
                    self.objects.remove(self.soldier_clicked)
                    c = 0'''

    '''def update(self):
        for o in self.objects:
            o.update()'''

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
            '''if not self.next_turn:
                self.surface.blit(self.soldier_image, (40, 280))
            else:
                self.surface.blit(self.soldier_image, (720, 280))
'''


            self.handle_events()
            # self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(self.frame_rate)