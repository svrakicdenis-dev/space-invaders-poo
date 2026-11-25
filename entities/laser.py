import pygame
from config import *


class Laser(pygame.sprite.Sprite):
    def __init__(self, position, speed, screen_offset, image=laser_sprite):
        super().__init__()
        self.offset = screen_offset
        self.image = image  # Use the loaded laser image
        self.rect = self.image.get_rect(center = position)  # Get the rectangle of the image
        self.speed = speed  # Set the speed of the laser

    def update(self):
        self.rect.y += self.speed  # Move the laser upward
        if self.rect.bottom < self.offset:  # Remove the laser if it goes off-screen
            self.kill()
