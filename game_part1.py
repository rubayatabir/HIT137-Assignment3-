import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animal Hero vs Human Enemies")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Frame rate
FPS = 60
clock = pygame.time.Clock()

# Load images
animal_img = pygame.image.load("animal_hero.png")
enemy_img = pygame.image.load("human_enemy.png")
collectible_img = pygame.image.load("collectible.png")
boss_img = pygame.image.load("final_boss.png")  # Final boss image

# Define Player (Animal Hero)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(animal_img, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.speed = 5
        self.health = 100
        self.is_jumping = False
        self.jump_speed = 10
        self.gravity = 0.5
        self.vertical_speed = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        
        # Jumping logic
        if not self.is_jumping:
            if keys[pygame.K_UP]:
                self.is_jumping = True
                self.vertical_speed = self.jump_speed
        else:
            self.rect.y -= self.vertical_speed
            self.vertical_speed -= self.gravity
            if self.rect.bottom >= HEIGHT - 50:  # Ground level
                self.rect.bottom = HEIGHT - 50
                self.is_jumping = False

    def shoot(self):
        projectile = Projectile(self.rect.centerx, self.rect.top)
        all_sprites.add(projectile)
        projectiles.add(projectile)

# Define Projectile (shot by player)
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -7

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Define Enemy (Human Enemy)
class Enemy(pygame.sprite.Sprite):
    def __init__(self, shoot=False):
        super().__init__()
        self.image = pygame.transform.scale(enemy_img, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(1, 3)
        self.health = 50
        self.can_shoot = shoot

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed = random.randint(1, 3)

# Define Final Boss
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(boss_img, (100, 100))  # Boss image loaded here
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.y = 20
        self.health = 200
        self.speed = 3

    def update(self):
        # Move boss back and forth
        self.rect.x += self.speed
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed *= -1

    def shoot(self):
        # Shoot projectiles downward
        if random.randint(0, 30) == 1:
            projectile = BossProjectile(self.rect.centerx, self.rect.bottom)
            all_sprites.add(projectile)
            boss_projectiles.add(projectile)

    def throw_grenade(self):
        # Throw a grenade downward
        if random.randint(0, 60) == 1:
            grenade = Grenade(self.rect.centerx, self.rect.bottom)
            all_sprites.add(grenade)
            boss_grenades.add(grenade)