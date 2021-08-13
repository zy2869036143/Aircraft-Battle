import pygame
from pygame.locals import *


# 爆炸精灵
class Explode(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.frame_width = 0
        self.frame_height = 0
        self.rect = 0, 0, 0, 0
        self.columns = 0
        self.last_frame = 1
        self.last_time = 0
        self.frame = 0
        self.first_frame = 0
        self.old_frame = 0
        self.x = x
        self.y = y

    def load(self, row=4, columns=8):
        self.master_image = pygame.image.load("explotion.png").convert_alpha()  # 载入整张图片
        self.master_rect = self.master_image.get_rect()  # 获取图片的rect值
        self.frame_width = self.master_rect.width // columns  # 计算单一帧的宽度
        self.frame_height = self.master_rect.height // row  # 计算单一帧的高度
        self.rect = self.x - self.frame_width // 2, self.y, self.frame_width, self.frame_height  # 更新rect
        self.columns = columns  # 存储列的值（用以后续计算）
        self.last_frame = row * columns - 1  # 计算是有0开始的，需要 -1
        self.end = False

    def update(self, screen):
        self.frame += 1  # 帧序号 +1
        if self.frame == self.last_frame:
            self.end = True  # 终止播放
        elif self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width  # 计算 subsurface 的 x 坐标
            frame_y = (self.frame // self.columns) * self.frame_height  # 计算 subsurface 的 y 坐标

            rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)  # 获取subsurface 的 rect
            self.image = self.master_image.subsurface(rect)  # 更新self.image
            self.old_frame = self.frame  # 更新self.old_frame
        screen.blit(self.image, self.rect)  # 显示图像


def explo(screen, x, y):
    my_explode = Explode(x, y)
    my_explode.load(4, 8)
    framerate = pygame.time.Clock()
    try:
        while True:
            framerate.tick(100)
            pygame.display.update()
            my_explode.update(screen)
            if my_explode.end:
                break
    except ValueError:
        pass


# 激光控制精灵
class Laser(pygame.sprite.Sprite):
    def __init__(self, craft):
        self.frame_width = 0
        self.frame_height = 0
        self.rect = 0, 0, 0, 0
        self.columns = 0
        self.last_frame = 1
        self.last_time = 0
        self.frame = 0
        self.first_frame = 0
        self.old_frame = 0
        self.x = craft.x
        self.y = craft.y
        self.craft = craft

    def load(self, row=2, columns=4):
        master_image = pygame.image.load("laser.png").convert_alpha()  # 载入整张图片
        w, h = master_image.get_size()
        self.master_image = pygame.transform.smoothscale(master_image, (w * 3 // 2, h // 2))
        self.master_rect = self.master_image.get_rect()  # 获取图片的rect值
        self.frame_width = self.master_rect.width // columns  # 计算单一帧的宽度
        self.frame_height = self.master_rect.height // row  # 计算单一帧的高度
        self.rect = self.craft.x - self.frame_height // 2, self.craft.y - self.frame_width, self.frame_height, self.frame_width  # 更新rect
        self.columns = columns  # 存储列的值（用以后续计算）
        self.last_frame = row * columns - 1  # 计算是有0开始的，需要 -1
        self.end = False
        self.width = self.frame_height
        self.length = self.frame_width

    def update(self, screen):
        self.rect = self.craft.x - self.frame_height // 2, self.craft.y - self.frame_width, self.frame_height, self.frame_width
        self.frame += 1
        self.x = self.craft.x
        # 帧序号 +1
        if self.frame >= self.last_frame:
            self.frame = self.first_frame  # 循环播放
        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width  # 计算 subsurface 的 x 坐标
            frame_y = (self.frame // self.columns) * self.frame_height  # 计算 subsurface 的 y 坐标
            rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)  # 获取subsurface 的 rect
            self.image = self.master_image.subsurface(rect)  # 更新self.image
            self.old_frame = self.frame  # 更新self.old_frame
        screen.blit(pygame.transform.rotate(self.image, 90), self.rect)
