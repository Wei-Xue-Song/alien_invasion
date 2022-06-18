import sys
from time import sleep
from typing import Tuple

import pygame
from pygame.event import Event

from alien import Alien
from bullet import Bullet
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self) -> None:
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption(self.settings.title)

        # 创建一个用于存储游戏信息的实例, 并创建记分牌
        self.stats = GameStats(self.settings)
        self.sb = Scoreboard(self.screen, self.settings, self.stats)

        # 创建外星人编组
        self.aliens = pygame.sprite.Group()
        # 创建子弹编组
        self.bullets = pygame.sprite.Group()
        # 创建飞船
        self.ship = Ship(self.screen, self.settings)

        # 创建外星人群
        self._create_fleet()

        # 创建Play按钮
        self.play_button = Button(self.screen, 'Play')

    def get_number_aliens_x(self, alien: Alien) -> int:
        """计算每行可容纳多少个外星人"""
        alien_width = alien.rect.width
        screen_width = self.settings.screen_width
        available_space_x = screen_width - alien_width
        # 外星人的间距为外星人宽度
        return available_space_x // (2 * alien_width)

    def get_number_rows(self, alien: Alien) -> int:
        """计算屏幕可容纳多少行外星人"""
        alien_height = alien.rect.height
        ship_height = self.ship.rect.height
        screen_height = self.settings.screen_height
        available_space_y = screen_height - ship_height - 3 * alien_height
        return available_space_y // (2 * alien_height)

    def _create_alien(self, row_number: int, alien_number: int) -> None:
        """创建一个外星人并将其放置在当前行"""
        alien = Alien(self.screen, self.settings)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.y = alien_height + 2 * alien_height * row_number
        alien.rect.x = alien.x
        alien.rect.y = alien.y
        self.aliens.add(alien)

    def _create_fleet(self) -> None:
        """创建外星人群"""
        alien = Alien(self.screen, self.settings)
        number_rows = self.get_number_rows(alien)
        number_aliens_x = self.get_number_aliens_x(alien)

        # 创建外星人群
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(row_number, alien_number)

    def _fire_bullet(self) -> None:
        """创建一颗子弹并将其加入编组bullets中"""
        if len(self.bullets) < self.settings.bullet_limit:
            bullet = Bullet(self.screen, self.settings, self.ship)
            self.bullets.add(bullet)

    def _start_game(self) -> None:
        """开始游戏"""
        # 重置游戏的统计信息
        self.stats.reset_stats()
        self.stats.game_active = True
        # bugfix: 从开始新游戏到有外星人被射杀之间显示上一次的得分
        self.sb.prep_score()

        # 清空余下的外星人和子弹
        self.aliens.empty()
        self.bullets.empty()

        # 创建一群新的外星人并让飞船居中
        self._create_fleet()
        self.ship.center_ship()

        # 重置游戏的动态设置
        self.settings.initialize_dynamic_settings()

        # 隐藏鼠标光标
        pygame.mouse.set_visible(False)

    def _check_play_button(self, mouse_pos: Tuple[int, int]) -> None:
        """在玩家单击Play按钮时开始游戏"""
        # bugfix: 仅在game_active为False, 点击Play按钮, 游戏才重新开始
        if not self.stats.game_active and self.play_button.rect.collidepoint(mouse_pos):
            self._start_game()

    def _check_keyup_event(self, event: Event) -> None:
        """响应松开"""
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

    def _check_keydown_event(self, event: Event) -> None:
        """响应按键"""
        if event.key == pygame.K_q:  # 按下键盘Q键退出游戏
            pygame.quit()
            sys.exit()
        elif event.key == pygame.K_p:  # 按下键盘P键开始游戏
            self._start_game()
        elif event.key == pygame.K_LEFT:  # 按下键盘方向左键左移飞船
            self.ship.moving_left = True
        elif event.key == pygame.K_RIGHT:  # 按下键盘方向右键右移飞船
            self.ship.moving_right = True
        elif event.key == pygame.K_SPACE:  # 按下键盘空格键飞船开火
            self._fire_bullet()

    def _check_events(self) -> None:
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _update_bullets(self) -> None:
        """更新子弹的位置并删除消失的子弹"""
        # 更新子弹的位置
        self.bullets.update()

        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # 删除发生碰撞的子弹和外星人
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens,
                                                True, True)
        # bugfix: 被同一颗子弹消灭的所有外星人都计入得分
        for _, aliens in collisions.items():
            self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()

        # 如果外星人全被消灭
        if not self.aliens:
            # 删除现有的所有子弹, 并创建一个新的外星人群
            self.bullets.empty()
            self._create_fleet()
            # 加快游戏节奏, 提升游戏难度
            self.settings.increase_speed()

    def _change_fleet_direction(self) -> None:
        """将整群外星人下移，并改变它们的方向"""
        for alien in self.aliens:
            alien.y += self.settings.fleet_drop_speed
            alien.rect.y = alien.y
        self.settings.fleet_direction *= -1

    def _check_fleet_edges(self) -> None:
        """有外星人到达边缘时采取相应措施"""
        for alien in self.aliens:
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _ship_hit(self) -> None:
        """响应外星人被飞船撞到"""
        if self.stats.ships_left > 0:
            # 将ship_left减1
            self.stats.ships_left -= 1

            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的外星人，并将飞船放到屏幕底部中央
            self._create_fleet()
            self.ship.center_ship()

            # 暂停
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_aliens(self) -> None:
        """检查是否有外星人位于屏幕边缘，并更新整群外星人的位置"""
        self._check_fleet_edges()
        self.aliens.update()

        # 检查是否有外星人撞到飞船
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 检查是否有外星人到达了屏幕底端
        for alien in self.aliens:
            if alien.rect.bottom >= self.screen_rect.bottom:
                self._ship_hit()  # 像飞船被撞到一样处理
                break

    def _update_screen(self) -> None:
        """更新屏幕上的图像，并切换到新屏幕"""
        # 每次循环时都重绘屏幕
        self.screen.fill(self.settings.bg_color)

        # 绘制飞船和外星人
        self.ship.blit_ship()
        self.aliens.draw(self.screen)

        # 在飞船和外星人后面重绘所有子弹
        for bullet in self.bullets:
            bullet.draw_bullet()

        # 显示得分
        self.sb.show_score()

        # 如果游戏处于非活动状态，就绘制Play按钮
        if not self.stats.game_active:
            self.play_button.draw_button()

        # 让最近绘制的屏幕可见
        pygame.display.flip()

    def run_game(self) -> None:
        """开始游戏的主循环"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
