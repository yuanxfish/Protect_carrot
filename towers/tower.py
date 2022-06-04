import math
import pygame.draw
import time
import os
from menu.menu import Menu
import math

menu_bg = pygame.image.load(os.path.join("game_assets","menu1.png"))
upgrade_btn= pygame.image.load(os.path.join("game_assets","upgrade.png"))


class Tower:
    tower_imgs = []

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.sell_price = [0, 0, 0]
        self.price = [0, 0, 0]
        self.level = 1
        self.selected = False
        self.menu = Menu(self, self.x, self.y, menu_bg, [220, 260, "MAX"])
        self.menu.add_btn(upgrade_btn, "Upgrade")
        self.tower_count = 0
        self.tower_img = None
        self.range = 100
        self.inRange = False
        self.left = True
        self.timer = time.time()
        self.damage = 1
        self.moving = False
        self.place_color = (0, 0, 255, 100)

    def draw_radius(self, win):
        """画可攻击范围"""
        if self.selected:
            surface = pygame.Surface((self.range * 4, self.range * 4), pygame.SRCALPHA, 32)
            pygame.draw.circle(surface, (193, 210, 240, 100), (self.range, self.range), self.range, 0)
            win.blit(surface, (self.x - self.range, self.y - self.range))

    def draw_placement(self, win):

        surface = pygame.Surface((self.range * 4, self.range * 4), pygame.SRCALPHA, 32)
        pygame.draw.circle(surface, self.place_color, (30, 30), 30, 0)
        win.blit(surface, (self.x - 30, self.y- 30))

    def draw(self, win):
        """画固定炮塔和移动炮塔"""

        if self.inRange and not self.moving:
            self.tower_count += 1
            if self.tower_count >= len(self.tower_imgs) :
                self.tower_count = 0
        else:
            self.tower_count = 0

        self.tower_img = self.tower_imgs[self.tower_count ]
        win.blit(self.tower_img, ((self.x + self.width / 2 ) - (self.tower_img.get_width() / 2), (self.y  + self.height /2)- (self.tower_img.get_height()/2)))

        if self.selected:
            self.menu.draw(win)



    def change_range(self, r):
        self.range = r

    def attack(self, enemies):
        money = 0

        self.inRange = False
        enemy_closest = []

        for enemy in enemies:
            x = enemy.x
            y = enemy.y

            dis = math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
            if dis < self.range:
                self.inRange = True
                enemy_closest.append(enemy)
        enemy_closest.sort(key=lambda x: x.path_pos)
        enemy_closest = enemy_closest[ : : -1]
        if len(enemy_closest) > 0:
            first_enemy = enemy_closest[0]
            if time.time() - self.timer >= 0:
                self.timer = time.time()
                if first_enemy.hit(self.damage) == True:
                    money = first_enemy.money
                    enemies.remove(first_enemy)


            if first_enemy.x < self.x and not (self.left):
                self.left = True
                for x, img in enumerate(self.tower_imgs):
                    self.tower_imgs[x] = pygame.transform.flip(img, True, False)

            elif self.left and first_enemy.x > self.x:
                self.left = False
                for x, img in enumerate(self.tower_imgs):
                    self.tower_imgs[x] = pygame.transform.flip(img, True, False)

        return money


    def click(self,  X, Y):
        if X <= self.x + self.width  + self.tower_img.get_width() and X >= self.x + self.width -self.tower_img.get_width() :
            if Y <= self.y + self.height + self.tower_img.get_height()  and Y >= self.y + self.height - self.tower_img.get_height():
                return True

        return False

    def sell(self):
        return self.sell_price[self.level-1]

    def upgrade(self):

        if self.level < len(self.tower_imgs) :
            self.level += 1
            self.damage += 1

    def get_upgrade_cost(self):
        return self.price[self.level-1]

    def move(self, x, y):
        self.x = x
        self.y = y
        self.menu.x = x
        self.menu.y = y
        self.menu.update()

    def collide(self, otherTower):
        x2 = otherTower.x
        y2 = otherTower.y

        dis = math.sqrt((x2 - self.x) ** 2 + (y2 - self.y) ** 2)
        if dis >= 50:
            return False
        else:
            return True

