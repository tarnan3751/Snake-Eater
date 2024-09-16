import pygame
import random
import time

# Initialize pygame
pygame.init()

# Define colors
white = (255, 255, 255)
dark_yellow = (204, 204, 0)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Screen dimensions
game_width = 600
game_height = 400
header_height = 40  # Height of the score/lives header
total_height = game_height + header_height  # Total height including the header

# Create the display window
dis = pygame.display.set_mode((game_width, total_height))
pygame.display.set_caption('Snake Eater')

# Set game clock and speed
clock = pygame.time.Clock()

# Snake block size (each segment is 10x10)
snake_block = 10
initial_speed = 15  # Initial speed of the snake
snake_speed = initial_speed  # Current speed of the snake

# Load images for snake parts, food, obstacles, etc.
snake_head_img = pygame.image.load('snake_head.png')
snake_body_img = pygame.image.load('snake_body.png')
snake_tail_img = pygame.image.load('snake_tail.png')
apple_image = pygame.image.load('apple.png')
bomb_image = pygame.image.load('bomb.png')
field_image = pygame.image.load('grassy_field.png')
skull_image = pygame.image.load('skull.png')
forest_background = pygame.image.load('forest_background.png')  # Main menu background image

# Scale images to fit the required sizes
apple_image = pygame.transform.scale(apple_image, (20, 20))  # Food image scaled to 20x20 pixels
bomb_image = pygame.transform.scale(bomb_image, (30, 30))  # Bomb image scaled to 30x30 pixels
skull_image = pygame.transform.scale(skull_image, (50, 50))  # Skull image for game over screen
field_image = pygame.transform.scale(field_image, (game_width, game_height))  # Game background
snake_head_img = pygame.transform.scale(snake_head_img, (snake_block, snake_block))  # Snake head fits in 10x10 grid
snake_body_img = pygame.transform.scale(snake_body_img, (snake_block, snake_block))  # Snake body
snake_tail_img = pygame.transform.scale(snake_tail_img, (snake_block, snake_block))  # Snake tail
forest_background = pygame.transform.scale(forest_background, (game_width, total_height))  # Main menu background

# Font settings
font_style = pygame.font.SysFont("roboto", 25)  # Font for messages
score_font = pygame.font.SysFont("roboto", 30)  # Font for displaying scores
title_font = pygame.font.SysFont("roboto", 50)  # Font for the game title in the main menu

# Function to display the score, lives, and level at the top of the screen
def our_score(score, lives, level, total_score):
    # Draw the black rectangle at the top of the screen
    pygame.draw.rect(dis, black, [0, 0, game_width, header_height])
    
    # Prepare the text with score, lives, and level
    text = f"Score: {score} | Total: {total_score} | Lives: {lives} | Level: {level}"
    text_surface = score_font.render(text, True, dark_yellow)  # Render text in dark yellow
    text_rect = text_surface.get_rect(center=(game_width // 2, header_height // 2))  # Center the text horizontally
    dis.blit(text_surface, text_rect)  # Display the text

# Function to draw the snake (with head, body, and tail)
def our_snake(snake_block, snake_list, current_direction):
    # Get the position of the head
    head = snake_list[-1]  # Last element in the list is the head
    
    # Rotate the head based on the current direction
    if current_direction == 'RIGHT':
        rotated_head = pygame.transform.rotate(snake_head_img, 270)
    elif current_direction == 'LEFT':
        rotated_head = pygame.transform.rotate(snake_head_img, 90)
    elif current_direction == 'DOWN':
        rotated_head = pygame.transform.rotate(snake_head_img, 180)
    else:  # Moving up
        rotated_head = snake_head_img

    # Draw the snake if it has only 2 segments (head and tail)
    if len(snake_list) == 2:
        tail = snake_list[0]  # First element is the tail
        next_tail = snake_list[1]  # Second element is the head
        
        # Rotate the tail based on its direction relative to the head
        if tail[0] > next_tail[0]:  # Moving right
            rotated_tail = pygame.transform.rotate(snake_tail_img, 90)
        elif tail[0] < next_tail[0]:  # Moving left
            rotated_tail = pygame.transform.rotate(snake_tail_img, 270)
        elif tail[1] > next_tail[1]:  # Moving down
            rotated_tail = snake_tail_img  # No rotation needed
        else:  # Moving up
            rotated_tail = pygame.transform.rotate(snake_tail_img, 180)

        # Draw the tail and head
        dis.blit(rotated_tail, (tail[0], tail[1] + header_height))
        dis.blit(rotated_head, (head[0], head[1] + header_height))
        return  # Stop here if the snake has only 2 segments

    # Draw the head
    dis.blit(rotated_head, (head[0], head[1] + header_height))

    # Draw the body segments (if there are more than 2 segments)
    if len(snake_list) > 2:
        for segment in snake_list[1:-1]:
            dis.blit(snake_body_img, (segment[0], segment[1] + header_height))

        # Draw the tail, rotated based on its direction
        tail = snake_list[0]
        next_tail = snake_list[1]
        if tail[0] > next_tail[0]:  # Moving right
            rotated_tail = pygame.transform.rotate(snake_tail_img, 90)
        elif tail[0] < next_tail[0]:  # Moving left
            rotated_tail = pygame.transform.rotate(snake_tail_img, 270)
        elif tail[1] > next_tail[1]:  # Moving down
            rotated_tail = snake_tail_img
        else:  # Moving up
            rotated_tail = pygame.transform.rotate(snake_tail_img, 180)

        dis.blit(rotated_tail, (tail[0], tail[1] + header_height))

# Function to display messages in the center of the screen
def message(msg, color):
    mesg = font_style.render(msg, True, color)  # Render the message with specified color
    mesg_rect = mesg.get_rect(center=(game_width // 2, total_height // 2 + 40))  # Center the message
    dis.blit(mesg, mesg_rect)  # Display the message

# Function to display the final score after the game ends
def display_final_score(total_score):
    final_score = score_font.render("Total Score: " + str(total_score), True, dark_yellow)  # Render final score
    final_score_rect = final_score.get_rect(center=(game_width // 2, total_height // 2))  # Center the score
    dis.blit(final_score, final_score_rect)  # Display final score

# Function to create obstacles (bombs) that do not overlap with the snake or spawn too close to the player
def create_obstacles(num_obstacles, snake_list, player_position):
    obstacles = []
    safe_distance = 10  # Ensure obstacles are at least 1 grid space away from the player
    for _ in range(num_obstacles):
        while True:
            # Generate a random position for the obstacle
            obs_x = round(random.randrange(0, game_width - snake_block) / 10.0) * 10.0
            obs_y = round(random.randrange(0, game_height - snake_block) / 10.0) * 10.0
            # Ensure obstacle is far enough from the player and not overlapping with the snake
            if abs(obs_x - player_position[0]) >= safe_distance or abs(obs_y - player_position[1]) >= safe_distance:
                if [obs_x, obs_y] not in snake_list:
                    obstacles.append([obs_x, obs_y])
                    break
    return obstacles

# Function to draw obstacles (bombs)
def draw_obstacles(obstacles):
    for obstacle in obstacles:
        # Draw bomb image centered in the grid
        dis.blit(bomb_image, (obstacle[0] - 10, obstacle[1] + header_height - 10))

# Main menu function
def main_menu():
    while True:
        # Draw the forest background
        dis.blit(forest_background, (0, 0))

        # Draw the title "Snake Eater" inside a black rectangle
        pygame.draw.rect(dis, black, [0, 0, game_width, 100])
        title_surface = title_font.render("Snake Eater", True, red)
        title_rect = title_surface.get_rect(center=(game_width // 2, 50))
        dis.blit(title_surface, title_rect)

        # Create start and quit buttons
        start_button = pygame.Rect(game_width // 2 - 75, 150, 150, 50)
        quit_button = pygame.Rect(game_width // 2 - 75, 250, 150, 50)

        # Draw buttons with text
        pygame.draw.rect(dis, white, start_button)
        pygame.draw.rect(dis, white, quit_button)
        start_text = font_style.render("Start Game", True, black)
        quit_text = font_style.render("Quit", True, black)
        start_text_rect = start_text.get_rect(center=start_button.center)
        quit_text_rect = quit_text.get_rect(center=quit_button.center)
        dis.blit(start_text, start_text_rect)
        dis.blit(quit_text, quit_text_rect)

        # Update display to show the menu
        pygame.display.update()

        # Check for user input (clicking buttons)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit the game if the window is closed
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):  # Start the game if "Start Game" button is clicked
                    return
                if quit_button.collidepoint(event.pos):  # Quit the game if "Quit" button is clicked
                    pygame.quit()
                    quit()

# Main game loop function
def gameLoop():
    lives = 3  # Player starts with 3 lives
    level = 1  # Starting level
    total_score = 0  # Total score across all lives
    global snake_speed  # Use the global snake_speed variable
    game_over = False  # Game over flag
    current_direction = 'UP'  # Initial direction of the snake

    main_menu()  # Show the main menu before the game starts

    while True:
        game_close = False  # Flag to indicate if the player lost a life
        snake_speed = initial_speed  # Reset snake speed at the start of each life
        x1 = game_width / 2  # Snake's initial x position (center)
        y1 = game_height / 2  # Snake's initial y position (center)
        x1_change = 0  # No movement in the x direction initially
        y1_change = 0  # No movement in the y direction initially
        snake_list = []  # List to store the snake's body segments
        length_of_snake = 1  # Initial length of the snake
        score_in_current_life = 0  # Score for the current life

        # Generate random position for food (apple)
        foodx = round(random.randrange(0, game_width - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, game_height - snake_block) / 10.0) * 10.0

        # Create obstacles based on the current level
        obstacles = create_obstacles(level + 1, snake_list, [x1, y1])

        # Game loop for each life
        while not game_over and not game_close:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Quit the game if the window is closed
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:  # Handle arrow key presses to change direction
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

            # Move the snake based on the current direction
            x1 = (x1 + x1_change) % game_width
            y1 = (y1 + y1_change) % game_height

            # Draw the game field (grassy background)
            dis.blit(field_image, (0, header_height))

            # Draw the food (apple) and obstacles (bombs)
            dis.blit(apple_image, (foodx - 5, foody + header_height - 5))
            draw_obstacles(obstacles)

            # Update snake position
            snake_head = [x1, y1]
            snake_list.append(snake_head)
            if len(snake_list) > length_of_snake:
                del snake_list[0]  # Remove the tail segment when the snake moves

            # Check if the snake hits itself
            for x in snake_list[:-1]:
                if x == snake_head:
                    game_close = True  # The player loses a life if the snake hits itself
                    current_direction = 'UP'

            # Check if the snake hits any obstacles
            for obstacle in obstacles:
                if snake_head == obstacle:
                    game_close = True  # The player loses a life if the snake hits a bomb
                    current_direction = 'UP'

            # Draw the snake and update the score display
            our_snake(snake_block, snake_list, current_direction)
            our_score(score_in_current_life, lives, level, total_score)
            pygame.display.update()

            # Check if the snake eats the food (apple)
            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, game_width - snake_block) / 10.0) * 10.0
                foody = round(random.randrange(0, game_height - snake_block) / 10.0) * 10.0
                length_of_snake += 1  # Increase the length of the snake
                snake_speed += 0.5  # Increase the snake speed
                score_in_current_life += 1  # Increase the current life score

                # Increase level every 5 points and generate new obstacles
                if length_of_snake % 5 == 0:
                    level += 1
                    obstacles = create_obstacles(level + 1, snake_list, [x1, y1])

            clock.tick(snake_speed)  # Control the speed of the game

            # If the player loses a life, reduce lives and check game over
            if game_close:
                total_score += score_in_current_life  # Add current life score to total score
                lives -= 1  # Decrease lives
                if lives <= 0:  # End the game if no lives are left
                    game_over = True
                    current_direction = 'UP'  # Reset direction after game over

        # Game over screen
        if game_over:
            dis.fill(black)  # Fill the screen with black
            skull_rect = skull_image.get_rect(center=(game_width // 2, total_height // 2 - 50))  # Display skull image
            dis.blit(skull_image, skull_rect)
            display_final_score(total_score)  # Show the final total score
            message("Game Over! Press R to Restart, Q to Quit, or M for Main Menu", red)  # Game over message
            pygame.display.update()

            # Handle restart, quit, or return to main menu
            while game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:  # Quit the game
                            pygame.quit()
                            quit()
                        if event.key == pygame.K_r:  # Restart the game
                            lives = 3
                            level = 1
                            total_score = 0
                            game_over = False
                            break
                        if event.key == pygame.K_m:  # Return to the main menu
                            lives = 3
                            level = 1
                            total_score = 0
                            main_menu()  # Return to main menu
                            game_over = False
                            break

# Start the game by calling the main game loop
gameLoop()
