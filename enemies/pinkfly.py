import pygame
import os
from .enemy import Enemy


class PinkFly(Enemy):
    imgs = [pygame.image.load(os.path.join("game_assets/enemies/2", str(x) + "_run.png")) for x in range(3)]

    def __init__(self):
        super().__init__()
        self.name = "pinkfly"
        self.money = 7
        self.max_health = 5
        self.health = self.max_health
