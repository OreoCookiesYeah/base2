# pygame python第三方游戏库   .pyd 动态模块(可以导入,但是看不到源码) .py 静态模块
import pygame  # 官方推荐这样导入
from pygame.locals import *
import sys
import time
import random

# 定义常量记录数据 (常量特点: 字母全大写  一旦定义,不要修改记录的值)
WINDOW_H = 768
WINDOW_W = 512

class Item:  # 游戏元素类
    window = None  # 类属性 记录所在的窗口

    @classmethod
    def set_window(cls, window):
        cls.window = window

    def __init__(self, img_path, x, y):
        self.img = pygame.image.load(img_path)  # 元素图片
        self.x = x  # 元素坐标
        self.y = y

    def display(self):
        """贴元素图"""
        self.window.blit(self.img, (self.x, self.y))


class Bullet(Item):  # 子弹类
    def move(self):
        """向上飞"""
        self.y -= 15

        # def __del__(self):
        #     print("子弹将要被删除")


class BasePlane(Item):  # 基础飞机类
    pass


class EnemyPlane(BasePlane):  # 敌人飞机类
    def move(self):
        """向下飞"""
        self.y += 10
        # 判断是否飞出边界
        if self.y >= WINDOW_H:  # 重新回到窗口顶部
            self.y = random.randint(-500, -70)
            self.x = random.randint(0, WINDOW_W - 100)
            self.img = pygame.image.load("res/img-plane_%d.png" % random.randint(1, 7))


class HeroPlane(BasePlane):  # 英雄飞机类
    def __init__(self, img_path, x, y):
        super().__init__(img_path, x, y)
        self.bullets = []  # 记录发出的所有子弹

    def move_left(self):
        """左移"""
        self.x -= 5

    def move_right(self):
        """右移"""
        self.x += 5

    def fire(self):
        """发射子弹"""
        # 创建子弹对象
        # 子弹x = 飞机x + 飞机宽度一半 - 子弹宽度一半
        # 子弹y =  飞机y - 子弹高度
        bullet = Bullet("res/bullet_9.png", self.x + 50, self.y - 31)
        self.bullets.append(bullet)

    def display_bullets(self):
        """贴子弹图"""
        out_window_bullets = []
        for bullet in self.bullets:
            # 判断子弹是否飞出边界
            if bullet.y >= -31:  # 在边界内,显示和移动
                bullet.display()
                bullet.move()
            else:  # 出了边界,删除子弹
                # self.bullets.remove(bullet)
                out_window_bullets.append(bullet)

        for out_window_bullet in out_window_bullets:
            self.bullets.remove(out_window_bullet)


class Map(Item):  # 地图类
    pass


def main():  # 一般将程序的入口定义为main函数
    """主函数"""
    # 1. 创建窗口
    window = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    # 设置游戏元素所在的窗口
    Item.set_window(window)
    # 创建地图对象
    map = Map("res/img_bg_level_1.jpg", 0, 0)
    # 创建飞机对象
    hero_plane = HeroPlane("res/hero2.png", WINDOW_W / 2 - 60, WINDOW_H / 2 - 39)
    enemy_list = []  # 记录每架敌机
    for _ in range(5):
        enemy_plane = EnemyPlane('res/img-plane_%d.png' % random.randint(1, 7), random.randint(0, WINDOW_W - 100),
                                 random.randint(-500, -70))
        enemy_list.append(enemy_plane)
    while True:
        # 贴背景图
        # window.blit(bg_img, (0, 0))
        map.display()
        # 贴飞机图
        hero_plane.display()
        for enemy in enemy_list:
            enemy.display()
            enemy.move()
        # 贴子弹图
        hero_plane.display_bullets()
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
                    hero_plane.fire()

        # 检测键盘长按事件
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_a] or pressed_keys[K_LEFT]:
            # x -= 5
            hero_plane.move_left()
        if pressed_keys[K_d] or pressed_keys[K_RIGHT]:
            # x += 5
            hero_plane.move_right()
        time.sleep(0.02)  # 让循环每执行一次,休息一段时间  让CPU可以做别的工作


if __name__ == '__main__':
    main()