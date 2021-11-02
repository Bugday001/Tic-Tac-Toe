from TicTacToe_game import TicTacToe
import sys
import pygame
from pygame.locals import *

pygame.init()
# 绘制棋盘
space = 60  # 四周留下的边距
cell_size = 40  # 每个格子大小
cell_num = 4
grid_size = cell_size * (cell_num - 1) + space * 2  # 棋盘的大小
screen_caption = pygame.display.set_caption('井字棋')
screen = pygame.display.set_mode((grid_size, grid_size))  # 设置窗口长宽
# 结果字体与restart按钮
font1 = pygame.font.Font("font/font.ttf", 24)
font2 = pygame.font.Font("font/font.ttf", 20)
font_position = [(55, 0), (85, 200)]
white = (255, 255, 255)
black = (30, 30, 30)
running = True
an = 0  # 结果
ch = 0


# 人类下棋及控制
def man_move():
    global ch, an, g
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # restart game
        elif event.type == MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            if an:
                if font_position[1][0] <= x <= font_position[1][0] + 50 and font_position[1][1] <= y <= \
                        font_position[1][1] + 30:
                    an = 0
                    # 删除原来的数据，重新建立棋盘数据
                    del g
                    g = TicTacToe()
            else:
                xi = int(round((x - space - cell_size / 2) * 1.0 / cell_size))  # 获取到x方向上取整的序号
                yi = int(round((y - space - cell_size / 2) * 1.0 / cell_size))  # 获取到y方向上取整的序号
                ch = g.move(xi, yi)


# 绘制出棋子位置
def refresh_board():
    global ch, an
    screen.fill((128, 128, 128))  # 将界面设置为蓝色
    # 画边界
    for x in range(0, cell_size * cell_num, cell_size):
        pygame.draw.line(screen, (200, 200, 200), (x + space, 0 + space),
                         (x + space, cell_size * (cell_num - 1) + space), 1)
    for y in range(0, cell_size * cell_num, cell_size):
        pygame.draw.line(screen, (200, 200, 200), (0 + space, y + space),
                         (cell_size * (cell_num - 1) + space, y + space), 1)
    # 画棋子
    for x, y, player in g.chess:
        piece_location = [int((x + 0.5) * cell_size) + space, int((0.5 + y) * cell_size) + space]
        if player == 1:
            pygame.draw.circle(screen, white, piece_location, 16, 16)
        else:
            pygame.draw.circle(screen, black, piece_location, 16, 16)
    # 判结果人类获胜
    if an == 1:
        text = font1.render("VICTORY!!", True, white)
        text2 = font2.render("RESTART", True, white)
        screen.blit(text, (font_position[0][0]+10, font_position[0][1]))
        screen.blit(text2, font_position[1])
        ch = 0
    # 判结果电脑获胜
    elif an == -1:
        text1 = font1.render("GAME OVER!", True, white)
        text2 = font2.render("RETRY", True, white)
        screen.blit(text1, font_position[0])
        screen.blit(text2, font_position[1])

    elif g.cur_step == 10:
        text1 = font1.render("Stalemate!", True, white)
        text2 = font2.render("RETRY", True, white)
        screen.blit(text1, (font_position[0][0]+10, font_position[0][1]))
        screen.blit(text2, font_position[1])
        an = 2


def main():
    global ch, an, running
    clock = pygame.time.Clock()
    while running:
        ch = 0
        # 人类下棋
        man_move()
        refresh_board()
        an = g.game_result()
        if an == 0 and ch:
            xa, ya = g.ai_move()
        # 判断结果
        an = g.game_result()
        # 刷新棋盘
        refresh_board()
        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    g = TicTacToe()  # 初始化
    main()
