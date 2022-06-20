from settings import Settings


class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, settings: Settings) -> None:
        """初始化统计信息"""
        self.settings = settings
        self.reset_stats()

        # 游戏刚启动处于非活动状态
        self.game_active = False

        # 任何情况下都不应重置最高得分
        self._init_high_score()

    def _init_high_score(self) -> None:
        """初始化最高分"""
        filename = self.settings.high_score_file

        try:
            with open(filename, 'r') as f:
                high_score = f.read()
        except FileNotFoundError:
            high_score = 0

        self.high_score = int(high_score)

    def reset_stats(self) -> None:
        """"初始化游戏运行期间可能变化的统计信息"""
        self.score = 0
        self.level = 1
        self.ships_left = self.settings.ship_limit - 1
