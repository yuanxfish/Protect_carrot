import pygame
import os

pygame.font.init()
gold = pygame.image.load(os.path.join("game_assets", "Gold.png"))


class Button:
    def __init__(self, menu, img, name):
        self.name = name
        self.img = img
        self.x = menu.x - 35
        self.y = menu.y - 55
        self.menu = menu
        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def click(self, X, Y):
        """如果位置与菜单碰撞则返回"""
        if X <= self.x + self.width and X >= self.x:
            if Y <= self.y + self.height and Y >= self.y:
                return True
        return False

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def update(self):
        self.x = self.menu.x - 35
        self.y = self.menu.y - 55


class PlayPauseButton(Button):
    def __init__(self, play_img, pause_img, x, y):
        self.img = play_img
        self.play = play_img
        self.pause = pause_img
        self.x = x
        self.y = y
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.paused = True

    def draw(self, win):
        if self.paused:
            win.blit(self.play, (self.x, self.y))
        else:
            win.blit(self.pause, (self.x, self.y))


class MainButton(Button):
    def __init__(self, x, y, img, name, cost):
        self.name = name
        self.img = img
        self.x = x
        self.y = y
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.cost = cost


class Menu:
    """炮塔升级菜单"""

    def __init__(self, tower, x, y, img, item_cost):
        self.x = x
        self.y = y
        self.width = img.get_width()
        self.height = img.get_height()
        self.item_cost = item_cost
        self.buttons = []
        self.items = 0
        self.bg = img
        self.font = pygame.font.Font("WORLDOFW.TTF", 14)
        self.tower = tower

    def add_btn(self, img, name):
        self.items += 1
        self.buttons.append(Button(self, img, name))

    def get_item_cost(self):
        """升级花费"""
        return self.item_cost[self.tower.level - 1]

    def draw(self, win):
        """画炮塔升级按钮和升级花费金币"""
        win.blit(self.bg, (self.x - self.bg.get_width() / 2, self.y - self.bg.get_height() * 1.5))
        for item in self.buttons:
            item.draw(win)
            win.blit(gold, (item.x + item.width + 13, item.y))
            text = self.font.render(str(self.item_cost[self.tower.level - 1]), 1, (255, 255, 255))
            win.blit(text, (item.x + item.width + 17, item.y + gold.get_height()))

    def get_clicked(self, X, Y):
        """返回选中物品"""
        for btn in self.buttons:
            if btn.click(X, Y):
                return btn.name

        return None

    def update(self):
        """更新炮塔位置"""
        for btn in self.buttons:
            btn.update()


class MainMenu(Menu):
    """炮塔选择菜单"""

    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.width = img.get_width()
        self.height = img.get_height()
        self.buttons = []
        self.items = 0
        self.bg = img
        self.font = pygame.font.Font("WORLDOFW.TTF", 14)

    def add_btn(self, img, name, cost):
        """炮塔在选择菜单位置"""
        self.items += 1
        btn_x = self.x - (self.items) * 135 + 230
        btn_y = self.y - 140
        self.buttons.append(MainButton(btn_x, btn_y, img, name, cost))

    def get_item_cost(self, name):
        """购买炮塔花销"""
        for btn in self.buttons:
            if btn.name == name:
                return btn.cost
        return -1

    def draw(self, win):
        """画菜单上的炮塔"""
        win.blit(self.bg, (self.x - self.bg.get_width() / 2, self.y - self.bg.get_height() * 1.5))
        for item in self.buttons:
            item.draw(win)
