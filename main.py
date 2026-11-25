import pygame, sys, random
pygame.init() # Initialize Pygame
from config import *
from engine.game import Game

pygame.display.set_icon(icon)

"""

Pygame : Python Edition
Made By : Thomas Sa. & Denis Sv.

"""

clock = pygame.time.Clock() # Create a clock object to control the frame rate
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
            running = False
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
        screen.blit(game.spaceship_group.sprite.original_image, (x, 750))
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
    clock.tick(FPS)  # Limit the frame rate to 60 FPS
