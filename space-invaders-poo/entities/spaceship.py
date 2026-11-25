import pygame
from entities.laser import Laser


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, screen_offset):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset = screen_offset
        self.original_image = pygame.image.load("sprites/spaceship.png")
        self.empty_image = pygame.Surface(self.original_image.get_size(), pygame.SRCALPHA)
        self.image = self.original_image
        self.rect = self.image.get_rect(
            center=((self.screen_width + self.offset) // 2, self.screen_height - 50)
        )
        self.speed = 5
        self.lasers_group = pygame.sprite.Group()
        self.laser_ready = True
        self.laser_time = 0
        self.laser_delay = 500
        self.laser_sound = pygame.mixer.Sound("sfx/shoot.wav")

        # Paramètres du clignotement après dégâts
        self.is_blinking = False
        self.blink_start_time = 0
        self.blink_duration = 1500  # Durée totale (1,5 seconde)
        self.blink_interval = 100   # Rythme du clignotement (toutes les 100 ms)

    def get_user_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > self.offset:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < self.screen_width:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE] and self.laser_ready:
            self.shoot()

    def shoot(self):
        self.laser_ready = False
        laser = Laser(
            position=(self.rect.centerx, self.rect.top),
            speed=-8,
            screen_offset=self.offset,
        )
        self.lasers_group.add(laser)
        self.laser_time = pygame.time.get_ticks()
        self.laser_sound.play()

    def trigger_blink(self):
        self.is_blinking = True
        self.blink_start_time = pygame.time.get_ticks()

    def update_blink(self):
        if not self.is_blinking:
            return

        elapsed = pygame.time.get_ticks() - self.blink_start_time
        if elapsed >= self.blink_duration:
            self.is_blinking = False
            self.image = self.original_image
        elif (elapsed // self.blink_interval) % 2 == 0:
            self.image = self.empty_image
        else:
            self.image = self.original_image

    def update(self):
        self.get_user_input()
        self.lasers_group.update()
        self.recharge_laser()
        self.update_blink()

    def recharge_laser(self):
        if not self.laser_ready:
            if pygame.time.get_ticks() - self.laser_time >= self.laser_delay:
                self.laser_ready = True

    def reset(self):
        self.rect = self.original_image.get_rect(
            center=((self.screen_width + self.offset) // 2, self.screen_height - 50)
        )
        self.lasers_group.empty()
        self.laser_ready = True
        self.is_blinking = False
        self.image = self.original_image