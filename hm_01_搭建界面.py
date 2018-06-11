# pygame python第三方游戏库   .pyd 动态模块(可以导入,但是看不到源码) .py 静态模块
import pygame  # 官方推荐这样导入


def main():  # 一般将程序的入口定义为main函数
    """主函数"""
    # 1. 创建窗口
    window = pygame.display.set_mode((512, 768))
    # 2.贴背景图
    # 加载图片
    image = pygame.image.load("res/img_bg_level_1.jpg")
    while True:
        # 贴图（指定坐标，将图片绘制到窗口）
        window.blit(image, (0, 0))
        # 3.刷新窗口
        pygame.display.update()

if __name__ == '__main__':
    main()