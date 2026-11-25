import pygame
from config import SCREEN_HEIGHT, SCREEN_OFFSET


class Laser(pygame.sprite.Sprite):
    _cached_image = None

    def __init__(self, position, speed, screen_offset=SCREEN_OFFSET):
        super().__init__()
        if Laser._cached_image is None:
            Laser._cached_image = pygame.image.load("sprites/laser.png")
        self.offset = screen_offset
        self.image = Laser._cached_image
        self.rect = self.image.get_rect(center=position)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < self.offset or self.rect.top > SCREEN_HEIGHT + 30:
            self.kill()