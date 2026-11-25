import pygame, random

# Colors
gray = (29, 29, 29)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# font
font = pygame.font.Font("font/PressStart2P.ttf", 20)

# Sprites
spaceship_sprite = pygame.image.load("sprites/spaceship.png") # Load spaceship sprite
spaceship_sprite.fill((green), special_flags=pygame.BLEND_RGB_MULT) # Changes its color
spaceship_explosion_sprite = pygame.image.load("sprites/blown.png")
spaceship_explosion_sprite.fill((red), special_flags=pygame.BLEND_RGB_MULT)

laser_sprite = pygame.image.load("sprites/laser.png")  # Load laser sprite
spaceship_laser_sprite = laser_sprite.copy()
spaceship_laser_sprite.fill((green), special_flags=pygame.BLEND_RGB_MULT)
invaders_laser_sprite = laser_sprite.copy()
invaders_laser_sprite.fill((white), special_flags=pygame.BLEND_RGB_MULT)

invader0_sprite = pygame.image.load("sprites/invader0.png")
invader0_1_sprite = pygame.image.load("sprites/invader0_1.png")

invader1_sprite = pygame.image.load("sprites/invader1.png")
invader1_1_sprite = pygame.image.load("sprites/invader1_1.png")

invader2_sprite = pygame.image.load("sprites/invader2.png")
invader2_1_sprite = pygame.image.load("sprites/invader2_1.png")

mystery_invader_sprite = pygame.image.load("sprites/mystery.png")
mystery_invader_sprite.fill((red), special_flags=pygame.BLEND_RGB_MULT)

row_types = [2, 1, 1, 0, 0] # Row invader types, leave default value for original experience
"""
Invader type 2 = 300 pts
Invader type 1 = 200 pts
Invader type 0 = 100 pts
"""

# Sounds
laser_sound = pygame.mixer.Sound("sfx/shoot.wav")
explosion_sound = pygame.mixer.Sound("sfx/explosion.wav")
invader_killed_sound = pygame.mixer.Sound("sfx/invaderkilled.wav")
game_over_sound = pygame.mixer.Sound("sfx/game_over.wav")
ufo_highpitch = pygame.mixer.Sound("sfx/ufo_highpitch.wav")
ufo_lowpitch = pygame.mixer.Sound("sfx/ufo_lowpitch.wav")
impact_sound = pygame.mixer.Sound("sfx/impact.wav")


# Volumes
start_volume = 0.5
game_over_volume = 0.5

invader_killed_volume = 0.3
laser_volume = 0.3
impact_volume = 0.5
ufo_volume = 0.5
explosion_volume = 0.5

# Game variables
invincible_duration = 1500
shooting_interval_for_invaders = 300


# Screen variables
screen_width = 750
screen_height = 700
screen_offset = 50 # Ensure the game doesn't brutally ends on both sides of the screen + allows for the construction of the UI

# Obstacle grid
obstacle_grid = [ # Initialize the obstacle grid
    [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
    [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
    [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1],
    [1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],
    [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1]]


screen = pygame.display.set_mode((screen_width + screen_offset, screen_height + screen_offset*2)) # Display window
pygame.display.set_caption("Space Invaders : Python Edition") # Set window title

can_shoot = pygame.USEREVENT + 1 # Define a custom event for shooting
can_shoot_timer = shooting_interval_for_invaders # Set the timer interval for shooting in milliseconds

mystery_invader_spawn = pygame.USEREVENT # Set the timer interval for spawning mystery enemies in milliseconds
mystery_invader_interval = random.randint(10000, 20000) # Set the timer interval for spawning mystery enemies in milliseconds

pygame.time.set_timer(can_shoot, can_shoot_timer) # Set the timer for shooting
pygame.time.set_timer(mystery_invader_spawn, mystery_invader_interval) # Set the timer for spawning mystery enemies

game_over_txt = font.render("GAME OVER", False, red)
score_txt = font.render("SCORE", False, white)
highscore_txt = font.render("HI-SCORE", False, white)

FPS = 60
icon = pygame.image.load("sprites/game_icon.png")
