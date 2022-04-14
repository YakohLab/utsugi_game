import pygame
from pygame.locals import *
import sys
import numpy as np

#キャラ情報(No,得意手,ダメージ1,ダメージ2,体力)
a = np.array([[1,1,3,1,12], [2,2,2,1,15], [3,3,3,2,10]])

#カード情報(No,attack,health,damage,special)
b = np.array([[1,1,0,0,0],[2,0,3,0,0],[3,0,0,2,0],[4,0,0,0,1]])

#所持アイテム情報
c = np.array([[1,1],[1,2],[1,3]])

#ガチャ確率


#状態保存(キャラ選択など)
s = np.array([1,1])

#np.save("save", a)

np.savez("save", chara = a, spell = b, item = c, state = s)
z = np.load("save.npz")
print(z["chara"])