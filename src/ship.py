import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """初始化飞船并设置其初始位置"""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load(r"../images/ship.gif")  # .load()方法返回这个图象的surface
        self.rect = self.image.get_rect()  # .get_rect()方法获取相应surface的rect属性
        self.screen_rect = screen.get_rect()

        # rect对象中有若干属性来表示这个对象在屏幕中的位置：
        # 属性centerx, centery表示中心的x,y坐标
        # 属性top、bottom、left、right表示矩形四边的位置
        # 属性x,y表示矩形左上角的坐标

        # 将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx  # 令飞船的中心x坐标与屏幕的x坐标相同
        self.rect.bottom = self.screen_rect.bottom   # 令飞船的底部与屏幕的底部相同

        # 在飞船的属性center中存储小数值
        self.center = float(self.rect.centerx)
        self.bottom = float(self.rect.bottom)

        # 移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """根据移动标志调整飞船的位置"""
        # 更新center而不是centerx
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        # 这里注意用两个if来实现同时按下不移动，如果用elif则会导致右箭头始终处于优先判断
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.center -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.bottom += self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.bottom -= self.ai_settings.ship_speed_factor

        # 根据self.center更新rect对象
        self.rect.centerx = self.center
        self.rect.bottom = self.bottom

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)  # .blit()方法根据rect指定的位置将image绘制到屏幕

    def center_ship(self):
        """让飞船在屏幕上居中"""
        self.center = self.screen_rect.centerx
        self.bottom = self.screen_rect.bottom
