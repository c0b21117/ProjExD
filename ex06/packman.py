from time import sleep
from tkinter import font
import pygame as pg
import sys
import tkinter
from random import randint
from itertools import count
import maze_maker as mm # 練習8
import os

class Screen:
    def __init__(self, title, wh,bgimg):
        pg.display.set_caption(title) #タイトル
        self.sfc = pg.display.set_mode(wh) #画面の大きさ(1600, 900)
        self.rct = self.sfc.get_rect()
        self.bgi_sfc = pg.image.load(bgimg) #背景
        self.bgi_rct = self.bgi_sfc.get_rect()

    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct)


class Text:# テキストを出力させるクラス

    def __init__(self,text,color,basyo):
        self.text = text
        self.color = color
        self.size = basyo
    
    def blit(self, scr:Screen):
        font = pg.font.Font(None,300)
        t = font.render(self.text, True, self.color)
        scr.sfc.blit(t, self.size)


class Packman:
    key_delta = {
        pg.K_UP:    [0, -10],
        pg.K_DOWN:  [0, +10],
        pg.K_LEFT:  [-10, 0],
        pg.K_RIGHT: [+10, 0],
    }

    def __init__(self, color, radius, vxy, scr:Screen):
        self.sfc = pg.Surface((radius*2, radius*2)) # 空のSurface
        self.sfc.set_colorkey((0, 0, 0)) # 四隅の黒い部分を透過させる
        pg.draw.circle(self.sfc, color, (radius, radius), radius) # packmanの円を描く
        self.rct = self.sfc.get_rect()
        self.rct.centerx = 80
        self.rct.centery = 80
        self.vx, self.vy = vxy

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        key_states = pg.key.get_pressed()
        for key, delta in Packman.key_delta.items():
            if key_states[key]:
                self.rct.centerx += delta[0]
                self.rct.centery += delta[1]            
        self.blit(scr) # =scr.sfc.blit(self.sfc, self.rct)


class Enemy:
    def __init__(self, color, radius, vxy, scr:Screen):
        self.sfc = pg.Surface((radius*2, radius*2)) # 空のSurface
        self.sfc.set_colorkey((0, 0, 0)) # 四隅の黒い部分を透過させる
        pg.draw.circle(self.sfc, color, (radius, radius), radius) # 爆弾用の円を描く
        self.rct = self.sfc.get_rect()
        self.rct.centerx = randint(200, 1300)
        self.rct.centery = randint(0, scr.rct.height)
        self.vx, self.vy = vxy

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        self.rct.move_ip(self.vx, self.vy)
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        self.blit(scr) # =scr.sfc.blit(self.sfc, self.rct)

class Map:
    map =[[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
           [1,0,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1],
           [1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1],
           [1,0,0,1,0,0,0,0,0,0,1,1,1,0,0,0,0,1,1,1],
           [1,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1,1],
           [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,1,0,0,0,0,1,1,0,1,0,0,0,0,0,1,0,0,0,1],
           [1,0,0,0,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,2],
           [1,0,0,0,0,0,1,1,0,1,1,0,0,1,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,1,0,0,1,1,0,0,0,0,1],
           [1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,1],
           [1,0,0,0,1,0,0,1,0,1,1,0,0,0,0,0,0,1,0,1],
           [1,1,0,0,1,0,1,1,0,0,1,1,1,0,1,1,1,1,1,1],
           [1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1],
           [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
    row,col = len(map), len(map[0]) # マップの行数,列数を取得
    imgs = [None] * 256             # マップチップ
    msize = 800/len(map)                    # 1マスの大きさ[px]
    # マップの描画
    def draw(self, screen):
        for i in range(self.row):
            for j in range(self.col):
                screen.blit(self.imgs[self.map[i][j]], (j*self.msize,i*self.msize))

def check_bound(obj_rct, scr_rct):
    """
    obj_rct：こうかとんrct，または，爆弾rct
    scr_rct：スクリーンrct
    領域内：+1／領域外：-1
    """
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right: 
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom: 
        tate = -1
    return yoko, tate

#def check_wall(obj_rct, scr_rct):
    

def main():
    scrn_sfc = pg.display.set_mode((1600, 900))
    scr = Screen("PACKMAN", (1500, 800), "fig/pg_bg.jpg")
    pac = Packman((0, 255, 255), 20, (+5, +5), scr)
    enm = Enemy((255, 0, 0), 20, (0, +5), scr)
    over = Text("GAMEOVER",(255,255,255),(200,400))
    cre = Text("GAMECREA",(255,0,0),(200,400))
    Map.imgs[0] = pg.image.load("fig/black.png")         # 道
    Map.imgs[1] = pg.image.load("fig/gray.png")         # 壁
    Map.imgs[2] = pg.image.load("fig/6.png")#こうかとん
    map = Map()

    clock = pg.time.Clock() # 練習1
    while True:
        scr.blit() # 練習2
        map.draw(scrn_sfc)
        pg.display.update()
        for event in pg.event.get(): # 練習2
            if event.type == pg.QUIT:
                return

        # 練習4
        pac.update(scr)

        # 練習7
        enm.update(scr)

        # 練習8
        if pac.rct.colliderect(enm.rct): # こうかとんrctが爆弾rctと重なったら
            over.blit(scr)
            pg.display.update()
            sleep(3)
            return

        pg.display.update() #練習2
        clock.tick(300)


if __name__ == "__main__":
    pg.init() # 初期化
    main()    # ゲームの本体
    pg.quit() # 初期化の解除
    sys.exit()

