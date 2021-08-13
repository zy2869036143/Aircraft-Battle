import sys
import pygame.display
from war_module import *
from pygame.locals import *
from collision_detector import *
from collision_detector import enemy_attack as enemy_attack_thread
from mainpage import main
from chose_plane import get_type
from a import EnemyAttack, Boss, boss_list, SupplementFactory
from checkpointchoice import checkpointchoice


radius = [200]
class RadiusPluse(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.diri = 1
        self.stop = False

    def run(self):
        while True:
            radius[0] += self.diri
            if radius[0] >= 500:
                self.diri = -1
            elif radius[0] <= 100:
                self.diri = 1
            time.sleep(0.01)

            if self.stop:
                break


def rotate(number: int):
    infor = []
    for i in range(0, number):

        ship = WarCraftFactory.e_get_bullet(2)
        width, height = ship.get_size()
        ship = pygame.transform.smoothscale(ship, (width, height))

        protect_bullet = Bullet(0, 0, 5, 1, degree=0, isenemy=True, isBoss=True)
        protect_bullet.img = ship
        protect_bullet_list.append(protect_bullet)

        bullet_list.append(protect_bullet)
        infor.append([protect_bullet, i * 360.0 / number, Point(0, 0), Point(0, 0)])

    return infor


class MyMap(pygame.sprite.Sprite):

    def __init__(self, x, y, round=0):
        maps = [
            ["./map/space.png", 1],
            ["./map/map0.png", 2],
            ["./map/map30.png", 2]
        ]

        self.x = x
        self.y = y
        self.bg = pygame.image.load(maps[round][0]).convert_alpha()

    def map_rolling(self):
        if self.y < -600:
            self.y = 600
        else:
            self.y -= 4

    def map_update(self):
        screen.blit(self.bg, (self.x, self.y))
        pygame.display.update()

    def set_pos(self, x, y):
        self.x = x
        self.y = y


class mapgo(Thread):
    def __init__(self, m1, m2):
        Thread.__init__(self)
        self.stop = False
        self.m1 = m1
        self.m2 = m2

    def run(self):
        while True:
            self.m1.map_rolling()
            self.m2.map_rolling()
            time.sleep(0.01)
            if self.stop:
                break


boss_current = None
infor = []


# ************************************
def asdasdasda(radius_pluse):
    first_rotate = True
    second_rotate = True
    while True:
        # print("未进入")
        bias = 180
        try:
            if enemy_attack_thread[0].round == 1 and enemy_attack_thread[0].existBoss:

                if first_rotate:
                    print("__FIRST_________ROTATE(12)___________")
                    infor = rotate(12)
                    first_rotate = False
                for protect_bu, angle, pos, old_pos in infor:

                    # move the ship
                    angle = wrap_angle(angle - 0.1)
                    pos.x = math.sin(math.radians(angle)) * radius[0]
                    pos.y = math.cos(math.radians(angle)) * radius[0]

                    # rotate the ship
                    delta_x = (pos.x - old_pos.x)
                    delta_y = (pos.y - old_pos.y)
                    rangle = math.atan2(delta_y, delta_x)
                    rangled = wrap_angle(-math.degrees(rangle))

                    scratch_ship = pygame.transform.rotate(protect_bu.img, rangled + bias)

                    old_pos.x = pos.x
                    old_pos.y = pos.y
                    # draw the ship
                    protect_bu.degree = rangled + bias

                    width, height = scratch_ship.get_size()
                    try:
                        x = boss_list[0].x + pos.x - width // 2
                        y = boss_list[0].y + pos.y - height // 2

                        protect_bu.x = x
                        protect_bu.y = y
                        protect_bu.collision_y = y + height // 2
                        protect_bu.collision_x = x + width // 2

                        if 180 <= boss_list[0].life <= 400:
                            bias = 90
                            radius[0] = 200
                            radius_pluse.stop
                        elif boss_list[0].life < 180:
                            bias = 180
                            if second_rotate:
                                protect_bullet_list.clear()
                                infor = rotate(12)
                                second_rotate = False

                        for index in range(0, len(infor)):
                            infor[index][1] -= 0.1
                    except IndexError:
                        pass
            else:
                first_rotate = True
                second_rotate = True
                protect_bullet_list.clear()
            time.sleep(0.01)
        except IndexError:
            pass


# *************************************************


def print_text(font, x, y, text, color=(255, 255, 255)):
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x, y))


def wrap_angle(angle):
    return angle % 360



pygame.init()

font = pygame.font.Font("typeface1.TTF", 20)
font_large = pygame.font.Font("typeface1.TTF", 100)

scn_w = 600
scn_h = 600

screen = pygame.display.set_mode((scn_w, scn_h))


# 子弹与飞机的碰撞检测线程，专门负责检测碰撞，更新屏幕上的所有对象
collision_thread = Thread(target=global_collision, args=(screen,))
collision_thread.start()

# 敌我阵营飞机的碰撞检测线程
plane_collision_thread = Thread(target=plane_collision)
plane_collision_thread.start()

# 激光控制线程
laser_thread = Thread(target=laser_shoot, args=(screen,))
laser_thread.start()

# 检测是否吃到补给的线程
supp_thread = Thread(target=eat_supplement)
supp_thread.start()

# 玩家破坏保护子弹的线程
attack_protect_thread = Thread(target=bullet_attack_protect, args=(screen,))
attack_protect_thread.start()

# 保护子弹攻击玩家的线程
thread = Thread(target=ano_thread, args=(screen,))
thread.start()

# 保护子弹旋转半径的控制
radius_plus_thread = RadiusPluse()
radius_plus_thread.start()

#
旋转 = Thread(target=asdasdasda, args=(radius_plus_thread,))
旋转.start()

# 初始界面，玩家点击的按钮
# 返回一个整数值
# 返回1 表示单人游戏
# 返回2 表示双人游戏
# 其他未定，有待补充

while True:

    choice = main()
    pygame.key.set_repeat(1000, 1)
    first = True

    # 设置窗口标题
    pygame.display.set_caption("飞机大战")
    if choice == 1:
        type = get_type()
        craft = WarCraftFactory.get_war_craft(type)
        craft = Craft(craft, 300, scn_h, craft.get_size()[0], craft.get_size()[1], type, state=0)
        craft.start()
        add_plane(craft)
    elif choice == 2:
        type = get_type()
        type2 = get_type(chosen=type + 1)
        craft = WarCraftFactory.get_war_craft(type)
        craft = Craft(craft, scn_w // 3, scn_h, craft.get_size()[0], craft.get_size()[1], type, state=2)
        craft.start()
        add_plane(craft)

        craft2 = WarCraftFactory.get_war_craft(type2)
        craft2 = Craft(craft2, 2 * scn_w // 3, scn_h, craft2.get_size()[0], craft2.get_size()[1], type2, state=2)
        craft2.start()
        add_plane(craft2)

    # 粘连键设置
    pygame.key.set_repeat(8, 50)

    round = checkpointchoice()

    enemy_attack = EnemyAttack(round)
    enemy_attack_thread.append(enemy_attack)

    boss = Boss(enemy_attack_thread, screen)
    boss.start()

    if round == 1:
        score[0] = 150
    elif round == 2:
        score[0] = 430
    first = True

    allPass = False
    while not allPass and score[1] >= 0:

        m1 = MyMap(0, 0, round)
        m2 = MyMap(0, 600, round)

        m1.map_update()
        print_text(font_large, 200, 290, "预备:3")
        pygame.display.update()
        time.sleep(1)
        m1.map_update()
        print_text(font_large, 200, 290, "预备:2")
        pygame.display.update()
        time.sleep(1)
        m1.map_update()
        print_text(font_large, 200, 290, "预备:1")
        pygame.display.update()
        time.sleep(1)
        m1.map_update()
        print_text(font_large, 100, 285, "关卡{}开始".format(round + 1))
        pygame.display.update()
        time.sleep(1)

        if first:
            first = False
            print("开始闯关")
            enemy_attack_thread[0].start()

        map_thread = mapgo(m1, m2)
        map_thread.start()

        produce_suplement = SupplementFactory()
        produce_suplement.start()

        # # 子弹与飞机的碰撞检测线程，专门负责检测碰撞，更新屏幕上的所有对象
        # collision_thread = Thread(target=global_collision, args=(screen,))
        # collision_thread.start()

        # 补给物品
        sup = Supplement(0)
        sup.start()
        supplement_list.append(sup)

        sup = Supplement(1)
        sup.start()
        supplement_list.append(sup)

        sup = Supplement(2)
        sup.start()
        supplement_list.append(sup)

        while True:
            # 多按键控制
            # clock.tick(10000)

            # 地图绘制
            screen.blit(m1.bg, (0, m1.y))
            screen.blit(m2.bg, (0, m2.y))

            # 按键控制
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if choice == 1:
                        if keys[K_ESCAPE]:
                            pygame.quit()
                            sys.exit()
                        if keys[K_w] and craft.y - craft.speed_y > 0:
                            craft.draw_y -= craft.speed_y
                            craft.y -= craft.speed_y
                        if keys[K_a] and craft.x - craft.speed_x > 0:
                            craft.x -= craft.speed_x
                            craft.draw_x -= craft.speed_x
                        if keys[K_s] and craft.y - craft.speed_y < scn_h - craft.length:
                            craft.draw_y += craft.speed_y
                            craft.y += craft.speed_y
                        if keys[K_d] and craft.x + craft.speed_x < scn_w:
                            craft.x += craft.speed_x
                            craft.draw_x += craft.speed_x

                        if keys[K_f] and craft.life <= 0:
                            craft = WarCraftFactory.get_war_craft(type)
                            craft = Craft(craft, 300, scn_h, craft.get_size()[0], craft.get_size()[1], type, state=0)
                            craft.start()
                            add_plane(craft)
                            protect = Protect(craft)
                            protect.start()
                            add_plane(protect)


                    elif choice == 2:

                        if keys[K_ESCAPE]:
                            sys.exit()
                        if keys[K_w] and craft.y - craft.speed_y > 0:
                            craft.draw_y -= craft.speed_y
                            craft.y -= craft.speed_y
                        if keys[K_a] and craft.x - craft.speed_x > 0:
                            craft.x -= craft.speed_x
                            craft.draw_x -= craft.speed_x
                        if keys[K_s] and craft.y - craft.speed_y < scn_h - craft.length:
                            craft.draw_y += craft.speed_y
                            craft.y += craft.speed_y
                        if keys[K_d] and craft.x + craft.speed_x < scn_w:
                            craft.x += craft.speed_x
                            craft.draw_x += craft.speed_x

                        if keys[K_f] and craft.life <= 0:
                            craft = WarCraftFactory.get_war_craft(type)
                            craft = Craft(craft, scn_w // 3, scn_h, craft.get_size()[0], craft.get_size()[1], type,
                                          state=0)
                            craft.start()
                            add_plane(craft)
                            protect = Protect(craft)
                            protect.start()
                            add_plane(protect)
                        if craft.life <= 0:
                            print_text(font, 0, 560, "按F键复活")

                        if keys[K_UP] and craft2.y - craft2.speed_y > 0:
                            craft2.draw_y -= craft2.speed_y
                            craft2.y -= craft2.speed_y
                        if keys[K_LEFT] and craft2.x - craft2.speed_x > 0:
                            craft2.x -= craft2.speed_x
                            craft2.draw_x -= craft2.speed_x
                        if keys[K_DOWN] and craft2.y - craft2.speed_y < scn_h - craft2.length:
                            craft2.draw_y += craft2.speed_y
                            craft2.y += craft2.speed_y
                        if keys[K_RIGHT] and craft2.x + craft2.speed_x < scn_w:
                            craft2.x += craft2.speed_x
                            craft2.draw_x += craft2.speed_x

                        if keys[K_m] and craft2.life <= 0:
                            craft2 = WarCraftFactory.get_war_craft(type2)
                            craft2 = Craft(craft2, 2 * scn_w // 3, scn_h, craft2.get_size()[0], craft2.get_size()[1],
                                           type2, state=0)
                            craft2.start()
                            add_plane(craft2)
                            protect = Protect(craft2)
                            protect.start()
                            add_plane(protect)

            # 玩家飞机的绘制
            for craft001 in player_list:
                if not isinstance(craft001, Protect):
                    screen.blit(craft001.craft, (craft001.draw_x, craft001.draw_y))
                else:
                    craft001.p_r.center = (craft.x, craft.y)
                    screen.blit(pygame.transform.rotate(craft001.protect, craft001.degree),
                                (craft001.x - 110, craft001.y - 120))

            # 复活提示信息的绘制
            if craft.life <= 0 and score[1] >= 0:
                print_text(font, 0, 560, "按F键复活")
            try:
                if craft2.life <= 0 and score[1] >= 0:
                    print_text(font, 500, 580, "按M键复活")
            except Exception:
                pass

            # 第二关BOSS旋转的保护子弹的绘制
            try:
                if enemy_attack.round == 1 and boss_list[0].life >= 0 and enemy_attack.existBoss:
                    for protect_bu in protect_bullet_list:
                        screen.blit(pygame.transform.rotate(protect_bu.img, protect_bu.degree),
                                    (protect_bu.x, protect_bu.y))
            except IndexError:
                pass

            # 补给物品的绘制
            for s in supplement_list:
                screen.blit(s.img, (s.x, s.y))

            # 绘制玩家战斗机的所有子弹。设置了偏转角度后的绘制。
            for bullet in bullet_list:
                if bullet.degree > 90:
                    screen.blit(pygame.transform.rotate(bullet.img, bullet.degree - 90),
                                (bullet.x - bullet.length * math.cos(math.radians(180 - bullet.degree)), bullet.y))
                else:
                    screen.blit(pygame.transform.rotate(bullet.img, bullet.degree - 90), (bullet.x, bullet.y))

            # 敌方飞机的绘制
            for enemy in plane_list:
                if enemy.isenemy:
                    screen.blit(enemy.craft, (enemy.draw_x, enemy.draw_y))
                    if enemy.isBoss:
                        boss_current = enemy
                        print_text(font, 250, 20, "BOSS生命值:{}".format(enemy.life))

            # 爆炸效果的绘制
            for explo in explo_list:
                explo.update(screen)
                if explo.end:
                    explo_list.remove(explo)

            # 绘制玩家激光图片
            for laser in laser_list:
                laser.update(screen)

            # 飞机阵亡的处理
            if score[1] < 0:
                for player in player_list:
                    player.stop = True
                player_list.clear()
                break

            print_text(font, 0, 0, "得分: " + "{}".format(score[0]))
            print_text(font, 0, 580, "生命值{}".format(score[1]))

            pygame.display.update()

            # 过关提示
            if enemy_attack.passOne:
                print("end___")
                break

        # 玩家没有通过某一关
        if score[1] < 0 and len(player_list) == 0:
            print("玩家死亡")
            enemy_attack_thread[0].stop = True

            for plane in plane_list:
                plane.stop = True
                plane_list.remove(plane)
            for player in player_list:
                player.stop = True
                player_list.remove(player)

            bullet_list.clear()
            player_list.clear()
            boss_list.clear()
            laser_list.clear()
            plane_list.clear()
            enemy_attack_thread.clear()

            time.sleep(1)

            produce_suplement.stop = True
            boss.stop = True
            print_text(font_large, 50, 300, "游戏失败！")
            pygame.display.update()
            score[1] = 10
            score[0] = 0
            time.sleep(3)

            break
        else:
            # 玩家顺利通过某一关
            print("玩家通关")
            for player in player_list:
                if not isinstance(player, Protect):
                    while player.y > 0:
                        player.y -= 5
                        player.draw_y -= 5

                        for craft001 in player_list:
                            if not isinstance(craft001, Protect):
                                screen.blit(craft001.craft, (craft001.draw_x, craft001.draw_y))
                            else:
                                craft001.p_r.center = (craft.x, craft.y)
                                screen.blit(pygame.transform.rotate(craft001.protect, craft001.degree),
                                            (craft001.x - 110, craft001.y - 120))
                        pygame.display.update()
                        time.sleep(0.01)

            try:
                for player in player_list:
                    if isinstance(player, Craft):
                        player.reset()

                enemy_attack_thread[0].passOne = False
                enemy_attack_thread[0].change = True
                map_thread.stop = True
                round += 1
                boss.exist = False
                boss.round += 1
                score[0] += 100

                enemy_attack_thread[0].round += 1
                if enemy_attack_thread[0].round >= 3:
                    allPass = True
            except Exception:
                pass
