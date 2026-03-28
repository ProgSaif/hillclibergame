import os
os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
import random
import math
import time

pygame.init()

WIDTH, HEIGHT = 1000, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hill Climb Racing")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 22)

WHITE=(255,255,255)
BLACK=(0,0,0)
GREEN=(0,200,0)
RED=(200,0,0)
BLUE=(50,120,255)
YELLOW=(255,220,0)

GRAVITY = 0.5

class Car:
    def __init__(self):
        self.x = 200
        self.y = 300
        self.vel_y = 0
        self.speed = 0
        self.fuel = 100
        self.alive = True

    def update(self, terrain_height):
        keys = pygame.key.get_pressed()

        # auto acceleration (because web can't detect keyboard)
        if self.fuel > 0:
            self.speed += 0.05
            self.fuel -= 0.03
        else:
            self.speed *= 0.98

        self.vel_y += GRAVITY
        self.y += self.vel_y

        ground_y = terrain_height(self.x)

        if self.y > ground_y - 40:
            self.y = ground_y - 40
            self.vel_y = 0

        if self.speed > 8:
            self.speed = 8

        self.x += self.speed

        if self.y > HEIGHT:
            self.alive = False

    def draw(self, scroll):
        pygame.draw.rect(screen, RED, (200, self.y-20, 60, 30))
        pygame.draw.circle(screen, BLACK, (220, self.y+10), 15)
        pygame.draw.circle(screen, BLACK, (250, self.y+10), 15)

car = Car()

def terrain_height(x):
    return int(300 + 80 * math.sin(x * 0.01))

coins = []
for i in range(80):
    coins.append([random.randint(400, 7000), random.randint(150, 300)])

fuel_cans = []
for i in range(20):
    fuel_cans.append([random.randint(600, 7000), random.randint(150, 300)])

score = 0
scroll = 0

while True:
    clock.tick(30)
    screen.fill(BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    if car.alive:
        car.update(terrain_height)
        scroll = car.x - 200

    # terrain
    for x in range(WIDTH):
        world_x = x + scroll
        y = terrain_height(world_x)
        pygame.draw.line(screen, GREEN, (x,y), (x,HEIGHT))

    # coins
    for coin in coins[:]:
        screen_x = coin[0] - scroll
        if -50 < screen_x < WIDTH+50:
            pygame.draw.circle(screen, YELLOW, (int(screen_x), coin[1]), 10)

        if abs(car.x - coin[0]) < 40 and abs(car.y - coin[1]) < 40:
            coins.remove(coin)
            score += 10

    # fuel
    for fuel in fuel_cans[:]:
        screen_x = fuel[0] - scroll
        if -50 < screen_x < WIDTH+50:
            pygame.draw.rect(screen, RED, (screen_x, fuel[1], 20, 25))

        if abs(car.x - fuel[0]) < 40 and abs(car.y - fuel[1]) < 40:
            fuel_cans.remove(fuel)
            car.fuel = min(100, car.fuel + 30)

    car.draw(scroll)

    fuel_text = font.render(f"Fuel: {int(car.fuel)}", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(fuel_text, (20,20))
    screen.blit(score_text, (20,50))

    if not car.alive:
        over = font.render("GAME OVER", True, WHITE)
        screen.blit(over, (450,250))

    pygame.display.update()
    pygame.image.save(screen, "frame.png")

    time.sleep(0.03)
