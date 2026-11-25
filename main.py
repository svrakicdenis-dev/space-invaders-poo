"""
Space Invaders : Python Edition
Fait : Thomas Salayet & Denis Svrakic
"""

import random
import sys
import pygame
from config import (
    CAN_SHOOT_TIMER,
    FPS,
    MYSTERY_MAX_INTERVAL,
    MYSTERY_MIN_INTERVAL,
    SCREEN_HEIGHT,
    SCREEN_OFFSET,
    SCREEN_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from engine import Game, Renderer


def main():
    pygame.init()
    icon = pygame.image.load("sprites/invader1_1.png")
    pygame.display.set_icon(icon)

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Space Invaders : Python Edition")
    clock = pygame.time.Clock()

    mystery_invader_spawn = pygame.USEREVENT
    can_shoot = pygame.USEREVENT + 1

    pygame.time.set_timer(can_shoot, CAN_SHOOT_TIMER)
    pygame.time.set_timer(
        mystery_invader_spawn, random.randint(MYSTERY_MIN_INTERVAL, MYSTERY_MAX_INTERVAL)
    )

    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_OFFSET, can_shoot)
    renderer = Renderer(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == can_shoot and game.game_is_running and not game.paused:
                game.fire_invaders_lasers()
            elif (
                event.type == mystery_invader_spawn
                and game.game_is_running
                and not game.paused
            ):
                game.spawn_mystery_invader()
                next_interval = random.randint(
                    MYSTERY_MIN_INTERVAL, MYSTERY_MAX_INTERVAL
                )
                pygame.time.set_timer(mystery_invader_spawn, next_interval)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if game.game_is_running:
                        game.paused = not game.paused
                    else:
                        running = False
                elif event.key == pygame.K_SPACE and not game.game_is_running:
                    game.reset()

        game.update()
        renderer.draw(game)
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()