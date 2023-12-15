import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Most Difficult Game")

# Colors
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)

# Player attributes
player_width, player_height = 50, 50
player_x, player_y = screen_width // 2, screen_height - player_height - 30
player_velocity = 7
player_jump = False
player_jump_velocity = -10
player_gravity = 0.5

# Enemy attributes
enemy_width, enemy_height = 30, 30
enemy_x, enemy_y = screen_width, screen_height - enemy_height - 30
enemy_velocity = 5
enemy_spawn = True

# Platform attributes for different levels
platforms = [
    [0, screen_height - 20, screen_width, 20],
    [300, 400, 200, 20],
    [500, 250, 200, 20],
    [100, 100, 200, 20],
    [650, 50, 150, 20],  # Extra platform for level 2
    [200, 400, 200, 20],  # Additional platform for level 3
    [500, 150, 200, 20],  # Additional platform for level 3
    [0, 50, 150, 20]  # Additional platform for level 4
]

# Coins for different levels
coins = [
    [700, 400],
    [500, 200],
    [100, 50],
    [200, 350],
    [600, 100],
    [350, 200],
    [500, 300],
    [100, 200],
    [700, 100],
    [50, 10]
]
collected_coins = []

# Score
score = 0
font = pygame.font.Font(None, 36)

# Level and game states
level = 1
game_over = False
victory = False

# Sound effects
coin_sound = pygame.mixer.Sound('coin_sound.wav')  # Replace 'coin_sound.wav' with your sound file
game_over_sound = pygame.mixer.Sound('game_over_sound.wav')  # Replace 'game_over_sound.wav' with your sound file
victory_sound = pygame.mixer.Sound('victory_sound.wav')  # Replace 'victory_sound.wav' with your sound file

# Game loop
running = True
while running:
    screen.fill(white)  # Clear the screen

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game over and victory screens
    if game_over:
        game_over_sound.play()  # Play game over sound
        end_text = font.render("GAME OVER", True, red)
        screen.blit(end_text, (screen_width // 2 - 100, screen_height // 2))
        pygame.display.flip()
        continue  # Skip the rest of the loop if game is over
    elif victory:
        victory_sound.play()  # Play victory sound
        end_text = font.render("VICTORY!", True, green)
        screen.blit(end_text, (screen_width // 2 - 100, screen_height // 2))
        pygame.display.flip()
        continue  # Skip the rest of the loop if victory

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_velocity
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_velocity

    # Player jumping
    if not player_jump:
        if keys[pygame.K_SPACE]:
            player_jump = True
    else:
        if player_jump_velocity < 0:
            player_y += player_jump_velocity
            player_jump_velocity += player_gravity
        else:
            player_jump = False
            player_jump_velocity = -10

    # Apply gravity
    if player_y < screen_height - player_height:
        player_y += player_gravity

    # Draw platforms for current level
    for platform in platforms[:level + 1]:
        pygame.draw.rect(screen, green, platform)

        # Collision detection with platforms
        if (player_y + player_height >= platform[1] and player_y + player_height <= platform[1] + platform[3]) \
                and (player_x + player_width >= platform[0] and player_x <= platform[0] + platform[2]):
            player_jump = False
            player_jump_velocity = -10
            if player_y < platform[1]:
                player_y = platform[1] - player_height

    # Draw coins for current level
    for coin in coins[:level * 3 + 1]:
        if coin not in collected_coins:
            pygame.draw.circle(screen, yellow, coin, 10)

            # Collision detection with coins
            if (player_x < coin[0] + 10 and player_x + player_width > coin[0] and
                    player_y < coin[1] + 10 and player_y + player_height > coin[1]):
                collected_coins.append(coin)
                score += 10
                coin_sound.play()  # Play the coin collection sound

    # Draw player
    pygame.draw.rect(screen, blue, (player_x, player_y, player_width, player_height))

    # Check victory or game over
    if not enemy_spawn and not collected_coins and level == 4:
        victory = True
    elif not enemy_spawn and not collected_coins:
        level += 1
        platforms.append([random.randint(0, screen_width - 200), random.randint(0, screen_height - 50), 200, 20])  # Random platform for next level
        coins.extend([[random.randint(0, screen_width - 20), random.randint(0, screen_height - 20)] for _ in range(level * 3)])  # Random coins for next level
        enemy_spawn = True
    elif enemy_spawn and level > 1:
        game_over = True

    # Display score and level
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    level_text = font.render(f"Level: {level}", True, (0, 0, 0))
    screen.blit(level_text, (screen_width - 120, 10))

    pygame.display.flip()

pygame.quit()
