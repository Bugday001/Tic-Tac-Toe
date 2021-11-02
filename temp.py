#
#
# class TicTacToe:
#
#     def __init__(self):
#         self.cell_num = 3  # 格子数
#         self.g_map = [[0 for y in range(self.cell_num)] for x in range(self.cell_num)]
#         self.t_map = self.g_map.copy()  # 临时棋盘，求解回报值
#         self.cur_step = 0  # 步数
#         self.chess = []
#         self.full = 0  # 是否下满了
#         self.player = 1  # -1是电脑，1是人类
#         self.best_loc = [0, 0]  # 电脑下棋的最佳位置
#
#     # 玩家落子
#     def move(self, pos_x, pos_y):
#         self.player = -1  # 下次电脑下棋
#         if 0 <= pos_x <= self.cell_num - 1 and 0 <= pos_y <= self.cell_num - 1:  # 判断能否落子
#             if self.g_map[pos_x][pos_y] == 0:
#                 self.g_map[pos_x][pos_y] = 1
#                 self.cur_step += 1
#                 self.chess.append((pos_x, pos_y, 1))
#                 return 1
#         else:
#             return 0
#
#     # 判断游戏结局。0进行中，1玩家胜，-1电脑胜利，2平局
#     def game_result(self):
#         # 判断是否横向三子
#         count = 0
#         for y in range(self.cell_num):
#             count = 0
#             for x in range(self.cell_num):
#                 count += self.g_map[x][y]
#             if count % 3 == 0 and count != 0:
#                 return count / 3
#         # 判断是否纵向三子
#         for x in range(self.cell_num):
#             count = 0
#             for y in range(self.cell_num):
#                 count += self.g_map[x][y]
#             if count % 3 == 0 and count != 0:
#                 return count / 3
#         # 判断是否左上-右下三子
#         count = 0
#         count += self.g_map[0][0]+self.g_map[1][1]+self.g_map[2][2]
#         if count % 3 == 0 and count != 0:
#             return count / 3
#         # 判断是否右上-左下三子
#         count = 0
#         count += self.g_map[0][2] + self.g_map[1][1] + self.g_map[2][0]
#         if count % 3 == 0 and count != 0:
#             return count / 3
#         # 判和
#         if self.full:
#             return 2
#         return 0
#
#     # 电脑下棋：-1
#     def ai_move(self):
#         self.maxmin_search(9-self.cur_step)
#         self.player = 1  # 下次人类下棋
#         self.g_map[self.best_loc[0]][self.best_loc[1]] = -1
#         self.cur_step += 1
#         self.chess.append((self.best_loc[0], self.best_loc[1], 2))
#         return self.best_loc[0], self.best_loc[1]
#
#         # self.full = 1
#         # return -1, -1  # 满了
#
#     def logic(self):
#         pass
#
#     # 合法的落棋位置集合
#     def legal_loc(self):
#         left_loc = []
#         for i in range(self.cell_num):
#             for j in range(self.cell_num):
#                 if self.g_map[i][j] == 0:
#                     left_loc.append((i,j))
#         return left_loc
#
#     # 落棋
#     def move_piece(self, loc):
#         self.g_map[loc[0]][loc[1]] = self.player
#         self.player *= -1  # 切换下次的player
#
#     # 悔棋
#     def remove_piece(self, loc):
#         self.g_map[loc[0]][loc[1]] = 0
#         self.player *= -1  # 切换上次的player
#
#     # 评分
#     def each_value(self, player):
#         # 填满棋子
#         for i in range(self.cell_num):
#             for j in range(self.cell_num):
#                 if self.g_map[i][j] != 0:
#                     self.t_map[i][j] = self.g_map[i][j]
#                 else:
#                     self.t_map[i][j] = player
#         # 评分
#         count = 0
#         for y in range(self.cell_num):
#             for x in range(self.cell_num):
#                 count += self.t_map[x][y]
#             count = int(count / 3)
#         for x in range(self.cell_num):
#             for y in range(self.cell_num):
#                 count += self.t_map[x][y]
#             count = int(count / 3)
#         # 斜的
#         count += int((self.t_map[0][0] + self.t_map[1][1] + self.t_map[2][2]) / 3)
#         count += int((self.t_map[0][2] + self.t_map[1][1] + self.t_map[2][0]) / 3)
#         return count
#
#     def Evaluate(self):
#         if self.game_result() == -1:
#             return 999
#         elif self.game_result() == 1:
#             return -999
#         # 电脑评分
#         ai_value = self.each_value(-1)
#         # 人类评分
#         man_value = self.each_value(1)
#         return ai_value + man_value
#
#     def maxmin_search(self, depth):
#         if -1 == self.game_result() or 1 == self.game_result():
#             return self.Evaluate()
#         if depth == 0:
#             return self.Evaluate()
#         if self.player == -1:
#             best_value = -999
#         elif self.player == 1:
#             best_value = 999
#         # 得到空的位置
#         left_loc = self.legal_loc()
#         for loc in left_loc:
#             self.move_piece(loc)
#             value = self.maxmin_search(depth-1)
#             self.remove_piece(loc)
#             if self.player == 1:
#                 if value < best_value:
#                     best_value = value
#                     if depth == 9-self.cur_step:
#                         self.best_loc = loc
#             elif self.player == -1:
#                 if value > best_value:
#                     best_value = value
#                     if depth == 9 - self.cur_step:
#                         self.best_loc = loc
#         return best_value
#
#
#
