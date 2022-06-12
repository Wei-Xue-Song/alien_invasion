import sys
from time import sleep

from game_stats import GameStats

import pygame
from pygame.event import Event

from alien import Alien
from bullet import Bullet
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

        # 创建一个用于存储游戏信息的实例
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.aliens = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        self._create_fleet()

    def get_number_aliens_x(self):
        """计算每行可容纳多少个外星人"""
        alien = Alien(self)
        alien_width = alien.rect.width
        screen_width = self.settings.screen_width
        available_space_x = screen_width - alien_width
        # 外星人的间距为外星人宽度
        return available_space_x // (2 * alien_width)

    def get_number_rows(self):
        """计算屏幕可容纳多少行外星人"""
        alien = Alien(self)
        alien_height = alien.rect.height
        ship_height = self.ship.rect.height
        screen_height = self.settings.screen_height
        available_space_y = screen_height - ship_height - 3 * alien_height
        return available_space_y // (2 * alien_height)

    def _create_alien(self, row_number: int, alien_number: int):
        """创建一个外星人并将其放置在当前行"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.y = alien_height + 2 * alien_height * row_number
        alien.rect.x = alien.x
        alien.rect.y = alien.y
        self.aliens.add(alien)

    def _create_fleet(self):
        """创建外星人群"""
        number_rows = self.get_number_rows()
        number_aliens_x = self.get_number_aliens_x()

        # 创建外星人群
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(row_number, alien_number)

    def _fire_bullet(self):
        """创建一颗子弹并将其加入编组bullets中"""
        if len(self.bullets) < self.settings.bullet_limit:
            self.bullets.add(Bullet(self))

    def _check_keyup_event(self, event: Event):
        """响应松开"""
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

    def _check_keydown_event(self, event: Event):
        """响应按键"""
        if event.key == pygame.K_q:
            pygame.quit()
            sys.exit()
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_event(event)

    def _check_bullet_alien_collision(self):
        """响应子弹和外星人的碰撞"""
        # 删除发生碰撞的子弹和外星人
        pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if not self.aliens:
            # 删除现有的所有子弹，并创建一个新的外星人群
            self.bullets.empty()
            self._create_fleet()

    def _update_bullets(self):
        """更新子弹的位置并删除消失的子弹"""
        # 更新子弹的位置
        self.bullets.update()

        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # 检查是否有子弹击中外星人
        self._check_bullet_alien_collision()

    def _change_fleet_direction(self):
        """将整群外星人下移，并改变它们的方向"""
        for alien in self.aliens:
            alien.y += self.settings.fleet_drop_speed
            alien.rect.y = alien.y
        self.settings.fleet_direction *= -1

    def _check_fleet_edges(self):
        """有外星人到达边缘时采取相应措施"""
        for alien in self.aliens:
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _ship_hit(self):
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

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕底端"""
        for alien in self.aliens:
            if alien.rect.bottom >= self.screen_rect.bottom:
                self._ship_hit()  # 像飞船被撞到一样处理
                break

    def _update_aliens(self):
        """检查是否有外星人位于屏幕边缘，并更新整群外星人的位置"""
        self._check_fleet_edges()
        self.aliens.update()

        # 检查是否有外星人撞到飞船
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 检查是否有外星人到达了屏幕底端
        self._check_aliens_bottom()

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        # 每次循环时都重绘屏幕
        self.screen.fill(self.settings.bg_color)

        # 绘制飞船和外星人
        self.ship.blit_ship()
        self.aliens.draw(self.screen)

        # 在飞船和外星人后面重绘所有子弹
        for bullet in self.bullets:
            bullet.draw_bullet()

        # 让最近绘制的屏幕可见
        pygame.display.flip()

    def run_game(self):
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
