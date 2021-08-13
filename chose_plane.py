import pygame
from pygame.locals import *
import sys
from war_module import WarCraftFactory

bcground = [["./bcg/bc1.jfif",1 ,1 ,"经历深海历练的战斗机"], ["./bcg/bc2.jpeg",3,2],["./bcg/bc3.png",3,2],["./bcg/bc4.jfif",6,5]]

def get_bcg(index):
    bc = pygame.image.load(bcground[index][0]).convert()
    w, h = bc.get_size()
    bc = pygame.transform.smoothscale(bc,(bcground[index][2]* w//bcground[index][1], bcground[index][2]* h//bcground[index][1]))
    return bc


def get_type(chosen=None) -> int:

    pygame.init()
    pygame.mixer.init()

    # 背景设置
    type = 1
    if type == chosen:
        type += 1

    bg_size = width, height = 600, 600
    screen = pygame.display.set_mode(bg_size)
    pygame.display.set_caption("飞机大战")
    background = get_bcg(type-1)

    rec = background.get_rect()
    rec.center = (310, 315)
    screen.blit(background, rec)

    plane1 = WarCraftFactory.get_war_craft(type-1,enlarge=3)
    rect = plane1.get_rect()
    rect.center = (300, 300)
    screen.blit(plane1, rect)

    black = (0, 0, 0)
    fontObj = pygame.font.Font("typeface2.TTF", 30)
    text1 = fontObj.render("请选择您的出征战斗机。" + str(chr(9801)) + "J键切换，K键确认", True, black, (255, 255, 255))
    textRect1 = text1.get_rect()
    textRect1.center = (300, 15)
    screen.blit(text1, textRect1)




    while True:

        for event in pygame.event.get():
            if event.type == KEYDOWN:


                keys = pygame.key.get_pressed()
                if event.type == QUIT or keys[K_ESCAPE]:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()

                if keys[K_j]:
                    type %= len(bcground)
                    type += 1
                    if  chosen==type : type +=1

                    background = get_bcg(type-1)
                    rec  = background.get_rect()
                    rec.center = (310,315)
                    screen.blit(background, rec)

                    plane = WarCraftFactory.get_war_craft(type-1, enlarge=3)
                    # 右下角对齐(width - rect1[0], height - rect1[1])
                    rect = plane.get_rect()
                    rect.center=(310,270)

                    screen.blit(plane, rect)

                    black = (0, 0, 0)
                    fontObj = pygame.font.Font("typeface2.TTF", 30)
                    text1 = fontObj.render("请选择您的出征战斗机。"+str(chr(9801))+"J键切换，K键确认", True, black,(255,255,255))
                    textRect1 = text1.get_rect()
                    textRect1.center = (300, 15)
                    screen.blit(text1, textRect1)

                elif event.key == K_k:
                    return type-1
                    break
                keys = None
        pygame.display.update()