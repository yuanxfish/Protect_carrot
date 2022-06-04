import pygame
import os
from .enemy import Enemy


class GreenFly(Enemy):
    imgs = [pygame.image.load(os.path.join("game_assets/enemies/3", str(x) + "_run.png")) for x in range(3)]

    def __init__(self):
        super().__init__()
        self.name = "greenfly"
        self.money = 14
        self.max_health = 8
        self.health = self.max_health
