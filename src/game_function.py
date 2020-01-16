import sys
import pygame

from src.bullet import Bullet
from src.alien import Alien
from time import sleep
from random import randint
from random import choice


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        # 退出
        if event.type == pygame.QUIT:
            exit_game(stats)
        # 鼠标按下
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                              aliens, bullets, mouse_x, mouse_y)
        # 键盘按下
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, stats, sb, screen, ship, aliens, bullets)
        # 键盘松开
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_keydown_events(event, ai_settings, stats, sb, screen, ship, aliens, bullets):
    """响应按键"""
    # 是→箭头
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    # 是←箭头
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    # 是↑箭头
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    # 是↓箭头
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    # 空格
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    # 按q退出游戏
    elif event.key == pygame.K_q:
        exit_game(stats)
    # 按p开始游戏
    elif event.key == pygame.K_p:
        start_game(ai_settings, screen, stats, sb, ship, aliens,
                   bullets)


def exit_game(stats):
    """退出游戏"""
    with open(r'../high_score/high_score.txt', 'w') as file:
        file.write(str(stats.high_score))
    sys.exit()


def check_keyup_events(event, ship):
    """响应松开"""
    # 是→箭头
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    # 是←箭头
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    # 是↑箭头
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    # 是↓箭头
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y):
    """在玩家单击Play按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 开始游戏
        start_game(ai_settings, screen, stats, sb, ship, aliens,
                   bullets)


def start_game(ai_settings, screen, stats, sb, ship, aliens,
               bullets):
    """开始游戏"""
    # 重置游戏设置
    ai_settings.initialize_dynamic_settings()

    # 隐藏光标
    pygame.mouse.set_visible(False)

    # 重置游戏统计信息
    stats.reset_stats()
    stats.game_active = True

    # 重置记分牌图象
    sb.prep_image()

    # 清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()

    # 创建一群新的外星人，并让飞船居中
    create_fleet(ai_settings, screen, aliens)
    ship.center_ship()


def update_screen(ai_settings, screen, ship, stats, sb, bullets, character, aliens, play_button):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 重绘屏幕
    screen.fill(ai_settings.bg_color)

    # 绘制角色
    character.draw_character()

    # 这里注意绘制的顺序就能实现图案覆盖
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # 绘制飞船
    ship.blitme()

    # 绘制外星人
    aliens.draw(screen)  # 对编组调用.draw()方法会自动绘制里面的每个元素，位置由元素的rect决定

    # 显示得分
    sb.show_score()

    # 如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """更新子弹的位置并删除已消失的子弹"""
    # 更新子弹的位置
    bullets.update()

    # 删除已消失的子弹
    for bullet in bullets.copy():  # 这里创建副本来遍历，对原列表进行删除，实际上复杂度是O(n^2)，还没有考虑删除移动元素的开销
        if bullet.rect.bottom <= 0:  # 如果不用Group()直接用列表，是否能改进到O(n)?
            bullets.remove(bullet)  # 这里还不知道Group()内部实现是链表还是数组，对于子弹应当使用链表
    # print(len(bullets))

    # 响应子弹与外星人的碰撞
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """响应子弹和外星人的碰撞"""
    # 检查是否有子弹击中了外星人
    # 如果是这样，就删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        # collisions是一个字典，以子弹为key，外星人的列表为值，列表中包含碰撞的所有外星人
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # 删除现有的子弹，加快游戏节奏，并新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, aliens)

        # 如果整群外星人都被消灭，就提高一个等级
        start_new_level(stats, sb)


def start_new_level(stats, sb):
    """升级游戏"""
    stats.level += 1
    sb.prep_level()


def fire_bullet(ai_settings, screen, ship, bullets):
    """如果还没有到达限制，就发射一颗子弹"""
    # 创建一颗子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:  # 检查子弹数量
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def create_fleet(ai_settings, screen, aliens):
    """创建外星人群"""
    # 创建外星人群
    for alien_number in range(5):
        # 创建一个外星人
        create_alien(ai_settings, screen, aliens)


def create_alien(ai_settings, screen, aliens):
    """创建一个外星人"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = randint(alien_width, screen.get_rect().right - alien_width)
    # 如果外星人的x坐标在创建时就和屏幕碰撞将会有bug
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height
    alien.fleet_direction = choice([1, -1])
    aliens.add(alien)


def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """更新外星人群中所有外星人的位置"""
    # 检查是否有外星人位于屏幕边缘，并更新整群外星人的位置
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)

    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, alien)


def change_fleet_direction(ai_settings, alien_in_crash):
    """将发生碰撞的外星人向下移，并改变它的方向"""
    alien_in_crash.rect.y += ai_settings.fleet_drop_speed
    alien_in_crash.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    # 将ships_left减1
    if stats.ships_left > 0:
        stats.ships_left -= 1

        # 更新记分牌
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, aliens)
        ship.center_ship()

        # 暂停
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样进行处理
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break


def check_high_score(stats, sb):
    """检查是否诞生了新的最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
