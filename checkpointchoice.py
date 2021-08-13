import pygame
import sys
from pygame.locals import *
def checkpointchoice():        
    pygame.init()
    pygame.mixer.init()

    #背景设置
    bg_size = width, height = 600, 600
    screen = pygame.display.set_mode(bg_size)
    pygame.display.set_caption("飞机大战")

     #文字设置
    fontObj = pygame.font.Font("typeface1.TTF" ,40)
    textSurfaceObj = fontObj.render('关卡选择', True, (184,253,186))
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (300, 20)
    screen.blit(textSurfaceObj, textRectObj)
    
    white=(255,255,255)
    black=(0,0,0)
    fontObj = pygame.font.Font("typeface2.TTF" ,40)
    textSurfaceObj = fontObj.render('第一关', True, black,white)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (300, 200)
    screen.blit(textSurfaceObj, textRectObj)

    fontObj = pygame.font.Font("typeface2.TTF" ,40)
    textSurfaceObj = fontObj.render('第二关', True,  black,white)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (300, 280)
    screen.blit(textSurfaceObj, textRectObj)

    fontObj = pygame.font.Font("typeface2.TTF" ,40)
    textSurfaceObj = fontObj.render('第三关', True,  black,white)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (300, 360)
    screen.blit(textSurfaceObj, textRectObj)


    #背景音乐，当进入其他界面时可切换
    pygame.mixer.music.load("mainpagemusic.wav")
    pygame.mixer.music.play(-1, 0.0)
 
    
    

    while True:
     # 获取事件
        for event in pygame.event.get():
            # 判断事件是否为退出事件
            if event.type == QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            if event.type ==MOUSEBUTTONDOWN and 180<=event.pos[1]<=220 and 240<=event.pos[0]<=360:
                #第一关接口
                return 0
            if event.type ==MOUSEBUTTONDOWN and  260<=event.pos[1]<=300 and 240<=event.pos[0]<=360:               
                #第二关接口
                return 1
            if event.type ==MOUSEBUTTONDOWN and  340<=event.pos[1]<=380 and 240<=event.pos[0]<=360:
                #第三关接口
                return 2
            x, y = pygame.mouse.get_pos()
            if  180<=y<=220 and 240<=x<=360:
                 background = pygame.image.load("./map/space.png").convert()
                 screen.blit(background, (0, 0))
                   #文字设置
                 fontObj = pygame.font.Font("typeface1.TTF" ,40)
                 textSurfaceObj = fontObj.render('关卡选择', True, (184,253,186))
                 textRectObj = textSurfaceObj.get_rect()
                 textRectObj.center = (100, 20)
                 screen.blit(textSurfaceObj, textRectObj)
    
                 white=(255,255,255)
                 black=(0,0,0)
                 fontObj = pygame.font.Font("typeface2.TTF" ,40)
                 textSurfaceObj = fontObj.render('第一关', True, black,white)
                 textRectObj = textSurfaceObj.get_rect()
                 textRectObj.center = (300, 200)
                 screen.blit(textSurfaceObj, textRectObj)

                 fontObj = pygame.font.Font("typeface2.TTF" ,40)
                 textSurfaceObj = fontObj.render('第二关', True,  black,white)
                 textRectObj = textSurfaceObj.get_rect()
                 textRectObj.center = (300, 280)
                 screen.blit(textSurfaceObj, textRectObj)

                 fontObj = pygame.font.Font("typeface2.TTF" ,40)
                 textSurfaceObj = fontObj.render('第三关', True,  black,white)
                 textRectObj = textSurfaceObj.get_rect()
                 textRectObj.center = (300, 360)
                 screen.blit(textSurfaceObj, textRectObj)
            elif 260<=y<=300 and 240<=x<=360:
                 background = pygame.image.load("./map/map.jpeg").convert()
                 screen.blit(background, (0, 0))
                    #文字设置
                 fontObj = pygame.font.Font("typeface1.TTF" ,40)
                 textSurfaceObj = fontObj.render('关卡选择', True, (184,253,186))
                 textRectObj = textSurfaceObj.get_rect()
                 textRectObj.center = (100, 20)
                 screen.blit(textSurfaceObj, textRectObj)
    
                 white=(255,255,255)
                 black=(0,0,0)
                 fontObj = pygame.font.Font("typeface2.TTF" ,40)
                 textSurfaceObj = fontObj.render('第一关', True, black,white)
                 textRectObj = textSurfaceObj.get_rect()
                 textRectObj.center = (300, 200)
                 screen.blit(textSurfaceObj, textRectObj)

                 fontObj = pygame.font.Font("typeface2.TTF" ,40)
                 textSurfaceObj = fontObj.render('第二关', True,  black,white)
                 textRectObj = textSurfaceObj.get_rect()
                 textRectObj.center = (300, 280)
                 screen.blit(textSurfaceObj, textRectObj)

                 fontObj = pygame.font.Font("typeface2.TTF" ,40)
                 textSurfaceObj = fontObj.render('第三关', True,  black,white)
                 textRectObj = textSurfaceObj.get_rect()
                 textRectObj.center = (300, 360)
                 screen.blit(textSurfaceObj, textRectObj)
                
                
            elif 340<=y<=380 and 240<=x<=360:
                 background = pygame.image.load("./map/map3.jpeg").convert()
                 screen.blit(background, (0, 0))
                    #文字设置
                 fontObj = pygame.font.Font("typeface1.TTF" ,40)
                 textSurfaceObj = fontObj.render('关卡选择', True, (184,253,186))
                 textRectObj = textSurfaceObj.get_rect()
                 textRectObj.center = (100, 20)
                 screen.blit(textSurfaceObj, textRectObj)
    
                 white=(255,255,255)
                 black=(0,0,0)
                 fontObj = pygame.font.Font("typeface2.TTF" ,40)
                 textSurfaceObj = fontObj.render('第一关', True, black,white)
                 textRectObj = textSurfaceObj.get_rect()
                 textRectObj.center = (300, 200)
                 screen.blit(textSurfaceObj, textRectObj)

                 fontObj = pygame.font.Font("typeface2.TTF" ,40)
                 textSurfaceObj = fontObj.render('第二关', True,  black,white)
                 textRectObj = textSurfaceObj.get_rect()
                 textRectObj.center = (300, 280)
                 screen.blit(textSurfaceObj, textRectObj)

                 fontObj = pygame.font.Font("typeface2.TTF" ,40)
                 textSurfaceObj = fontObj.render('第三关', True,  black,white)
                 textRectObj = textSurfaceObj.get_rect()
                 textRectObj.center = (300, 360)
                 screen.blit(textSurfaceObj, textRectObj)
                
            else:
                 background = pygame.image.load("background.gif").convert()
                 screen.blit(background, (0, 0))
                    #文字设置
                 fontObj = pygame.font.Font("typeface1.TTF" ,40)
                 textSurfaceObj = fontObj.render('关卡选择', True, (184,253,186))
                 textRectObj = textSurfaceObj.get_rect()
                 textRectObj.center = (100, 20)
                 screen.blit(textSurfaceObj, textRectObj)
    
                 white=(255,255,255)
                 black=(0,0,0)
                 fontObj = pygame.font.Font("typeface2.TTF" ,40)
                 textSurfaceObj = fontObj.render('第一关', True, black,white)
                 textRectObj = textSurfaceObj.get_rect()
                 textRectObj.center = (300, 200)
                 screen.blit(textSurfaceObj, textRectObj)

                 fontObj = pygame.font.Font("typeface2.TTF" ,40)
                 textSurfaceObj = fontObj.render('第二关', True,  black,white)
                 textRectObj = textSurfaceObj.get_rect()
                 textRectObj.center = (300, 280)
                 screen.blit(textSurfaceObj, textRectObj)

                 fontObj = pygame.font.Font("typeface2.TTF" ,40)
                 textSurfaceObj = fontObj.render('第三关', True,  black,white)
                 textRectObj = textSurfaceObj.get_rect()
                 textRectObj.center = (300, 360)
                 screen.blit(textSurfaceObj, textRectObj)
                
            
            pygame.display.update()



