import pygame

from scoreboard import Scoreboard
from settings import Settings
from ship import Ship
from character import Character
from pygame.sprite import Group
from game_stats import GameStats
from button import Button

import game_function as gf


def run_game():
    # 初始化游戏、设置并创建一个屏幕对象
    pygame.init()  # 初始化背景设置
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))  # 创建surface对象
    pygame.display.set_caption("Alien Invasion")

    # 创建Play按钮
    play_button = Button(ai_settings, screen, "Play")

    # 创建一艘飞船
    ship = Ship(ai_settings, screen)

    # 创建一个用于存储子弹的编组
    bullets = Group()

    # 创建一组外星人
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # 创建游戏角色
    character = Character(screen)

    # 创建一个用于存储游戏统计信息的实例，并创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # 开始游戏的主循环
    while True:

        # 监听事件
        gf.check_events(ai_settings=ai_settings, screen=screen, stats=stats, play_button=play_button,
                        sb=sb, ship=ship, aliens=aliens, bullets=bullets)

        if stats.game_active:
            # 根据标志修改飞船位置
            ship.update()
            # 更新子弹
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            # 更新外星人
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)

        # 更新屏幕
        gf.update_screen(ai_settings=ai_settings, screen=screen, stats=stats, ship=ship, character=character,
                         aliens=aliens, bullets=bullets, play_button=play_button, sb=sb)


run_game()
