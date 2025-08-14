import pygame
import random
from ai_model import train_model

pygame.init()

# Game window setup
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Fruit Ninja Bot")
font = pygame.font.SysFont("Arial", 36)

# Load images
fruit_image = pygame.image.load("C:/Users/ASUS/Downloads/fruit-ninja-ai/fruit-ninja-ai/assets/fruit.png")
bomb_image = pygame.image.load("C:/Users/ASUS/Downloads/fruit-ninja-ai/fruit-ninja-ai/assets/bomb.png")


# Load AI model
model = train_model()

# Game variables
score = 0
lives = 3

# Falling object class
class FallingObject:
    def __init__(self):
        self.type = random.choice(["fruit", "bomb"])
        self.color = (255, 0, 0) if self.type == "fruit" else (0, 0, 0)
        self.size = random.randint(20, 40)
        self.speed = random.randint(3, 7)
        self.x = random.randint(50, WIDTH - 50)
        self.y = -self.size
        self.image = pygame.transform.scale(
            fruit_image if self.type == "fruit" else bomb_image,
            (self.size * 2, self.size * 2)
        )

    def move(self):
        self.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, (self.x - self.size, self.y - self.size))


def extract_features(obj):
    r, g, b = obj.color
    return [r, g, b, obj.size, obj.speed]


def show_start_screen():
    screen.fill((173, 216, 230))
    title = font.render("AI FRUIT NINJA BOT", True, (255, 0, 0))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
    pygame.display.flip()


def show_game_over():
    screen.fill((255, 255, 255))
    msg = font.render("GAME OVER!", True, (255, 0, 0))
    screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.delay(3000)
# Game initialization
running = True
clock = pygame.time.Clock()
objects = []
frame_count = 0

show_start_screen()
pygame.time.wait(2000)

while running:
    clock.tick(60)  # 60 FPS
    screen.fill((173, 216, 230))  # Light blue background

    # Spawn objects every 30 frames
    frame_count += 1
    if frame_count % 30 == 0:
        objects.append(FallingObject())

    # Handle events (for quitting)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move and draw all objects
    for obj in list(objects):  # Copy list to avoid iteration issues
        obj.move()
        obj.draw(screen)

        features = extract_features(obj)
        prediction = model.predict([features])[0]

        # Check if object reached bottom
        if obj.y > HEIGHT:
            if prediction == "fruit":
                lives -= 1
            objects.remove(obj)

        # AI slices only fruit
        elif prediction == "fruit":
            score += 1
            objects.remove(obj)

        # AI avoids bombs
        elif prediction == "bomb":
            continue

    # Display score and lives
    score_text = font.render(f"Score: {score}  Lives: {lives}", True, (0, 0, 0))
    screen.blit(score_text, (20, 20))

    # End game if lives are 0
    if lives <= 0:
        show_game_over()
        running = False

    pygame.display.flip()

pygame.quit()
