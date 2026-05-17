import math

import pygame

from src.entities.bullet import Bullet


class Tower:
    def __init__(
        self,
        image_path,
        bullet_image_path,
        position,
        range_radius,
        fire_interval,
        damage,
        bullet_speed,
        can_rotate=True,
    ):
        self.original_image = pygame.image.load(str(image_path)).convert_alpha()
        self.bullet_image_path = bullet_image_path
        self.position = pygame.Vector2(position)
        self.range_radius = range_radius
        self.fire_interval = fire_interval
        self.damage = damage
        self.bullet_speed = bullet_speed
        self.can_rotate = can_rotate

        self.cooldown_timer = 0
        self.rotation_angle = 0

    def update(self, delta_time, enemies):
        if self.cooldown_timer > 0:
            self.cooldown_timer -= delta_time
            if self.cooldown_timer < 0:
                self.cooldown_timer = 0

        target = self.find_target(enemies)
        if target is None:
            return None

        if self.can_rotate:
            self.update_rotation(target.position)

        if self.cooldown_timer > 0:
            return None

        self.cooldown_timer = self.fire_interval
        return Bullet(
            self.bullet_image_path,
            self.position,
            target,
            self.bullet_speed,
            self.damage,
        )

    def draw(self, surface):
        if self.can_rotate:
            image = pygame.transform.rotate(self.original_image, self.rotation_angle)
        else:
            image = self.original_image

        image_rect = image.get_rect(center=(self.position.x, self.position.y))
        surface.blit(image, image_rect)

    def find_target(self, enemies):
        for enemy in enemies:
            if not enemy.can_be_targeted():
                continue

            if self.position.distance_to(enemy.position) <= self.range_radius:
                return enemy

        return None

    def update_rotation(self, target_position):
        direction = target_position - self.position
        self.rotation_angle = -math.degrees(math.atan2(direction.y, direction.x))

    def get_status_text(self):
        if self.cooldown_timer <= 0.05:
            return "Tower: ready"

        return f"Tower: reload {self.cooldown_timer:.1f}s"
