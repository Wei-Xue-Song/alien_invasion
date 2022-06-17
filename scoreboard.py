import pygame.font
from pygame import Surface

from game_stats import GameStats
from settings import Settings


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

        # 准备初始得分图像
        self.prep_score()

    def prep_score(self) -> None:
        """将得分转换为一幅渲染的图像"""
        self.score_image = self.font.render(
            str(self.stats.score), True, self.text_color, self.settings.bg_color)
        self.score_rect = self.score_image.get_rect()

        # 在屏幕右上角显示得分
        self.screen_rect.top = 20
        self.score_rect.right = self.screen_rect.right - 20

    def show_score(self) -> None:
        """在屏幕上显示得分"""
        self.screen.blit(self.score_image, self.score_rect)
