import pygame
import random
import math
from pygame import mixer

pygame.init()

# Create screen of height 600 and width 800
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invader Game")
icon = pygame.image.load('mask.png')
pygame.display.set_icon(icon)
snake_img=pygame.image.load('snake.png')
#Load music
mixer.music.load('olo.mp3')
mixer.music.play(-1)

# Load bullet image
bullet_img = pygame.image.load('minus.png')
bullet_img1= pygame.image.load('minus (1).png')

# Create clock for consistent frame rate
clock = pygame.time.Clock()

# Player
player_img = pygame.image.load('spaceship.png')
player_x = 370
player_y = 480
player_x_change = 0

def player(x, y):
    screen.blit(player_img, (x, y))

# Enemy
enemy_img = pygame.image.load('enemy.png')
enemies = []

def create_enemy():
    enemy_x = random.randint(0, 768)
    enemy_y = random.randint(50, 150) 
    enemies.append({"x": enemy_x, "y": enemy_y, "health": 2})  

def draw_enemy(x, y):
    screen.blit(enemy_img, (x, y))

def remove_offscreen_enemies():
    for enemy in enemies:
        if enemy["y"] >= 600:
            enemies.remove(enemy)
            create_enemy()

# Initial enemies
enemies_number=7
for i in range(enemies_number):
    create_enemy()
def player_enemy_bullet_collision(px, py, bx, by):
    distance = math.sqrt((px - bx) ** 2 + (py - by) ** 2)
    if distance < 27:  # Adjust the collision radius as needed
        return True
    else:
        return False

# Bullets
bullets = []
bullet_y_change=3
bullet_timer = 0  # Timer for bullet firing
bullet_interval = 500  # in milliseconds

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = "ready"

    def fire(self):
        self.state = "fire"

    def move(self):
        if self.state == "fire":
            self.y -= bullet_y_change
            if self.y <= 0:
                self.state = "ready"
    

def fire_bullet(x, y):
    # Create bullets with different initial positions
    new_bullet_left = Bullet(x - 16, y) 
    new_bullet_right = Bullet(x + 40, y)  
    new_bullet_center = Bullet(x+12.5, y)  

    # Fire all bullets
    new_bullet_left.fire()
    new_bullet_right.fire()
    new_bullet_center.fire()

    
    bullets.append(new_bullet_left)
    bullets.append(new_bullet_right)
    bullets.append(new_bullet_center)


# Collision
def collision(ex, ey, bx, by):
    distance = math.sqrt(math.pow(ex - bx, 2) + math.pow(ey - by, 2))
    if distance < 31:
        return True
    else:
        return False
#enemy bullets
class EnemyBullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = "ready"

    def fire(self):
        self.state = "fire"

    def move(self):
        if self.state == "fire":
            self.y += bullet_y_change 
            if self.y >= 600:
                self.state = "ready"
enemy_bullets = []
enemy_bullet_timer = 0
enemy_bullet_interval = 5000 #in milliseconds
# Function to create enemy bullets
def create_enemy_bullet(x, y):
    new_enemy_bullet = EnemyBullet(x, y)
    new_enemy_bullet.fire()
    enemy_bullets.append(new_enemy_bullet)
game_over = False

# Function to draw enemy bullets
def draw_enemy_bullet(x, y):
    screen.blit(bullet_img, (x + 8, y + 5))

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# Game Over Text
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over_text():
    over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
class Boss:
    def __init__(self, x, y, health):
        self.x = x
        self.y = y
        self.health = health
        self.direction = 1  # Initial direction of movement

    def move(self):
        self.x += self.direction * 2  # Move boss horizontally
        # Oscillate on a fixed y-coordinate
        self.y = 100 + 50 * math.sin(self.x / 20)  
        if self.x <= 0 or self.x >= 700:
            self.direction *= -1  

    def is_hit(self, bullet):
        # Check if the boss is hit by a bullet
        distance = math.sqrt((bullet.x - self.x) ** 2 + (bullet.y - self.y) ** 2)
        return distance < 32  # Adjust hitbox radius as needed
    def draw(self, screen):
        # Draw boss on the screen
        boss_img = pygame.image.load('boss_ship.png')
        screen.blit(boss_img, (self.x, self.y))


# Define boss enemy variables
boss_health = 10
boss = Boss(400, 100, boss_health)
boss_spawn_score = 2
boss_spawned = False
# Game loop
running = True
left_pressed = False
right_pressed = False

while running:

    screen.fill((0, 0, 0))

       # screen.blit(background, (0, 0))
    if not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    left_pressed = True
                if event.key == pygame.K_RIGHT:
                    right_pressed = True

            # Stop moving the player when arrow key is released
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left_pressed = False
                if event.key == pygame.K_RIGHT:
                    right_pressed = False

        # Player movement
        if left_pressed:
            player_x_change = -5
        elif right_pressed:
            player_x_change = 5
        else:
            player_x_change = 0

        player_x += player_x_change
        if player_x <= 0:
            player_x = 0
        elif player_x >= 736:
            player_x = 736

        # Enemy movement
        for enemy in enemies:
            enemy["y"] += 0.3  
        # Enemy shooting mechanism
        if pygame.time.get_ticks() - enemy_bullet_timer >= enemy_bullet_interval:
            enemy_bullet_timer = pygame.time.get_ticks()
            for enemy in enemies:
                create_enemy_bullet(enemy["x"], enemy["y"])
                # Enemy bullet movement
        for enemy_bullet in enemy_bullets:
            enemy_bullet.move()
        # Check for player-enemy bullet collision
        for enemy_bullet in enemy_bullets:
            if player_enemy_bullet_collision(player_x, player_y, enemy_bullet.x, enemy_bullet.y):
                game_over = True
                
        

        # Draw enemy bullets
        for enemy_bullet in enemy_bullets:
            if enemy_bullet.state == "fire":
                draw_enemy_bullet(enemy_bullet.x, enemy_bullet.y)


        # Bullet movement
        for bullet in bullets:
            bullet.move()

        # Bullet firing mechanism
        if pygame.time.get_ticks() - bullet_timer >= bullet_interval:
            bullet_timer = pygame.time.get_ticks()
            fire_bullet(player_x, player_y)
            # bullet_sound = mixer.Sound('ulu.mp3')
            # bullet_sound.play()

        # Collision
        for enemy in enemies[:]:
            for bullet in bullets:
                if collision(enemy["x"], enemy["y"], bullet.x, bullet.y):
                    bullets.remove(bullet) # Remove bullet upon collision
                    enemy["health"] -= 1
                    if enemy["health"] <= 0:
                        enemies.remove(enemy)
                        create_enemy()  
                        score_value += 1
                        if score_value % 10 ==0:
                            create_enemy()
        # Boss spawning
        if score_value >= boss_spawn_score and score_value % boss_spawn_score == 0 and not boss_spawned:
            boss = Boss(400, 100, 10)
            boss_spawned = True
        # Boss movement
        if boss and boss_spawned:
            boss.move()
            boss.draw(screen)
        
        # Check for collision between boss and bullets
        for bullet in bullets:
            if boss and boss.is_hit(bullet):
                bullets.remove(bullet)  # Remove bullet upon collision with boss
                boss.health -= 1
                if boss.health <= 0:
                    boss = None 
                    boss_spawned=False 
                    score_value += 10 
                    bullet_img=bullet_img1 
        
    
        # Draw objects
        
        player(player_x, player_y)
        for enemy in enemies:
            draw_enemy(enemy["x"], enemy["y"])
        for bullet in bullets:
            if bullet.state == "fire":
                screen.blit(bullet_img, (bullet.x + 8, bullet.y + 5))
        show_score(10, 10)


        # Game Over
        for enemy in enemies:
            if enemy["y"] > 440:
                
                game_over=True
                

        remove_offscreen_enemies()
    else:
        game_over_text()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(snake_img,(320,100))
    pygame.display.update()
    clock.tick(60)  # Ensure 60 frames per second
    
        

pygame.quit()
#-----------------------------------------------------------------------------------------------------------#
