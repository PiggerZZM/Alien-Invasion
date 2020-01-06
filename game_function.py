import sys
import pygame

from bullet import Bullet


def check_events(ai_settings, screen, ship, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        # 退出
        if event.type == pygame.QUIT:
            sys.exit()

        # 按下
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        # 松开
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """响应按键"""
    # 是→箭头
    if event.key == pygame.K_RIGHT:
        # 向右标志设为真
        ship.moving_right = True
    # 是←箭头
    elif event.key == pygame.K_LEFT:
        # 向左标志设为真
        ship.moving_left = True
    # 空格
    elif event.key == pygame.K_SPACE:
        # 创建一颗子弹，并将其加入到编组bullets中
        if len(bullets) < ai_settings.bullets_allowed:  # 检查子弹数量
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)


def check_keyup_events(event, ship):
    """响应松开"""
    # 是→箭头
    if event.key == pygame.K_RIGHT:
        # 向右标志设为假
        ship.moving_right = False
    # 是←箭头
    elif event.key == pygame.K_LEFT:
        # 向左标志设为假
        ship.moving_left = False


def update_screen(ai_settings, screen, ship, bullets, character):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 重绘屏幕
    screen.fill(ai_settings.bg_color)

    # 这里注意绘制的顺序就能实现图案覆盖
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # 绘制飞船
    ship.blitme()

    # 绘制角色
    character.draw_character()

    # 让最近绘制的屏幕可见
    pygame.display.flip()
