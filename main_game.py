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

# Define Boss Projectile
class BossProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 7

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

# Define Grenade
class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 255, 0))  # Yellow grenade
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

# Define Collectible
class Collectible(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(collectible_img, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = 2

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)

# Scoring system and health bar
def draw_text(surface, text, size, x, y, color=WHITE):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def draw_health_bar(surface, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)

def game_over_screen():
    screen.fill(BLACK)
    draw_text(screen, "GAME OVER", 64, WIDTH // 2, HEIGHT // 4, RED)
    draw_text(screen, "Press R to Restart or Q to Quit", 32, WIDTH // 2, HEIGHT // 2, WHITE)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False  # Restart the game
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()

def reset_game():
    global player, all_sprites, enemies, collectibles, projectiles, boss_projectiles, boss_grenades, score, level, boss_fight, boss
    player = Player()
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    collectibles = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    boss_projectiles = pygame.sprite.Group()
    boss_grenades = pygame.sprite.Group()

    all_sprites.add(player)

    # Add enemies and collectibles
    for _ in range(8):
        enemy = Enemy(shoot=True)
        all_sprites.add(enemy)
        enemies.add(enemy)

    for _ in range(3):
        collectible = Collectible()
        all_sprites.add(collectible)
        collectibles.add(collectible)

    score = 0
    level = 1
    boss_fight = False
    boss = None

# Create game entities and reset the game for the first time
reset_game()

# Game loop
running = True

while running:
    clock.tick(FPS)

    # Process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update entities
    all_sprites.update()

    # Check if boss fight should start
    if score >= 100 and not boss_fight:
        boss_fight = True
        boss = Boss()
        all_sprites.add(boss)

    if boss_fight and boss:
        boss.shoot()
        boss.throw_grenade()

    # Check for projectiles hitting enemies
    hits = pygame.sprite.groupcollide(projectiles, enemies, True, True)
    for hit in hits:
        score += 10
        enemy = Enemy(shoot=True)
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Check for player collecting items
    collect_hits = pygame.sprite.spritecollide(player, collectibles, True)
    for collectible in collect_hits:
        score += 5

    # Check for enemies hitting the player
    enemy_hits = pygame.sprite.spritecollide(player, enemies, False)
    for hit in enemy_hits:
        player.health -= 10
        if player.health <= 0:
            game_over_screen()
            reset_game()

    # Check for boss projectiles and grenades hitting the player
    if boss_fight:
        projectile_hits = pygame.sprite.spritecollide(player, boss_projectiles, True)
        grenade_hits = pygame.sprite.spritecollide(player, boss_grenades, True)
        for hit in projectile_hits + grenade_hits:
            player.health -= 20
            if player.health <= 0:
                game_over_screen()
                reset_game()

    # Draw everything
    screen.fill(BLACK)
    all_sprites.draw(screen)
    draw_text(screen, f'Score: {score}', 20, WIDTH // 2, 10)
    draw_health_bar(screen, 10, 10, player.health)

    if boss_fight and boss:
        draw_health_bar(screen, WIDTH // 2 - 50, 40, boss.health)

    pygame.display.flip()

pygame.quit()
