import pygame

from settings import Settings
from ship import Ship
from character import Character
from pygame.sprite import Group
from alien import Alien

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

    # 创建一个外星人
    alien = Alien(ai_settings, screen)

    # 创建游戏角色
    character = Character(screen)

    # 开始游戏的主循环
    while True:

        # 监听事件
        gf.check_events(ai_settings=ai_settings, screen=screen, ship=ship, bullets=bullets)

        # 根据标志修改飞船位置
        ship.update()

        # 更新子弹
        gf.update_bullets(bullets)

        # 更新屏幕
        gf.update_screen(ai_settings=ai_settings, screen=screen, ship=ship, character=character, bullets=bullets, alien=alien)


run_game()

