import pygame
import random
import time

# Initialize pygame
pygame.init()

# Define colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Screen dimensions
game_width = 600
game_height = 400
header_height = 40  # Height of the black bar for score, lives, and level
total_height = game_height + header_height

# Create the display window with additional height for the black bar
dis = pygame.display.set_mode((game_width, total_height))
pygame.display.set_caption('Snake Game - Enhanced with Snake Images')

# Set game clock and speed
clock = pygame.time.Clock()

# Snake block size (still 10x10 for collision)
snake_block = 10

# Initial speed
initial_speed = 15
snake_speed = initial_speed

# Load images for snake (head, body, tail), apple (food), bomb (obstacle), grassy field, and skull for restart screen
snake_head_img = pygame.image.load('snake_head.png')
snake_body_img = pygame.image.load('snake_body.png')
snake_tail_img = pygame.image.load('snake_tail.png')
apple_image = pygame.image.load('apple.png')
bomb_image = pygame.image.load('bomb.png')
field_image = pygame.image.load('grassy_field.png')  # Grassy field background image
skull_image = pygame.image.load('skull.png')  # Skull image for restart screen

# Scale food image to 20x20 pixels (visual size only)
apple_image = pygame.transform.scale(apple_image, (20, 20))
# Scale bomb image to 30x30 pixels (visual size only)
bomb_image = pygame.transform.scale(bomb_image, (30, 30))
# Scale skull image to fit the restart screen
skull_image = pygame.transform.scale(skull_image, (50, 50))
# Scale field image to cover the game area
field_image = pygame.transform.scale(field_image, (game_width, game_height))
# Scale snake head, body, and tail images to fit the grid size (10x10 pixels)
snake_head_img = pygame.transform.scale(snake_head_img, (snake_block, snake_block))
snake_body_img = pygame.transform.scale(snake_body_img, (snake_block, snake_block))
snake_tail_img = pygame.transform.scale(snake_tail_img, (snake_block, snake_block))

# Define font (Roboto)
font_style = pygame.font.SysFont("roboto", 25)
score_font = pygame.font.SysFont("roboto", 30)

# Function to display score, lives, and level in the black bar, centered horizontally
def our_score(score, lives, level, total_score):
    # Fill the header area with black color
    pygame.draw.rect(dis, black, [0, 0, game_width, header_height])

    # Render the score, lives, and level, center horizontally
    text = f"Score: {score} | Total: {total_score} | Lives: {lives} | Level: {level}"
    text_surface = score_font.render(text, True, yellow)
    text_rect = text_surface.get_rect(center=(game_width // 2, header_height // 2))
    dis.blit(text_surface, text_rect)

# Updated function to draw the snake with head, body, and tail images
def our_snake(snake_block, snake_list):
    # Draw head (rotate based on movement direction)
    if len(snake_list) == 1:
        # Only draw the head if the snake has one segment
        head = snake_list[0]
        dis.blit(snake_head_img, (head[0], head[1] + header_height))
        return

    head = snake_list[-1]  # Last element is the head
    prev_head = snake_list[-2]  # Previous head position to calculate direction
    if head[0] > prev_head[0]:  # Moving right
        rotated_head = pygame.transform.rotate(snake_head_img, 270)
    elif head[0] < prev_head[0]:  # Moving left
        rotated_head = pygame.transform.rotate(snake_head_img, 90)
    elif head[1] > prev_head[1]:  # Moving down
        rotated_head = pygame.transform.rotate(snake_head_img, 180)  
    else:  # Moving up
        rotated_head = snake_head_img

    dis.blit(rotated_head, (head[0], head[1] + header_height))

    # If the snake has more than two segments, draw the body and tail
    if len(snake_list) > 2:
        # Draw the body
        for segment in snake_list[1:-1]:
            dis.blit(snake_body_img, (segment[0], segment[1] + header_height))

        # Draw the tail
        tail = snake_list[0]  # First element is the tail
        next_tail = snake_list[1]  # Next element after tail to calculate direction
        if tail[0] > next_tail[0]:  # Moving right
            rotated_tail = pygame.transform.rotate(snake_tail_img, 90)
        elif tail[0] < next_tail[0]:  # Moving left
            rotated_tail = pygame.transform.rotate(snake_tail_img, 270)
        elif tail[1] > next_tail[1]:  # Moving down
            rotated_tail = snake_tail_img  # No rotation needed
        else:  # Moving up
            rotated_tail = pygame.transform.rotate(snake_tail_img, 180)

        dis.blit(rotated_tail, (tail[0], tail[1] + header_height))

# Message display function, centered horizontally and lower on the screen for restart screen
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    mesg_rect = mesg.get_rect(center=(game_width // 2, total_height // 2 + 40))
    dis.blit(mesg, mesg_rect)

# Function to display the final score after losing
def display_final_score(total_score):
    final_score = score_font.render("Total Score: " + str(total_score), True, yellow)
    final_score_rect = final_score.get_rect(center=(game_width // 2, total_height // 2))
    dis.blit(final_score, final_score_rect)

# Updated function to create obstacles at least 1 grid space away from the player
def create_obstacles(num_obstacles, snake_list, player_position):
    obstacles = []
    safe_distance = 10  # Safe distance of 1 grid space (10x10 pixels)

    for _ in range(num_obstacles):
        while True:
            # Generate random obstacle position
            obs_x = round(random.randrange(0, game_width - snake_block) / 10.0) * 10.0
            obs_y = round(random.randrange(0, game_height - snake_block) / 10.0) * 10.0
            
            # Check if the obstacle is at least one space away from the player's position
            if abs(obs_x - player_position[0]) >= safe_distance or abs(obs_y - player_position[1]) >= safe_distance:
                # Ensure obstacle doesn't overlap with the snake
                if [obs_x, obs_y] not in snake_list:
                    obstacles.append([obs_x, obs_y])
                    break

    return obstacles

# Function to draw obstacles (bombs)
def draw_obstacles(obstacles):
    for obstacle in obstacles:
        # Draw bomb image at the obstacle position, centering the 30x30 image in the 10x10 grid
        dis.blit(bomb_image, (obstacle[0] - 10, obstacle[1] + header_height - 10))

# Main game loop
def gameLoop():
    lives = 3
    level = 1
    total_score = 0  # Track total score over all lives
    global snake_speed
    game_over = False
    current_direction = 'UP' # initial direction of the snake

    while True:
        # Initial game state
        game_close = False
        snake_speed = initial_speed
        x1 = game_width / 2
        y1 = game_height / 2
        x1_change = 0
        y1_change = 0
        snake_list = []
        length_of_snake = 1
        score_in_current_life = 0  # Reset score for the current life

        foodx = round(random.randrange(0, game_width - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, game_height - snake_block) / 10.0) * 10.0

        # Create obstacles with the updated function, ensuring obstacles spawn away from the player
        obstacles = create_obstacles(level + 1, snake_list, [x1, y1])

        while not game_over and not game_close:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and current_direction != 'RIGHT':
                        x1_change = -snake_block
                        y1_change = 0
                        current_direction = 'LEFT'

                    elif event.key == pygame.K_RIGHT and current_direction != 'LEFT':
                        x1_change = snake_block
                        y1_change = 0
                        current_direction = 'RIGHT'

                    elif event.key == pygame.K_UP and current_direction != 'DOWN':
                        y1_change = -snake_block
                        x1_change = 0
                        current_direction = 'UP'
                        
                    elif event.key == pygame.K_DOWN and current_direction != 'UP':
                        y1_change = snake_block
                        x1_change = 0
                        current_direction = 'DOWN'

            x1 = (x1 + x1_change) % game_width
            y1 = (y1 + y1_change) % game_height

            # Draw grassy field background
            dis.blit(field_image, (0, header_height))

            # Draw food and obstacles
            # Draw apple image at food position, centering the 20x20 image in the 10x10 grid
            dis.blit(apple_image, (foodx - 5, foody + header_height - 5))
            draw_obstacles(obstacles)

            snake_head = [x1, y1]
            snake_list.append(snake_head)

            if len(snake_list) > length_of_snake:
                del snake_list[0]

            # Check if the snake hits itself
            for x in snake_list[:-1]:
                if x == snake_head:
                    game_close = True

            # Check if the snake hits any obstacles
            for obstacle in obstacles:
                if snake_head == obstacle:
                    game_close = True

            # Draw the snake and display the score
            our_snake(snake_block, snake_list)
            our_score(score_in_current_life, lives, level, total_score)
            pygame.display.update()

            # Check if the snake eats the food
            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, game_width - snake_block) / 10.0) * 10.0
                foody = round(random.randrange(0, game_height - snake_block) / 10.0) * 10.0
                length_of_snake += 1
                snake_speed += 0.5
                score_in_current_life += 1

                if length_of_snake % 5 == 0:
                    level += 1
                    # Create new obstacles for the next level
                    obstacles = create_obstacles(level + 1, snake_list, [x1, y1])

            clock.tick(snake_speed)

            if game_close:
                total_score += score_in_current_life  # Add current life score to total score
                lives -= 1
                if lives <= 0:
                    game_over = True

        # Game over logic when the player loses all lives
        if game_over:
            dis.fill(black)  # Black background for the restart screen

            # Display skull image and final score
            skull_rect = skull_image.get_rect(center=(game_width // 2, total_height // 2 - 50))
            dis.blit(skull_image, skull_rect)

            display_final_score(total_score)  # Display the total score over all lives

            # Show the "Game Over" message
            message("Game Over! Press R to Restart or Q to Quit", red)

            pygame.display.update()

            # Handle restart or quit after game over
            while game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            pygame.quit()
                            quit()
                        if event.key == pygame.K_r:
                            # Reset the game state and restart
                            lives = 3
                            level = 1
                            total_score = 0  # Reset total score
                            game_over = False
                            break

# Start the game
gameLoop()
