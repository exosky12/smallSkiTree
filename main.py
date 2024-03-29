import pygame
import sys
import random
import os
from skieur import Skieur
from obstacle import Obstacle
from background import Background

pygame.init()
font = pygame.font.Font(os.path.join("assets", "font", "snowtop-caps.regular.ttf"), 56)
vent = pygame.mixer.Sound(os.path.join("assets", "sound", "vent.mp3"))

width, height = 400, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("SkiTree Game")

white = (255, 255, 255)
blue = (0, 0, 255)
background = Background('background.webp', [0,0], width, height)

skieur = Skieur(width // 2, height - 200)
obstacles = []

points = 0
points_per_pixel = 0.01

OBSTACLE_INTERVAL = 150
obstacle_timer = OBSTACLE_INTERVAL
OBSTACLE_SPEED_INITIAL = 4
OBSTACLE_SPEED_INCREMENT = 0.1
MAX_OBSTACLES = 10

SCROLL_LIMIT = 150

with open("data/meilleur_score.txt", "r") as file:
    content = file.read()

best_score = int(content) if content else 0

vent.play()

game_running = True
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not skieur.alive:
                skieur = skieur(width // 2, height - 100)
                obstacles = []
                points = 0
                skieur.speed = 4
                obstacle_timer = OBSTACLE_INTERVAL
                game_running = True

    if skieur.alive:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and skieur.x > 0:
            skieur.move_diagonal("left")
        elif keys[pygame.K_RIGHT] and skieur.x < width - skieur.rect.width:
            skieur.move_diagonal("right")
        else:
            skieur.move_diagonal("straight")

    obstacle_timer -= skieur.speed
    if obstacle_timer <= 0:
        obstacle_x = random.randint(0, width)
        obstacle_y = -50
        obstacle_image = random.choice(["tree.png", "tree_trunk.png"])
        obstacle_width, obstacle_height = 60, 60

        if "tree" in obstacle_image:
            obstacle_width, obstacle_height = 80, 110
        elif "tree_trunk" in obstacle_image:
            obstacle_width, obstacle_height = 10, 10

        obstacle_speed = OBSTACLE_SPEED_INITIAL + points * OBSTACLE_SPEED_INCREMENT
        obstacles.append(Obstacle(obstacle_x, obstacle_y, obstacle_image, obstacle_speed, obstacle_width, obstacle_height))
        obstacle_timer = OBSTACLE_INTERVAL

    obstacles_to_remove = [obstacle for obstacle in obstacles if obstacle.y > height]
    for obstacle in obstacles_to_remove:
        obstacles.remove(obstacle)

    for obstacle in obstacles:
        obstacle.move()

    for obstacle in obstacles:
        if (
            skieur.x < obstacle.x + obstacle.rect.width
            and skieur.x + skieur.rect.width > obstacle.x
            and skieur.y < obstacle.y + obstacle.rect.height
            and skieur.y + skieur.rect.height > obstacle.y
        ):
            print("Collision! Game Over.")

            if points > best_score:
                best_score = round(points)
                with open("data/meilleur_score.txt", "w") as file:
                    file.write(str(best_score))

            skieur.alive = False
            game_running = False

    if skieur.speed < 10:
        skieur.speed += 0.001

    points += skieur.speed * points_per_pixel

    if skieur.x > width - SCROLL_LIMIT:
        skieur.x = width - SCROLL_LIMIT

        for obstacle in obstacles:
            obstacle.x -= int(skieur.speed)

    elif skieur.x < SCROLL_LIMIT:
        skieur.x = SCROLL_LIMIT

        for obstacle in obstacles:
            obstacle.x += int(skieur.speed)

    window.fill([255, 255, 255])
    window.blit(background.image, background.rect)

    skieur.display(window)

    for obstacle in obstacles:
        obstacle.display(window)

    text_points = font.render(f"{int(points)}", True, blue)
    rect_points = text_points.get_rect(topright=(width - 10, 10))
    window.blit(text_points, rect_points)

    text_best_score = font.render(f"{int(best_score)}", True, (255, 0, 0))
    rect_best_score = text_best_score.get_rect(topright=(width - 10, 70))
    window.blit(text_best_score, rect_best_score)

    pygame.display.flip()

    pygame.time.Clock().tick(90)