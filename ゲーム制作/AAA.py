import pygame
from pygame.locals import *
import pygame.mixer
import sys
import numpy as np
import random

from state import State

#def関数で役割を分けた
#https://aidiary.hatenablog.com/entry/20081012/1281193197
#上記のサイトを参考にしている

FONT_PATH = "NuAnkoMochi-Reg.otf"

#キャラ情報(No,得意手,ダメージ1,ダメージ2,体力)
a = np.array([[1,1,3,1,12], [2,2,2,1,15], [3,3,3,2,10]])

#カード情報(No,attack,health,damage,special)
b = np.array([[1,1,0,0,0],[2,0,3,0,0],[3,0,0,2,0],[4,0,0,0,1]])

#所持アイテム情報
c = np.array([[1,1],[1,2],[1,3]])

#ガチャ確率


#状態保存(キャラ選択など)
#s = np.array([1,1])

#np.savez("save", chara = a, spell = b, item = c, state = s)

deck = np.load("save.npz")["state"][0]
chara = np.load("save.npy")
spells = np.load("save.npz")["spell"]

myspell = spells[0]

allyy = chara[deck -1]
enemy = chara[1]

#画像の読み取り
red = pygame.image.load("mon_026.bmp")  
green = pygame.image.load("mon_028.bmp")
blue = pygame.image.load("mon_024.bmp")
dra = pygame.image.load("mon_013.bmp")
slash1 = pygame.image.load("slash.png") 
slash2 = pygame.image.load("slash2.png") 
slash3 = pygame.image.load("slash3.png") 
slash4 = pygame.image.load("slash4.png") 
slash5 = pygame.image.load("slash5.png") 
bump = pygame.image.load("bump.png")

#画像のリサイズ
red = pygame.transform.scale(red, (200, 240)) 
green = pygame.transform.scale(green, (200, 240)) 
blue = pygame.transform.scale(blue, (200, 240)) 
dra = pygame.transform.scale(dra, (200, 240)) 
slash1 = pygame.transform.scale(slash1, (200, 240)) 
slash2 = pygame.transform.scale(slash2, (200, 240)) 
slash3 = pygame.transform.scale(slash3, (200, 240)) 
slash4 = pygame.transform.scale(slash4, (200, 240)) 
slash5 = pygame.transform.scale(slash5, (200, 240)) 
bump = pygame.transform.scale(bump, (200, 240)) 

#サウンド
pygame.mixer.init()

SE0=pygame.mixer.Sound("click.mp3")
SE1=pygame.mixer.Sound("se_damage1.mp3")		#効果音の設定
SE2=pygame.mixer.Sound("se_damage2.mp3")
SE3=pygame.mixer.Sound("se_damage3.mp3")
SE4=pygame.mixer.Sound("se_damage4.mp3")
SE5=pygame.mixer.Sound("se_damage5.mp3")
SE6=pygame.mixer.Sound("kaifuku.wav")
SE7=pygame.mixer.Sound("up.mp3")
SE8=pygame.mixer.Sound("end.mp3")

pygame.mixer.music.load("title.mp3")	#BGMの設定
pygame.mixer.music.play(-1)			#BGMの出力

#global変数
log1 = "てきがあらわれた！"
log2 = "[space]"
HP1 = 10
HP2 = 30
enemychoice = 0
#deck = np.load("save.npz")["state"][0]
mons = [red,green,blue]
effect = [slash1, slash2, slash3, slash4, slash5, bump]
SE_slas = [SE1, SE2, SE3, SE4]
ON = 0
zyankeka = 0

button = pygame.Rect(30, 30, 50, 50)  # creates a rect object
button2 = pygame.Rect(100, 30, 70, 50)  # creates a rect object

class Menu():
    def __init__(self):
        self.state=State()
        pygame.init()
        # ゲームオブジェクトを初期化
        self.init_game()

    def init_game(self):
        pass
         
    def show(self):
        SCREEN_SIZE = (960, 640)  # 画面サイズ
        pygame.display.set_caption("ムシキング")
        screen = pygame.display.set_mode(SCREEN_SIZE)

        global log1
        global log2
        global deck
        global HP1
        global HP2
        global ON
        global zyankeka
        global allyy
        global chara

        # メインループ開始(ここで主だってゲームを動かしている)
        clock = pygame.time.Clock()
        while True:
            clock.tick(30)

            #描画
            screen.fill((0,0,0))
            sysfont = pygame.font.Font(FONT_PATH, 40)            

            #テキストログ
            log_1 = sysfont.render(log1, False, (255,255,255))
            log_2 = sysfont.render(log2, False, (255,255,255))

            #HPログ
            HP_1 = sysfont.render( "あなた:" + str(HP1), False, (255,255,255))
            HP_2 = sysfont.render( "あいて:" + str(HP2), False, (255,255,255))

            #ゲーム状態の違いによって異なる画面を表示する
            if self.state.game_state[0] == self.state.START: #メニュー画面の構成
                Title1 = sysfont.render("じゃんけんモンスターズ", False, (255,255,255))
                screen.blit(Title1, (350,90))
                mode1 = sysfont.render("シングルプレイ [1]", False, (255,255,255))
                screen.blit(mode1, (350,200))
                mode2 = sysfont.render("キャラ選択 [2]", False, (255,255,255))
                screen.blit(mode2, (350,260))
                mode3 = sysfont.render("ガチャ [3]", False, (255,255,255))
                screen.blit(mode3, (350,320))
                mode4 = sysfont.render("おわる [4]", False, (255,255,255))
                screen.blit(mode4, (350,450))

            elif self.state.game_state[0] == self.state.single_PLAY:
                screen.blit(log_1, (175,420))      
                screen.blit(log_2, (175,480))      
                screen.blit(mons[deck-1], (150,100)) 
                screen.blit(dra, (630,100)) 
                screen.blit(HP_1, (160,350)) 
                screen.blit(HP_2, (645,350)) 

            elif self.state.game_state[0] == self.state.single_command1:
                screen.blit(log_1, (160,420))      
                screen.blit(log_2, (160,480))      
                screen.blit(mons[deck-1], (150,100)) 
                screen.blit(dra, (630,100)) 
                screen.blit(HP_1, (160,350)) 
                screen.blit(HP_2, (645,350))      

            elif self.state.game_state[0] == self.state.single_command2:
                screen.blit(log_1, (160,420))      
                screen.blit(log_2, (160,480))      
                screen.blit(mons[deck-1], (150,100)) 
                screen.blit(dra, (630,100)) 
                screen.blit(HP_1, (160,350)) 
                screen.blit(HP_2, (645,350))                    

            elif self.state.game_state[0] == self.state.single_show:
                screen.blit(log_1, (160,420))      
                screen.blit(log_2, (160,480))      
                screen.blit(mons[deck-1], (150,100)) 
                screen.blit(dra, (630,100)) 
                screen.blit(HP_1, (160,350)) 
                screen.blit(HP_2, (645,350)) 

            elif self.state.game_state[0] == self.state.single_result1:
                screen.blit(log_1, (160,420))      
                screen.blit(log_2, (160,480))      
                screen.blit(mons[deck-1], (150,100)) 
                screen.blit(dra, (630,100))
                if zyankeka == 1:
                    screen.blit(effect[ON], (630,100))  
                elif zyankeka == 2:
                    screen.blit(effect[ON], (150,100)) 
                else:
                    screen.blit(effect[ON], (150,100)) 
                    screen.blit(effect[ON], (630,100))  
                screen.blit(HP_1, (160,350)) 
                screen.blit(HP_2, (645,350)) 

            elif self.state.game_state[0] == self.state.single_result2:
                screen.blit(log_1, (160,420))      
                screen.blit(log_2, (160,480))      
                screen.blit(mons[deck-1], (150,100)) 
                screen.blit(dra, (630,100)) 
                screen.blit(HP_1, (160,350)) 
                screen.blit(HP_2, (645,350))     

            elif self.state.game_state[0] == self.state.single_match:
                screen.blit(log_1, (160,420))      
                screen.blit(log_2, (160,480))      
                screen.blit(mons[deck-1], (150,100)) 
                screen.blit(dra, (630,100)) 
                screen.blit(HP_1, (160,350)) 
                screen.blit(HP_2, (645,350)) 

            elif self.state.game_state[0] == self.state.CHOOSE:
                screen.blit(red, (50,150)) 
                screen.blit(green, (380,150))
                screen.blit(blue, (710,150))
                screen.blit(log_1, (175,420))      
                screen.blit(log_2, (175,480)) 
                ex1 = sysfont.render("サラマン[1]", False, (255,255,255))
                screen.blit(ex1, (50,90))
                ex2 = sysfont.render("ドリー [2]", False, (255,255,255))
                screen.blit(ex2, (380,80))
                ex3 = sysfont.render("ウンディ[3]", False, (255,255,255))
                screen.blit(ex3, (710,80))             

            elif self.state.game_state[0] == self.state.LOTTERY:
                screen.blit(log_1, (160,420))      
                screen.blit(log_2, (160,480))  
                pygame.display.update()

            #キーイベント処理
            #キー操作(スペースボタン)によってゲーム状態を変える
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                elif event.type == KEYDOWN: #メニューからの画面遷移
                    if self.state.game_state[0] == self.state.START:
                        if event.key == K_1:
                            SE0.play()
                            self.state.game_state[0] = self.state.single_PLAY
                            self.AT1 = allyy[2]
                            self.AT2 = allyy[3]
                            allyy = chara[deck -1]
                            ON = 0
                            HP1 = allyy[4]
                            HP2 = 30
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load("w001.wav")	#BGMの設定
                            pygame.mixer.music.play(-1)			#BGMの出力

                        if event.key == K_2:
                            self.state.game_state[0] = self.state.CHOOSE
                            log1 = "キャラをせんたく"
                            log2 = "[space]でけってい"
                            SE0.play()
                        if event.key == K_3:
                            self.state.game_state[0] = self.state.LOTTERY
                            log1 = "ちょうせいちゅう"
                            log2 = "[space]でタイトルにもどる"      
                            SE0.play()
                        if event.key == K_4:
                            pygame.quit()
                            sys.exit()

                    elif self.state.game_state[0] == self.state.single_PLAY:
                        if event.key == K_SPACE:
                            self.state.game_state[0] = self.state.single_command1
                            SE0.play()
                            log1 = "コマンドをせんたく"
                            log2 = "パー[1], グー[2], チョキ[3]"  
                        

                    elif self.state.game_state[0] == self.state.single_command1: 
                        if event.key == K_1:
                            SE0.play()
                            self.choice1 = 1
                            self.state.game_state[0] = self.state.single_command2
                            log1 = "スペルをせんたく"
                            log2 = "パワー[1], ついげき[2], かいふく[3]" 

                        if event.key == K_2:
                            SE0.play()
                            self.choice1 = 2
                            self.state.game_state[0] = self.state.single_command2
                            log1 = "スペルをせんたく"
                            log2 = "パワー[1], ついげき[2], かいふく[3]" 

                        if event.key == K_3:
                            SE0.play()
                            self.choice1 = 3
                            self.state.game_state[0] = self.state.single_command2 
                            log1 = "スペルをせんたく"
                            log2 = "パワー[1], ふいうち[2], かいふく[3]" 

                    elif self.state.game_state[0] == self.state.single_command2:   
                        self.enemychoice = random.randint(1, 3)

                        if event.key == K_1:
                            SE0.play()
                            self.choice2 = 1
                            self.state.game_state[0] = self.state.single_show
                            log1 = "あなた:" + zyankenchoice(self.choice1) + "、あいて:" + zyankenchoice(self.enemychoice)
                            log2 = "[space]"  

                        if event.key == K_2:
                            SE0.play()
                            self.choice2 = 2
                            self.state.game_state[0] = self.state.single_show
                            log1 = "あなた:" + zyankenchoice(self.choice1) + "あいて:" + zyankenchoice(self.enemychoice)
                            log2 = "[space]"  

                        if event.key == K_3:
                            SE0.play()
                            self.choice2 = 3
                            self.state.game_state[0] = self.state.single_show   
                            log1 = "あなた:" + zyankenchoice(self.choice1) + "あいて:" + zyankenchoice(self.enemychoice)
                            log2 = "[space]"  

                    elif self.state.game_state[0] == self.state.single_show:
                        zyankeka = zyanken(self.choice1, self.enemychoice)

                        if zyanken(self.choice1, self.enemychoice) == 1:
                            if event.key == K_SPACE:
                                SE0.play()
                                self.state.game_state[0] = self.state.single_result2
                                log1 = "かち。スペルはつどう！"
                                if self.choice2 == 1:
                                    SE7.play()
                                    self.AT1 += 1
                                    self.AT2 += 1
                                    log2 = "ATTACKが1上がった！[space]"

                                elif self.choice2 == 2:
                                    SE5.play()
                                    HP2 -= 2
                                    log2 = "あいてに2のダメージ！[space]"
                                
                                elif self.choice2 == 3:
                                    SE6.play()
                                    HP1 += 3
                                    log2 = "HPが3かいふくした！[space]"

                        elif zyanken(self.choice1, self.enemychoice) == 2:
                            if event.key == K_SPACE:
                                SE_slas[random.randint(0,3)].play()
                                self.state.game_state[0] = self.state.single_result1
                                ON = random.randint(0, 4)
                                log1 = "まけ。あなたに" + str(enemy[3]) + "ダメージ！"
                                log2 = "[space]"  
                                HP1 = HP1 - enemy[3]
 
                        elif zyanken(self.choice1, self.enemychoice) == 3:
                            if event.key == K_SPACE:
                                SE5.play()
                                self.state.game_state[0] = self.state.single_result1
                                ON = 5
                                log1 = "あいこ。おたがいに1ダメージ！"
                                log2 = "[space]"   
                                HP1 = HP1 - 1
                                HP2 = HP2 - 1

                    elif self.state.game_state[0] == self.state.single_result1:
                        if HP1 > 0 and HP2 > 0:
                            if event.key == K_SPACE:
                                SE0.play()
                                self.state.game_state[0] = self.state.single_command1
                                log1 = "コマンドをせんたく"
                                log2 = "パー[1], グー[2], チョキ[3]" 
                        
                        else:
                            if event.key == K_SPACE:
                                SE8.play()
                                pygame.mixer.music.stop()			#BGMの停止
                                self.state.game_state[0] = self.state.single_match                                                            
                                log2 = "[space]でタイトルにもどる" 
                                if HP2 < 1:
                                    log1 = "あいてをたおした！！"
                                elif HP1 < 1:
                                    log1 = "たいりょくがつきた・・・"
                                else:
                                    log1 = "あいうち、、おしい！"                                    


                    elif self.state.game_state[0] == self.state.single_result2:                        
                        if event.key == K_SPACE:
                            SE_slas[random.randint(0,3)].play()
                            self.state.game_state[0] = self.state.single_result1
                            log2 = "[space]"
                            ON = random.randint(0, 4)

                            if allyy[1] == self.choice1:
                                log1 = "あいてに" + str(self.AT1) + "ダメージ！"
                                HP2 -= self.AT1
                            
                            else:
                                log1 = "あいてに" + str(self.AT2) + "ダメージ！"
                                HP2 -= self.AT2

                    elif self.state.game_state[0] == self.state.single_match:
                        if event.key == K_SPACE:
                            SE0.play()
                            self.state.game_state[0] = self.state.START
                            log1 = "てきがあらわれた！"
                            log2 = "[space]"
                            pygame.mixer.music.load("title.mp3")	#BGMの設定
                            pygame.mixer.music.play(-1)			#BGMの出力

                    #2番目
                    elif self.state.game_state[0] == self.state.CHOOSE:
                        if event.key == K_1:
                            SE0.play()
                            deck = 1
                            log1 = "(1)パーがつよいバランスタイプ"

                        if event.key == K_2:
                            SE0.play()
                            deck = 2
                            log1 = "(2)グーがつよいディフェンスタイプ"

                        if event.key == K_3:
                            SE0.play()
                            deck = 3
                            log1 = "(3)チョキがつよいアタッカータイプ"

                        if event.key == K_SPACE:
                            SE0.play()
                            log1 = "てきがあらわれた！"
                            log2 = "[space]"
                            s = np.array([1,deck])
                            np.savez("save", chara = a, spell = b, item = c, state = s)
                            self.state.game_state[0] = self.state.START

                    #3番目
                    elif self.state.game_state[0] == self.state.LOTTERY:
                        if event.key == K_SPACE:
                            SE0.play()
                            log1 = "てきがあらわれた！"
                            log2 = "[space]"
                            self.state.game_state[0] = self.state.START


                    elif self.state.gameplay[0] == self.state.end:
                        if event.key == K_SPACE:
                            self.state.game_state[0] = self.state.START
                            self.state.gameplay[0] = self.state.off

            pygame.display.update()


            





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

#じゃんけんの手
def zyankenchoice(num):
    choice = ""
    if num == 1:
        choice = "パー"
    elif num == 2:
        choice = "グー"
    elif num == 3:
        choice = "チョキ"
    return choice

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
        ally[4] = ally[4] - damage

#スペル処理
def spellStep(choice, AT, HP1, HP2):
    effect = ""

    if choice == 1:
        effect = "ATTACKが1上がった！"

    elif choice == 2:
        effect = "HPが3かいふくした！"
    
    elif choice == 3:
        effect = "あいてに2のついかダメージ！"
    
    return effect

#戦闘処理
def battleStep(choi):
    #while ally[4] > 0 and enemy[4] > 0:
    choice = choi
    enemyChoice = random.randint(1, 3)
    res = zyanken(choice, enemyChoice)
    dmg = damagecalc(choice, enemyChoice, res)
    damageStep(res, dmg)
    zyankekka(res,dmg)
    spellStep(myspell, myspell, res)
    print("味方HP:",int(ally[4]),"相手HP:",int(enemy[4]))
    
    #print("戦闘終了！")

#キャラ情報(No,名前,得意手,ダメージ1,ダメージ2,体力)
#a = np.array([[1,1,3,1,12], [2,2,2,1,15], [3,3,3,2,10]])




#実処理
Menu().show()