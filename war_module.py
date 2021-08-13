import pygame
import random
import time
import math
from threading import Thread
from collision_detector import bullet_list

class Point(object):
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    # X property
    def getx(self): return self.__x

    def setx(self, x): self.__x = x

    x = property(getx, setx)

    # Y property
    def gety(self): return self.__y

    def sety(self, y): self.__y = y

    y = property(gety, sety)

    # def __str__(self):
    #     return "{X:" + "{:.0f}".format(self.__x) + \
    #            ",Y:" + "{:.0f}".format(self.__y) + "}"





# 战斗机工厂类，只是从图库中绘制合适的位图，根据index指定
class WarCraftFactory:

    def get_bullet(index):
        bullets = [
            ["./bullets/p1b1.png", 3], ["./bullets/p2b2.png", 3], ["./bullets/p3b3.png", 2],
            ["./bullets/p4b4.png", 3], ["./bullets/super_wea.png", 2],
        ]
        bullet = pygame.image.load(bullets[index][0]).convert_alpha()
        width, height = bullet.get_size()
        bullet = pygame.transform.smoothscale(bullet, (width // bullets[index][1], height // bullets[index][1]))
        return bullet

    def get_bullet_damage(index):
        damage = [
            [2, 0.1],
            [2, 0.1],
            [2, 0.1],
            [2, 0.1],
            [10, 0.05]
        ]
        return damage[index]

    def e_get_bullet(index):
        bullets = [
            ["./bullets/ene.png", 2],
            ["./bullets/ene.png", 2],
            ["./bullets/boss2_bullet.png", 3],
            ["./bullets/eneBoss3.png",4]
        ]
        bullet = pygame.image.load(bullets[index][0]).convert_alpha()
        width, height = bullet.get_size()
        bullet = pygame.transform.smoothscale(bullet, (width // bullets[index][1], height // bullets[index][1]))
        return bullet

    def get_war_craft(index, enlarge=1):
        war_crafts = [
            ["./crafts/plane1.png", 6], ["./crafts/plane2.png", 6], ["./crafts/plane3.png", 2],
            ["./crafts/plane4.png", 3], ["./crafts/super_craft.png", 4]
        ]
        wc = pygame.image.load(war_crafts[index][0]).convert_alpha()
        width, height = wc.get_size()
        wc = pygame.transform.smoothscale(wc, (
        width * enlarge // war_crafts[index][1], height * enlarge // war_crafts[index][1]))

        return wc

    def get_enemy(index1, index2):
        # 特别之处，敌机图片采用三维列表
        # 第一个索引所指向的二维数组表示某一个关卡内的敌机信息
        # 第二个索引表示当前关卡内的敌机图片
        enemys = [
            [
                ["./enemy/enemy1.png", 1],
                ["./enemy/enemy2.png", 2],
                ["./enemy/enemy4.png", 2],
                ["./enemy/enemy5.png", 2]
            ],
            [
                ["./enemy/pre1.png", 4],
                ["./enemy/pre2.png", 4],
                ["./enemy/pre3.png", 4],
                ["./enemy/pre4.png", 4],
                ["./enemy/pre5.png", 4],
                ["./enemy/pre6.png", 4],
                ["./enemy/pre7.png", 4],
                ["./enemy/pre8.png", 4],
            ],
        ]
        if index1 ==2:
            index1 = random.randint(0,1)
        enemy = pygame.image.load(enemys[index1][index2][0]).convert_alpha()
        width, height = enemy.get_size()
        enemy = pygame.transform.smoothscale(enemy,
                                             (width // enemys[index1][index2][1], height // enemys[index1][index2][1]))
        return enemy

    def get_boss(index):
        bosses = [
            ["./enemy/boss1.png", 2],
            ["./enemy/boss2.png", 2],
            ["./enemy/boss3.png", 2]
        ]
        boss = pygame.image.load(bosses[index][0]).convert_alpha()
        width, height = boss.get_size()
        boss = pygame.transform.smoothscale(boss, (width // bosses[index][1], height // bosses[index][1]))
        return boss

    def get_supplement(index):
        supplements = [
            ["./supplement/sp1.png", 2],  # 弹药补给，增强玩家攻击力
            ["./supplement/sp2.png", 2],  # 生命补给，增加一条生命
            ["./supplement/sp3.png", 2],  # 保护补给，增加一个保护罩
        ]
        sp = pygame.image.load(supplements[index][0]).convert_alpha()
        width, height = sp.get_size()
        sp = pygame.transform.smoothscale(sp, (width // supplements[index][1], height // supplements[index][1]))
        return sp



# 不同飞机开火的时间间隔不同，依据飞机属性type而定
time_delay = [0.23, 0.23, 0.23, 0.23, 1]

class Bullet():
    def __init__(self, initial_x: int, initial_y: int, bias: int, type: int, degree=90, isenemy: bool = False, isBoss = False):
        if not isenemy:
            self.img = WarCraftFactory.get_bullet(type)
        else:
            # 获取敌机子弹的图片
            if isBoss:
                self.img = WarCraftFactory.e_get_bullet(type+1)
            else :
                self.img = WarCraftFactory.e_get_bullet(0)

        self.speed = 20 + random.randint(3, 8)
        self.life = 200
        size = self.img.get_size()
        self.width = size[0]
        self.length = size[1]
        self.x = initial_x - self.width // 2
        self.y = initial_y - self.length // 2 - bias // 2 + 5
        self.collision_x = initial_x
        self.collision_y = initial_y
        self.degree = degree
        self.isenemy = isenemy
        self.type = type
        self.damage, self.speed_time = WarCraftFactory.get_bullet_damage(type)



# 战斗机类:
# 类成员：
# craft:bitmap 位图
# x:int:中心点x坐标 水平方向
# y:int:中心点y坐标 竖直方向
# width:飞机宽度 水平方向
# length:飞机长度 竖直方向
# 类操作:
# fire(): 开火

class Craft(Thread):

    def __init__(self, craft, x, y, width, length, type: int, life: int = 1, state: int = 0, isenemy: bool = False, isBoss =  False):
        Thread.__init__(self)

        self.reset_x = x
        self.reset_y = y
        self.reset_draw_x = x - width / 2
        self.reset_draw_y = y - length / 2


        self.craft = craft
        self.life = life
        self.width = width // 2
        self.daemon = True
        self.length = length // 2
        self.draw_x = x - width / 2
        self.draw_y = y - length / 2
        self.x = x
        self.y = y
        self.type = type
        self.speed_x = 10
        self.speed_y = 13
        self.state = state
        self.isenemy = isenemy
        self.stop = False
        self.isBoss = isBoss


    def reset(self):
        self.x = self.reset_x
        self.y = self.reset_y
        self.draw_x = self.reset_draw_x
        self.draw_y = self.reset_draw_y

    def __move_one_bullet__(self, bullet) -> None:
        while 0 < bullet.y < 600:
            if not bullet.isenemy:
                if bullet.degree == 90:
                    bullet.y -= bullet.speed
                    bullet.collision_y -= bullet.speed
                else:
                    bullet.x += bullet.speed * math.cos(math.radians(bullet.degree))
                    bullet.y -= bullet.speed * math.sin(math.radians(bullet.degree))
                    bullet.collision_x += bullet.speed * math.cos(math.radians(bullet.degree))
                    bullet.collision_y -= bullet.speed * math.sin(math.radians(bullet.degree))
            else:
                bullet.x -= bullet.speed * math.cos(math.radians(bullet.degree))
                bullet.y += bullet.speed * math.sin(math.radians(bullet.degree))
                bullet.collision_x -= bullet.speed * math.cos(math.radians(bullet.degree))
                bullet.collision_y += bullet.speed * math.sin(math.radians(bullet.degree))
            time.sleep(bullet.speed_time)
        else:
            try:
                bullet_list.remove(bullet)
            except:
               pass
    def fire(self):
        if self.state == 1:
            # 定义飞机攻击方式1：90度范围内，三路散射
            bullet1 = Bullet(self.x, self.y, self.width, self.type, degree=135, isenemy=self.isenemy)
            bullet_list.append(bullet1)
            bullet2 = Bullet(self.x, self.y, self.width, self.type, degree=90, isenemy=self.isenemy)
            bullet_list.append(bullet2)
            bullet3 = Bullet(self.x, self.y, self.width, self.type, degree=45, isenemy=self.isenemy)
            bullet_list.append(bullet3)
            bullet_move1 = Thread(target=self.__move_one_bullet__, args=(bullet1,))
            bullet_move2 = Thread(target=self.__move_one_bullet__, args=(bullet2,))
            bullet_move3 = Thread(target=self.__move_one_bullet__, args=(bullet3,))
            bullet_move1.start()
            bullet_move2.start()
            bullet_move3.start()
        elif self.state == 2:
            # 定义飞机攻击方式2：120度范围内，五路散射
            bullet1 = Bullet(self.x, self.y, self.width, self.type, degree=30, isenemy=self.isenemy)
            bullet_list.append(bullet1)
            bullet2 = Bullet(self.x, self.y, self.width, self.type, degree=60, isenemy=self.isenemy)
            bullet_list.append(bullet2)
            bullet3 = Bullet(self.x, self.y, self.width, self.type, degree=90, isenemy=self.isenemy)
            bullet_list.append(bullet3)
            bullet4 = Bullet(self.x, self.y, self.width, self.type, degree=120, isenemy=self.isenemy)
            bullet_list.append(bullet4)
            bullet5 = Bullet(self.x, self.y, self.width, self.type, degree=150, isenemy=self.isenemy)
            bullet_list.append(bullet5)
            bullet_move1 = Thread(target=self.__move_one_bullet__, args=(bullet1,))
            bullet_move2 = Thread(target=self.__move_one_bullet__, args=(bullet2,))
            bullet_move3 = Thread(target=self.__move_one_bullet__, args=(bullet3,))
            bullet_move4 = Thread(target=self.__move_one_bullet__, args=(bullet4,))
            bullet_move5 = Thread(target=self.__move_one_bullet__, args=(bullet5,))
            bullet_move1.start()
            bullet_move2.start()
            bullet_move3.start()
            bullet_move4.start()
            bullet_move5.start()
        elif self.state == 3:
            self.stop == True
        elif self.isBoss:
            if self.type==0:
                degree = list(range(0, 360))
                if self.life>=230:
                    degree = [de for de in degree if de % 16 == 0]
                    for de in degree:
                        bullet = Bullet(self.x, self.y, self.width, self.type, degree=de, isenemy=self.isenemy,isBoss=True)
                        bullet_list.append(bullet)
                        bullet_move = Thread(target=self.__move_one_bullet__, args=(bullet,))
                        bullet_move.start()
                        time.sleep(0.08)
                else:
                    degree = [de for de in degree if de % 14 == 0]
                    for de in degree:
                        bullet = Bullet(self.x, self.y, self.width, self.type, degree=de, isenemy=self.isenemy, isBoss=True)
                        bullet_list.append(bullet)
                        bullet_move = Thread(target=self.__move_one_bullet__, args=(bullet,))
                        bullet_move.start()
            elif self.type == 1:
                # 第二关BOSS攻击方式
                # print("第二关BOSS攻击方式")
                degree = list(range(0, 360))
                if self.life > 400:
                    pass
                else:
                    degree = [de for de in degree if de % 16 == 0]
                    for de in degree:
                        bullet = Bullet(self.x, self.y, self.width, self.type, degree=de, isenemy=self.isenemy,
                                        isBoss=True)
                        bullet_list.append(bullet)
                        bullet_move = Thread(target=self.__move_one_bullet__, args=(bullet,))
                        bullet_move.start()
            elif self.type == 2:
                print("第三关BOSS攻击方式")
                degree = list(range(0, 360))
                degree = [de for de in degree if de % 16 == 0]
                for de in degree:
                    bullet = Bullet(self.x, self.y, self.width, self.type, degree=de, isenemy=self.isenemy,
                                    isBoss=True)
                    bullet_list.append(bullet)
                    bullet_move = Thread(target=self.__move_one_bullet__, args=(bullet,))
                    bullet_move.start()


        else:
            # 飞机默认攻击方式，单路射击
            bullet = Bullet(self.x, self.y, self.width, self.type, isenemy=self.isenemy)
            bullet_list.append(bullet)
            bullet_move = Thread(target=self.__move_one_bullet__, args=(bullet,))
            bullet_move.start()

    def run(self):
        while True:
            self.fire()
            # 开火时间间隔
            if not self.isenemy:
                time.sleep(time_delay[self.type])
            else:
                time.sleep(2)
            # 如果敌机生命值小于等于0，终止该线程。
            if self.stop:
                break


class Supplement(Thread):
    def __init__(self, type: int, speed=10, eaten=False):
        Thread.__init__(self)
        self.img = WarCraftFactory.get_supplement(type)
        self.x = random.randint(10, 500)
        self.y = random.randint(10, 500)
        self.type = type
        self.width, self.length = self.img.get_size()
        self.speed = speed
        self.eaten = eaten

    def run(self):
        while True:
            try:
                randm_direction = random.randint(0, 3)
                # 向下移动
                if randm_direction == 0:
                    if self.x + self.speed < 600:
                        self.x += self.speed
                    else:
                        continue
                elif randm_direction == 1:
                    if self.x - self.speed > 0:
                        self.x -= self.speed
                    else:
                        continue
                elif randm_direction == 2:
                    if self.y + self.speed < 600:
                        self.y += self.speed
                    else:
                        continue
                elif randm_direction == 3:
                    if self.y - self.speed > 0:
                        self.y -= self.speed
                    else:
                        continue
                if self.eaten:
                    break
                time.sleep(0.02)
            except:
                print("supplement move error")


