import pygame, random
from entities.spaceship import Spaceship
from entities.obstacle import Obstacle
from config import *
from entities.invaders import invader, mystery_invader
from entities.laser import Laser

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
        self.explosion_sound = explosion_sound
        self.invader_killed_sound = invader_killed_sound
        self.game_over_sound = game_over_sound
        self.ufo_highpitch = ufo_highpitch
        self.ufo_lowpitch = ufo_lowpitch
        self.impact_sound = impact_sound
        self.level = 1
        self.paused = False
        pygame.mixer.music.load("sfx/start.wav")
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(start_volume)

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
        for row in range(len(row_types)):  # Create 5 rows of enemies
            for col in range(10):  # Create 10 columns of enemies
                type = row_types[row]  # Determine the type of enemy based on the row
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
            laser_sprite = Laser(position=(random_enemy.rect.centerx, random_enemy.rect.bottom), speed=4, screen_offset=self.offset, image=invaders_laser_sprite)  # Create a laser at the enemy's position
            self.invaders_lasers_group.add(laser_sprite)  # Add the laser to the enemies' lasers group

    def spawn_mystery_invader(self):
        if len(self.mystery_invaders_group) == 0:  # Check if there are no mystery enemies on the screen
            mystery_enemy_sprite = mystery_invader(self.screen_width, self.offset)  # Create a new mystery enemy
            self.mystery_invaders_group.add(mystery_enemy_sprite)  # Add the mystery enemy to the group
            self.ufo_highpitch.play()
            self.ufo_highpitch.set_volume(ufo_volume)
            self.ufo_lowpitch.play()
            self.ufo_lowpitch.set_volume(ufo_volume)

    def check_for_collisions(self):

        # Check for collisions between spaceship lasers and enemies
        for laser in self.spaceship_group.sprite.lasers_group:
            enemy_hit = pygame.sprite.spritecollideany(laser, self.invaders_group)  # Check if the laser hits any enemy
            if enemy_hit:
                self.invader_killed_sound.play()
                self.invader_killed_sound.set_volume(invader_killed_volume)
                self.score += (enemy_hit.type+1) * 100
                laser.kill()  # Remove the laser
                enemy_hit.kill()  # Remove the enemy
                self.check_for_highscore()

        # Check for collisions between spaceship lasers and mystery enemies
        spaceship = self.spaceship_group.sprite
        for laser in self.spaceship_group.sprite.lasers_group:
            mystery_invader_hit = pygame.sprite.spritecollideany(laser, self.mystery_invaders_group)  # Check if the laser hits any mystery enemy
            if mystery_invader_hit:
                self.invader_killed_sound.play()
                self.invader_killed_sound.set_volume(invader_killed_volume)
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
                if not spaceship.is_invincible():
                    if self.lives <= 0:  # Check if the player has no lives left
                        self.game_over()  # Call the game over method
                    else:
                        self.impact_sound.play(maxtime=invincible_duration)
                        self.impact_sound.set_volume(impact_volume)
                        spaceship.hit()
                        self.lives -= 1  # Decrease the player's lives by 1

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
            self.spaceship_group.sprite.explode()
            self.explosion_sound.play()
            self.explosion_sound.set_volume(explosion_volume)
            self.game_over_sound.play()
            self.game_over_sound.set_volume(game_over_volume)
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

            with open("engine/highscore.txt", "w") as file:
                file.write(str(self.highscore))

    def load_highscore(self):
        try:
            with open("engine/highscore.txt", "r") as file:
                self.highscore = int(file.read())
        except FileNotFoundError:
            self.highscore = 0
