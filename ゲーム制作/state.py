import pygame
from pygame.locals import *
import sys

#クラス変数化する

class State:
    def __init__(self):
        # ゲーム状態の初期設定
        #ゲーム状態の変数追加
        self.START, self.single_PLAY, self.CHOOSE, self.LOTTERY, self.single_command1, self.single_command2 ,self.single_show, self.single_result1, self.single_result2 ,self.single_match = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        self.stay, self.ready = (0, 1)
        self.on, self.off, self.end= (0, 1, 2)
        # 画面遷移に伴うゲーム状態
        self.game_state = []
        if len(self.game_state) == 0:
            self.game_state.append(self.START)
        # # マルチプレイ待機画面遷移におけるゲーム状態の定義
        # self.connect_ready = []
        # if len(self.connect_ready) == 0:
        #     self.connect_ready.append(self.stay)
        # self.gameplay = []
        # if len(self.gameplay) == 0:
        #     self.gameplay.append(self.off)    

        