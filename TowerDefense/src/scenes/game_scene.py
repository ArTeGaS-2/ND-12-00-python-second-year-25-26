import pygame

from settings import (
    MAP_DATA_PATH,
    SIDEBAR_PANEL_PATH,
    SIDEBAR_WIDTH,
    SIDEBAR_X,
    WHITE,
    WINDOW_HEIGHT,
)
from src.map.tile_map import TileMap


class GameScene:
    def __init__(self, game):
        self.game = game
        self.tile_map = TileMap(MAP_DATA_PATH)
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
        pass

    def draw(self, surface):
        self.tile_map.draw(surface)
        surface.blit(self.sidebar_panel, (SIDEBAR_X, 0))
        self.draw_sidebar(surface)

    def draw_sidebar(self, surface):
        title_surface = self.title_font.render("Game Panel", True, WHITE)
        surface.blit(title_surface, (SIDEBAR_X + 40, 55))

        self.draw_sidebar_block(surface, "Build", "Basic Tower", 45, 220)
        self.draw_sidebar_block(surface, "Resources", "Coins: 120", 45, 380)
        self.draw_sidebar_block(surface, "Status", "Lives: 10", 45, 550)

        wave_text = self.text_font.render("Wave: waiting", True, WHITE)
        surface.blit(wave_text, (SIDEBAR_X + 55, 640))

        path_text = self.text_font.render(
            f"Path points: {len(self.tile_map.path_points)}",
            True,
            WHITE,
        )
        surface.blit(path_text, (SIDEBAR_X + 55, 675))

    def draw_sidebar_block(self, surface, title, value, x_offset, y):
        title_surface = self.section_font.render(title, True, WHITE)
        value_surface = self.text_font.render(value, True, WHITE)

        surface.blit(title_surface, (SIDEBAR_X + x_offset, y))
        surface.blit(value_surface, (SIDEBAR_X + x_offset, y + 40))
