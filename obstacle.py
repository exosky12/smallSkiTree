import pygame
import os
import random

class Obstacle:
    def __init__(self, x, y, image_path, speed, width, height):
        self.x = x
        self.y = y
        self.image = pygame.image.load(os.path.join("assets", "images", image_path))
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.speed = speed

    def move(self):
        self.y += self.speed

    def display(self, window):
        window.blit(self.image, (self.x, self.y))