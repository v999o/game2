import os
import pygame
from pygame.rect import Rect
from game import Game
import colors
import config as c

class Breakout(Game):
    def __init__(self):
        Game.__init__(self, 'Game 2', c.screen_width, c.screen_height, c.background_image, c.gamesquare_image, c.capital_image, c.soldier_image, c.fieldsquare_red_image, c.fieldsquare_blue_image, c.frame_rate)
        self.screen = Rect(0, 0, c.screen_width, c.screen_height)



def main():
    Breakout().run()


if __name__ == '__main__':
    main()
