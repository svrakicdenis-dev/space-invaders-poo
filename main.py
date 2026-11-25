import pygame, sys, random

pygame.init() # Initialize Pygame
icon = pygame.image.load("sprites/invader1_1.png")
pygame.display.set_icon(icon)
"""

Pygame : Python Edition
Made By : Thomas Sa. & Denis Sv.

"""


# ----- Variables -----

# Set up the display
screen_width = 750
screen_height = 700
screen_offset = 50 # Ensure the game doesn't brutally ends on both sides of the screen + allows for the construction of the UI

# Define colors
gray = (29, 29, 29)
white = (255, 255, 255)
red = (255, 0, 0)

# Define font and texts
font = pygame.font.Font("font/PressStart2P.ttf", 20)

game_over_txt = font.render("GAME OVER", False, red)
score_txt = font.render("SCORE", False, white)
highscore_txt = font.render("HI-SCORE", False, white)

# Define sprites
spaceship_image = pygame.image.load("sprites/spaceship.png")  # Load spaceship image
laser_image = pygame.image.load("sprites/laser.png")  # Load laser image




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
can_shoot_timer = 300 # Set the timer interval for shooting in milliseconds

mystery_invader_spawn = pygame.USEREVENT # Set the timer interval for spawning mystery enemies in milliseconds
mystery_invader_interval = random.randint(10000, 20000) # Set the timer interval for spawning mystery enemies in milliseconds

pygame.time.set_timer(can_shoot, can_shoot_timer) # Set the timer for shooting
pygame.time.set_timer(mystery_invader_spawn, mystery_invader_interval) # Set the timer for spawning mystery enemies




clock = pygame.time.Clock() # Create a clock object to control the frame rate


# ----- Spaceship class -----
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, screen_offset):
        super().__init__()
        self.offset = screen_offset
        self.image = spaceship_image  # Use the loaded spaceship image
        self.rect = self.image.get_rect(center=((screen_width + self.offset)// 2, screen_height - 50))  # Place the spaceship 
        self.speed = 5  # Set the speed of the spaceship
        self.lasers_group = pygame.sprite.Group()  # Create a group to hold the lasers
        self.laser_ready = True  # Flag to check if the laser can be fired (avoids continuous firing)
        self.laser_time = 0  # Timer to control the laser firing rate
        self.laser_delay = 500 # Delay counter for laser firing
        self.laser_sound = pygame.mixer.Sound("sfx/shoot.wav")

    def get_user_input(self):
        keys = pygame.key.get_pressed()  # Get the state of all keyboard buttons
        if keys[pygame.K_LEFT] and self.rect.left > self.offset:  # Move left if left arrow is pressed and not at the edge
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:  # Move right if right arrow is pressed and not at the edge of the window
            self.rect.x += self.speed
        if keys[pygame.K_SPACE] and self.laser_ready:  # Fire laser if spacebar is pressed and the laser is ready
            self.laser_ready = False  # Set the flag to False to indicate that the laser is not ready to be fired again
            laser = Laser(position=(self.rect.centerx, self.rect.top), speed=-8, screen_offset=self.offset)  # Create a new laser at the spaceship's position
            self.lasers_group.add(laser)  # Add the laser to the lasers group
            self.laser_time = pygame.time.get_ticks()  # Record the time when the laser was fired
            self.laser_sound.play()

    def update(self):
        self.get_user_input()  # Update the spaceship's position based on user input
        self.lasers_group.update()  # Update the lasers' positions
        self.recharge_laser()  # Check if the laser can be recharged

    def recharge_laser(self):
        if not self.laser_ready:  # If the laser is not ready
            time_since_pressed = pygame.time.get_ticks()  # Get the current time in milliseconds
            if time_since_pressed - self.laser_time >= self.laser_delay:  # If the delay has passed
                self.laser_ready = True  # Set the laser to be ready again

    def reset(self):
        self.rect = self.image.get_rect(center=((screen_width + self.offset) // 2, screen_height - 50))
        self.lasers_group.empty()

# ----- Laser class -----
class Laser(pygame.sprite.Sprite):
    def __init__(self, position, speed, screen_offset):
        super().__init__()
        self.offset = screen_offset
        self.image = laser_image  # Use the loaded laser image
        self.rect = self.image.get_rect(center = position)  # Get the rectangle of the image
        self.speed = speed  # Set the speed of the laser

    def update(self):
        self.rect.y += self.speed  # Move the laser upward
        if self.rect.bottom < self.offset:  # Remove the laser if it goes off-screen
            self.kill()

# ----- Block class -----
# Contains each block of the obstacle
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((3, 3))  # Create a surface for the obstacle
        self.image.fill((255, 255, 255)) 
        self.rect = self.image.get_rect(topleft = (x, y))

# ----- Obstacle class -----
class Obstacle:
    def __init__(self, x, y):
        self.blocks_group = pygame.sprite.Group()  # Create a sprite group for the blocks
        for row in range(len(obstacle_grid)):
            for col in range(len(obstacle_grid[row])):
                if obstacle_grid[row][col] == 1:
                    block = Block(col * 3 + x, row * 3 + y)  # Create an instance of the Block class
                    self.blocks_group.add(block)  # Add the block to the group

# ----- Invader Class -----
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

# ----- Mystery Invader Class -----
class mystery_invader(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_offset):
        super().__init__()
        self.screen_width = screen_width
        self.offset = screen_offset
        self.image = pygame.image.load("sprites/mystery.png")  # Load the mystery enemy image
        x=random.choice([self.offset//2 , screen_width + self.offset - self.image.get_width()])
        if x == self.offset//2:
            self.speed = 3
        else:
            self.speed = -3
        self.rect = self.image.get_rect(topleft=(x, 80))  # Get the rectangle of the image
        # self.image = pygame.transform.scale(self.image, (54, 22))  # Scale the image

    def update(self):
        self.rect.x += self.speed  # Move the mystery enemy in the specified direction
        if self.rect.left > self.screen_width + screen_offset//2:  # Check if the mystery enemy has moved off-screen
            self.kill()  # Remove the mystery enemy from all groups
        elif self.rect.right < self.offset//2:  # Check if the mystery enemy has moved off-screen
            self.kill()  # Remove the mystery enemy from all groups

# ----- Game Class -----
class Game:
    def __init__(self, screen_width, screen_height, screen_offset):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset = screen_offset
        self.spaceship_group = pygame.sprite.GroupSingle()
        self.spaceship_group.add(Spaceship(self.screen_width, self.screen_height, self.offset))  # Create a sprite group for the spaceship
        self.obstacles = []  # List to hold the obstacles
        self.create_obstacles()  # Create the obstacles
        self.obstacles = self.create_obstacles()  # Store the created obstacles in the list
        self.invaders_group = pygame.sprite.Group()  # Create a sprite group for the enemies
        self.spawn_invaders()  # Create the enemies
        self.invaders_direction = 1  # Set the initial direction of the enemies
        self.invaders_lasers_group = pygame.sprite.Group()  # Create a sprite group for the enemies' lasers
        self.mystery_invaders_group = pygame.sprite.GroupSingle()  # Create a sprite group for the mystery enemies
        self.lives = 3  # Set the initial number of lives for the player
        self.game_is_running = True  # Flag to control the game loop
        self.score = 0
        self.highscore = 0
        self.load_highscore()
        self.explosion_sound = pygame.mixer.Sound("sfx/explosion.wav")
        self.invaderkilled_sound = pygame.mixer.Sound("sfx/invaderkilled.wav")
        self.game_over_sound = pygame.mixer.Sound("sfx/game_over.wav")
        self.ufo_highpitch = pygame.mixer.Sound("sfx/ufo_highpitch.wav")
        self.ufo_lowpitch = pygame.mixer.Sound("sfx/ufo_lowpitch.wav")
        self.level = 1
        self.paused = False
        pygame.mixer.music.load("sfx/start.wav")
        pygame.mixer.music.play()

    def create_obstacles(self):
        obstacle_width = len(obstacle_grid[0]) * 3  # Calculate the width of the obstacle based on the grid
        spacing = (self.screen_width + screen_offset - (4 * obstacle_width)) // 5  # Calculate the spacing between obstacles
        obstacles = []
        for i in range(4):  # Create 4 obstacles
            x = spacing + (obstacle_width + spacing) * i  # Calculate the x position of the obstacle
            y = self.screen_height - 150  # Set the y position of the obstacle
            obstacle = Obstacle(x, self.screen_height - 150)  # Create an instance of the Obstacle class
            obstacles.append(obstacle)  # Add the obstacle to the list
        return obstacles  # Return the list of obstacles

    def draw_obstacles(self):
        for obstacle in self.obstacles:
            obstacle.blocks_group.draw(screen)  # Draw each block in the obstacle group

    def spawn_invaders(self):
        for row in range(5):  # Create 5 rows of enemies
            for col in range(10):  # Create 10 columns of enemies
                type = (row % 3)  # Determine the type of enemy based on the row
                x = col * 60 + 100  # Calculate the x position of the enemy
                y = row * 50 + 150  # Calculate the y position of the enemy
                inst_enemy = invader(type, x + screen_offset//2, y)  # Create an instance of the enemy class
                self.invaders_group.add(inst_enemy)  # Add the enemy to the enemies group

    def move_invaders(self):
        self.invaders_group.update(self.invaders_direction)  # Update the position of the enemies based on the current direction

        has_invader_reach_edge = any(enemy.rect.right >= self.screen_width + screen_offset // 2 or enemy.rect.left <= self.offset // 2 for enemy in self.invaders_group)  # Check if any enemy has reached the edge of the screen
        if has_invader_reach_edge:  # If any enemy has reached the edge
            self.invaders_direction *= -1  # Reverse the direction of the enemies
            for enemy in self.invaders_group:  # Move all enemies down by 10 pixels
                enemy.rect.y += 10

    def fire_invaders_lasers(self):
        if len(self.invaders_group) > 0:  # Check if there are any enemies left
            random_enemy = random.choice(self.invaders_group.sprites())  # Choose a random enemy from the group
            laser_sprite = Laser(position=(random_enemy.rect.centerx, random_enemy.rect.bottom), speed=4, screen_offset=self.offset)  # Create a laser at the enemy's position
            self.invaders_lasers_group.add(laser_sprite)  # Add the laser to the enemies' lasers group

    def spawn_mystery_invader(self):
        if len(self.mystery_invaders_group) == 0:  # Check if there are no mystery enemies on the screen
            mystery_enemy_sprite = mystery_invader(self.screen_width, self.offset)  # Create a new mystery enemy
            self.mystery_invaders_group.add(mystery_enemy_sprite)  # Add the mystery enemy to the group
            self.ufo_highpitch.play()
            self.ufo_lowpitch.play()

    def check_for_collisions(self):
        # Check for collisions between spaceship lasers and enemies
        for laser in self.spaceship_group.sprite.lasers_group:
            enemy_hit = pygame.sprite.spritecollideany(laser, self.invaders_group)  # Check if the laser hits any enemy
            if enemy_hit:
                self.invaderkilled_sound.play()
                self.score += (enemy_hit.type+1) * 100
                laser.kill()  # Remove the laser
                enemy_hit.kill()  # Remove the enemy
                self.check_for_highscore()

        # Check for collisions between spaceship lasers and mystery enemies
        for laser in self.spaceship_group.sprite.lasers_group:
            mystery_invader_hit = pygame.sprite.spritecollideany(laser, self.mystery_invaders_group)  # Check if the laser hits any mystery enemy
            if mystery_invader_hit:
                self.invaderkilled_sound.play()
                self.score += 500
                laser.kill()  # Remove the laser
                mystery_invader_hit.kill()  # Remove the mystery enemy
                self.check_for_highscore()

        for obstacle in self.obstacles:
            for block in obstacle.blocks_group:
                # Check for collisions between spaceship lasers and obstacle blocks
                for laser in self.spaceship_group.sprite.lasers_group:
                    if pygame.sprite.collide_rect(laser, block):  # Check if the laser collides with the block
                        laser.kill()  # Remove the laser
                        block.kill()  # Remove the block

                # Check for collisions between enemies' lasers and obstacle blocks
                for laser in self.invaders_lasers_group:
                    if pygame.sprite.collide_rect(laser, block):  # Check if the laser collides with the block
                        laser.kill()  # Remove the laser
                        block.kill()  # Remove the block

        for laser in self.invaders_lasers_group:
            if pygame.sprite.collide_rect(laser, self.spaceship_group.sprite):  # Check if the laser collides with the spaceship
                laser.kill()  # Remove the laser
                self.lives -= 1  # Decrease the player's lives by 1
                if self.lives <= 0:  # Check if the player has no lives left
                    self.game_over()  # Call the game over method

        # Check if 2 lasers collide with each others
        for invader_laser in self.invaders_lasers_group:
            for spaceship_laser in self.spaceship_group.sprite.lasers_group:
                if pygame.sprite.collide_rect(invader_laser, spaceship_laser):
                    invader_laser.kill() # Remove both lasers
                    spaceship_laser.kill()


        if len(self.invaders_group) > 0:
            for invader in self.invaders_group:
                for obstacle in self.obstacles:
                    for block in obstacle.blocks_group:
                        if pygame.sprite.collide_rect(invader, block):  # Check if the enemy collides with the block
                            block.kill()  # Remove the block

                if pygame.sprite.collide_rect(invader, self.spaceship_group.sprite):  # Check if the enemy collides with the spaceship
                    self.game_over()  # Call the game over method

    def check_for_next_level(self):
        if len(self.invaders_group) == 0: # Check if enemy are left
            self.level += 1
            self.invaders_direction = 1
            self.invaders_lasers_group.empty()
            self.spaceship_group.sprite.reset()
            self.spawn_invaders()
            self.obstacles = self.create_obstacles()
            new_timer = max(can_shoot_timer - (self.level - 1) * 30, 100)
            pygame.time.set_timer(can_shoot, new_timer)


    def game_over(self):
            self.explosion_sound.play()
            self.game_over_sound.play()
            self.game_is_running = False  # Set the game running flag to False

    def reset(self):
        self.game_is_running = True
        self.lives = 3
        self.spaceship_group.sprite.reset()
        self.invaders_group.empty()
        self.invaders_lasers_group.empty()
        self.spawn_invaders()
        self.mystery_invaders_group.empty()
        self.obstacles = self.create_obstacles()
        self.score = 0
        self.level = 1
        self.invaders_direction = 1
        pygame.time.set_timer(can_shoot, can_shoot_timer)

    def check_for_highscore(self):
        if self.score > self.highscore:
            self.highscore = self.score

            with open("highscore.txt", "w") as file:
                file.write(str(self.highscore))

    def load_highscore(self):
        try:
            with open("highscore.txt", "r") as file:
                self.highscore = int(file.read())
        except FileNotFoundError:
            self.highscore = 0

game = Game(screen_width, screen_height, screen_offset)  # Create an instance of the Game class

running = True
while running:
    # 1. Handling Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == can_shoot and game.game_is_running and not game.paused:  # Check if the custom shooting event has occurred
            game.fire_invaders_lasers()  # Fire lasers from the enemies
        if event.type == mystery_invader_spawn and game.game_is_running and not game.paused:  # Check if the custom mystery enemy spawn event has occurred
            game.spawn_mystery_invader()  # Spawn a mystery enemy
            mystery_invader_interval = random.randint(10000, 20000)  # Set a new random timer for the next spawn
            pygame.time.set_timer(mystery_invader_spawn, mystery_invader_interval)  # Reset the timer for spawning mystery enemies
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and game.game_is_running:
            game.paused = not game.paused

        keys = pygame.key.get_pressed()  # Get the state of all keyboard buttons
        if keys[pygame.K_ESCAPE] and game.game_is_running == False:
            pygame.quit()
            sys.exit()

        if keys[pygame.K_SPACE] and game.game_is_running == False:
            game.reset()
        

    # 2. Updating Positions
    if game.game_is_running and not game.paused:  # Check if the game is still running
        pygame.display.update()  # Update the display
        game.spaceship_group.update()  # Update the spaceship's position and lasers
        game.move_invaders()  # Move the enemies
        game.invaders_lasers_group.update()  # Update the enemies' lasers' positions
        game.mystery_invaders_group.update()  # Update the mystery enemies' positions
        game.check_for_collisions()  # Check for collisions between lasers and enemies
        game.check_for_next_level()



    # 3. Drawing to the Screen
    # UI Elements
    screen.fill(gray)  # Fill the screen with gray
    pygame.draw.rect(screen, white, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)
    pygame.draw.line(screen, white, (25, 730), (775, 730), 3)

    if not game.game_is_running:
        screen.blit(game_over_txt, (570, 750, 50, 50)) # Formatted game over screen
    elif game.paused:
        pause_txt = font.render("PAUSED", False, white)
        screen.blit(pause_txt, (570, 750))
    else:
        level_txt = font.render(f"LEVEL {game.level:02}", False, white) # Formatted level screen
        screen.blit(level_txt, (570, 750, 50, 50))

    x = 50
    for life in range(game.lives):
        screen.blit(game.spaceship_group.sprite.image, (x, 750))
        x += 50


    # Formatted score
    screen.blit(score_txt, (50, 25 , 50, 50))
    formatted_score = str(game.score).zfill(5)
    game_score_txt = font.render(formatted_score, False, white)
    screen.blit(game_score_txt, (50, 45, 50, 50))

    # Formatted highscore
    screen.blit(highscore_txt, (550, 25, 50, 50))
    formatted_highscore = str(game.highscore).zfill(5)
    game_highscore_txt = font.render(formatted_highscore, False, white)
    screen.blit(game_highscore_txt, (610, 45, 50, 50))

    game.spaceship_group.draw(screen)  # Draw the spaceship
    game.spaceship_group.sprite.lasers_group.draw(screen)  # Draw the lasers
    game.draw_obstacles()  # Draw the obstacles
    for obstacles in game.obstacles:
        obstacles.blocks_group.draw(screen)  # Draw each block in the obstacle group
    game.invaders_group.draw(screen)  # Draw the enemies
    game.invaders_lasers_group.draw(screen)  # Draw the enemies' lasers
    game.mystery_invaders_group.draw(screen)  # Draw the mystery enemies
    pygame.display.flip()  # Update the display
    clock.tick(60)  # Limit the frame rate to 60 FPS
