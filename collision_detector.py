# len(obj)==4
# obj in [bullet, plane]
# obj[0]: x
# obj[1]: y
# obj[2]: width
# obj[3]: length
import random

from death import explo,Explode
import math
import time
from threading import Thread
from death import Laser

plane_list  = []
player_list = []
bullet_list = []
protect_bullet_list = []
laser_list = []
supplement_list = []
score = [0, 10]
enemy_attack=[]
explo_list = []


def add_plane(plane: object) -> None:
    plane_list.append(plane)
    if not plane.isenemy:
        player_list.append(plane)


def collision(bullet: [], plane: []) -> bool:
    # 采用欧氏距离度量碰撞
    safe_distance = min([plane[2], plane[3]])
    distance = math.sqrt(math.pow(bullet[0] - plane[0], 2) + math.pow(bullet[1] - plane[1], 2))
    if distance <= safe_distance:
        return True
    else:
        return False


# 敌机子弹与我机，我机子弹与敌机的碰撞检测函数
def global_collision(screen ) -> None:
    while True:
        try:
            for plane in plane_list:
                p = [plane.x, plane.y, plane.width, plane.length]
                for bullet in bullet_list:
                    b = [bullet.collision_x, bullet.collision_y, bullet.width, bullet.length]
                    if collision(b, p) and (plane.isenemy != bullet.isenemy):
                        plane.life -= bullet.damage
                        if bullet.type == 4: pass
                        else:
                            bullet_list.remove(bullet)
                        if plane.life <= 0:
                            plane.stop = True
                            # 移除飞机
                            plane_list.remove(plane)
                            score[0] += random.randint(1, 5)

                            explo = Explode(plane.x, plane.y)
                            explo.load(4,8)
                            explo_list.append(explo)

                            if not isinstance(plane, Protect) and plane.isBoss:
                                enemy_attack[0].passOne = True

                            if plane.isenemy == False:
                                # 如果是我方飞机，再从player里删除
                                if not isinstance(plane, Protect): score[1] -= 1
                                if not isinstance(plane, Protect) and plane.state == 3:
                                    laser_list.remove(plane.laser)
                                player_list.remove(plane)
            # 不需要一有资源就检测，0.01秒的检测间隔足够
            time.sleep(0.01)
        except ValueError as e: pass


# 旋转保护子弹的碰撞线程
def ano_thread(screen):
    while True:
        try:
            for plane in player_list:
                p = [plane.x, plane.y, plane.width, plane.length]
                # print("LEN BULLET LIST PRO {}" .format(len(protect_bullet_list)))
                for bullet in protect_bullet_list:
                    b = [bullet.collision_x, bullet.collision_y, bullet.width, bullet.length]
                    if not plane.isenemy and collision(b,p):
                        plane.life -= 2
                        if not isinstance(plane, Protect) and plane.state == 3:
                            laser_list.remove(plane.laser)
                        if plane.life <=0:
                            plane.stop = True
                            if not isinstance(plane, Protect) and not plane.isenemy:
                                score[1] -= 1
                            explo = Explode(plane.x, plane.y)
                            explo.load(4, 8)
                            explo_list.append(explo)
                            player_list.remove(plane)
                            plane_list.remove(plane)
            time.sleep(0.1)
        except ValueError as e:
            print(e)


def bullet_attack_protect(screen):
    while True:
        try:
            for protect_bullet in protect_bullet_list:
                p = [protect_bullet.x, protect_bullet.y, protect_bullet.width, protect_bullet.length]
                for bullet in bullet_list:
                    b = [bullet.collision_x, bullet.collision_y, bullet.width, bullet.length]
                    if not bullet.isenemy and collision(b, p):
                        protect_bullet.life -= 2
                        bullet_list.remove(bullet)
                        explo = Explode(protect_bullet.x, protect_bullet.y)
                        explo.load(4, 8)
                        explo_list.append(explo)
                        if protect_bullet.life <= 0:
                            protect_bullet_list.remove(protect_bullet)
            time.sleep(0.03)
        except ValueError as e:
            print(e)


# 敌机与我机的碰撞
def plane_collision() -> None:
    while True:
        try:
            for plane in plane_list:
                if plane.isenemy:
                    p1 = [plane.x, plane.y, plane.width, plane.length]
                    for player in player_list:
                        p2 = [player.x, player.y, player.width, player.length]
                        if collision(p1, p2):
                            # 如果我机和敌机碰撞，我机死亡，并同时给敌机造成巨大伤害
                            player.life -= 1
                            plane.life -= 10
                            if plane.life <= 0:
                                # 停止开火
                                if not isinstance(plane, Protect) and plane.isBoss:
                                    enemy_attack[0].ccc = True
                                    enemy_attack[0].change = True
                                    enemy_attack[0].existBoss = False
                                    enemy_attack[0].passOne = True
                                    score[0] += 100
                                plane.stop = True
                                # 移除敌机
                                plane_list.remove(plane)
                                score[0] += random.randint(1, 5)

                                if not isinstance(plane, Protect) and plane.state == 3:
                                    laser_list.remove(plane.laser)
                            if player.life <= 0:
                                player.stop = True
                                player_list.remove(player)
                                if not isinstance(player, Protect) and player.state == 3:
                                    laser_list.remove(player.laser)
            time.sleep(0.01)
        except ValueError:
            pass



# 保护罩
import pygame


class Protect(Thread):

    def __init__(self, craft):
        Thread.__init__(self)
        protect = pygame.image.load("protector.png").convert_alpha()
        self.protect = pygame.transform.smoothscale(protect, (protect.get_size()[0] // 15, protect.get_size()[1] // 15))
        self.isenemy = False
        self.p_r = protect.get_rect()
        self.life = 13
        self.craft = craft
        self.x = craft.x
        self.y = craft.y
        self.width, self.length = self.protect.get_size()
        self.degree = 0
        self.stop = False

    def run(self):
        while True:
            self.degree += 1
            self.x = self.craft.x
            self.y = self.craft.y
            time.sleep(1 / 360)
            self.degree %= 360
            if self.stop:
                break


def eat_supplement():
    while True:
        try:
            for s in supplement_list:
                s_inf = [s.x, s.y, s.width, s.length]
                for player in player_list:
                    pl_inf = [player.x, player.y, player.width, player.length]
                    if collision(s_inf, pl_inf):
                        if s.type == 0 and not isinstance(player, Protect):
                            player.state += (1 if player.state < 3 else 0)
                            if player.state == 3:
                                laser = Laser(player)
                                laser.load()
                                player.laser = laser
                                laser_list.append(laser)
                            time.sleep(0.01)
                            s.eaten = True
                            supplement_list.remove(s)
                        elif s.type == 1 and not isinstance(player, Protect):
                            protect = Protect(player)
                            protect.start()
                            add_plane(protect)
                            time.sleep(0.01)
                            s.eaten = True
                            supplement_list.remove(s)
                        elif s.type == 2 and not isinstance(player, Protect):
                            score[1] += 1
                            time.sleep(0.01)
                            s.eaten = True
                            supplement_list.remove(s)
                        elif s.type == 3 and not isinstance(player, Protect):
                            pass
            time.sleep(0.01)
        except:
            pass

# 激光攻击伤害
def laser_shoot(screen):
    while True:
        try:
            for laser in laser_list:
                for plane in plane_list:
                    if plane.isenemy:
                        if abs(plane.x - laser.x) < laser.width // 2 and plane.y < laser.craft.y:
                            plane.life -= 3
                            if plane.life <= 0:
                                if not isinstance(plane, Protect) and plane.isBoss:
                                    enemy_attack[0].ccc = True
                                    enemy_attack[0].change = True
                                    enemy_attack[0].existBoss = False
                                    enemy_attack[0].passOne = True
                                    score[0] += 100
                                plane.stop = True
                                plane_list.remove(plane)
                                score[0] += random.randint(1, 5)
                                t = Thread(target=explo, args=(screen, plane.x, plane.y))
                                t.start()

            time.sleep(0.1)
        except:
            print("laser error")


