from config import *

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((3, 3))  # Create a surface for the obstacle
        self.image.fill((green)) 
        self.rect = self.image.get_rect(topleft = (x, y))

class Obstacle:
    def __init__(self, x, y):
        self.blocks_group = pygame.sprite.Group()  # Create a sprite group for the blocks
        for row in range(len(obstacle_grid)):
            for col in range(len(obstacle_grid[row])):
                if obstacle_grid[row][col] == 1:
                    block = Block(col * 3 + x, row * 3 + y)  # Create an instance of the Block class
                    self.blocks_group.add(block)  # Add the block to the group