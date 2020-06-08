import pygame
import sys


def run_test():
    # 创建一个屏幕对象
    pygame.init()  # 初始化背景设置
    screen = pygame.display.set_mode((800, 600))  # 创建surface对象
    pygame.display.set_caption("Test Events")

    # 主循环
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                print(event.type)  # KEYDOWN实际上是2


run_test()
