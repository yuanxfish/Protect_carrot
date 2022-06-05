import os.path
import pygame
import os
from enemies.yellowfly import YellowFly
from enemies.pinkfly import PinkFly
from enemies.greenfly import GreenFly
from enemies.boss import Boss
from towers.tstar import TStar
from towers.tblue import TBlue
from towers.tgreen import TGreen
import time
import random
from menu.menu import MainMenu,PlayPauseButton
pygame.font.init()
pygame.init()
pygame.display.set_caption('Carrot_Fantasy')

lives_img = pygame.image.load(os.path.join("game_assets", "heart.png"))
main_img = pygame.image.load(os.path.join("game_assets", "menu.png"))
tstar_img = pygame.image.load(os.path.join("game_assets", "tstar.png"))
tgreen_img = pygame.image.load(os.path.join("game_assets", "tgreen.png"))
tblue_img = pygame.image.load(os.path.join("game_assets", "tblue.png"))

play_btn = pygame.image.load(os.path.join("game_assets", "button_play.png"))
pause_btn = pygame.image.load(os.path.join("game_assets", "button_pause.png"))
sound_btn = pygame.image.load(os.path.join("game_assets","sound_button.png"))
sound_off_btn = pygame.image.load(os.path.join("game_assets","sound_off_button.png"))

tower_names = ["tstar", "tblue", "tgreen"]

pygame.mixer.music.load(os.path.join("game_assets", "BGMusic.mp3"))
# 每一波四种怪物数量
waves = [
    [10, 5, 0],
    [15, 10, 0],
    [20, 15, 0],
    [25, 20, 0],
    [25, 20, 5, 1],
    [25, 20, 10],
    [25, 20, 15],
    [25, 25, 10],
    [25, 25, 15],
    [25, 25, 20, 3],
    [25, 25, 25],
    [30, 25, 20],
    [30, 30, 20],
    [30, 30, 25],
    [35, 30, 25, 5],
]

class Game:
    def __init__(self, win):
        self.width = 920
        self.height = 460
        self.win  = win
        self.enemys = []
        self.towers = []
        self.lives = 10
        self.money = 550
        self.bg = pygame.image.load(os.path.join("game_assets", "BG.png"))
        self.map01 = pygame.image.load(os.path.join("game_assets", "MAP1.png"))
        self.home = pygame.image.load(os.path.join("game_assets", "home.png"))
        self.carrot = pygame.image.load(os.path.join("game_assets", "carrot.png"))
        self.upmenu = pygame.image.load(os.path.join("game_assets", "upmenu.png"))
        self.timer = time.time()
        self.life_font = pygame.font.Font("WORLDOFW.TTF", 16)
        self.money_font = pygame.font.Font("WORLDOFW.TTF", 20)
        self.wave_font = pygame.font.Font("WORLDOFW.TTF", 27)
        self.selected_tower = None
        self.menu = MainMenu(self.width - main_img.get_width() + 40, 530, main_img)
        self.menu.add_btn(tstar_img, "tstar_img", 160)
        self.menu.add_btn(tgreen_img, "tgreen_img", 160)
        self.menu.add_btn(tblue_img, "tblue_img", 180)
        self.moving_object = None
        self.wave = 4
        self.current_wave = waves[self.wave][:]
        self.pause = True
        self.music_on = True
        self.playPauseButton = PlayPauseButton(play_btn, pause_btn, 600, 5)
        self.soundButton = PlayPauseButton(sound_btn, sound_off_btn, 640, 3)

    def gen_enemies(self):
        """生成下一波怪物"""

        if sum(self.current_wave) == 0:
            if len(self.enemys) == 0:
                self.wave += 1
                self.current_wave = waves[self.wave]
                self.pause = True
                self.playPauseButton.paused = self.pause
        else:
            wave_enemies = [YellowFly(), PinkFly(), GreenFly(), Boss()]
            for x in range(len(self.current_wave)):
                if self.current_wave[x] != 0:
                    self.enemys.append(wave_enemies[x])
                    self.current_wave[x] = self.current_wave[x] - 1
                    break

    def run(self):
        pygame.mixer.music.play(-1)
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(2)
            if self.pause == False:
                if time.time() - self.timer >= random.randrange(1, 10) / 3:
                    self.timer = time.time()
                    self.gen_enemies()

            pos = pygame.mouse.get_pos()

            if self.moving_object:
                self.moving_object.move(pos[0], pos[1])
                tower_list = self.towers[:]
                collide = False
                for tower in tower_list:
                    if tower.collide(self.moving_object):
                        collide = True
                        tower.place_color = (255, 0, 0, 100)
                        self.moving_object.place_color = (255, 0, 0, 100)
                    else:
                        tower.place_color = (0, 0, 255, 100)
                        if not collide:
                            self.moving_object.place_color = (0, 0, 255, 100)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONUP:

                    if self.moving_object:
                        not_allowed = False
                        tower_list = self.towers[:]
                        for tower in tower_list:
                            if tower.collide(self.moving_object)  :
                                not_allowed = True

                        if not not_allowed and self.point_to_line(self.moving_object):
                            if self.moving_object.name in tower_names:
                                self.towers.append(self.moving_object)
                            self.moving_object.moving = False
                            self.moving_object = None

                    else:
                        """控制游戏暂停继续"""
                        if self.playPauseButton.click(pos[0], pos[1]):
                            self.pause = not (self.pause)
                            self.playPauseButton.paused = self.pause

                        """控制音乐暂停继续"""
                        if self.soundButton.click(pos[0], pos[1]):
                            self.music_on = not (self.music_on)
                            self.soundButton.paused = self.music_on
                            if self.music_on:
                                pygame.mixer.music.unpause()
                            else:
                                pygame.mixer.music.pause()

                        """点击购买炮塔"""
                        mainmenu_button = self.menu.get_clicked(pos[0], pos[1])
                        if mainmenu_button:
                            cost = self.menu.get_item_cost(mainmenu_button)
                            if self.money >= cost:
                                self.money -= cost
                                self.add_tower(mainmenu_button)

                        """点击炮塔升级"""
                        btn_clicked = None
                        if self.selected_tower:
                            btn_clicked = self.selected_tower.menu.get_clicked(pos[0], pos[1])
                            if btn_clicked:
                                if btn_clicked == "Upgrade":
                                    cost = self.selected_tower.get_upgrade_cost()
                                    if self.money >= cost:
                                        self.money -= cost
                                        self.selected_tower.upgrade()
                        if not (btn_clicked):
                            for tw in self.towers:
                                if tw.click(pos[0], pos[1]):
                                    tw.selected = True
                                    self.selected_tower = tw
                                else:
                                    tw.selected = False
            if not self.pause:
                to_del = []

                for en in self.enemys:
                    en.move()
                    if en.y <= 78:
                        to_del.append(en)
                for d in to_del:
                    self.lives -= 1
                    self.enemys.remove(d)

                for tw in self.towers:
                    self.money += tw.attack(self.enemys)

                if self.lives <= 0:
                    print("You Lose")
                    run = False

            self.draw()

        pygame.quit()

    def point_to_line(self,tower):

        return True

    def draw(self):
        self.win.blit(self.bg, (0, 0))
        self.win.blit(self.map01, (0, 0))
        self.win.blit(self.home, (88, 28))
        self.win.blit(self.carrot, (818, 8))
        self.win.blit(self.upmenu, (250, 0))
        if self.moving_object:
            for tower in self.towers:
                tower.draw_placement(self.win)

            self.moving_object.draw_placement(self.win)

        """画炮塔"""
        for tw in self.towers:
            tw.draw(self.win)
        """画怪物"""
        for en in self.enemys:
            en.draw(self.win)

        if self.selected_tower:
            self.selected_tower.draw(self.win)

        """画移动炮塔"""
        if self.moving_object:
            self.moving_object.draw(self.win)



        self.menu.draw(self.win)

        self.playPauseButton.draw(self.win)
        self.soundButton.draw(self.win)

        """画出生命点"""
        text = self.life_font.render(str(self.lives), 1, (255, 255, 255))
        life = lives_img
        self.win.blit(life, (855, 32))
        self.win.blit(text, (878, 37))
        pygame.display.update()

        """画金币"""
        text = self.money_font.render(str(self.money), 1, (255, 255, 255))
        self.win.blit(text, (300, 7))
        pygame.display.update()

        """画波数"""
        text = self.wave_font.render("Wave  " + str(self.wave + 1), 1, (255, 255, 255))
        self.win.blit(text, (400, 4))
        pygame.display.update()

    def add_tower(self, name):
        x, y = pygame.mouse.get_pos()
        name_list = ["tstar_img", "tblue_img", "tgreen_img"]
        object_list = [TStar(x, y), TBlue(x, y), TGreen(x, y)]

        try:
            obj = object_list[name_list.index(name)]
            self.moving_object = obj
            obj.moving = True

        except Exception as e:
            print(str(e) + "NOT VALID NAME")
