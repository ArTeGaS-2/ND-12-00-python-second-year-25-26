import pygame


class Button:
    def __init__(self, x, y, width, height, image_path, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(str(image_path)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.text = text
        self.font = font

    def draw(self, surface):
        surface.blit(self.image, self.rect)

        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
