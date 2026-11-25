import random
import pygame


class Invader(pygame.sprite.Sprite):
    _frames_cache = {}

    def __init__(self, invader_type, x, y):
        super().__init__()
        self.type = invader_type
        self.score_value = (invader_type + 1) * 100

        if invader_type not in Invader._frames_cache:
            Invader._frames_cache[invader_type] = [
                pygame.image.load(f"sprites/invader{invader_type}.png"),
                pygame.image.load(f"sprites/invader{invader_type}_1.png"),
            ]

        self.frames = Invader._frames_cache[invader_type]
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, direction):
        self.rect.x += direction
        self.image = self.frames[(pygame.time.get_ticks() // 500) % 2]


class MysteryInvader(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_offset):
        super().__init__()
        self.screen_width = screen_width
        self.offset = screen_offset
        self.image = pygame.image.load("sprites/mystery.png")
        self.score_value = 500

        start_left = self.offset // 2
        start_right = self.screen_width + self.offset - self.image.get_width()
        x = random.choice([start_left, start_right])
        self.speed = 3 if x == start_left else -3
        self.rect = self.image.get_rect(topleft=(x, 80))

    def update(self):
        self.rect.x += self.speed
        if (
            self.rect.left > self.screen_width + self.offset // 2
            or self.rect.right < self.offset // 2
        ):
            self.kill()