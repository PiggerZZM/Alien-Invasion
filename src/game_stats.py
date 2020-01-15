import os


class GameStats():
    """跟踪游戏的统计信息"""

    def __init__(self, ai_settings):
        """初始化统计信息"""
        self.ai_settings = ai_settings
        # 游戏刚启动时处于非活动状态
        self.game_active = False
        self.reset_stats()

        # 在开始时读入high_score.txt中记录的最高分，如果不存在则最高分为0
        if os.path.exists(r'../high_score/high_score.txt'):
            with open(r'../high_score/high_score.txt', 'r') as file:
                self.high_score = int(file.read())
        else:
            self.high_score = 0

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

