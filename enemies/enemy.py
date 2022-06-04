import pygame
import math


class Enemy:
    imgs = []

    def __init__(self):
        self.width = 64
        self.height = 64
        self.animation_count = 0
        self.health = 1
        self.vel = 3
        self.path = [(83, 50), (83, 100), (83, 170), (83, 233), (159, 233), (240, 233), (300, 233),
                     (300, 200), (300, 170), (405, 170), (510, 170),(550, 170), (550, 200), (550, 233), (630, 233),
                     (730, 233),(780, 233),(780, 151), (780, 50), (-10000,50)]
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.img = None
        self.dis = 0
        self.path_pos = 0
        self.move_dis = 0
        self.max_health = 0
        self.speed_increase = 2


    def draw(self, win):
        self.animation_count += 1
        self.img = self.imgs[self.animation_count//100]
        win.blit(self.img, (self.x, self.y))
        self.draw_health_bar(win)

    def draw_health_bar(self, win):
        length = 30
        move_by = length / self.max_health
        health_bar = move_by * self.health

        pygame.draw.rect(win, (255, 0, 0), (self.x + 10, self.y - 10, length, 5), 0)
        pygame.draw.rect(win, (0, 255, 0), (self.x + 10, self.y - 10, health_bar, 5), 0)

    def collide(self, X, Y):

        if X <= self.x + self.width and X >= self.x:
            if Y <= self.y + self.health and Y >=self.y:
                return True

        return False

    def move(self):

        self.animation_count += 1
        if self.animation_count >= len(self.imgs * 100):
            self.animation_count = 0

        x1, y1 = self.path[self.path_pos]
        if self.path_pos + 1 >= len(self.path):
            x2, y2 = (1000, 47)
        else:
            x2, y2 = self.path[self.path_pos + 1]

        move_dis = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        dirn = ((x2-x1)/3 * self.speed_increase, (y2-y1)/3 * self.speed_increase)

        move_x, move_y = (self.x +dirn[0] , self.y + dirn[1] )
        self.dis += math.sqrt((move_x - x1) ** 2 + (move_y - y1) ** 2)

        if self.dis >= move_dis:
            self.dis = 0
            self.path_pos += 1
            if self.path_pos >= len(self.path):
                return False

        self.x = move_x
        self.y = move_y
        return True

    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            return True
        return False