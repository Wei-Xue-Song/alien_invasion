import pygame
from pygame import Surface
from pygame.sprite import Sprite
from settings import Settings
from ship import Ship


class Bullet(Sprite):
    """一个对飞船发射的子弹进行管理的类"""
    def __init__(self, settings: Settings, screen: Surface, ship: Ship):
        super(Bullet, self).__init__()
        self.screen = screen

        # 在(0, 0)处创建一个表示子弹的矩形，再设置正确的位置
        self.rect = pygame.Rect(0, 0, settings.bullet_width,
                                settings.bullet_height)
        self.rect.midtop = ship.rect.midtop

        self.y = float(self.rect.y)
        self.color = settings.bullet_color
        self.speed = settings.bullet_speed

    def update(self):
        """向上移动子弹"""
        self.y -= self.speed
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
