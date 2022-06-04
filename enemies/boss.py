import pygame
import os
from .enemy import Enemy


class Boss(Enemy):
    imgs = [pygame.image.load(os.path.join("game_assets/enemies/boss", str(x) + "_run.png")) for x in range(2)]

    def __init__(self):
        super().__init__()
        self.name = "boss"
        self.money = 140
        self.max_health = 30
        self.health = self.max_health


