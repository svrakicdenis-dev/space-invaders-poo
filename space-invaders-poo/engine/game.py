import random
import pygame
from config import CAN_SHOOT_TIMER, HIGHSCORE_FILE, OBSTACLE_GRID
from entities import Invader, Laser, MysteryInvader, Obstacle, Spaceship


class Game:
    def __init__(self, screen_width, screen_height, screen_offset, can_shoot_event):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset = screen_offset
        self.can_shoot_event = can_shoot_event

        self.spaceship_group = pygame.sprite.GroupSingle(
            Spaceship(self.screen_width, self.screen_height, self.offset)
        )
        self.obstacles = self.create_obstacles()
        self.invaders_group = pygame.sprite.Group()
        self.spawn_invaders()
        self.invaders_direction = 1
        self.invaders_lasers_group = pygame.sprite.Group()
        self.mystery_invaders_group = pygame.sprite.GroupSingle()

        self.lives = 3
        self.game_is_running = True
        self.paused = False
        self.score = 0
        self.highscore = 0
        self.level = 1
        self.load_highscore()

        self.explosion_sound = pygame.mixer.Sound("sfx/explosion.wav")
        self.invaderkilled_sound = pygame.mixer.Sound("sfx/invaderkilled.wav")
        self.game_over_sound = pygame.mixer.Sound("sfx/game_over.wav")
        self.ufo_highpitch = pygame.mixer.Sound("sfx/ufo_highpitch.wav")
        self.ufo_lowpitch = pygame.mixer.Sound("sfx/ufo_lowpitch.wav")

        pygame.mixer.music.load("sfx/start.wav")
        pygame.mixer.music.play()

    def create_obstacles(self):
        obstacle_width = len(OBSTACLE_GRID[0]) * 3
        spacing = (self.screen_width + self.offset - (4 * obstacle_width)) // 5
        obstacles = []
        for i in range(4):
            x = spacing + (obstacle_width + spacing) * i
            y = self.screen_height - 150
            obstacles.append(Obstacle(x, y))
        return obstacles

    def spawn_invaders(self):
        for row in range(5):
            for col in range(10):
                invader_type = row % 3
                x = col * 60 + 100 + self.offset // 2
                y = row * 50 + 150
                self.invaders_group.add(Invader(invader_type, x, y))

    def move_invaders(self):
        self.invaders_group.update(self.invaders_direction)
        reached_edge = any(
            inv.rect.right >= self.screen_width + self.offset // 2
            or inv.rect.left <= self.offset // 2
            for inv in self.invaders_group
        )
        if reached_edge:
            self.invaders_direction *= -1
            for inv in self.invaders_group:
                inv.rect.y += 10

    def fire_invaders_lasers(self):
        if self.invaders_group:
            shooter = random.choice(self.invaders_group.sprites())
            laser = Laser(
                position=(shooter.rect.centerx, shooter.rect.bottom),
                speed=4,
                screen_offset=self.offset,
            )
            self.invaders_lasers_group.add(laser)

    def spawn_mystery_invader(self):
        if len(self.mystery_invaders_group) == 0:
            self.mystery_invaders_group.add(
                MysteryInvader(self.screen_width, self.offset)
            )
            self.ufo_highpitch.play()
            self.ufo_lowpitch.play()

    def update(self):
        if not self.game_is_running or self.paused:
            return
        self.spaceship_group.update()
        self.move_invaders()
        self.invaders_lasers_group.update()
        self.mystery_invaders_group.update()
        self.check_for_collisions()
        self.check_for_next_level()

    def check_for_collisions(self):
        player = self.spaceship_group.sprite

        # Tirs du joueur -> envahisseurs et vaisseau bonus
        for laser in player.lasers_group:
            invader_hit = pygame.sprite.spritecollideany(laser, self.invaders_group)
            if invader_hit:
                self.invaderkilled_sound.play()
                self.score += invader_hit.score_value
                laser.kill()
                invader_hit.kill()
                self.check_for_highscore()
                continue

            mystery_hit = pygame.sprite.spritecollideany(
                laser, self.mystery_invaders_group
            )
            if mystery_hit:
                self.invaderkilled_sound.play()
                self.score += mystery_hit.score_value
                laser.kill()
                mystery_hit.kill()
                self.check_for_highscore()

        # Lasers -> obstacles
        for obstacle in self.obstacles:
            pygame.sprite.groupcollide(
                player.lasers_group, obstacle.blocks_group, True, True
            )
            pygame.sprite.groupcollide(
                self.invaders_lasers_group, obstacle.blocks_group, True, True
            )

        # Lasers ennemis -> joueur (avec clignotement et courte invincibilité)
        for laser in self.invaders_lasers_group:
            if pygame.sprite.collide_rect(laser, player):
                laser.kill()
                if not player.is_blinking:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over()
                    else:
                        player.trigger_blink()

        # Lasers joueur <-> lasers ennemis
        pygame.sprite.groupcollide(
            self.invaders_lasers_group, player.lasers_group, True, True
        )

        # Envahisseurs -> obstacles et joueur
        for inv in self.invaders_group:
            for obstacle in self.obstacles:
                pygame.sprite.spritecollide(inv, obstacle.blocks_group, True)
            if pygame.sprite.collide_rect(inv, player):
                self.game_over()

    def check_for_next_level(self):
        if len(self.invaders_group) == 0:
            self.level += 1
            self.invaders_direction = 1
            self.invaders_lasers_group.empty()
            self.spaceship_group.sprite.reset()
            self.spawn_invaders()
            self.obstacles = self.create_obstacles()
            new_timer = max(CAN_SHOOT_TIMER - (self.level - 1) * 30, 100)
            pygame.time.set_timer(self.can_shoot_event, new_timer)

    def game_over(self):
        self.explosion_sound.play()
        self.game_over_sound.play()
        self.game_is_running = False

    def reset(self):
        self.game_is_running = True
        self.paused = False
        self.lives = 3
        self.spaceship_group.sprite.reset()
        self.invaders_group.empty()
        self.invaders_lasers_group.empty()
        self.mystery_invaders_group.empty()
        self.spawn_invaders()
        self.obstacles = self.create_obstacles()
        self.score = 0
        self.level = 1
        self.invaders_direction = 1
        pygame.time.set_timer(self.can_shoot_event, CAN_SHOOT_TIMER)

    def check_for_highscore(self):
        if self.score > self.highscore:
            self.highscore = self.score
            with open(HIGHSCORE_FILE, "w", encoding="utf-8") as file:
                file.write(str(self.highscore))

    def load_highscore(self):
        try:
            with open(HIGHSCORE_FILE, "r", encoding="utf-8") as file:
                self.highscore = int(file.read().strip() or 0)
        except (FileNotFoundError, ValueError):
            self.highscore = 0