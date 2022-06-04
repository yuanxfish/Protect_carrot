import pygame
from .tower import Tower
import os
import math
from menu.menu import Menu

menu_bg = pygame.image.load(os.path.join("game_assets","menu1.png"))
upgrade_btn= pygame.image.load(os.path.join("game_assets","upgrade.png"))
class TStar(Tower):

    tower_imgs = [pygame.image.load(os.path.join("game_assets/towers/1", str(x) + ".png")) for x in range(1, 4)]

    def __init__(self, x, y):
        super().__init__(x, y)
        self.damage = 1

        self.menu = Menu(self, self.x, self.y, menu_bg, [220, 260, "MAX"])
        self.menu.add_btn(upgrade_btn, "Upgrade")

        self.name = "tstar"

    def get_upgrade_cost(self):
        return self.menu.get_item_cost()

    def draw(self, win):
        super().draw_radius(win)
        super().draw(win)

