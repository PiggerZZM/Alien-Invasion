import pygame


class Character():
    """游戏角色类"""

    def __init__(self, screen):
        self.screen = screen

        # 加载图象
        self.image = pygame.image.load(r"images/ZZM.gif")

    def draw_character(self):
        # 这里要注意.blit()方法的实现原理，第一个参数是Surface对象，表示要绘制的对象
        # 第二个参数是rect对象，绘制时取rect对象的左上角坐标作为Surface对象的左上角坐标
        screen_rect = self.screen.get_rect()
        image_rect = self.image.get_rect()
        image_rect.centerx = screen_rect.centerx
        image_rect.centery = screen_rect.centery

        self.screen.blit(self.image, image_rect)
