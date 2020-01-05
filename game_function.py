import sys

import pygame


def check_events(ship):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        # 退出
        if event.type == pygame.QUIT:
            sys.exit()

        # 按下
        elif event.type == pygame.KEYDOWN:
            # 是→箭头
            if event.key == pygame.K_RIGHT:
                # 向右标志设为真
                ship.moving_right = True

        # 松开
        elif event.type == pygame.KEYUP:
            # 是→箭头
            if event.key == pygame.K_RIGHT:
                # 向右标志设为假
                ship.moving_right = False


def update_screen(ai_settings, screen, ship, avatar):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    avatar.draw_character()

    # 让最近绘制的屏幕可见
    pygame.display.flip()