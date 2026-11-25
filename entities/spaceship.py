import pygame
from entities.laser import Laser
from config import *

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, screen_offset):
        super().__init__()
        self.offset = screen_offset
        self.image = spaceship_sprite  # Use the loaded spaceship image
        self.rect = self.image.get_rect(center=((screen_width + self.offset)// 2, screen_height - 50))  # Place the spaceship 
        self.speed = 5  # Set the speed of the spaceship
        self.lasers_group = pygame.sprite.Group()  # Create a group to hold the lasers
        self.laser_ready = True  # Flag to check if the laser can be fired (avoids continuous firing)
        self.laser_time = 0  # Timer to control the laser firing rate
        self.laser_delay = 500 # Delay counter for laser firing
        self.laser_sound = laser_sound
        self.laser_sound.set_volume(laser_volume)
        self.original_image = self.image
        self.blank_image = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)  # fully transparent
        self.invincible_duration = invincible_duration
        self.hit_time = -self.invincible_duration

    def get_user_input(self):
        keys = pygame.key.get_pressed()  # Get the state of all keyboard buttons
        if keys[pygame.K_LEFT] and self.rect.left > self.offset:  # Move left if left arrow is pressed and not at the edge
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:  # Move right if right arrow is pressed and not at the edge of the window
            self.rect.x += self.speed
        if keys[pygame.K_SPACE] and self.laser_ready:  # Fire laser if spacebar is pressed and the laser is ready
            self.laser_ready = False  # Set the flag to False to indicate that the laser is not ready to be fired again
            laser = Laser(position=(self.rect.centerx, self.rect.top), speed=-8, screen_offset=self.offset, image=spaceship_laser_sprite)  # Create a new laser at the spaceship's position
            self.lasers_group.add(laser)  # Add the laser to the lasers group
            self.laser_time = pygame.time.get_ticks()  # Record the time when the laser was fired
            self.laser_sound.play()

    def update(self):
        self.get_user_input()  # Update the spaceship's position based on user input
        self.lasers_group.update()  # Update the lasers' positions
        self.recharge_laser()  # Check if the laser can be recharged

        if self.is_invincible():
            if (pygame.time.get_ticks() // 100) % 2 == 0:
                self.image = self.blank_image
            else:
                self.image = self.original_image
        else:
            self.image = self.original_image

    def recharge_laser(self):
        if not self.laser_ready:  # If the laser is not ready
            time_since_pressed = pygame.time.get_ticks()  # Get the current time in milliseconds
            if time_since_pressed - self.laser_time >= self.laser_delay:  # If the delay has passed
                self.laser_ready = True  # Set the laser to be ready again

    def reset(self):
        self.rect = self.image.get_rect(center=((screen_width + self.offset) // 2, screen_height - 50))
        self.lasers_group.empty()
        self.hit_time = -self.invincible_duration
        self.image = self.original_image

    def hit(self):
        self.hit_time = pygame.time.get_ticks()

    def is_invincible(self):
        return pygame.time.get_ticks() - self.hit_time < self.invincible_duration

    def explode(self):
        self.image = spaceship_explosion_sprite
