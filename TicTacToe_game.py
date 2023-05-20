import os
import sys
import random

import numpy as np

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from pygame import mixer
from pygame.locals import *

from TicTacToe_alpha_beta import alpha_ai

white = (255, 255, 255)
black = (30, 30, 30)

class TicGame:
    def __init__(self, seed=0, board_size=3, silent_mode=True):
        # 绘制棋盘
        self.space = 60  # 四周留下的边距
        self.cell_size = 40  # 每个格子大小
        self.draw_cells_num = 4
        self.grid_size = self.cell_size * (self.draw_cells_num - 1) + self.space * 2  # 棋盘的大小
        if not silent_mode:
            pygame.init()
            self.screen_caption = pygame.display.set_caption('井字棋')
            self.screen = pygame.display.set_mode((self.grid_size, self.grid_size))  # 设置窗口长宽
            # 结果字体与restart按钮
            self.font1 = pygame.font.Font("font/font.ttf", 24)
            self.font2 = pygame.font.Font("font/font.ttf", 20)

        self.font_position = [(55, 0), (85, 200)]
        self.result = 0  # 结果
        self.seed_value = seed
        random.seed(seed) # Set random seed.
        self.cell_num = 3  # 格子数
        self.g_map = np.zeros((self.cell_num, self.cell_num), dtype=np.int8)
        self.reset()

    def reset(self):
        self.g_map = np.zeros((self.cell_num, self.cell_num), dtype=np.int8)
        self.chess = []
        self.player = -1
        self.full = 0
        self.cur_step = 0  # 步数

    def step(self, action):
        # print("action", self.player, action)
        pos_x, pos_y = action
        if 0 <= pos_x <= self.cell_num - 1 and 0 <= pos_y <= self.cell_num - 1:  # 判断能否落子
            if self.g_map[pos_x][pos_y] == 0:
                self.g_map[pos_x][pos_y] = self.player
                self.cur_step += 1
                self.chess.append((pos_x, pos_y, self.player))
                self.player *= -1  # 下次电脑下棋
        info ={
            "map": self.g_map
        }
        return self.game_result(), info

    def _check_action_validity(self, action):
        pos_x = action // 3
        pos_y = action % 3
        if 0 <= pos_x <= self.cell_num - 1 and 0 <= pos_y <= self.cell_num - 1 \
            and self.g_map[pos_x][pos_y] == 0:  # and self.game_result() == 0:
            return True
        return False
    
    # 判断游戏结局。0进行中，1玩家胜，-1电脑胜利，2平局
    def game_result(self):
        # 判断是否横向三子
        count = 0
        for y in range(self.cell_num):
            count = 0
            for x in range(self.cell_num):
                count += self.g_map[x][y]
            if count % 3 == 0 and count != 0:
                return count / 3
        # 判断是否纵向三子
        for x in range(self.cell_num):
            count = 0
            for y in range(self.cell_num):
                count += self.g_map[x][y]
            if count % 3 == 0 and count != 0:
                return count / 3
        # 判断是否左上-右下三子
        count = 0
        count += self.g_map[0][0]+self.g_map[1][1]+self.g_map[2][2]
        if count % 3 == 0 and count != 0:
            return count / 3
        # 判断是否右上-左下三子
        count = 0
        count += self.g_map[0][2] + self.g_map[1][1] + self.g_map[2][0]
        if count % 3 == 0 and count != 0:
            return count / 3
        # 判和
        if not (0 in self.g_map):
            return 2
        return 0

    # 绘制出棋子位置
    def refresh_board(self):
        self.result = self.game_result()
        self.screen.fill((128, 128, 128))  # 将界面设置为蓝色
        # 画边界
        for x in range(0, self.cell_size * self.draw_cells_num, self.cell_size):
            pygame.draw.line(self.screen, (200, 200, 200), (x + self.space, 0 + self.space),
                            (x + self.space, self.cell_size * (self.draw_cells_num - 1) + self.space), 1)
        for y in range(0, self.cell_size * self.draw_cells_num, self.cell_size):
            pygame.draw.line(self.screen, (200, 200, 200), (0 + self.space, y + self.space),
                            (self.cell_size * (self.draw_cells_num - 1) + self.space, y + self.space), 1)
        # 画棋子
        for y, x, player in self.chess:
            piece_location = [int((x + 0.5) * self.cell_size) + self.space, int((0.5 + y) * self.cell_size) + self.space]
            if player == 1:
                pygame.draw.circle(self.screen, white, piece_location, 16, 16)
            else:
                pygame.draw.circle(self.screen, black, piece_location, 16, 16)
        # 判结果人类获胜
        if self.result == 1:
            text = self.font1.render("VICTORY!!", True, white)
            text2 = self.font2.render("RESTART", True, white)
            self.screen.blit(text, (self.font_position[0][0]+10, self.font_position[0][1]))
            self.screen.blit(text2, self.font_position[1])
            self.player = -1  # 下次电脑下棋
        # 判结果电脑获胜
        elif self.result == -1:
            text1 = self.font1.render("GAME OVER!", True, white)
            text2 = self.font2.render("RETRY", True, white)
            self.screen.blit(text1, self.font_position[0])
            self.screen.blit(text2, self.font_position[1])

        elif self.cur_step == 10:
            text1 = self.font1.render("Stalemate!", True, white)
            text2 = self.font2.render("RETRY", True, white)
            self.screen.blit(text1, (self.font_position[0][0]+10, self.font_position[0][1]))
            self.screen.blit(text2, self.font_position[1])
            self.result = 2
    

    def man_move(self):
        """
        人类下棋及控制
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # restart game
            elif event.type == MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                if self.result:
                    if self.font_position[1][0] <= x <= self.font_position[1][0] + 50 and self.font_position[1][1] <= y <= \
                            self.font_position[1][1] + 30:
                        self.reset()
                else:
                    yi = int(round((x - self.space - self.cell_size / 2) * 1.0 / self.cell_size))  # 获取到x方向上取整的序号
                    xi = int(round((y - self.space - self.cell_size / 2) * 1.0 / self.cell_size))  # 获取到y方向上取整的序号
                    _ = self.step([xi, yi])

    def render(self):
        self.screen.fill((0, 0, 0))

        self.man_move()
        self.refresh_board()
        
        pygame.display.flip()


        

if __name__ == "__main__":
    import time

    seed = random.randint(0, 1e9)
    ai = alpha_ai()
    pygame.init()
    game = TicGame(seed=seed, silent_mode=False)
    clock = pygame.time.Clock()
    while True:
        ch = 0
        # 人类下棋
        game.render()
        game.result = game.game_result()
        # if game.result == 0 and game.player==-1:
        #     x, y = ai.ai_move(game.g_map)
        #     print(x, y)
        #     game.step([x, y])
        #     game.player = 1
        # 判断结果
        game.result = game.game_result()
        # 刷新棋盘
        game.refresh_board()
        pygame.display.flip()
        clock.tick(30)
