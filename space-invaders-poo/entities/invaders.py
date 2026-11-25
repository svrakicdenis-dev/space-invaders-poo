import pygame, random
from config import *

class invader(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        super().__init__()
        self.type = type
        self.frames = [
            pygame.image.load(f"sprites/invader{type}.png"),
            pygame.image.load(f"sprites/invader{type}_1.png")
        ]
        path = f"sprites/enemy{type}.png"  # Construct the path to the enemy image based on its type
        self.image = self.frames[0]  # Load the enemy image
        self.rect = self.image.get_rect(topleft=(x, y))  # Get the rectangle of the image

    def update(self, direction):
        self.rect.x += direction  # Move the enemy in the specified direction
        self.image = self.frames[(pygame.time.get_ticks() // 500) % 2]
        if self.rect.right >= screen_width or self.rect.left <= 0:  # Check if the enemy has reached the edge of the screen
            return True  # Return True if the enemy has reached the edge
        return False  # Return False if the enemy has not reached the edge

class mystery_invader(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_offset):
        super().__init__()
        self.screen_width = screen_width
        self.offset = screen_offset
        self.image = mystery_invader_sprite  # Load the mystery enemy image
        x=random.choice([self.offset//2 , screen_width + self.offset - self.image.get_width()])
        if x == self.offset//2:
            self.speed = 3
        else:
            self.speed = -3
        self.rect = self.image.get_rect(topleft=(x, 80))  # Get the rectangle of the image

    def update(self):
        self.rect.x += self.speed  # Move the mystery enemy in the specified direction
        if self.rect.left > self.screen_width + screen_offset//2:  # Check if the mystery enemy has moved off-screen
            self.kill()  # Remove the mystery enemy from all groups
        elif self.rect.right < self.offset//2:  # Check if the mystery enemy has moved off-screen
            self.kill()  # Remove the mystery enemy from all groups