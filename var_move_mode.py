import random

from war_module import Craft
from war_module import WarCraftFactory
import math
from collision_detector import add_plane


# 大雁阵列
def formation_mode1(round=0):
    if round ==2:
        round = random.randint(0,1)
    length = 3
    if round ==1:
        length = 7
    c = random.randint(0,length)
    for i in [0,1,2,3,4,5]:
        enemy = WarCraftFactory.get_enemy(round,c)
        enemy = Craft(enemy, 100*i, 200*math.sin(i/6*math.pi)-200 , enemy.get_size()[0], enemy.get_size()[1], 3 ,life=5,isenemy=True)
        add_plane(enemy)
        enemy.start()

# 五角星阵列
def fomation_mode2(round=0):
    if round == 2:
        round = random.randint(0, 1)
    length = 3
    if round == 1:
        length = 7
    c = random.randint(0, length)
    for i in [0,1,2,3,4]:
        enemy = WarCraftFactory.get_enemy(round,c)
        enemy = Craft(enemy,300+100*math.cos((18+72*i)*2*math.pi/360),100*math.sin((18+72*i)*2*math.pi/360) , enemy.get_size()[0], enemy.get_size()[1], 3 ,life=5,isenemy=True)
        add_plane(enemy)
        enemy.start()

#3.米字型阵列
def formation_mode3(round=0):
    for i in [0,1,2,3,4,5,6,7]:
        enemy = WarCraftFactory.get_enemy(0,1)
        enemy = Craft(enemy,300+25*math.cos((45*i)*2*math.pi/360),25*math.sin((45*i)*2*math.pi/360) , enemy.get_size()[0], enemy.get_size()[1], 3 ,life=3,isenemy=True)
        add_plane(enemy)
        enemy.start()
        enemy = WarCraftFactory.get_enemy(0,1)
        enemy = Craft(enemy,300+75*math.cos((45*i)*2*math.pi/360),75*math.sin((45*i)*2*math.pi/360) , enemy.get_size()[0], enemy.get_size()[1], 3 ,life=3,isenemy=True)
        add_plane(enemy)
        enemy.start()
        enemy = WarCraftFactory.get_enemy(0,1)
        enemy = Craft(enemy,300+125*math.cos((45*i)*2*math.pi/360),125*math.sin((45*i)*2*math.pi/360) , enemy.get_size()[0], enemy.get_size()[1], 3 ,life=3,isenemy=True)
        add_plane(enemy)
        enemy.start()