from game import Game
import pygame
import os

start_btn = pygame.image.load(os.path.join("game_assets", "start_button.png"))

class MainScreen:
    def __init__(self):
        self.width = 920
        self.height = 460
        self.bg = pygame.image.load(os.path.join("game_assets", "BG1.png"))
        self.win = pygame.display.set_mode((self.width, self.height))
        self.btn = (460 - start_btn.get_width()/2, 230- start_btn.get_height()/2,start_btn.get_width(),start_btn.get_height())

    def run(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()

                    if self.btn[0] <= x <= self.btn[0] + self.btn[2]:
                        if self.btn[1] <= y <= self.btn[1] + self.btn[3]:
                            game = Game(self.win)
                            game.run()
            self.draw()

        pygame.quit()

    def draw(self):
        self.win.blit(self.bg, (0, 0))
        self.win.blit(start_btn,(self.btn[0], self.btn[1]))
        pygame.display.update()
