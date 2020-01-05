import pygame

from settings import Settings
from ship import Ship
from character import Character

import game_function as gf


def run_game():
    # 初始化游戏、设置并创建一个屏幕对象
    pygame.init()  # 初始化背景设置
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))  # 创建surface对象
    pygame.display.set_caption("Alien Invasion")

    # 创建一艘飞船
    ship = Ship(ai_settings, screen)

    # 创建游戏角色
    avatar = Character(screen)

    # 开始游戏的主循环
    while True:

        # 监听事件
        gf.check_events(ship)

        # 根据标志修改飞船位置
        ship.update()

        # 更新屏幕
        gf.update_screen(ai_settings, screen, ship, avatar)


run_game()

