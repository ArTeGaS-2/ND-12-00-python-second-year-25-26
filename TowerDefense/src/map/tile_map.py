import json

import pygame

from settings import (
    BUILD_SPOT_TILE_PATH,
    GOAL_TILE_PATH,
    GRASS_TILE_PATH,
    ROAD_TILE_PATH,
    SPAWN_TILE_PATH,
)


class TileMap:
    def __init__(self, json_path):
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.tile_size = data["tile_size"]
        self.cols = data["cols"]
        self.rows = data["rows"]
        self.grid = data["grid"]

        self.tile_images = {
            0: self.load_tile(GRASS_TILE_PATH),
            1: self.load_tile(ROAD_TILE_PATH),
            2: self.load_tile(SPAWN_TILE_PATH),
            3: self.load_tile(GOAL_TILE_PATH),
            4: self.load_tile(BUILD_SPOT_TILE_PATH),
        }

        self.path_points = self.build_path()

    def load_tile(self, image_path):
        image = pygame.image.load(str(image_path)).convert_alpha()
        return pygame.transform.scale(image, (self.tile_size, self.tile_size))

    def draw(self, surface):
        for row_index, row in enumerate(self.grid):
            for col_index, tile_value in enumerate(row):
                image = self.tile_images[tile_value]
                x = col_index * self.tile_size
                y = row_index * self.tile_size
                surface.blit(image, (x, y))

    def build_path(self):
        current = self.find_tile(2)
        previous = None
        path_tiles = [current]

        while self.get_tile_value(current) != 3:
            next_tile = self.find_next_path_tile(current, previous)
            path_tiles.append(next_tile)
            previous = current
            current = next_tile

        return [self.get_tile_center(tile) for tile in path_tiles]

    def find_tile(self, target_value):
        for row_index, row in enumerate(self.grid):
            for col_index, tile_value in enumerate(row):
                if tile_value == target_value:
                    return col_index, row_index

        raise ValueError(f"Tile with value {target_value} was not found.")

    def find_next_path_tile(self, current, previous):
        for neighbor in self.get_neighbors(current):
            if neighbor == previous:
                continue

            tile_value = self.get_tile_value(neighbor)
            if tile_value in (1, 3):
                return neighbor

        raise ValueError("Path is broken. Could not find the next tile.")

    def get_neighbors(self, tile_position):
        col, row = tile_position
        neighbors = []

        directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
        for delta_col, delta_row in directions:
            next_col = col + delta_col
            next_row = row + delta_row

            if 0 <= next_col < self.cols and 0 <= next_row < self.rows:
                neighbors.append((next_col, next_row))

        return neighbors

    def get_tile_value(self, tile_position):
        col, row = tile_position
        return self.grid[row][col]

    def get_tile_center(self, tile_position):
        col, row = tile_position
        center_x = col * self.tile_size + self.tile_size // 2
        center_y = row * self.tile_size + self.tile_size // 2
        return center_x, center_y
