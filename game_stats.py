from settings import Settings


class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, settings: Settings) -> None:
        """初始化统计信息"""
        self.settings = settings
        self.reset_stats()

        self.game_active = True  # 游戏刚启动处于活动状态

    def reset_stats(self):
        """"初始化游戏运行期间可能变化的统计信息"""
        self.ships_left = self.settings.ship_limit - 1
