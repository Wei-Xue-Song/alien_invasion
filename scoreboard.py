import pygame.font
from pygame import Surface
from pygame.sprite import Group

from game_stats import GameStats
from settings import Settings
from ship import Ship


class Scoreboard:
    """显示得分信息的类"""

    def __init__(self, screen: Surface, settings: Settings, stats: GameStats) -> None:
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.settings = settings
        self.stats = stats

        # 显示得分信息时使用的字体设置
        self.text_color = 30, 30, 30
        self.font = pygame.font.SysFont(None, 48)

        self.prep_images()

    def prep_images(self) -> None:
        """准备包含当前得分、最高得分、等级和剩余飞船的图像"""
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self) -> None:
        """将当前得分转换为一幅渲染的图像"""
        # f-string采用 {content:format}设置字符串格式 :后使用,作为千位分隔符
        self.score_image = self.font.render(f'{round(self.stats.score, -1):,}', True,
                                            self.text_color, self.settings.bg_color)
        self.score_rect = self.score_image.get_rect()

        # 屏幕右上角显示当前得分
        self.screen_rect.top = 20
        self.score_rect.right = self.screen_rect.right - 20

    def prep_high_score(self) -> None:
        """将最高得分转换为一幅渲染的图像"""
        # f-string采用 {content:format}设置字符串格式 :后使用,作为千位分隔符
        self.high_score_image = self.font.render(f'{round(self.stats.high_score, -1):,}', True,
                                                 self.text_color, self.settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()

        # 屏幕顶部中央显示最高得分
        self.high_score_rect.top = self.score_rect.top
        self.high_score_rect.centerx = self.screen_rect.centerx

    def prep_level(self) -> None:
        """将等级转换为一幅渲染的图像"""
        self.level_image = self.font.render(f'{self.stats.level}', True,
                                            self.text_color, self.settings.bg_color)
        self.level_rect = self.level_image.get_rect()

        # 将等级放在得分下方
        self.level_rect.top = self.score_rect.bottom
        self.level_rect.right = self.score_rect.right

    def prep_ships(self) -> None:
        """显示还剩下多少飞船"""
        self.ships = Group()
        for number in range(self.stats.ships_left):
            ship = Ship(self.screen, self.settings)
            # 屏幕左上角显示余下的飞船
            ship.rect.y = 10
            ship.rect.x = 10 + ship.rect.width * number
            self.ships.add(ship)

    def show_score(self) -> None:
        """在屏幕上显示得分、等级"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)

    def check_high_score(self) -> None:
        """检查是否诞生了最高得分"""
        if self.stats.high_score < self.stats.score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
