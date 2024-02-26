import pygame
import os

width, height = 800, 600

class Skieur:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.images = {
            "straight": pygame.image.load(os.path.join("assets", "images", "skieur.png")),
            "left": pygame.image.load(os.path.join("assets", "images", "skieur_gauche.png")),
            "much_left": pygame.image.load(os.path.join("assets", "images", "skieur_bcpgauche.png")),
            "right": pygame.image.load(os.path.join("assets", "images", "skieur_droite.png")),
            "much_right": pygame.image.load(os.path.join("assets", "images", "skieur_bcpdroite.png")),
        }
        self.image = self.images["straight"]
        self.image = pygame.transform.scale(self.image, (30, 50))
        self.rect = self.image.get_rect()
        self.speed = 4
        self.alive = True

    def move_diagonal(self, direction):
        if self.alive:
            if direction == "left" and self.x > 0:
                self.x -= self.speed
                self.image = self.images["much_left"]
            elif direction == "right" and self.x < width - self.rect.width:
                self.x += self.speed
                self.image = self.images["much_right"]
            else:
                self.image = self.images["straight"]

            self.rect.topleft = (self.x, self.y)

    def display(self, window):
        if self.alive:
            window.blit(self.image, (self.x, self.y))
