import pygame

from settings import Settings
from ship import Ship
from character import Character
from pygame.sprite import Group

import game_function as gf


def run_game():
    # 初始化游戏、设置并创建一个屏幕对象
    pygame.init()  # 初始化背景设置
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))  # 创建surface对象
    pygame.display.set_caption("Alien Invasion")

    # 创建一艘飞船
    ship = Ship(ai_settings, screen)

    # 创建一个用于存储子弹的编组
    bullets = Group()

    # 创建游戏角色
    character = Character(screen)

    # 开始游戏的主循环
    while True:

        # 监听事件
        gf.check_events(ai_settings=ai_settings, screen=screen, ship=ship, bullets=bullets)

        # 根据标志修改飞船位置
        ship.update()

        # 更新子弹位置
        bullets.update()

        # 删除已消失的子弹
        for bullet in bullets.copy():  # 这里创建副本来遍历，对原列表进行删除，实际上复杂度是O(n^2)，还没有考虑删除移动元素的开销
            if bullet.rect.bottom <= 0:  # 如果不用Group()直接用列表，是否能改进到O(n)?
                bullets.remove(bullet)  # 这里还不知道Group()内部实现是链表还是数组，对于子弹应当使用链表
        # print(len(bullets))

        # 更新屏幕
        gf.update_screen(ai_settings=ai_settings, screen=screen, ship=ship, character=character, bullets=bullets)


run_game()

