import pygame
import random
import sys

# --- Config ---
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 1280
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
SKY_BLUE = (135, 206, 235)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Helicopter Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 50, bold=True)

class Helicopter:
    def __init__(self):
        self.rect = pygame.Rect(100, SCREEN_HEIGHT // 2, 60, 50)
        self.velocity = 0
        self.gravity = 0.5
        self.lift = -10  # Jump strength
        
    def move(self):
        self.velocity += self.gravity
        self.rect.y += int(self.velocity)
        
    def jump(self):
        self.velocity = self.lift
        
    def draw(self):
        # Draw body
        pygame.draw.rect(screen, RED, self.rect, border_radius=10)
        # Draw rotor
        pygame.draw.rect(screen, BLACK, (self.rect.x + 10, self.rect.y - 10, 40, 10))

class Obstacle:
    def __init__(self, x):
        self.x = x
        self.gap_size = 300  # Space between pipes
        self.width = 100
        self.top_height = random.randint(100, SCREEN_HEIGHT - self.gap_size - 100)
        self.speed = 5
        self.passed = False
        
    def move(self):
        self.x -= self.speed
        
    def draw(self):
        # Top Pipe
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.top_height))
        # Bottom Pipe
        pygame.draw.rect(screen, GREEN, (self.x, self.top_height + self.gap_size, self.width, SCREEN_HEIGHT))
        
    def check_collision(self, heli_rect):
        top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        bottom_rect = pygame.Rect(self.x, self.top_height + self.gap_size, self.width, SCREEN_HEIGHT)
        return top_rect.colliderect(heli_rect) or bottom_rect.colliderect(heli_rect)

# Game Variables
helicopter = Helicopter()
obstacles = [Obstacle(SCREEN_WIDTH + 200)]
score = 0
game_active = True

# --- Main Loop ---
while True:
    screen.fill(SKY_BLUE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Touch or Click to fly
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_active:
                helicopter.jump()
            else:
                # Restart Game
                helicopter = Helicopter()
                obstacles = [Obstacle(SCREEN_WIDTH + 200)]
                score = 0
                game_active = True

    if game_active:
        # Helicopter Update
        helicopter.move()
        helicopter.draw()
        
        # Check bounds (ceiling/floor)
        if helicopter.rect.top < 0 or helicopter.rect.bottom > SCREEN_HEIGHT:
            game_active = False

        # Obstacle Management
        if obstacles[-1].x < SCREEN_WIDTH - 400:
            obstacles.append(Obstacle(SCREEN_WIDTH + 50))
            
        for obs in obstacles:
            obs.move()
            obs.draw()
            
            # Collision
            if obs.check_collision(helicopter.rect):
                game_active = False
                
            # Score
            if not obs.passed and obs.x + obs.width < helicopter.rect.x:
                score += 1
                obs.passed = True
        
        # Remove old obstacles
        if obstacles[0].x < -150:
            obstacles.pop(0)
            
        # Draw Score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (50, 50))
        
    else:
        # Game Over Screen
        over_text = font.render("GAME OVER", True, BLACK)
        restart_text = font.render("Tap to Restart", True, WHITE)
        screen.blit(over_text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 50))
        screen.blit(restart_text, (SCREEN_WIDTH//2 - 160, SCREEN_HEIGHT//2 + 50))

    pygame.display.update()
    clock.tick(FPS)
