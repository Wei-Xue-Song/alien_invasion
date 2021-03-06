import pygame
from pygame import Surface
from pygame.sprite import Sprite

from settings import Settings


class Alien(Sprite):
    """表示单个外星人的类"""

    def __init__(self, screen: Surface, settings: Settings) -> None:
        """初始化外星人并设置其起始位置"""
        super(Alien, self).__init__()
        self.screen = screen
        self.settings = settings

        # 加载外星人图像并设置其rect属性
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # 每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的准确位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self) -> None:
        """向左或向右移动外星人"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self) -> bool:
        """检查外星人是否撞到了把屏幕边缘"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

        return False
