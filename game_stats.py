class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, ai_game) -> None:
        """初始化统计信息"""
        self.ships_left = None  # 剩余飞船数量
        self.settings = ai_game.settings
        self.game_active = True  # 游戏刚启动处于活动状态
        self.reset_stats()

    def reset_stats(self):
        """"初始化游戏运行期间可能变化的统计信息"""
        self.ships_left = self.settings.ship_limit - 1
