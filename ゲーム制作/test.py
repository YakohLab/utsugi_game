import pygame
from pygame.locals import *
import sys
import numpy as np
import random

#じゃんけん
def zyanken(p1, p2):
    result = 0

    if p1==1:
        if p2==1:
            result = 3
        elif p2==2:
            result = 1
        else:
            result = 2
    elif p1==2:
        if p2==1:
            result = 2
        elif p2==2:
            result = 3
        else:
            result = 1
    elif p1==3:
        if p2==1:
            result = 1
        elif p2==2:
            result = 2
        else:
            result = 3
    else:
        print("1から3の整数を入力してください")

    return result

#じゃんけん結果
def zyankekka(result,damage):
    if result == 1:
        print("あなたの勝ち！相手に",damage,"ダメージ")
    elif result == 2:
        print("あなたの負け！あなたに",damage,"ダメージ")
    else:
        print("あいこ")

#ダメージ計算
def damagecalc(p1, p2, result):
    damage = 0

    if result == 1:
        if p1 == ally[1]:
            damage = ally[2]
        else:
            damage = ally[3]
    elif result == 2:
        if p2 == enemy[1]:
            damage = enemy[2]
        else:
            damage = enemy[3]
    
    return damage

#ダメージ処理
def damageStep(result, damage):
    if result == 1:
        enemy[4] = enemy[4] - damage
    elif result == 2:
        ally[4] = ally[4] -damage

def spellStep(p1,p2,result):
    if result == 1:
        ally[2] += p1[1]
        ally[3] += p1[1]
        print("攻撃力が",p1[1],"上がった！")
        ally[4] += p1[2]
        print("体力が",p1[2],"回復した！")
        enemy[4] -= p1[3]
        print("敵に",p1[3],"の追加ダメージ！")

#戦闘処理
def battleStep():
    while ally[4] > 0 and enemy[4] > 0:
        print("パー:1, グー:2, チョキ:3")
        choice = int(input())
        enemyChoice = random.randint(1, 3)
        res = zyanken(choice, enemyChoice)
        dmg = damagecalc(choice, enemyChoice, res)
        damageStep(res, dmg)
        zyankekka(res,dmg)
        spellStep(myspell, myspell, res)
        print("味方HP:",int(ally[4]),"相手HP:",int(enemy[4]))
    
    print("戦闘終了！")

#キャラ情報(No,名前,得意手,ダメージ1,ダメージ2,体力)
#a = np.array([[1,1,3,1,12], [2,2,2,1,15], [3,3,3,2,10]])
chara = np.load("save.npy")
spells = np.load("save.npz")["spell"]

myspell = spells[0]

ally = chara[0]
enemy = chara[1]

c = battleStep()