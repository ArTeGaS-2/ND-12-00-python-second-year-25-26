import pygame

from settings import (
    BASIC_BULLET_PATH,
    BASIC_BULLET_SPEED,
    BASIC_ENEMY_PATH,
    BASIC_ENEMY_HP,
    BASIC_ENEMY_SPEED,
    BASIC_TOWER_CAN_ROTATE,
    BASIC_TOWER_DAMAGE,
    BASIC_TOWER_FIRE_INTERVAL,
    BASIC_TOWER_PATH,
    BASIC_TOWER_RANGE,
    MAP_DATA_PATH,
    SIDEBAR_PANEL_PATH,
    SIDEBAR_WIDTH,
    SIDEBAR_X,
    WHITE,
    WINDOW_HEIGHT,
)
from src.entities.enemy import Enemy
from src.entities.tower import Tower
from src.map.tile_map import TileMap


class GameScene:
    def __init__(self, game):
        self.game = game
        self.tile_map = TileMap(MAP_DATA_PATH)
        tower_tile = self.tile_map.find_tile(4)
        tower_position = self.tile_map.get_tile_center(tower_tile)

        self.enemies = [
            Enemy(
                BASIC_ENEMY_PATH,
                self.tile_map.path_points,
                BASIC_ENEMY_SPEED,
                BASIC_ENEMY_HP,
            )
        ]
        self.towers = [
            Tower(
                BASIC_TOWER_PATH,
                BASIC_BULLET_PATH,
                tower_position,
                BASIC_TOWER_RANGE,
                BASIC_TOWER_FIRE_INTERVAL,
                BASIC_TOWER_DAMAGE,
                BASIC_BULLET_SPEED,
                BASIC_TOWER_CAN_ROTATE,
            )
        ]
        self.bullets = []
        self.sidebar_panel = pygame.image.load(str(SIDEBAR_PANEL_PATH)).convert()
        self.sidebar_panel = pygame.transform.scale(
            self.sidebar_panel,
            (SIDEBAR_WIDTH, WINDOW_HEIGHT),
        )

        self.title_font = pygame.font.SysFont("arial", 34, bold=True)
        self.section_font = pygame.font.SysFont("arial", 26, bold=True)
        self.text_font = pygame.font.SysFont("arial", 24)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.is_running = False

    def update(self, delta_time):
        for enemy in self.enemies:
            enemy.update(delta_time)

        for tower in self.towers:
            bullet = tower.update(delta_time, self.enemies)
            if bullet is not None:
                self.bullets.append(bullet)

        for bullet in self.bullets:
            bullet.update(delta_time)

        self.bullets = [bullet for bullet in self.bullets if bullet.is_active]
        self.enemies = [
            enemy
            for enemy in self.enemies
            if not enemy.is_dead and not enemy.reached_goal
        ]

    def draw(self, surface):
        self.tile_map.draw(surface)

        for tower in self.towers:
            tower.draw(surface)

        for enemy in self.enemies:
            enemy.draw(surface)

        for bullet in self.bullets:
            bullet.draw(surface)

        surface.blit(self.sidebar_panel, (SIDEBAR_X, 0))
        self.draw_sidebar(surface)

    def draw_sidebar(self, surface):
        title_surface = self.title_font.render("Game Panel", True, WHITE)
        surface.blit(title_surface, (SIDEBAR_X + 40, 55))

        self.draw_sidebar_block(
            surface,
            "Build",
            self.towers[0].get_status_text(),
            45,
            220,
        )
        self.draw_sidebar_block(
            surface,
            "Bullets",
            f"Active: {len(self.bullets)}",
            45,
            380,
        )
        self.draw_sidebar_block(
            surface,
            "Enemies",
            f"Alive: {len(self.enemies)}",
            45,
            550,
        )

        wave_text = self.text_font.render("Wave: waiting", True, WHITE)
        surface.blit(wave_text, (SIDEBAR_X + 55, 640))

        enemy_text = self.text_font.render(self.get_enemy_status_text(), True, WHITE)
        surface.blit(enemy_text, (SIDEBAR_X + 55, 675))

        path_text = self.text_font.render(
            f"Tower rotate: {self.towers[0].can_rotate}",
            True,
            WHITE,
        )
        surface.blit(path_text, (SIDEBAR_X + 55, 705))

    def get_enemy_status_text(self):
        if not self.enemies:
            return "Enemy: destroyed"

        return self.enemies[0].get_status_text()

    def draw_sidebar_block(self, surface, title, value, x_offset, y):
        title_surface = self.section_font.render(title, True, WHITE)
        value_surface = self.text_font.render(value, True, WHITE)

        surface.blit(title_surface, (SIDEBAR_X + x_offset, y))
        surface.blit(value_surface, (SIDEBAR_X + x_offset, y + 40))
