import pygame


class Enemy:
    def __init__(self, image_path, path_points, speed):
        self.image = pygame.image.load(str(image_path)).convert_alpha()
        self.path_points = [pygame.Vector2(point) for point in path_points]
        self.speed = speed

        self.position = self.path_points[0].copy()
        self.target_index = 1
        self.reached_goal = len(self.path_points) <= 1

    def update(self, delta_time):
        if self.reached_goal:
            return

        target = self.path_points[self.target_index]
        direction = target - self.position
        distance_to_target = direction.length()

        if distance_to_target == 0:
            self.advance_to_next_target()
            return

        movement_distance = self.speed * delta_time
        if movement_distance >= distance_to_target:
            self.position = target
            self.advance_to_next_target()
            return

        direction.normalize_ip()
        self.position += direction * movement_distance

    def draw(self, surface):
        draw_x = self.position.x - self.image.get_width() / 2
        draw_y = self.position.y - self.image.get_height() / 2
        surface.blit(self.image, (draw_x, draw_y))

    def advance_to_next_target(self):
        if self.target_index >= len(self.path_points) - 1:
            self.reached_goal = True
            return

        self.target_index += 1

    def get_status_text(self):
        if self.reached_goal:
            return "Enemy: reached goal"

        return f"Enemy target: {self.target_index + 1}/{len(self.path_points)}"
