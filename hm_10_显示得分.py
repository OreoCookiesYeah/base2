# pygame python第三方游戏库   .pyd 动态模块(可以导入,但是看不到源码) .py 静态模块
import pygame  # 官方推荐这样导入
from pygame.locals import *
import sys
import time
import random

# 定义常量记录数据 (常量特点: 字母全大写  一旦定义,不要修改记录的值)
WINDOW_H = 768
WINDOW_W = 512
# 定义全局变量
enemy_list = []  # 记录每架敌机
score = 0  # 得分


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

    def is_hit_enemy(self, enemy):
        """判断是否击中敌机"""
        # 判断两个矩形是否相交，相交返回True, 否则返回False
        bullet_rect = Rect(self.x, self.y, 20, 31)
        enemy_rect = Rect(enemy.x, enemy.y, 100, 68)
        return pygame.Rect.colliderect(bullet_rect, enemy_rect)


class BasePlane(Item):  # 基础飞机类
    pass


class EnemyPlane(BasePlane):  # 敌人飞机类
    def __init__(self, img_path, x, y):
        super().__init__(img_path, x, y)
        self.is_hited = False  # 记录是否被击中

    def move(self):
        """向下飞"""
        self.y += 10
        # 判断是否飞出边界 or 击中敌机
        if self.y >= WINDOW_H or self.is_hited:  # 重新回到窗口顶部
            self.y = random.randint(-500, -70)
            self.x = random.randint(0, WINDOW_W - 100)
            self.img = pygame.image.load("res/img-plane_%d.png" % random.randint(1, 7))
            if self.is_hited:  # 重置飞机状态
                self.is_hited = False


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
        delete_bullets = []
        for bullet in self.bullets:
            # 判断子弹是否飞出边界
            if bullet.y >= -31:  # 在边界内,显示和移动
                # 判断是否击中敌机
                for enemy in enemy_list:
                    if bullet.is_hit_enemy(enemy):  # 击中敌机
                        delete_bullets.append(bullet)
                        # 将敌机击中的结果告诉敌机就可以了
                        enemy.is_hited = True
                        # 累加得分
                        global score
                        score += 10
                        break
                else:  # 没击中敌机
                    bullet.display()
                    bullet.move()
            else:  # 出了边界,删除子弹
                # self.bullets.remove(bullet)
                delete_bullets.append(bullet)

        for delete_bullet in delete_bullets:
            self.bullets.remove(delete_bullet)


class Map(Item):  # 地图类
    pass


def main():  # 一般将程序的入口定义为main函数
    """主函数"""
    # 初始化pygame库，图形处理不需要,但是文本/音效必须设置
    pygame.init()
    # 1. 创建窗口
    window = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    # 设置游戏元素所在的窗口
    Item.set_window(window)
    # 创建地图对象
    map = Map("res/img_bg_level_1.jpg", 0, 0)
    # 创建飞机对象
    hero_plane = HeroPlane("res/hero2.png", WINDOW_W / 2 - 60, WINDOW_H / 2 - 39)

    for _ in range(5):
        enemy_plane = EnemyPlane('res/img-plane_%d.png' % random.randint(1, 7), random.randint(0, WINDOW_W - 100),
                                 random.randint(-500, -70))
        enemy_list.append(enemy_plane)
    # 加载自定义字体，返回字体对象
    font_obj = pygame.font.Font("res/SIMHEI.TTF", 35)

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
        # 贴文本框
        # 设置文本，返回文本对象   render(文本内容， 抗锯齿，颜色)
        text_obj = font_obj.render("得分:%d" % score, 1, (255, 255, 255))
        # 设置文本的位置和尺寸   获取文本的Rect并修改Rect的中心点为 （300，300）
        text_rect = text_obj.get_rect(x=30, y=30)
        # 在指定位置和尺寸绘制指定文字对象
        window.blit(text_obj, text_rect)
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