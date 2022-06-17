from settings import Settings


class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, settings: Settings) -> None:
        """初始化统计信息"""
        self.settings = settings
        self.reset_stats()

        # 游戏刚启动处于非活动状态
        self.game_active = False

    def reset_stats(self):
        """"初始化游戏运行期间可能变化的统计信息"""
        self.score = 0
        self.ships_left = self.settings.ship_limit - 1
