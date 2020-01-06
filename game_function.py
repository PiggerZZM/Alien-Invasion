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
        fire_bullet(ai_settings, screen, ship, bullets)
    # 按q退出游戏
    elif event.key == pygame.K_q:
        sys.exit()


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


def update_screen(ai_settings, screen, ship, bullets, character, alien):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 重绘屏幕
    screen.fill(ai_settings.bg_color)

    # 这里注意绘制的顺序就能实现图案覆盖
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # 绘制飞船
    ship.blitme()

    # 绘制外星人
    alien.blitme()

    # 绘制角色
    character.draw_character()

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(bullets):
    """更新子弹的位置并删除已消失的子弹"""
    # 更新子弹的位置
    bullets.update()

    # 删除已消失的子弹
    for bullet in bullets.copy():  # 这里创建副本来遍历，对原列表进行删除，实际上复杂度是O(n^2)，还没有考虑删除移动元素的开销
        if bullet.rect.bottom <= 0:  # 如果不用Group()直接用列表，是否能改进到O(n)?
            bullets.remove(bullet)  # 这里还不知道Group()内部实现是链表还是数组，对于子弹应当使用链表
    # print(len(bullets))


def fire_bullet(ai_settings, screen, ship, bullets):
    """如果还没有到达限制，就发射一颗子弹"""
    # 创建一颗子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:  # 检查子弹数量
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

