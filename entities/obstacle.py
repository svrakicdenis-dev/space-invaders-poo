import pygame
from config import OBSTACLE_GRID, WHITE


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((3, 3))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(topleft=(x, y))


class Obstacle:
    def __init__(self, x, y, grid=OBSTACLE_GRID):
        self.blocks_group = pygame.sprite.Group()
        for row_idx, row in enumerate(grid):
            for col_idx, cell in enumerate(row):
                if cell == 1:
                    self.blocks_group.add(Block(col_idx * 3 + x, row_idx * 3 + y))