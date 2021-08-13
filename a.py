import random
from threading import  Thread
from collision_detector import plane_list, add_plane, player_list, score,supplement_list
from var_move_mode import formation_mode1, fomation_mode2, formation_mode3
import time
from death import explo
from war_module import  WarCraftFactory, Craft, Supplement

class CreatEnemy(Thread):
    def __init__(self, round, existBoss = False):
        Thread.__init__(self)
        self.round = round
        self.existBoss = existBoss
    def run(self):
        while True:
            if not self.existBoss:
                type = random.randint(0, 3)
                p_x = random.randint(10, 600)
                enemy1 = WarCraftFactory.get_enemy(self.round, type)
                if type == 3:
                    life = 5
                else:
                    life = 2
                enemy1 = Craft(enemy1, p_x, 0, enemy1.get_size()[0], enemy1.get_size()[1], 3, life=life, isenemy=True)
                add_plane(enemy1)
                enemy1.start()
                time.sleep(3)
            else:
                break


move_mode = []
class EnemyMoveMode0(Thread):
    def __init__(self, existBoss=False):
        Thread.__init__(self)
        self.existBoss = existBoss
    def run(self):
        while True:
            try:
                for enemy in plane_list:
                    if enemy.isenemy:
                        enemy.y += 5
                        enemy.draw_y += 5
                        if enemy.y > 600:
                            # 敌机飞出地图范围，关闭开火线程
                            enemy.stop = True
                            # 删除敌机
                            plane_list.remove(enemy)
                time.sleep(0.05)
                if self.existBoss :
                    break
            except ValueError:
                pass

class EnemyMoveMode1(Thread):
    def __init__(self,  existBoss=False):
        Thread.__init__(self)
        self.existBoss = existBoss
    def run(self):
        direction = 1
        while True:
            try:
                for enemy in plane_list:
                    if enemy.isenemy:
                        if 0 < enemy.x + 5 < 600:
                            enemy.x += direction * 5
                            enemy.draw_x += direction * 5
                        elif enemy.x + 5 >= 600:
                            direction = -1
                            enemy.x += direction * 5
                            enemy.draw_x += direction * 5
                        elif enemy.x - 5 <= 0:
                            direction = 1
                            enemy.x += direction * 5
                            enemy.draw_x += direction * 5
                time.sleep(0.05)
                if self.existBoss:
                    break
            except ValueError:
                pass

class EnemyMoveMode1and0(Thread):
    def __init__(self,  existBoss=False):
        Thread.__init__(self)
        self.existBoss = existBoss
    def run(self):
        direction = 1
        while True:
            try:
                for enemy in plane_list:
                    if enemy.isenemy:
                        enemy.y += 5
                        enemy.draw_y += 5
                        if enemy.y > 600:
                            # 敌机飞出地图范围，关闭开火线程
                            enemy.stop = True
                            # 删除敌机
                            plane_list.remove(enemy)

                        if 0 < enemy.x + 5 < 600:
                            enemy.x += direction * 5
                            enemy.draw_x += direction * 5
                        elif enemy.x + 5 >= 600:
                            direction = -1
                            enemy.x += direction * 5
                            enemy.draw_x += direction * 5
                        elif enemy.x - 5 <= 0:
                            direction = 1
                            enemy.x += direction * 5
                            enemy.draw_x += direction * 5
                time.sleep(0.05)
                if self.existBoss:
                    break
            except ValueError:
                pass


class EnemyMoveMode2(Thread):
    def __init__(self,  existBoss=False):
        Thread.__init__(self)
        self.existBoss = existBoss
    def run(self):
        while True:
            try:
                for enemy in plane_list:
                    if enemy.isenemy:
                        # enemy.y += 3
                        # enemy.draw_y += 3
                        for player in player_list:
                            if enemy.x <= player.x:
                                enemy.x += 0.1 * enemy.y
                                enemy.draw_x += 0.1 * enemy.y
                            if enemy.x >= player.x:
                                enemy.x -= 0.1 * enemy.y
                                enemy.draw_x -= 0.1 * enemy.y
                        if enemy.y > 600:
                            # 敌机飞出地图范围，关闭开火线程
                            enemy.stop = True
                            # 删除敌机
                            plane_list.remove(enemy)
                time.sleep(0.05)
                if self.existBoss :
                    break
            except ValueError:
                pass



class  EnemyMoveMode3(Thread):
    def __init__(self, existBoss=False):
        Thread.__init__(self)
        self.existBoss = existBoss

    def run(self):
        while True:
            try:
                for enemy in plane_list:
                    if enemy.isenemy:
                        enemy.y += 3
                        enemy.draw_y += 3
                        for player in player_list:
                            while enemy.y >= player.y:
                                enemy.y -= 6
                                enemy.draw_y -= 6
                            if enemy.x <= player.x:
                                enemy.x += 0.5
                                enemy.draw_x += 0.5
                            # if enemy.x >= player.x:
                            #     enemy.x -= 0.5
                            #     enemy.draw_x -= 0.5
                        if enemy.y > 600:
                            # 敌机飞出地图范围，关闭开火线程
                            enemy.stop = True
                            # 删除敌机
                            plane_list.remove(enemy)
                time.sleep(0.02)
                if self.existBoss :
                    break
            except ValueError:
                pass




class SupplementFactory(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.stop = False
        self.existBoss = len(boss_list)
    def run(self):
        while True:
            # 没有boss提供所有补给
            if not self.existBoss:
                type = random.randint(0,2)
            else :
            # 有boss仅提供火力补给
                type = 0
            supplement = Supplement(type)
            supplement_list.append(supplement)
            supplement.run()
            time.sleep(10)

            self.existBoss = len(boss_list)
            if self.stop:
                break






class EnemyAttack(Thread):

    def __init__(self, round, existBoss=False):
        Thread.__init__(self)
        self.round = round
        self.existBoss = existBoss
        self.change = True
        self.ccc = True
        self.passOne = False
        creatEnemy = CreatEnemy(round=self.round)
        self.creat_enemy = creatEnemy
        self.stop=False
    def run(self):
        sleep = [3, 5, 5]
        self.creat_enemy.start()
        while True:

            if self.ccc:
                creatEnemy = CreatEnemy(round=self.round)
                self.creat_enemy = creatEnemy
                self.ccc = False
                self.creat_enemy.round += 1
            if  self.change:
                self.change = False
                # 停止之前的所有移动模式
                for mode in move_mode:
                    mode.existBoss = True
                    move_mode.remove(mode)
                move_mode.clear()
                if not self.existBoss:
                    if self.round == 0:
                        # 第一关小兵的移动模式
                        mode = EnemyMoveMode0()
                        mode.start()
                        move_mode.append(mode)
                    elif self.round == 1:
                        # 第二关小兵移动模式
                        mode0 = EnemyMoveMode1and0()
                        mode0.start()
                        move_mode.append(mode0)
                    elif self.round ==2:
                        # 第三关小兵移动模式
                        mode = EnemyMoveMode3()
                        mode.start()
                        move_mode.append(mode)

                elif self.existBoss:
                    # BOSS移动模式
                    mode = EnemyMoveMode1()
                    mode.start()
                    move_mode.append(mode)
                    self.creat_enemy.existBoss=True
            else:
                if not self.existBoss:
                    if self.round == 0:
                        # 第一关小兵布阵方式
                        c = random.randint(0, 1)
                        if c == 0:
                            formation_mode1(self.round)
                    elif self.round == 1:
                        # 第二关小兵布阵方式
                        c = random.randint(0, 2)
                        if c == 0:
                            formation_mode1(self.round)
                        elif c == 1:
                            fomation_mode2(self.round)
                        elif c == 2:
                            formation_mode3(self.round)
                    elif self.round == 2:
                        # 第二关小兵布阵方式
                        c = random.randint(0, 2)
                        if c == 0:
                            formation_mode1(self.round)
                        elif c == 1:
                            fomation_mode2(self.round)
                        elif c == 2:
                            formation_mode3(self.round)
                    time.sleep(sleep[self.round])
            if self.stop: break
            time.sleep(0.1)




# 负责何时产生BOSS的类，并不对BOSS行为进行控制
boss_list=[]
class Boss(Thread):
    def __init__(self,enemy_attack, screen):
        Thread.__init__(self)
        self.round = enemy_attack[0].round
        self.enemy_attack = enemy_attack[0]
        self.creat_enemy = enemy_attack[0].creat_enemy
        self.exist = False
        self.screen = screen
        self.stop = False

    def run(self) -> None:
        while True:
            if not self.exist:
                if score[0]>=580:
                    # 第三关boss
                    for enemy in plane_list:
                        if enemy.isenemy:
                            enemy.life = -1
                            enemy.stop = True
                            t = Thread(target=explo, args=(self.screen, enemy.x, enemy.y))
                            t.start()
                            plane_list.remove(enemy)
                    self.creat_enemy.existBoss = True
                    self.enemy_attack.existBoss = True
                    self.enemy_attack.change =    True
                    self.exist = True
                    time.sleep(3)
                    boss = WarCraftFactory.get_boss(self.round)
                    boss = Craft(boss,300,200,boss.get_size()[0], boss.get_size()[1],type=self.round, isenemy=True,life=700, isBoss =True)
                    add_plane(boss)
                    boss_list.append(boss)
                    time.sleep(3)
                    boss.start()
                elif 430>score[0]>=330:
                    # 第二关boss
                    for enemy in plane_list:
                        if enemy.isenemy:
                            enemy.life = -1
                            enemy.stop = True
                            t = Thread(target=explo, args=(self.screen, enemy.x, enemy.y))
                            t.start()
                            plane_list.remove(enemy)
                    self.creat_enemy.existBoss = True
                    self.enemy_attack.existBoss = True
                    self.enemy_attack.change = True
                    self.exist = True
                    time.sleep(3)

                    boss = WarCraftFactory.get_boss(self.round)
                    boss = Craft(boss,300,150,boss.get_size()[0], boss.get_size()[1],type=self.round, isenemy=True,life=700, isBoss =True)
                    add_plane(boss)
                    boss_list.append(boss)

                    time.sleep(3)
                    boss.start()
                elif 50<=score[0]<150:
                    # 第一关Boss
                    for enemy in plane_list:
                        if enemy.isenemy:
                            enemy.life = -1
                            enemy.stop = True
                            t = Thread(target=explo, args=(self.screen, enemy.x, enemy.y))
                            t.start()
                            plane_list.remove(enemy)


                    self.enemy_attack.existBoss = True
                    self.enemy_attack.change = True
                    self.exist = True
                    self.creat_enemy.existBoss = True

                    time.sleep(3)

                    boss = WarCraftFactory.get_boss(self.round)
                    boss = Craft(boss, 300, 200, boss.get_size()[0], boss.get_size()[1],self.round, isenemy=True, life=500,isBoss=True)
                    add_plane(boss)

                    time.sleep(3)
                    boss.start()
            if self.stop:
                # boss被终结
                break
            time.sleep(2)


