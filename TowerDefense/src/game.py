import pygame

from settings import FPS, WINDOW_HEIGHT, WINDOW_TITLE, WINDOW_WIDTH
from src.scenes.menu_scene import MenuScene


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.current_scene = MenuScene(self)

    def set_scene(self, scene):
        self.current_scene = scene

    def run(self):
        while self.is_running:
            delta_time = self.clock.tick(FPS) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                else:
                    self.current_scene.handle_event(event)

            self.current_scene.update(delta_time)
            self.current_scene.draw(self.screen)
            pygame.display.flip()

        pygame.quit()
