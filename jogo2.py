import pygame
import sys
import random

pygame.init()

# Tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo Plataforma 2D")

# Cores
BLACK = (20, 20, 25)
GROUND_COLOR = (45, 45, 50)
RED = (200, 60, 60)

clock = pygame.time.Clock()
FPS = 60

# ---------------- PLAYER ----------------
class Player(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y):
        super().__init__()

        try:
            imagem_original = pygame.image.load("hk_inspired_sprite.png").convert_alpha()
            self.image = pygame.transform.scale(imagem_original, (80, 80))
        except:
            self.image = pygame.Surface((40, 60))
            self.image.fill((100, 150, 255))

        self.rect = self.image.get_rect()
        self.rect.midbottom = (start_x, start_y)

        self.vel_x = 0
        self.vel_y = 0
        self.speed = 6
        self.jump_power = -12
        self.gravity = 0.6
        self.on_ground = False

    def update(self, platforms):
        self.vel_y += self.gravity

        self.rect.x += self.vel_x

        # Limite lateral
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        self.rect.y += self.vel_y

        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.vel_y = self.jump_power


# ---------------- PLATFORM ----------------
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(GROUND_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))


# ---------------- ENEMY ----------------
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect(
            midbottom=(random.randint(50, WIDTH-50), 500)
        )
        self.speed = random.choice([-3, 3])

    def update(self):
        self.rect.x += self.speed

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed *= -1


# ---------------- SETUP ----------------
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
enemies = pygame.sprite.Group()

player = Player(WIDTH // 2, 400)
all_sprites.add(player)

# Chão principal
ground = Platform(0, 500, WIDTH, 100)
platforms.add(ground)
all_sprites.add(ground)

# Plataformas extras
for i in range(3):
    p = Platform(random.randint(100, 600), random.randint(250, 450), 120, 20)
    platforms.add(p)
    all_sprites.add(p)

# Inimigos
for i in range(2):
    e = Enemy()
    enemies.add(e)
    all_sprites.add(e)

# ---------------- LOOP ----------------
running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_SPACE, pygame.K_UP, pygame.K_w]:
                player.jump()

    keys = pygame.key.get_pressed()
    player.vel_x = 0

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.vel_x = -player.speed

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.vel_x = player.speed

    # Atualizações
    if not game_over:
        player.update(platforms)
        enemies.update()

        # Colisão com inimigos
        if pygame.sprite.spritecollide(player, enemies, False):
            game_over = True

    # Desenho
    screen.fill(BLACK)
    all_sprites.draw(screen)

    if game_over:
        font = pygame.font.SysFont(None, 60)
        text = font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(text, (WIDTH//2 - 150, HEIGHT//2))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
