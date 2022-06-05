import pygame
from pygame.sprite import Sprite


class Alien(Sprite):

    def __init__(self, ai_game) -> None:
        """初始化外星人并设置其起始位置"""
        super(Alien, self).__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # 加载外星人图像并设置其rect属性
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # 每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的准确位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def blit_alien(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image, self.rect)
