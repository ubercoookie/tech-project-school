# refactored to implement shooting in the Player instead of running loop

import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((1300, 800))
clock = pygame.time.Clock()
score = 0
font = pygame.font.SysFont(None, 36)  # You can choose font size here

# --- Sprite Classes ---
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("player ship.png")
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 7
        self.shoot_delay = 30
        self.delay = self.shoot_delay
        self.maxmag = 30
        self.magazine = self.maxmag
        

    def update(self, keys):
        if self.delay < self.shoot_delay:
            self.delay += 1
        if keys[pygame.K_a]: self.rect.x -= self.speed
        if keys[pygame.K_d]: self.rect.x += self.speed
        if keys[pygame.K_w]: self.rect.y -= self.speed
        if keys[pygame.K_s]: self.rect.y += self.speed
        if keys[pygame.K_9]:
            self.maxmag += 5
        if keys[pygame.K_r]: self.magazine = self.maxmag
        if keys[pygame.K_SPACE]: 
            if self.delay == self.shoot_delay and self.magazine > 0:
                self.shoot()
                self.delay = 0
                self.magazine -= 1
            
    
    def shoot(self):
        #print("Shooting", self.num)
        #self.num+=1
        #b1 = Bullet(self.rect.centerx, self.rect.centery, 0, -1)
        #b2 = Bullet(self.rect.centerx, self.rect.centery, 1, 0)
        b3 = Bullet(self.rect.centerx, self.rect.centery, -1, 0)
        #b4 = Bullet(self.rect.centerx, self.rect.centery, 0, 1)
        all_sprites.add( b3)
        bullets.add(b3)
        

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.change_direction()  # Set initial direction
        self.change_delay = 60  # Frames until next change (~1 second at 60 FPS)
        self.timer = 0          # Counter

    def change_direction(self):
        # Set a new random direction
        self.dx = random.choice([-3, -2, -1, 1, 2, 3])
        self.dy = random.choice([-3, -2, -1, 1, 2, 3])

    def update(self):
        # Move enemy
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Bounce off edges
        if self.rect.left <= 0 or self.rect.right >= 800:
            self.dx *= -1
        if self.rect.top <= 0 or self.rect.bottom >= 600:
            self.dy *= -1

        # Increment timer and maybe change direction
        self.timer += 1
        if self.timer >= self.change_delay:
            self.change_direction()
            self.timer = 0


class Enemy2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("enemy ship.png")  # transparent bg
        self.rect = self.image.get_rect(topleft=(x, y))
        self.dx = 3     

    def update(self):
        # Move enemy
        self.rect.x += self.dx

        if self.rect.left > 1300:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((0, 255, 0))  # Green bullet
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10  # Moves up
        self.dx = dx * self.speed
        self.dy = dy * self.speed


    def update(self):
        #self.rect.y += self.speed
        self.rect.y += self.dy
        self.rect.x += self.dx
        
        # Kill bullet if it leaves the screen
        if self.rect.bottom < 0:
            self.kill()


# --- Create Sprites ---
player =  Player(1200,400)
# addingenemies one by one
enemy = Enemy(400, 300)
enemy2 = Enemy(500, 400)
enemy3 = Enemy(300, 450)
enemies = pygame.sprite.Group(enemy, enemy2, enemy3)  # Group with enemies only
enemies.add(enemy, enemy2, enemy3)

#spawning enemies
spawn_timer = 0
spawn_delay = 1000 

enemies = pygame.sprite.Group()
# Spawn 10 enemies at random positions
if spawn_timer >= spawn_delay:
    x = random.randint(0, 1000)
    y = random.randint(0, 750)
    enemy = Enemy(x, y)
    enemies.add(enemy)



playerGroup = pygame.sprite.Group(player) # for killing player using hits = ...)
all_sprites = pygame.sprite.Group(player, enemies)
bullets = pygame.sprite.Group()
# all_sprites.add(Bullet)
# bullets.add(Bullet)


# --- Game loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player.magazine > 0:
                b3 = Bullet(player.rect.centerx, player.rect.centery, -1, 0)
                all_sprites.add (b3)
                bullets.add( b3)
        

        if event.type == pygame.QUIT:
            running = False

    # random spawning enemies2 on left
    dt = clock.tick(60)
    spawn_timer += dt 
    if spawn_timer >= spawn_delay:
        y = random.randint(0, 750)
        enemyC = Enemy2(0, y)   # Spawn at left edge
        enemies.add(enemyC)
        all_sprites.add(enemyC)
        spawn_timer = 0


    keys = pygame.key.get_pressed()
    #all_sprites.update(keys)
    player.update(keys)
    enemies.update()
    bullets.update()


    # --- Collision detection ---
    # collision bullet and enemy
    # pygame.sprite.groupcollide(bullets, enemies, True, True) 
    hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
    score += len(hits)
        #print("Score: ", score)
    #if pygame.sprite.groupcollide(playerGroup, enemies, True, True)

    if pygame.sprite.spritecollide(player, enemies, True):
        print("Collision detected!")

    # pygame.sprite.groupcollide(enemies, playerGroup, False, True)        # this line uses sprite group to kill enemy
    if score > 0 and score % 50 == 0:
     print('hsgbjf')

    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))  # Black color
    screen.blit(score_text, (10, 10))  # Position at top-left corner
    magazine_text = font.render(f"mag: {player.magazine}", True, (0, 0, 0))  # Black color
    screen.blit(magazine_text, (10, 50))  # Position at top-left corner
    pygame.display.flip()
    #clock.tick(60)

pygame.quit()
sys.exit()