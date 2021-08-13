import pygame
import sys
from pygame.locals import *
def main() -> int :

    pygame.init()
    pygame.mixer.init()

    #背景设置
    bg_size = width, height = 600, 600
    screen = pygame.display.set_mode(bg_size)
    pygame.display.set_caption("飞机大战")
    background = pygame.image.load("background.gif").convert()
    screen.blit(background, (0, 0))

    #文字设置
    fontObj = pygame.font.Font("typeface1.TTF" ,80)
    textSurfaceObj = fontObj.render('飞机大战', True, (7,121,118))
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (200, 100)
    screen.blit(textSurfaceObj, textRectObj)
    
    white=(255,255,255)
    black=(0,0,0)
    fontObj = pygame.font.Font("typeface2.TTF" ,40)
    textSurfaceObj = fontObj.render('单人游戏', True, black,white)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (200, 250)
    screen.blit(textSurfaceObj, textRectObj)

    fontObj = pygame.font.Font("typeface2.TTF" ,40)
    textSurfaceObj = fontObj.render('双人游戏', True,  black,white)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (200, 350)
    screen.blit(textSurfaceObj, textRectObj)

   

    #背景音乐，当进入其他界面时可切换
    pygame.mixer.music.load("mainpagemusic.wav")
    pygame.mixer.music.play(-1, 0.0)
 
    
    

    while True:
     # 获取事件
        for event in pygame.event.get():
            # 判断事件是否为退出事件
            keys = pygame.key.get_pressed()
            if event.type == QUIT or keys[K_ESCAPE]:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            if event.type ==MOUSEBUTTONDOWN and  220<=event.pos[1]<=270 and 120<=event.pos[0]<=280:
                #单人游戏接口
                return 1
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
                break
            if event.type ==MOUSEBUTTONDOWN and  320<=event.pos[1]<=370 and 120<=event.pos[0]<=280:
                #双人游戏接口                
                return 2
            # if event.type ==MOUSEBUTTONDOWN and  420<=event.pos[1]<=470 and 120<=event.pos[0]<=280:
            #     #关卡选择接口
            #     return 0
            # if event.type ==MOUSEBUTTONDOWN and  520<=event.pos[1]<=570 and 120<=event.pos[0]<=280:
            #     #游戏说明接口
            #     return 3
            
    
            # 绘制屏幕内容
        pygame.display.update()
