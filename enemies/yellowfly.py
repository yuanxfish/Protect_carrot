import pygame
import os
from .enemy import Enemy


class YellowFly(Enemy):
    imgs = [pygame.image.load(os.path.join("game_assets/enemies/1", str(x) + "_run.png")) for x in range(3)]

    def __init__(self):
        super().__init__()
        self.name = "yellowfly"
        self.money = 3
        self.max_health = 3
        self.health = self.max_health
