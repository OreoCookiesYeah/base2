# pygame python第三方游戏库   .pyd 动态模块(可以导入,但是看不到源码) .py 静态模块
import pygame  # 官方推荐这样导入
from pygame.locals import *
import sys
# 定义常量记录数据 (常量特点: 字母全大写  一旦定义,不要修改记录的值)
WINDOW_H = 768
WINDOW_W = 512

class HeroPlane:  # 英雄飞机类
    def __init__(self, img_path, x, y, window):
        self.img = pygame.image.load(img_path)  # 飞机图片
        self.x = x  # 飞机坐标
        self.y = y
        self.window = window  # 飞机所在的窗口

    def display(self):
        """贴飞机图"""
        self.window.blit(self.img, (self.x, self.y))  # 290 500

    def move_left(self):
        """左移"""
        self.x -= 5

    def move_right(self):
        """右移"""
        self.x += 5


def main():  # 一般将程序的入口定义为main函数
    """主函数"""
    # 1. 创建窗口
    window = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    # 2.贴背景图
    # 加载图片
    bg_img = pygame.image.load("res/img_bg_level_1.jpg")
    # plane_img = pygame.image.load("res/hero2.png")
    # # 定义变量记录飞机坐标
    # x = WINDOW_W / 2 - 60
    # y = WINDOW_H / 2 - 39
    # 创建飞机对象
    hero_plane = HeroPlane("res/hero2.png", WINDOW_W / 2 - 60, WINDOW_H / 2 - 39, window)
    while True:
        # 贴图（指定坐标，将图片绘制到窗口）
        window.blit(bg_img, (0, 0))
        # 贴飞机图
        # window.blit(plane_img, (x, y))  # 290 500
        hero_plane.display()
        # 3.刷新窗口
        pygame.display.update()

        # 获取新事件
        for event in pygame.event.get():
            # 1. 鼠标点击关闭窗口事件
            if event.type == QUIT:
                print("点击关闭窗口按钮")
                sys.exit()  # 关闭程序

            # 2. 键盘按下事件
            if event.type == KEYDOWN:
                # 判断用户按键
                if event.key == K_SPACE:
                    print("space")
        # 检测键盘长按事件
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_a] or pressed_keys[K_LEFT]:
            # x -= 5
            hero_plane.move_left()
        if pressed_keys[K_d] or pressed_keys[K_RIGHT]:
            # x += 5
            hero_plane.move_right()

if __name__ == '__main__':
    main()