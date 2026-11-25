import pygame
from config import GRAY, RED, WHITE


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font("font/PressStart2P.ttf", 20)
        self.game_over_txt = self.font.render("GAME OVER", False, RED)
        self.pause_txt = self.font.render("PAUSED", False, WHITE)
        self.score_txt = self.font.render("SCORE", False, WHITE)
        self.highscore_txt = self.font.render("HI-SCORE", False, WHITE)

    def draw(self, game):
        self.screen.fill(GRAY)
        pygame.draw.rect(self.screen, WHITE, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)
        pygame.draw.line(self.screen, WHITE, (25, 730), (775, 730), 3)

        # Statut (Game Over / Pause / Niveau)
        if not game.game_is_running:
            self.screen.blit(self.game_over_txt, (570, 750))
        elif game.paused:
            self.screen.blit(self.pause_txt, (570, 750))
        else:
            level_txt = self.font.render(f"LEVEL {game.level:02}", False, WHITE)
            self.screen.blit(level_txt, (570, 750))

        # Vies restantes (utilise original_image pour ne pas clignoter)
        x = 50
        for _ in range(game.lives):
            self.screen.blit(game.spaceship_group.sprite.original_image, (x, 750))
            x += 50

        # Score & Highscore
        self.screen.blit(self.score_txt, (50, 25))
        score_surface = self.font.render(str(game.score).zfill(5), False, WHITE)
        self.screen.blit(score_surface, (50, 45))

        self.screen.blit(self.highscore_txt, (550, 25))
        highscore_surface = self.font.render(str(game.highscore).zfill(5), False, WHITE)
        self.screen.blit(highscore_surface, (610, 45))

        # Entités du jeu
        game.spaceship_group.draw(self.screen)
        game.spaceship_group.sprite.lasers_group.draw(self.screen)
        for obstacle in game.obstacles:
            obstacle.blocks_group.draw(self.screen)
        game.invaders_group.draw(self.screen)
        game.invaders_lasers_group.draw(self.screen)
        game.mystery_invaders_group.draw(self.screen)

        pygame.display.flip()