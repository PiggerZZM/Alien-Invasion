import pygame


class Ship():

    def __init__(self, screen):
        """初始化飞船并设置其初始位置"""
        self.screen = screen

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load(r"images/ship.bmp")  # .load()方法返回这个图象的surface
        self.rect = self.image.get_rect()  # .get_rect()方法获取相应surface的rect属性
        self.screen_rect = screen.get_rect()

        # rect对象中有若干属性来表示这个对象在屏幕中的位置：
        # 属性centerx, centery表示中心的x,y坐标
        # 属性top、bottom、left、right表示矩形四边的位置
        # 属性x,y表示矩形左上角的坐标

        # 将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx  # 令飞船的中心x坐标与屏幕的x坐标相同
        self.rect.bottom = self.screen_rect.bottom   # 令飞船的底部与屏幕的底部相同

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)  # .blit()方法根据rect指定的位置将image绘制到屏幕


